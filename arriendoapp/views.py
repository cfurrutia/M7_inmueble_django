from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import InmuebleForm, CrearUsuarioForm, UsuarioEditForm
from .models import Inmueble, Comuna
from django.contrib import messages
from django.http import JsonResponse

def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

def lista_inmuebles(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'lista_inmuebles.html', {'inmuebles': inmuebles})

def detalle_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    return render(request, 'detalle_inmueble.html', {'inmueble': inmueble})

def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente. Por favor, inicia sesión.')
            return redirect('login')
    else:
        form = CrearUsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

@login_required
def editar_perfil(request):
    usuario = request.user.usuario
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'editar_perfil.html', {'form': form})

@login_required
def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.arrendador = request.user.usuario
            inmueble.save()
            usuario = request.user.usuario
            if usuario.tipo_usuario == 'arrendatario':
                usuario.tipo_usuario = 'arrendador'
            elif usuario.tipo_usuario == 'arrendatario':
                usuario.tipo_usuario = 'ambos'
            usuario.save()
            messages.success(request, 'Inmueble agregado exitosamente.')
            return redirect('perfil')
    else:
        form = InmuebleForm()
    return render(request, 'agregar_inmueble.html', {'form': form})

@login_required
def solicitar_arriendo(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)

    usuario = request.user.usuario
    if usuario.tipo_usuario == 'arrendador':
        usuario.tipo_usuario = 'ambos'
        usuario.save()
    messages.success(request, 'Solicitud de arriendo enviada.')
    return redirect('detalle_inmueble', inmueble_id=inmueble_id)