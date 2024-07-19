from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import Usuario, InmuebleForm, CrearUsuarioForm, UsuarioEditForm, SolicitudArriendoForm
from .models import Inmueble, Comuna, SolicitudArriendo
from django.http import JsonResponse

# Vista para obtener las comunas según la región seleccionada
def obtener_comunas(request):
    # Obtiene el ID de la región seleccionada
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    # Devuelve las comunas 
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

# Vista para listar todos los inmuebles
def lista_inmuebles(request):
    # Obtiene todos los inmuebles
    inmuebles = Inmueble.objects.all()
    return render(request, 'lista_inmuebles.html', {'inmuebles': inmuebles})

# Vista para mostrar el detalle de un inmueble
def detalle_inmueble(request, inmueble_id):
    # Obtiene el inmueble con el ID proporcionado, o devuelve un 404 si no se encuentra (test)
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    return render(request, 'detalle_inmueble.html', {'inmueble': inmueble})

# Vista para crear un nuevo usuario
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            Usuario.objects.create(
                user=user,
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos'),
                rut=form.cleaned_data.get('rut'),
                direccion=form.cleaned_data.get('direccion'),
                telefono=form.cleaned_data.get('telefono'),
                tipo_usuario=form.cleaned_data.get('tipo_usuario')
            )
            messages.success(request, 'Usuario creado exitosamente. Por favor, inicia sesión.')
            return redirect('login')
    else:
        form = CrearUsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        # Obtiene el nombre de usuario y la contraseña enviados en el formulario
        username = request.POST['username']
        password = request.POST['password']
        # Autentica al usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Inicia sesión con el usuario autenticado y redirige a la lista de inmuebles
            login(request, user)
            return redirect('lista_inmuebles')
        else:
            
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    else:
        return render(request, 'logout.html')

# Vista para mostrar el perfil del usuario
@login_required
def perfil(request):
    usuario = request.user.usuario
    inmuebles = Inmueble.objects.filter(arrendador=usuario)
    return render(request, 'perfil.html', {'usuario': usuario, 'inmuebles': inmuebles})

# Vista para editar el perfil del usuario
@login_required
def editar_perfil(request):
    usuario = request.user.usuario
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.user.email = form.cleaned_data.get('email')
            usuario.user.save()
            usuario.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'editar_perfil.html', {'form': form})

# Vista para agregar un nuevo inmueble
@login_required
def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            usuario = request.user.usuario
            inmueble.arrendador = usuario
            inmueble.save()
            
            # Cambiar el tipo de usuario a 'arrendador' si no lo era ya
            if usuario.tipo_usuario == 'arrendatario':
                usuario.tipo_usuario = 'arrendador'
                usuario.save()
            elif usuario.tipo_usuario == 'ambos':
                pass  # Ya es ambos, no necesita cambiar
            
            messages.success(request, 'Inmueble agregado exitosamente.')
            return redirect('perfil')
    else:
        form = InmuebleForm()
    return render(request, 'agregar_inmueble.html', {'form': form})

@login_required
def actualizar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user.usuario)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inmueble actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = InmuebleForm(instance=inmueble)
    return render(request, 'actualizar_inmueble.html', {'form': form, 'inmueble': inmueble})

@login_required
def borrar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user.usuario)
    if request.method == 'POST':
        inmueble.delete()
        messages.success(request, 'Inmueble borrado exitosamente.')
        return redirect('perfil')
    return render(request, 'borrar_inmueble.html', {'inmueble': inmueble})

# Vista para solicitar el arriendo de un inmueble
@login_required
def solicitar_arriendo(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    
    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.arrendatario = request.user
            solicitud.inmueble = inmueble
            solicitud.save()
            messages.success(request, 'Solicitud enviada exitosamente.')
            return redirect('detalle_inmueble', inmueble_id=inmueble.id)
    else:
        form = SolicitudArriendoForm()
    
    return render(request, 'solicitar_arriendo.html', {'form': form, 'inmueble': inmueble})

@login_required
def ver_solicitudes(request):
    usuario = request.user.usuario 
    
    inmuebles = Inmueble.objects.filter(arrendador=usuario)
    if not inmuebles.exists():
        messages.info(request, 'No tienes inmuebles para arrendar.')
        return redirect('perfil')
    
    solicitudes = SolicitudArriendo.objects.filter(inmueble__in=inmuebles)
    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes})
