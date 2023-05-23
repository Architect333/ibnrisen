"""
MVC Pattern: View module, parsing CLI arguments.
"""

import argparse
import sys

class ArgsSetup():
    """
    ### V (VIEW) --> User Interaction ###

    Update Database using the following arguments:
    C -> "CREATE record in Database from specified JSON <FILE>"
    R -> "READ record from Database"
    U -> "UPDATE record from Database according to specified JSON <FILE>"
    D -> "DELETE record from Database"

    Choose an action to perform from the following options:
    CONFIGS -> "Create configurations for devices"
    MATRIX -> "Show traffic matrix and draw topology"
    SAVE -> "Save configs to specified text <FILE>"
    """

    def __init__(self) -> None:
        self.action = ""
        self.inventory = ""
        self.create_configs = False
        self.create_matrix = False


    def args_setup(self):
        parser = argparse.ArgumentParser(description="Welcome to Intent-Based Networking IBNRisen")

        crud_group = parser.add_mutually_exclusive_group(required=False)
        crud_group.add_argument("-c", "--create", help="CREATE Inventory record in Database from specified YAML <FILE>")
        crud_group.add_argument("-r", "--read", help="READ record from Database", action="store_true")
        crud_group.add_argument("-u", "--update", help="UPDATE record from Database according to specified ID")
        crud_group.add_argument("-d", "--delete", help="DELETE record from Database according to specified ID")

        parser.add_argument("-m", "--matrix", help="Show traffic matrix and draw topology", required=False, action="store_true")
        
        argument = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

        if argument.create:
            self.action = "create"
            self.inventory = argument.create
        elif argument.read:
            self.action = "read"
        elif argument.update:
            self.action = "update"
            self.inventory = argument.update
        elif argument.delete:
            self.action = "delete"
            self.inventory = argument.delete

        if argument.matrix:
            self.create_matrix = argument.matrix


        return self.action, self.inventory, self.create_configs, self.create_matrix
        

if __name__ == "__main__":
    args_setup = ArgsSetup()
    args_setup.args_setup()
    