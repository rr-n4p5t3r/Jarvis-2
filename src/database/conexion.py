import psycopg2
from psycopg2 import DatabaseError
#from decouple import config

def conectar():
    try:
        return psycopg2.connect(
            host = '172.16.3.212',
            user = 'postgres',
            password = '$#4dM1n&%!.',
            database = 'JarvisDBDESA',
        )
    except DatabaseError as ex:
        raise ex