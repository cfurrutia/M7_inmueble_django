from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import InmuebleForm, CrearUsuarioForm, UsuarioEditForm
from .models import Inmueble, Comuna
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
        # Crea un formulario de creación de usuario con los datos enviados
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            # Guarda el usuario y redirige al usuario a la página de inicio de sesión
            form.save()
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
            
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'logout.html')

# Vista para mostrar el perfil del usuario
@login_required
def perfil(request):
    return render(request, 'perfil.html')

# Vista para editar el perfil del usuario
@login_required
def editar_perfil(request):
    # Obtiene el usuario asociado al usuario autenticado
    usuario = request.user.usuario
    if request.method == 'POST':
        # Crea un formulario de edición de usuario con los datos enviados
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            # Guarda los cambios en el usuario y redirige al perfil
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        # Crea un formulario de edición de usuario con los datos del usuario actual
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'editar_perfil.html', {'form': form})

# Vista para agregar un nuevo inmueble
@login_required
def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.arrendador = request.user.usuario
            inmueble.save()
            messages.success(request, 'Inmueble agregado exitosamente.')
            return redirect('perfil')
    else:
        form = InmuebleForm()
    return render(request, 'agregar_inmueble.html', {'form': form})

# Vista para solicitar el arriendo de un inmueble (aun no implementada en html urls)
@login_required
def solicitar_arriendo(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    # Obtiene el usuario autenticado y actualiza su tipo de usuario si es necesario
    usuario = request.user.usuario
    if usuario.tipo_usuario == 'arrendador':
        usuario.tipo_usuario = 'ambos'
        usuario.save()
    messages.success(request, 'Solicitud de arriendo enviada.')
    return redirect('detalle_inmueble', inmueble_id=inmueble_id)