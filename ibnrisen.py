import control

"""
INICIO POR COMMAND LINE.
EJECUTAR: "python ibnrisen.py [arguments]"

Help: python ibnrisen.py -h

- Para subir el inventario: python ibnrisen.py -c hosts.yaml
- Para ver los IDs del inventario: python ibnrisen.py -r
- Para actuaizar un registro: python ibnrisen.py -u [ID]
- Para borrar un registro: python ibnrisen.py -d [ID]


OPCIONES DISPONIBLES
    CRUD con ORM de PEEWEE
        Alta de inventario tomando informacion de archivo .yaml
        Lectura de registros en base de datos
        Actuazación de registro en base de datos
        Borrado de registro en base de datos
    CREACION DE TRAFFIC MATRIX Y DIBUJOS DE TOPOLOGÍA
"""

if __name__ == "__main__":
    ibn_run = control.IBNControl()