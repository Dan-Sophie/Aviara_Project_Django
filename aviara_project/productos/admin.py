from django.contrib import admin
from .models import Categoria, Producto, Detalle_Agricola, Detalle_Avicola

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Detalle_Agricola)
admin.site.register(Detalle_Avicola)

