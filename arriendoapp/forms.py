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
    # Campo para ingresar el correo electrónico(aun no he decidio si usar email o username )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # Guarda el usuario y crea un objeto Usuario asociado a él
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Usuario.objects.create(user=user)
        return user

# Formulario para editar un usuario
class UsuarioEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'rut', 'direccion', 'telefono', 'tipo_usuario', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el usuario tiene una cuenta asociada, se inicializa el campo de email con el correo actual
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Guarda los cambios en el usuario y actualiza el correo electrónico en la cuenta de usuario
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
            usuario.user.email = self.cleaned_data['email']
            usuario.user.save()
        return usuario
    
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje']