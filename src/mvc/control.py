"""
MVC Pattern: Control module, with all the logic to control database access and topology creation.
"""

import yaml
from getpass import getpass
import src.mvc.view as view
import src.mvc.model as model
import os
import pprint as pp
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import geojson
import geopandas
import src.services.observer as observer
from src.config.settings import TEXT_COLOR
from src.config.logging import logger
import src.services.server as server
import asyncio

class IBNControl():
    """
    ### MODULO DE CONTROL ###
        - CRUD en base de datos con ORM Peewee
        - Creacion de Matriz de Trafico y Dibujo de Topología con Networkx, GeoJSON y GeoPandas
    """

    def __init__(self) -> None:
        self.args_setup = view.ArgsSetup()
        self.args_control = self.args_setup.args_setup()

        self.action = self.args_control[0]
        self.inventory = self.args_control[1]
        self.create_configs = self.args_control[2]
        self.create_matrix = self.args_control[3]

        self.db_instance = model.DatabaseORM()
        self.observer = observer.CRUD_Observer(self.db_instance)    # Observe Data Base CRUD

        if self.action == "create":
            self.create_inventory()

        if self.action == "read":
            self.read_inventory()

        if self.action == "update":
            self.update_inventory(self.inventory)
        
        if self.action == "delete":
            self.delete_inventory(self.inventory)

        if self.create_matrix == True:
            self.build_matrix()


    def create_inventory(self):
        try:
            with open(self.inventory, 'r') as yaml_file:
                inventory_data = yaml.safe_load(yaml_file)

                for device in inventory_data:
                    neighbors = []
                    hostname = device
                    ip_address = inventory_data[device]['ip_address']
                    platform = inventory_data[device]['platform']
                    username = inventory_data[device]['username']
                    password = inventory_data[device]['password']
                    longitude = inventory_data[device]['geolocation'][0]['longitude']
                    latitude = inventory_data[device]['geolocation'][1]['latitude']
                    for interface_neighbor in inventory_data[device]['neighbors']:
                        for neighbor in interface_neighbor.values():
                            neighbors.append((hostname, neighbor))
                    
                    print(device)
                    pp.pprint(inventory_data[device])
                    self.db_instance.create_inventory(hostname, ip_address, platform, username, password, longitude, latitude, neighbors)

        except Exception as e:
                print("File not found. " + str(e))
 

    def read_inventory(self):
        self.db_instance.read_inventory()

    def update_inventory(self, id):
        self.db_instance.update_inventory(id)

    def delete_inventory(self, id):
        self.db_instance.delete_inventory(id)


    def build_matrix(self):

        try:

            if os.path.exists('src/files/geo_nodes.json'):
                os.remove('src/files/geo_nodes.json')

            if os.path.exists('src/files/geo_edges.json'):
                os.remove('src/files/geo_edges.json')
            
            inventory = self.db_instance.read_inventory()
            geo_neighborship = []
            edges = []
            node_geolocation = {}
            

            for device in inventory:
                neighbors = []

                hostname = device[0]
                longitude = device[5]
                latitude = device[6]
                neighbors = eval(device[7])

                # CREATE Points Geometry GeoJSON
                node_feature = geojson.Feature(
                    geometry = geojson.Point((longitude, latitude)),
                    properties = {'Hostname': hostname}
                    )

                with open('src/files/geo_nodes.json', 'a') as geo_nodes_file:
                    geojson.dump(node_feature, geo_nodes_file)
                    geo_nodes_file.write('\n')


                node_geolocation[hostname] = (longitude, latitude)
                
                for neighborship in neighbors:
                    edges.append(neighborship)
        
            for edge in edges:
                geo_neighborship.append((edge[0], edge[1], ( node_geolocation[edge[0]], node_geolocation[edge[1]] ) ))
                                            
            for geo_edge in geo_neighborship:
                edge_feature = geojson.Feature(
                    geometry = geojson.LineString(geo_edge[2]),
                    properties = { 'Circuito': str(geo_edge[0] + "-" + geo_edge[1]) }
                    )

                with open('src/files/geo_edges.json', 'a') as geo_edges_file:
                    geojson.dump(edge_feature, geo_edges_file)
                    geo_edges_file.write('\n')


            df = pd.DataFrame(geo_neighborship)
            print(df)
            nx_graph = nx.from_pandas_edgelist(df, source=0, target=1, create_using=nx.MultiDiGraph())
            print(nx_graph)
            nx.draw_spring(nx_graph, with_labels=True, font_weight='bold', node_color="green", edge_color='black')
            plt.show()


            geo_data_frame_nodes = geopandas.read_file('src/files/geo_nodes.json')
            geo_data_frame_edges = geopandas.read_file('src/files/geo_edges.json')

            print("")
            logger.info("Listing Nodes")
            print(geo_data_frame_nodes)
            print("")
            logger.info("Listing Edges")
            print(geo_data_frame_edges)
            print("\n")

            html_explore_map = geo_data_frame_nodes.explore(color="black", marker_kwds=dict(radius=15, fill=True), name="routers")
            geo_data_frame_edges.explore(m=html_explore_map, color="green", style_kwds=dict(weight=4), name="circuits")

            folium.TileLayer('Stamen Toner', control=True).add_to(html_explore_map)
            folium.LayerControl().add_to(html_explore_map)

            html_explore_map.save('www/index.html')
            logger.debug("Browse http://localhost:8000/docs for API Swagger")
            logger.debug("Browse http://localhost:8000/geograph for Geolocated Topology Drawing")
            print("")

            asyncio.run(server.main())
            

        except Exception as e:
            print(TEXT_COLOR['ERROR'] + "*** ERROR *** Matrix can't be created! " + str(e) + "\n" + TEXT_COLOR['END'])



if __name__ == "__main__":
    pass