from django.db import models
from django.contrib.auth.models import User

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=20, choices=[('ARRENDATARIO', 'Arrendatario'), ('ARRENDADOR', 'Arrendador')])
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    nombres = models.CharField(max_length=30, null=False, blank=False)
    apellidos = models.CharField(max_length=30, null=False, blank=False)
    rut = models.CharField(max_length=15, null=False, blank=False, unique=True)
    direccion = models.CharField(max_length=50, null=False, blank=False)
    telefono = models.CharField(max_length=15, null=False, blank=False)
    correo_electronico = models.EmailField(null=False, blank=False, unique=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Region(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=20, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comunas')

    def __str__(self):
        return f"{self.nombre}, {self.region.nombre}"
    
class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    direccion = models.CharField(max_length=200)
    comuna = models.ForeignKey('Comuna', on_delete=models.PROTECT)  # (en proceso)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.PROTECT)
    precio_mensual = models.IntegerField()
    usuarios = models.ManyToManyField(Usuario, through='InmuebleUsuario')

    def __str__(self):
        return f"{self.nombre} - {self.comuna.nombre}"    

class InmuebleUsuario(models.Model):
    ROLES = [
        ('ARRENDADOR', 'Arrendador'),
        ('ARRENDATARIO', 'Arrendatario'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ('usuario', 'inmueble', 'rol')

class ContratoArriendo(models.Model):
    inmueble_usuario = models.ForeignKey(InmuebleUsuario, on_delete=models.CASCADE, related_name='contratos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('ACTIVO', 'Activo'), ('TERMINADO', 'Terminado')], default='ACTIVO')

    def __str__(self):
        return f"{self.inmueble_usuario.usuario} - {self.inmueble_usuario.inmueble} ({self.estado})"