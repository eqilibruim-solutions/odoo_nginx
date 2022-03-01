import xmlrpc.client
from main import integracion_data
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')

def create_product(bd_integracion, bd_principal):
    datosmain = integracion_data(bd_principal)
    # conexion API WMS
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(datosmain[5]))
    uid = common.authenticate(datosmain[1], datosmain[3], datosmain[4], {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(datosmain[5]))

    conn = psycopg2.connect("host="+ HOST +" dbname=" + datosmain[2] + " user=" + USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    id = 0
    cur.execute("SELECT referencia, name, barcode, category, price, cost, unidad, peso, volumen, iva, lote FROM productos_wms WHERE id=0")
    datospsql = cur.fetchall()
    datarow = cur.rowcount
    try:
        for dato in datospsql:
            id = models.execute_kw(datosmain[1], uid, datosmain[4], 'product.template', 'create', [{
                    "default_code": str(dato[0]),
                    "name": str(dato[1]),
                    #"barcode": dato[2],
                    "categ_id": int(dato[3]),
                    "price": str(dato[4]),
                    "standard_price": str(dato[5]),
                    "uom_id": int(dato[6]),
                    "uom_po_id": int(dato[6]),
                    "type": "product",
                    #"tracking": dato[11],
                    "volume": str(dato[7]),
                    "weight": str(dato[8]),
                    "active": 1
                }])
    except Exception as e:
        print("Error insertando wms:", e)
        print("Id: ", id, " name: ", dato[0])
    conn.close()
    cur.close()
    return datarow

def update_product(bd_integracion, bd_principal):
    datosmain = integracion_data(bd_principal)
    # conexion API WMS
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(datosmain[5]))
    uid = common.authenticate(datosmain[1], datosmain[3], datosmain[4], {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(datosmain[5]))

    conn = psycopg2.connect("host="+ HOST +" dbname=" + datosmain[2] + " user=" + USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    cur.execute("SELECT id, referencia, barcode, name, category, price, cost, unidad, peso, volumen, iva, lote, vencimiento FROM productos_wms WHERE id<>0;")
    datospsql = cur.fetchall()
    datarow = cur.rowcount
    try:
        for dato in datospsql:
            if dato[2] == '':
                id = dato[0]
                models.execute_kw(datosmain[1], uid, datosmain[4], 'product.template', 'write', [[id], {
                    "default_code": dato[1],
                    #"barcode": dato[2],
                    "name": str(dato[3]),
                    "categ_id": int(dato[4]),
                    "price": str(dato[5]),
                    "list_price": str(dato[5]),
                    "standard_price": str(dato[6]),
                    #"uom_id": int(dato[7]),
                    #"uom_po_id": int(dato[7]),
                    #"taxes_id": dato[10],
                    #"supplier_taxes_id": dato[10],
                    #"type": "product",
                    "tracking": str(dato[11]),
                    "volume": str(dato[9]),
                    "weight": str(dato[8])
                }])
            else:
                id = dato[0]
                models.execute_kw(datosmain[1], uid, datosmain[4], 'product.template', 'write', [[id], {
                    "default_code": dato[1],
                    "barcode": dato[2],
                    "name": str(dato[3]),
                    "categ_id": int(dato[4]),
                    "price": str(dato[5]),
                    "list_price": str(dato[5]),
                    "standard_price": str(dato[6]),
                    "tracking": str(dato[11]),
                    "volume": str(dato[9]),
                    "weight": str(dato[8])
                }])
            if dato[11] == 'lot' and dato[12] != "0":
                id = dato[0]
                models.execute_kw(datosmain[1], uid, datosmain[4], 'product.template', 'write', [[id], {
                    "default_code": dato[1],
                    #"barcode": dato[2],
                    "name": str(dato[3]),
                    "categ_id": int(dato[4]),
                    "price": str(dato[5]),
                    "list_price": str(dato[5]),
                    "standard_price": str(dato[6]),
                    "tracking": str(dato[11]),
                    "volume": str(dato[9]),
                    "weight": str(dato[8]),
                    "use_expiration_date": int("1"),
                    "expiration_time": int(dato[12]),
                    "use_time": int(dato[12]),
                    "removal_time": int(dato[12]),
                    "alert_time": int(dato[12])
                }])
    except Exception as e:
        print("Error actualizando wms:", e)
        print("Id: ", id, " name: ", dato[3])        
    conn.close()
    cur.close()
    return datarow