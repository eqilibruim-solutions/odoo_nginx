from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')
DB = os.getenv('BD_WMS')

def sincronizaciones_log(empresa, tabla_sinc, obs, inicio, fin):
    # Insertando datos en log
    fin = now = datetime.now()
    conn = psycopg2.connect("host="+ HOST +" dbname=" + DB + " user=" + USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    insert_log = "INSERT INTO log_sincronizaciones(empresa, tabla_sincronizada, datos_sincronizados, fecha_inicio, fecha_fin) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(insert_log, (empresa, tabla_sinc, obs, inicio, fin))
    conn.commit()
    conn.close()
    cur.close()  