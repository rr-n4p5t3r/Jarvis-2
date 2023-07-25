# Proyecto Jarvis472
# Depuracion Jarvis
# Desarrollado por Ricardo Rosero - n4p5t3r
# Email: rrosero2000@gmail.com
import time
import psycopg2
from decouple import config

try:
    # Parámetros de conexión a PostgreSQL
    hostname = config('DB_HOST')
    username = config('DB_USER')
    password = config('DB_PASSWORD')
    database = config('DB_DATABASE')
    # Conexión a PostgreSQL
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cursor = conn.cursor()
    # Consulta a ejecutar
    consulta = """delete 
    from operacion o 
    where o.opr_idientificadoranddes = '-1' or o.opr_idientificadoranddes = '-2' or 
    o.opr_idientificadoranddes = '-3' or o.opr_idientificadoranddes = '-4' or 
    o.opr_idientificadoranddes = '-5' or o.opr_idientificadoranddes = '-6' or 
    o.opr_idientificadoranddes = '-7' or o.opr_idientificadoranddes = '-8' or 
    o.opr_idientificadoranddes = '-9' or o.opr_idientificadoranddes = '-10' or 
    o.opr_idientificadoranddes = '-11' or o.opr_idientificadoranddes = '-12' or 
    o.opr_idientificadoranddes = '-13' or o.opr_idientificadoranddes = '-14' """

    # Ejecución de la consulta
    cursor.execute(consulta)

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cierre de la conexión
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print("Error al ejecutar la consulta:", e)
