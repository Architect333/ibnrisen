import os

## DEFINE PATH ##
BASE_DIR = os.path.dirname((os.path.abspath(__file__)))

## DEFINE TEXT COLORS ##
TEXT_COLOR = {
    'ERROR': '\033[91m',
    'OK': '\33[32m',
    'END': '\033[0m'
    }

## DEFINE DATABASE PARAMETERS ##
DB_NAME = 'ibn2'
DB_ACCESS = {
    'Username': 'root',
    'Password': '',
    'URL': 'localhost',
    'Port': 3306
    }