# ibnrisen - Intent-Based Networking Risen!
Diplomatura Python UTN
- This tool allows you to consume your inventory using a YAML file and saving it to MySQL database.
- You can perform CRUD operations to the database named ibn2
- You can also draw a geolocated topology for further network analysis

## Next features planned ##
- Perform topology operations using Neo4j Graph Database
- Integrate with Nornir Framework for network automation operations


## Tested in local XAMPP MySQL Database Instance ##
*Requires local MySQL Database Service* 


# COMMAND LINE TOOL
RUN: *python ibnrisen.py [arguments]*

Help: python ibnrisen.py -h

- Create Inventory in MySQL Database from yaml file:
    *python ibnrisen.py -c hosts.yaml*

- Read Inventory from Database:
    *python ibnrisen.py -r*

- Update Inventory Record in Database:
    *python ibnrisen.py -u [ID]*

- Delete Inventory Recordin Database:
    *python ibnrisen.py -d [ID]*

- Create Topology Network Drawing and GeoMap Topology Drawing:
    *python ibnrisen.py -m*