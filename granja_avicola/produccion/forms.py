from django import forms
from .models import Lote, Produccion

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['producto', 'codigo_lote', 'cantidad_inicial', 'stock_minimo', 'fecha_produccion', 'fecha_vencimiento', 'estado_calidad']
        widgets = {
            'fecha_produccion': forms.DateInput(attrs={'type': 'date', 'class': 'form-input-oliva'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input-oliva'}),
            'producto': forms.Select(attrs={'class': 'form-select-oliva'}),
        }

class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ['lote', 'fecha_produccion', 'cantidad_recolectada', 'mortalidad_del_dia', 'observaciones']
        widgets = {
            'fecha_produccion': forms.DateInput(attrs={'type': 'date', 'class': 'form-input-oliva'}),
            'observaciones': forms.TextInput(attrs={'rows': 3, 'class': 'form-input-oliva'}),
        }