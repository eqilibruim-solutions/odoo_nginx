from .tableCreate import *
from main import *
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')

def load_data(bd_integracion, tabla, ruta):
    datos = integracion_data(bd_integracion)

    try:
        proceso = "Carga de archivo"
        conn = psycopg2.connect("host="+ HOST +" dbname=" + datos[2] + " user=" + USERNAME +" password="+ PASS +"")
        cur = conn.cursor()
        with open(ruta + tabla + '.csv', 'r', encoding='latin1' ) as f:
            #next(f)
            cur.copy_from(f, tabla, sep=';')
            conn.commit()
    except Exception as e:
        print("Error en el proceso: ", proceso, e)

    if conn:
        cur.close()
        conn.close()