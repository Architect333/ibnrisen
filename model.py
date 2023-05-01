from settings import TEXT_COLOR
from settings import DB_ACCESS
from settings import DB_NAME
from checks import InputCheck
from observer import Subject

#import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector

from peewee import *
from getpass import getpass

import colorlog

"""
LOGGING CONFIG
"""
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s: %(message)s',
    #datefmt = '%d/%b/%Y %H:%M:%S',
    reset = True,
    log_colors={
		'DEBUG':    'blue',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	    },
    )
)

logger = colorlog.getLogger('ibnrisen')
logger.addHandler(handler)
logger.setLevel('DEBUG')



"""
INIT DATABASE
"""

db_handler = mysql.connector.connect(user=DB_ACCESS['Username'], password=DB_ACCESS['Password'], host=DB_ACCESS['URL'], port=DB_ACCESS['Port'])
db_cursor = db_handler.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS " + DB_NAME)


mysql_db = MySQLDatabase(DB_NAME, user=DB_ACCESS['Username'], password=DB_ACCESS['Password'], host=DB_ACCESS['URL'], port=DB_ACCESS['Port'])

class BaseModel(Model):
    class Meta:
        database = mysql_db

class Inventory(BaseModel):
    hostname = CharField(unique=True)
    ip_address = CharField(unique=True)
    platform = CharField()
    username = CharField()
    password = CharField()
    longitude = FloatField()
    latitude = FloatField()
    neighbors = CharField()

class Flows(BaseModel):
    ip_source = CharField(unique=True)
    ip_destination = CharField(unique=True)
    service = CharField()

mysql_db.connect
mysql_db.create_tables([Inventory])



"""
DECORADORES PARA LOGGING DE CRUD EN BASE DE DATOS
"""

def DecoradorNuevoRegistro(funcion):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        logger.debug("Llamada a función para ingreso de nuevo registro. Llamada número " + str(wrapper.count))
        funcion(*args, **kwargs)
    wrapper.count = 0
    return wrapper

def DecoradorEliminacionRegistro(funcion):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        logger.debug("Llamada a función para eliminar registro. Llamada número " + str(wrapper.count))
        funcion(*args, **kwargs)
    wrapper.count = 0
    return wrapper

def DecoradorActualizacionRegistro(funcion):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        logger.debug("Llamada a función para actualizar registro. Llamada número " + str(wrapper.count))
        funcion(*args, **kwargs)
    wrapper.count = 0
    return wrapper

class DatabaseORM(Subject):
    """
    Utilizacion de ORM Peewee para interactuar con MySQL Database
    Extiendo la clase de Subject para utilizar el Patrón Observador
    """
    
    def __init__(self):
        pass

    @DecoradorNuevoRegistro
    def create_inventory(self, hostname, ip_address, platform, username, password, longitude, latitude, neighbors):
        inventory = Inventory()
        inventory.hostname = hostname
        inventory.ip_address = ip_address
        inventory.platform = platform
        inventory.username = username
        inventory.password = password
        inventory.longitude = longitude
        inventory.latitude = latitude
        inventory.neighbors = neighbors
        try:
            inventory.save()
            print(TEXT_COLOR['OK'] + "Record added successfully! \n" + TEXT_COLOR['END'])
            self.notify("Create")   # Notify Observer
        except Exception as e:
            print(TEXT_COLOR['ERROR'] + "***ERROR*** Record can't be created! " + str(e) + "\n" + TEXT_COLOR['END'])

    def read_inventory(self):
        inventory = Inventory()
        inventory_data = []

        for entry in inventory.select():    
            print(TEXT_COLOR['OK'] + "ID: " + str(entry) + TEXT_COLOR['END'])
            print("Hostname: " + entry.hostname)
            print("IP Address: " + entry.ip_address)
            print("Platform: " + entry.platform)
            print("Username: " + entry.username)
            print("Password: " + entry.password)
            print("Latitude: " + str(entry.longitude))
            print("Logitude: " + str(entry.latitude))
            print("Neighbors: " + entry.neighbors + "\n")

            inventory_data.append((entry.hostname, entry.ip_address, entry.platform, entry.username, entry.password, entry.longitude, entry.latitude, entry.neighbors))
        
        if inventory_data == []:
            print(TEXT_COLOR['ERROR'] + "***ERROR*** No records found!\n" + TEXT_COLOR['END'])
        self.notify("Read")   # Notify Observer
        return inventory_data
        


    @DecoradorActualizacionRegistro
    def update_inventory(self, id):
        hostname_input = input("Ingrese nuevo hostname: ")
        ip_address_input = input("Ingrese nueva dirección IP (formato a.b.c.d): ")
        platform_input = input("Ingrese nueva plataforma: ")
        username_input = input("Ingrese nuevo username: ")
        password_input = getpass("Ingrese nuevo password: ")
        longitude_input = input("Ingrese nuevo longitud (formato -180.000000 a 180.000000): ")
        latitude_input = input("Ingrese nuevo latitud (formato -90.000000 a 90.000000): ")
        neigbhors_input = input("Ingrese nuevos neighborships (formato Ej. [('hostname', 'neighbor_1'), ('hostname', 'neighbor_2'), ..., ('hostname', 'neighbor_n')]): ")
        print("")

        checks = InputCheck()
        result_ip = checks.ip_check(ip_address_input)
        result_long = checks.long_check(longitude_input)
        result_lat = checks.lat_check(latitude_input)

        if (result_ip == False) or (result_long == False) or (result_lat == False):
            print(TEXT_COLOR['ERROR'] + "*** ERROR *** Record can't be updated! " + "\n" + TEXT_COLOR['END'])
        else:
            update = Inventory.update(
                hostname = hostname_input,
                ip_address = ip_address_input,
                platform = platform_input,
                username = username_input,
                password = password_input,
                longitude = longitude_input,
                latitude = latitude_input,
                neighbors = neigbhors_input
                ).where(Inventory.id == id)

            try:
                update.execute()
                print(TEXT_COLOR['OK'] + "Record updated successfully! \n" + TEXT_COLOR['END'])
                self.notify("Update")   # Notify Observer
            except Exception as e:
                print(TEXT_COLOR['ERROR'] + "*** ERROR *** Record can't be updated! " + str(e) + "\n" + TEXT_COLOR['END'])


    @DecoradorEliminacionRegistro
    def delete_inventory(self, id):
        confirmacion = input("Confirme borrado presionando 'S': ")
        if confirmacion == "S":
            try:
                borrar = Inventory.get(Inventory.id == id)
                borrar.delete_instance()
                print(TEXT_COLOR['OK'] + "Record removed successfully! \n" + TEXT_COLOR['END'])
                self.notify("Delete")   # Notify Observer
            except Exception as e:
                print(TEXT_COLOR['ERROR'] + "*** ERROR *** Record can't be removed! " + str(e) + "\n" + TEXT_COLOR['END'])
        else:
            print(TEXT_COLOR['ERROR'] + "¡Operación cancelada!\n" + TEXT_COLOR['END'])


if __name__ == "__main__":
    pass