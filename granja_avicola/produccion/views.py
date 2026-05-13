from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produccion, Lote
from productos.models import Producto
from .forms import LoteForm, ProduccionForm

def lista_produccion(request):
    producciones = Produccion.objects.all()
    return render(request, 'produccion/lista.html', {'producciones': producciones})

def registrar_produccion(request):
    productos = Producto.objects.filter(estado=True)
    if request.method == 'POST':
        prod = get_object_or_404(Producto, id=request.POST.get('producto'))
        cantidad = int(request.POST.get('cantidad'))

        nueva_p = Produccion.objects.create (
            producto = prod,
            cantidad = cantidad,
            lote = request.POST.get('lote'),
            fecha_produccion = request.POST.get('fecha_produccion'),
            usuario = request.user,
            observaciones = request.POST.get('observaciones')
        )

        prod.stock += cantidad
        prod.save()

        messages.success(request, "Producción registrada y stock actualizado.")
        return redirect('lista_productos')
    return render(request, 'produccion/form_produccion.html', {'productos': productos})

def editar_produccion(request, pk):
    produccion = get_object_or_404(Produccion, pk=pk)
    productos = Producto.objects.filter(estado='Activo')
    if request.method == 'POST':
        prod_original = produccion.producto
        prod_original.stock -= produccion.cantidad_recolectada
        prod_original.save()
        
        produccion.cantidad_recolectada = int(request.POST.get('cantidad'))
        produccion.lote = request.POST.get('lote')
        produccion.fecha_produccion = request.POST.get('fecha_produccion')
        produccion.observaciones = request.POST.get('observaciones')
        produccion.save()
        
        prod_original.stock += produccion.cantidad_recolectada
        prod_original.save()

        messages.info(request, "Registro de producción corregido exitosamente.")
        return redirect('lista_productos')
    return render(request, 'produccion/form_produccion.html', {
        'produccion': produccion,
        'productos': productos
    })

def lista_lotes(request):
    lotes = Lote.objects.filter(esta_activo=True).order_by('-fecha_registro_sistema')
    return render(request, 'produccion/lista_lote.html', {'lotes': lotes})

def crear_lote(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.cantidad_actual = lote.cantidad_inicial
            lote.save()
            messages.success(request, f"Lote {lote.codigo_lote} creado con éxito.")
            return redirect('lista_lotes')
    else:
        form = LoteForm()
    return render(request, 'produccion/form_lote.html', {'form': form, 'titulo': 'Nuevo Lote'})

def editar_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method == 'POST':
        form = LoteForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            messages.info(request, "Información del lote actualizada.")
            return redirect('lista_lotes')
    else:
        form = LoteForm(instance=lote)
    return render(request, 'produccion/form_lote.html', {'form': form, 'titulo': 'Editar Lote'})

