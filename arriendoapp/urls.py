from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_inmuebles, name='lista_inmuebles'),
    path('crear/', views.crear_inmueble, name='crear_inmueble'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('<int:inmueble_id>/', views.detalle_inmueble, name='detalle_inmueble'),
    path('comuna/<int:comuna_id>/', views.inmuebles_por_comuna, name='inmuebles_por_comuna'),
    path('region/<int:region_id>/', views.inmuebles_por_region, name='inmuebles_por_region'),
]