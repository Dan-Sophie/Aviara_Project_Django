from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    unidad_medida = models.CharField(max_length=10)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Detalle_Agricola(Producto):
    variedad = models.CharField(max_length=100)
    estado_madurez = models.CharField(max_length=50)
    tratamiento = models.TextField()
    humedad_optima = models.CharField(max_length=50)

class Detalle_Avicola(Producto):
    talla = models.CharField(max_length=20)
    color_huevo = models.CharField(max_length=30)
    tipo_empaque = models.CharField(max_length=50)
    categoria_calidad = models.CharField(max_length=50)
    limpieza = models.BooleanField(default=True)