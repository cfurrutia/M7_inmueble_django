from django.db import connection
from .baseModel import BaseModel as bm

class InmuebleService(bm):
    class Meta:
        abstract = True

    def crear_tipo_inmueble(self, nombre, descripcion=''):
        sql = "INSERT INTO arriendoApp_tipoinmueble (nombre, descripcion) VALUES (%s, %s) RETURNING id"
        result = self.execute(sql, [nombre, descripcion])
        return result[0]['id'] if result else None

    def obtener_tipos_inmueble(self):
        sql = "SELECT * FROM arriendoApp_tipoinmueble"
        return self.executeQuery(sql)

    def crear_inmueble(self, nombre, descripcion, m2_construidos, m2_totales, estacionamientos, 
                    habitaciones, banos, direccion, comuna_id, tipo_inmueble_id, precio_mensual):
        sql = """
        INSERT INTO arriendoApp_inmueble 
        (nombre, descripcion, m2_construidos, m2_totales, estacionamientos, habitaciones, banos, direccion, comuna_id, tipo_inmueble_id, precio_mensual) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        RETURNING id
        """
        params = [nombre, descripcion, m2_construidos, m2_totales, estacionamientos, habitaciones, banos, direccion, comuna_id, tipo_inmueble_id, precio_mensual]
        result = self.execute(sql, params)
        return result[0]['id'] if result else None

    def actualizar_inmueble(self, inmueble_id, **kwargs):
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        sql = f"UPDATE arriendoApp_inmueble SET {set_clause} WHERE id = %s"
        params = list(kwargs.values()) + [inmueble_id]
        return self.execute(sql, params)

    def borrar_inmueble(self, inmueble_id):
        sql = "DELETE FROM arriendoApp_inmueble WHERE id = %s"
        return self.execute(sql, [inmueble_id])

inmueble_service = InmuebleService()