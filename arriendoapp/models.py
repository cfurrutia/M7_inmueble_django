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
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
        ('ambos', 'Ambos')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    rut = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='arrendatario')
    
    def __str__(self):
        return self.user.username
        
class Inmueble(models.Model):
    nombre = models.CharField(null= False, blank=False, max_length=100)
    descripcion = models.TextField(null= False, blank=False)
    m2_construidos = models.IntegerField(null= False, blank=False)
    m2_totales = models.IntegerField(null= False, blank=False)
    estacionamientos = models.IntegerField(null= False, blank=False)
    habitaciones = models.IntegerField(null= False, blank=False)
    banos = models.IntegerField(null= False, blank=False)
    direccion = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
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