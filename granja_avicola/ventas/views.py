from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido
from .forms import PedidoForm, DetallePedidoFormSet
from django.utils import timezone

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    
    context = {
        'pedidos': pedidos,
        'pedidos_pendientes_count': pedidos.filter(estado_pedido='PENDIENTE').count(),
        'pedidos_entregados_count': pedidos.filter(estado_pedido='ENTREGADO').count(),
        'total_ventas': sum(p.total_pedido for p in pedidos.filter(estado_pedido='ENTREGADO'))
    }

    return render(request, 'ventas/lista_pedidos.html', context)

def gestionar_pedido(request, pk=None):
    pedido = get_object_or_404(Pedido, pk=pk) if pk else None

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        formset = DetallePedidoFormSet(request.POST, instance=pedido)

        if form.is_valid() and formset.is_valid():
            pedido_guardado = form.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.pedido = pedido_guardado
                detalle.save()
            
            for obj in formset.deleted_objects:
                obj.delete()
            pedido_guardado.actualizar_total()
            messages.success(request, f"Pedido #{pedido_guardado.id} guardado correctamente.")
            return redirect('lista_pedidos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PedidoForm(instance=pedido)
        formset = DetallePedidoFormSet(instance=pedido)
    
    return render(request, 'ventas/pedido_form.html', {
        'form': form,
        'formset': formset,
        'pedido': pedido
    })

def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'ventas/pedido_detalle.html', {
        'pedido': pedido
    })

def cambiar_estado_pedido(request, pk, nuevo_estado):
    pedido = get_object_or_404(Pedido, pk=pk)
    estados_validos = [choice[0] for choice in Pedido.ESTADOS_PEDIDO]

    if nuevo_estado in estados_validos:
        if nuevo_estado == 'CAMINO':
            pedido.fecha_despacho = timezone.now()
        
        pedido.estado_pedido = nuevo_estado
        pedido.save()
        messages.success(request, f"Estado del pedido #{pedido.id} actualizado a {pedido.get_estado_pedido_display()}.")
    else:
        messages.error(request, "Estado no válido.")
    return redirect('lista_pedidos')

# Create your views here.
