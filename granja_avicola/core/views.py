from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import RegistroForm  
from django.contrib.auth.decorators import user_passes_test

def es_administrador(user):
    return user.is_superuser

@user_passes_test(es_administrador, login_url='login')
def home(request):
    return render(request, 'home.html')

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
