from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import RegistroForm, UsuarioForm
from django.contrib.auth import get_user_model
from import_export.formats.base_formats import XLSX
from .admin import UsuarioResource

Usuario = get_user_model()


def landing(request):
    return render(request, 'landing.html')

@login_required
def home(request):
    return render(request, 'admin/home.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            asunto = '¡ 𝓦𝓮𝓵𝓬𝓸𝓂𝓮 a Aviara !'
            mensaje = f'Hola {user.username}, gracias por registrarte en nuestra pagina de Aviara'
            email_desde = settings.EMAIL_HOST_USER
            email_para = [user.email]

            try:
                send_mail(asunto, mensaje, email_desde, email_para)
            except Exception as e:
                print(f"Error enviando correo: {e}")

            messages.success(request, "Cuenta creada exitosamente.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def redireccionar_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('home')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('landing')
    return render(request, 'admin/home.html')

@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@login_required
def carga_masiva_usuarios(request):
    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        dataset = UsuarioResource().export()
        nuevo_usuario_resource = UsuarioResource()
        archivo = request.FILES['archivo_excel']

        #Importamos usando el formato XLSX
        dataset.load(archivo.read(), format='xlsx')

        #Validar y guardar
        result = nuevo_usuario_resource.import_data(dataset, dry_run=False)

        if not result.has_errors():
            messages.success(request, f"¡Éxito! Se procesaron los usuarios correctamente.")
        else:
            messages.error(request, "Hubo un error en el formato del archivo.")
        return redirect('lista_usuarios')

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuarios.html', {'form': form, 'usuario': usuario})
