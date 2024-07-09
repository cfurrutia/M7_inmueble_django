from django.db import connection

class BaseModel():
    class Meta:
        abstract = True

    def executeQuery(self, sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros if parametros is not None else [])
            print(cursor.description)
            data = cursor.description
            row = cursor.fetchone()
            return row

    def execute(self, sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros if parametros is not None else [])
            try:
                row = cursor.fetchone()
                if row is not None:
                    return row
            except Exception as e:
                print("Error de consulta", e)
                return []
