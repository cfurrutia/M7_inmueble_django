import os, django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyectomodulo7.settings")
django.setup()

from arriendoapp.models import Inmueble, Comuna, Region
from django.db import connection

def listar_por_comuna(nombre_comuna):
    select = """ 
    SELECT inm.id, inm.nombre, inm.descripcion, comuna.nombre AS comuna_nombre, region.nombre AS region_nombre
    FROM arriendoapp_inmueble inm
    INNER JOIN arriendoapp_comuna comuna ON inm.comuna_id = comuna.id
    INNER JOIN arriendoapp_region region ON comuna.region_id = region.id
    WHERE comuna.nombre LIKE %s 
    """
    with connection.cursor() as cursor:
        cursor.execute(select, [f'%{nombre_comuna}%'])
        results = cursor.fetchall()

    with open("consultas/inmuebles_por_comuna.txt", "w", encoding="utf-8") as archivo:
        for row in results:
            archivo.write(f"ID: {row[0]} - Nombre: {row[1]} - Comuna: {row[3]}\n")
            archivo.write(f"Descripción: {row[2]}\n")
            archivo.write(f"Región: {row[4]}\n\n")

def listar_por_region(nombre_region):
    select = """ 
    SELECT inm.id, inm.nombre, inm.descripcion, comuna.nombre AS comuna_nombre, region.nombre AS region_nombre
    FROM arriendoapp_inmueble inm
    INNER JOIN arriendoapp_comuna comuna ON inm.comuna_id = comuna.id
    INNER JOIN arriendoapp_region region ON comuna.region_id = region.id
    WHERE region.nombre LIKE %s
    """
    with connection.cursor() as cursor:
        cursor.execute(select, [f'%{nombre_region}%'])
        results = cursor.fetchall()

    with open("consultas/inmuebles_por_region.txt", "w", encoding="utf-8") as archivo:
        current_region = ''
        for row in results:
            if row[4] != current_region:
                archivo.write(f"\nRegión: {row[4]}\n")
                current_region = row[4]
            archivo.write(f"ID: {row[0]} - Nombre: {row[1]} - Comuna: {row[3]}\n")
            archivo.write(f"Descripción: {row[2]}\n\n")

if __name__ == "__main__":
    listar_por_comuna("Providencia")
    listar_por_comuna("Valparaíso")
    listar_por_region("Valparaíso")
    listar_por_region("Región Metropolitana de Santiago")