import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyectomodulo7.settings")
django.setup()

from arriendoapp.models import Inmueble, Comuna, Region

def listar_por_comuna(nombre_comuna):
    
    inmuebles = Inmueble.objects.filter(comuna__nombre__icontains=nombre_comuna).select_related('comuna', 'comuna__region')
    
    with open("consultas/inmuebles_por_comuna.txt", "w", encoding="utf-8") as archivo:
        for inmueble in inmuebles:
            archivo.write(f"ID: {inmueble.id} - Nombre: {inmueble.nombre} - Comuna: {inmueble.comuna.nombre}\n")
            archivo.write(f"Descripción: {inmueble.descripcion}\n")
            archivo.write(f"Región: {inmueble.comuna.region.nombre}\n\n")

def listar_por_region(nombre_region):
    
    inmuebles = Inmueble.objects.filter(comuna__region__nombre__icontains=nombre_region).select_related('comuna', 'comuna__region')
    
    with open("consultas/inmuebles_por_region.txt", "w", encoding="utf-8") as archivo:
        current_region = ''
        for inmueble in inmuebles:
            region_nombre = inmueble.comuna.region.nombre
            if region_nombre != current_region:
                archivo.write(f"\nRegión: {region_nombre}\n")
                current_region = region_nombre
            archivo.write(f"ID: {inmueble.id} - Nombre: {inmueble.nombre} - Comuna: {inmueble.comuna.nombre}\n")
            archivo.write(f"Descripción: {inmueble.descripcion}\n\n")

if __name__ == "__main__":
    listar_por_comuna("Providencia")
    listar_por_comuna("Valparaíso")
    listar_por_region("Valparaíso")
    listar_por_region("Región Metropolitana de Santiago")