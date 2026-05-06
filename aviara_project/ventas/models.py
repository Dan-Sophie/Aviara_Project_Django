from django.db import models
from django.conf import settings
from productos.models import Producto
from usuarios.models import Distribuidor

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=50, default='Pendiente')
    metodo_pago = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=255)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    #Datos de Logística
    estado_entrega = models.CharField(max_length=50, default='En Preparación')
    novedad_entrega = models.TextField(null=True, blank=True)
    fecha_despacho = models.DateTimeField(null=True, blank=True)
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)

    #Datos del Distribuidor asignado.
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

class Detalle_Pedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField() 
    precio_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Evidencia_Entrega(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    foto_comprobante = models.ImageField(upload_to='evidencias/')
    firma_digital = models.ImageField(upload_to='firmas/', null=True, blank=True)
    fecha_hora_evidencia = models.DateTimeField(auto_now_add=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Evidencia Pedido {self.pedido.id}"
    