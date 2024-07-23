from django import forms
from .models import Inmueble, Usuario, Region, Comuna, SolicitudArriendo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Formulario para crear un inmueble
class InmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Comuna")

    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'banos', 'direccion', 'region', 'comuna', 'tipo_inmueble', 'precio_arriendo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].queryset = Comuna.objects.none()
        
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.region:
            self.fields['comuna'].queryset = self.instance.region.comuna_set.order_by('nombre')
                        
# Formulario para crear un usuario
class CrearUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombres = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    rut = forms.CharField(max_length=20, required=True)
    direccion = forms.CharField(max_length=200, required=True)
    telefono = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Usuario.objects.create(
                user=user,
                nombres=self.cleaned_data['nombres'],
                apellidos=self.cleaned_data['apellidos'],
                rut=self.cleaned_data['rut'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                tipo_usuario='arrendatario'  # Establecer como arrendatario por defecto
            )
        return user

# Formulario para editar un usuario
class UsuarioEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, disabled=False)
    rut = forms.CharField(disabled=False)
    tipo_usuario = forms.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES, disabled=True, required=False)

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'rut', 'direccion', 'telefono', 'tipo_usuario', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email
        self.fields['tipo_usuario'].initial = self.instance.tipo_usuario

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
        return usuario
    
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje']