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

- CREATE Inventory in MySQL Database importing from yaml file: *python ibnrisen.py -c hosts.yaml*
- READ Inventory: *python ibnrisen.py -r*
- UPDATE Inventory: *python ibnrisen.py -u [ID]*
- DELETE Inventory: *python ibnrisen.py -d [ID]*
- DRAW TOPOLOGY: *python ibnrisen.py -m*