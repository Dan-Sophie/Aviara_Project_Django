from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# Obtenemos el modelo 'usuarios.Usuario' configurado en Aviara
User = get_user_model()

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    documento = forms.CharField(
        required=True,
        label="Número de Documento",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1012345678'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "documento")
