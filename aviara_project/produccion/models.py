from django.db import models
from productos.models import Producto

class Lote(models.Model):
    codigo_lote = models.CharField(max_length=50, unique=True)
    fecha_produccion = models.DateField()
    fecha_vencimiento = models.DateField()
    cantidad_inicial = models.IntegerField()
    cantidad_actual = models.IntegerField()
    estado = models.BooleanField(default=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)

    def __str__(self):
        return f"Lote {self.codigo_lote} - {self.producto.nombre}"

class Produccion(models.Model):
    raza_ave = models.CharField(max_length=100)
    mortalidad_acumulada = models.IntegerField(default=0)
    observaciones = models.TextField()
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='seguimientos')

    def __str__(self):
        return f"Seguimiento {self.id} - Lote {self.lote.codigo_lote}"