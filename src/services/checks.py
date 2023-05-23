import re
from src.config.settings import TEXT_COLOR

class InputCheck():
    """
    Clase para realizar los input checks de las direcciones IP y de los valores de Geolocalización, Longitud y Latitud
    """

    def __init__(self) -> None:
        self.pattern_ip_address = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]|([1-3][0-9])"
        self.pattern_long = "^(\\+|-)?(?:180(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\\.[0-9]{1,6})?))$"
        self.pattern_lat = "^(\\+|-)?(?:90(?:(?:\\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\\.[0-9]{1,6})?))$"

    def ip_check(self, ip_address):
        if(re.match(self.pattern_ip_address, ip_address)):
            return True
        else:
            print(TEXT_COLOR['ERROR'] + "IP no válida. Utilice formato a.b.c.d/xx " + "\n" + TEXT_COLOR['END'])
            return False

    def long_check(self, longitude):
        if(re.match(self.pattern_long, longitude)):
            return True
        else:
            print(TEXT_COLOR['ERROR'] + "Longitud no válida. Utilice formato -180.000000 a 180.000000 " + "\n" + TEXT_COLOR['END'])
            return False

    def lat_check(self, latitude):
        if(re.match(self.pattern_lat, latitude)):
            return True
        else:
            print(TEXT_COLOR['ERROR'] + "Latitud no válida. Utilice formato -90.000000 a 90.000000 " + "\n" + TEXT_COLOR['END'])
            return False

if __name__ == "__main__":
        ip_address_input = input("Ingrese nueva dirección IP (formato a.b.c.d/xx): ")
        longitude_input = input("Ingrese nuevo longitud (formato -180.000000 a 180.000000): ")
        latitude_input = input("Ingrese nuevo latitud (formato -90.000000 a 90.000000): ")
        checks = InputCheck()
        result_ip = checks.ip_check(ip_address_input)
        result_long = checks.long_check(longitude_input)
        result_lat = checks.lat_check(latitude_input)

        if (result_ip == False) or (result_long == False) or (result_lat == False):
            print(TEXT_COLOR['ERROR'] + "*** ERROR *** Record can't be updated! " + "\n" + TEXT_COLOR['END'])