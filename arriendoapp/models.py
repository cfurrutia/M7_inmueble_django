from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    nombre = models.CharField(null= False, blank=False, max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(null= False, blank=False, max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TipoInmueble(models.Model):
    nombre = models.CharField(null= False,  blank=False, max_length=50)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('ARRENDATARIO', 'Arrendatario'),
        ('ARRENDADOR', 'Arrendador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(null=False, blank=False, max_length=100)
    apellidos = models.CharField(null=False, blank=False, max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(null=False, blank=False, max_length=200)
    telefono = models.CharField(null=False, blank=False, max_length=20)
    correo = models.EmailField(null=False, blank=False, unique=True)
    tipo_usuario = models.CharField(null=False, blank=False, max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
class Inmueble(models.Model):
    nombre = models.CharField(null= False, blank=False, max_length=100)
    descripcion = models.TextField(null= False, blank=False)
    m2_construidos = models.IntegerField(null= False, blank=False)
    m2_totales = models.IntegerField(null= False, blank=False)
    estacionamientos = models.IntegerField(null= False, blank=False)
    habitaciones = models.IntegerField(null= False, blank=False)
    banos = models.IntegerField(null= False, blank=False)
    direccion = models.CharField(max_length=200)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)
    precio_arriendo = models.IntegerField(null= False, blank=False)
    arrendador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class SolicitudArriendo(models.Model):
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return f"Solicitud de {self.arrendatario} para {self.inmueble}"