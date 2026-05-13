from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from productos.models import Producto
from usuarios.models import Distribuidor

class Pedido(models.Model):
        ESTADOS_PEDIDO = [
            ('PENDIENTE', 'Pendiente'),
            ('PROCESANDO', 'En Proceso'),
            ('CAMINO', 'En Camino'),
            ('ENTREGADO', 'Entregado'),
            ('CANCELADO', 'Cancelado'),
        ]
        usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
        fecha_pedido = models.DateTimeField(auto_now_add=True)
        estado_pedido = models.CharField(max_length=50, choices=ESTADOS_PEDIDO, default='PENDIENTE')
        metodo_pago = models.CharField(max_length=50)
        direccion_entrega = models.CharField(max_length=255)
        total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        distribuidor = models.ForeignKey(Distribuidor, on_delete=models.SET_NULL, null=True, blank=True)    
        fecha_despacho = models.DateTimeField(null=True, blank=True)
        fecha_entrega_real = models.DateTimeField(null=True, blank=True)
        novedad_entrega = models.TextField(null=True, blank=True)

        def __str__(self):
            return f"Pedido {self.id} - {self.usuario.get_full_name()} ({self.get_estado_pedido_display()})"
        
        def clean(self):
            if self.pk:
                original = Pedido.objects.get(pk=self.pk)
                if original.estado_pedido == 'CAMINO' and self.estado_pedido == 'CANCELADO':
                    raise ValidationError("No se puede calcular un pedido que ya está en camino.")
        
        def actualizar_total(self):
            total = sum(detalle.subtotal for detalle in self.detalles.all())
            self.total_pedido = total
            self.save()

class Detalle_Pedido(models.Model):
        pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
        producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
        cantidad = models.PositiveIntegerField() 
        precio_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)
        subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

        def save(self, *args, **kwargs):
            self.subtotal = self.cantidad * self.precio_unitario_venta
            super().save(*args, **kwargs)
            self.pedido.actualizar_total()
        
        def clean(self):
            if self.cantidad > self.producto.cantidad:
                raise ValidationError(f"No hay suficiente stock de {self.producto_nombre}. Disponible: {self.producto.cantidad}")


class Evidencia_Entrega(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='evidencia')
    foto_comprobante = models.ImageField(upload_to='evidencias/')
    firma_digital = models.ImageField(upload_to='firmas/', null=True, blank=True)
    fecha_hora_evidencia = models.DateTimeField(auto_now_add=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Evidencia Pedido {self.pedido.id}"