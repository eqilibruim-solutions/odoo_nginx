import xmlrpc.client
from main import integracion_data
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')

def create_customer(bd_integracion, bd_principal):
    datosmain = integracion_data(bd_principal)
    # conexion API WMS
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(datosmain[5]))
    uid = common.authenticate(datosmain[1], datosmain[3], datosmain[4], {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(datosmain[5]))

    conn = psycopg2.connect("host="+ HOST +" dbname=" + datosmain[2] + " user=" + USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    cur.execute("SELECT l10n_latam_identification_type_id, vat, name, email, phone, mobile, street, zip, city, state_id, country_id FROM clientes_wms where id=0")
    datospsql = cur.fetchall()
    for dato in datospsql:
        id = models.execute_kw(datosmain[1], uid, datosmain[4], 'res.partner', 'create', [{
            'l10n_latam_identification_type_id': int(dato[0]),
            'vat': dato[1],
            'name': dato[2],
            'email': dato[3],
            'phone': dato[4],
            'mobile': dato[5],
            'street': dato[6],
            'zip': dato[7],
            'city': dato[8],
            'state_id': int(dato[9]),
            'country_id': int(dato[10]),
            'customer_rank': int("1")
        }])
    conn.close()
    cur.close()

def update_customer(bd_integracion, bd_principal):
    datosmain = integracion_data(bd_principal)
    # conexion API WMS
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(datosmain[5]))
    uid = common.authenticate(datosmain[1], datosmain[3], datosmain[4], {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(datosmain[5]))

    conn = psycopg2.connect("host="+ HOST +" dbname=" + datosmain[2] + " user=" + USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone, mobile, street, zip, city, state_id, country_id FROM clientes_wms WHERE id<>0")
    datospsql = cur.fetchall()
    for dato in datospsql:
        id = dato[0]
        models.execute_kw(datosmain[1], uid, datosmain[4], 'res.partner', 'write', [[id], {
            'name': dato[1],
            'phone': dato[3],
            'mobile': dato[4],
            'street': dato[5],
            'zip': dato[6],
            'city': dato[7]
        }])
    conn.close()
    cur.close()