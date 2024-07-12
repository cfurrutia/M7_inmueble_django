from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import InmuebleForm, UsuarioForm
from .models import Usuario, Inmueble, Comuna, Region


def crear_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inmuebles')
    else:
        form = InmuebleForm()
    return render(request, 'crear_inmueble.html', {'form': form})

def lista_inmuebles(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'lista_inmuebles.html', {'inmuebles': inmuebles})

def detalle_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id)
    return render(request, 'detalle_inmueble.html', {'inmueble': inmueble})

def inmuebles_por_comuna(request, comuna_id):
    comuna = get_object_or_404(Comuna, pk=comuna_id)
    inmuebles = Inmueble.objects.filter(comuna=comuna)
    return render(request, 'inmuebles_por_comuna.html', {'comuna': comuna, 'inmuebles': inmuebles})

def inmuebles_por_region(request, region_id):
    region = get_object_or_404(Region, pk=region_id)
    inmuebles = Inmueble.objects.filter(comuna__region=region)
    return render(request, 'inmuebles_por_region.html', {'region': region, 'inmuebles': inmuebles})

def crear_usuario(request):
    if request.method == 'POST':
        
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['correo'],
                email=form.cleaned_data['correo'],
                password=form.cleaned_data['password']
            )
            usuario = Usuario.objects.create(
                user=user,
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                rut=form.cleaned_data['rut'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                correo=form.cleaned_data['correo'],
                tipo_usuario=form.cleaned_data['tipo_usuario']
            )
            
            return redirect('alguna_url')
    else:
        form = UsuarioForm()
    
    return render(request, 'crear_usuario.html', {'form': form})