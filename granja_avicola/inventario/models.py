from django.db import models
from produccion.models import Lote
from django.core.exceptions import ValidationError
from django.conf import settings

class Merma(models.Model):

    ESTADOS_MERMA = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada')
    ]

    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='mermas')
    cantidad_perdida = models.PositiveIntegerField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100)
    observaciones = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS_MERMA, default='PENDIENTE')
    reportado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='mermas_reportadas')
    

    def __str__(self):
        return f"Merma {self.id} - {self.lote.codigo_lote} ({self.estado})"
    
    #Validación: No permite registrar más de lo que hay en el lote
    def clean(self):
        if self.estado == 'APROBADA' and self.cantidad_perdida > self.lote.cantidad_actual:
            raise ValidationError (
                f"No se puede aprobar la merma. La cantidad perdida ({self.cantidad_perdida})"
                f"supera el stock actual del lote ({self.lote.cantidad_actual})"
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk:
            original = Merma.objects.get(pk=self.pk)
            if original.estado != 'APROBADA' and self.estado == 'APROBADA':
                self.lote.cantidad_actual -= self.cantidad_perdida
                self.lote.save()
            elif original.estado == 'APROBADA' and self.estado != 'APROBADA':
                self.lote.cantidad_actual += self.cantidad_perdida
                self.lote.save()
        super().save(*args, **kwargs)