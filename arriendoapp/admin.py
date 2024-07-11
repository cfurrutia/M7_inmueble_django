from django.contrib import admin
from .models import Region, Comuna, TipoInmueble, Usuario, Inmueble, SolicitudArriendo

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(TipoInmueble)
admin.site.register(Usuario)
admin.site.register(Inmueble)
admin.site.register(SolicitudArriendo)
