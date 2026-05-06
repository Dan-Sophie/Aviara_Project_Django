from django.db import models
from produccion.models import Lote

class Merma(models.Model):
    cantidad_perdida = models.IntegerField()
    fecha_reporte = models.DateField(auto_now_add=True)
    motivo = models.TextField()
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='mermas')

    def __str__(self):
        return f"Merma de {self.cantidad_perdida} en Lote {self.lote.codigo_lote}"
    
    def save(self, *args, **kwargs):
        self.lote.cantidad_actual -= self.cantidad_perdida
        self.lote.save()
        super().save(*args, **kwargs)