from django.contrib import admin
from .models import Pedido, Detalle_Pedido, Evidencia_Entrega

admin.site.register(Pedido)
admin.site.register(Detalle_Pedido)
admin.site.register(Evidencia_Entrega)
