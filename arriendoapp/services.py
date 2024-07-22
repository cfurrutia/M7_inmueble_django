from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Usuario, Inmueble, Comuna, SolicitudArriendo

# Servicios para Usuario

def crear_usuario(form):
    user = form.save()
    usuario = Usuario.objects.create(
        user=user,
        nombres=form.cleaned_data.get('nombres'),
        apellidos=form.cleaned_data.get('apellidos'),
        rut=form.cleaned_data.get('rut'),
        direccion=form.cleaned_data.get('direccion'),
        telefono=form.cleaned_data.get('telefono'),
        tipo_usuario=form.cleaned_data.get('tipo_usuario')
    )
    return usuario

def actualizar_usuario(usuario_id, **kwargs):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for key, value in kwargs.items():
        setattr(usuario, key, value)
    usuario.save()
    return usuario

# Servicios para Inmueble

def obtener_comunas(region_id):
    return Comuna.objects.filter(region_id=region_id).order_by('nombre')

def listar_inmuebles():
    return Inmueble.objects.all()

def obtener_inmueble(inmueble_id):
    return get_object_or_404(Inmueble, id=inmueble_id)

def crear_inmueble(form, usuario):
    inmueble = form.save(commit=False)
    inmueble.arrendador = usuario
    inmueble.save()
    return inmueble

def actualizar_inmueble(inmueble_id, **kwargs):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    for key, value in kwargs.items():
        setattr(inmueble, key, value)
    inmueble.save()
    return inmueble

def borrar_inmueble(inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    inmueble.delete()

# Servicios para SolicitudArriendo

def crear_solicitud_arriendo(form, usuario, inmueble):
    solicitud = form.save(commit=False)
    solicitud.arrendatario = usuario
    solicitud.inmueble = inmueble
    solicitud.save()
    return solicitud

def listar_solicitudes(usuario):
    inmuebles = Inmueble.objects.filter(arrendador=usuario)
    return SolicitudArriendo.objects.filter(inmueble__in=inmuebles)