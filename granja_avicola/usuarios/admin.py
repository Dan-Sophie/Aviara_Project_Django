from django.contrib import admin
from .models import Rol, TipoDocumento, Usuario, Distribuidor

admin.site.register(Rol)
admin.site.register(TipoDocumento)
admin.site.register(Usuario)
admin.site.register(Distribuidor)
