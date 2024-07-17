from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.lista_inmuebles, name='lista_inmuebles'),
    path('perfil/', views.perfil, name='perfil'),
    path('inmueble/<int:inmueble_id>/', views.detalle_inmueble, name='detalle_inmueble'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('agregar_inmueble/', views.agregar_inmueble, name='agregar_inmueble'),
    path('actualizar_inmueble/<int:inmueble_id>/', views.actualizar_inmueble, name='actualizar_inmueble'),
    path('borrar_inmueble/<int:inmueble_id>/', views.borrar_inmueble, name='borrar_inmueble'),
    path('obtener_comunas/', views.obtener_comunas, name='obtener_comunas'),
    path('solicitar_arriendo/<int:inmueble_id>/', views.solicitar_arriendo, name='solicitar_arriendo'),
    
]