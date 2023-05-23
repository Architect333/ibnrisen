# ibnrisen
Diplomatura Python UTN

# Tested in local XAMPP MySQL Database Instance
*Requires local MySQL Database Service* 


# COMMAND LINE TOOL
RUN: *python ibnrisen.py [arguments]*

Help: python ibnrisen.py -h

- Create Inventory in MySQL Database from yaml file: *python ibnrisen.py -c hosts.yaml*
- Read Inventory from Database: *python ibnrisen.py -r*
- Update Inventory Record in Database: *python ibnrisen.py -u [ID]*
- Delete Inventory Recordin Database: *python ibnrisen.py -d [ID]*
- Create Topology Network Drawing and GeoMap Topology Drawing: *python ibnrisen.py -d [ID]*