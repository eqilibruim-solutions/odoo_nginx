import os
import sys
from dotenv import load_dotenv
import psycopg2
from pathlib import Path
from utils.tableCreate import *

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')
DB = os.getenv('BD_WMS')

def init_integracion(empresa):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ DB +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    call_table = "SELECT nombre_compania, wms_bd_principal, wms_bd_integracion, wms_username_api, wms_token_api, wms_endpoint_db, wms_tipo_integracion, ruta_datos, api_endpoint, api_username, api_token FROM maestra_integradora WHERE wms_bd_principal=%s"
    cur.execute(call_table, (empresa,))
    conn.commit()
    datospsql = cur.fetchall()

    # variables valida si existe
    datarow = cur.rowcount
    if datarow == 1:
        compania = datospsql[0][0]
        bd_principal = datospsql[0][1]
        bd_integracion = datospsql[0][2]
        username_api = datospsql[0][3]
        token_api = datospsql[0][4]
        url_api = datospsql[0][5]

        def create_database(database):
            try:
                conn.autocommit = True
                cur = conn.cursor()
                c_database = "CREATE DATABASE "+ database +";"
                cur.execute(c_database)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("BD creada")
                conn.rollback()

        # Creacion base de datos y tablas
        create_database(bd_integracion)
        deletetable = ['productos_wms', 'categorias_wms', 'clientes_wms', 'unidad_medida', 't_iva', 'proveedores_wms', 'tipo_identificacion']
        for deldata in deletetable:
            deletetab(bd_integracion, deldata)
        m_productos(bd_integracion)
        m_clientes(bd_integracion)
        m_proveedores(bd_integracion)
        m_pedidos(bd_integracion)

        return datospsql
    else:
        error = 'No existe la empresa'
        return error

    if conn:
        cur.close()
        conn.close()
    
def integracion_data(empresa):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ DB +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    call_table = "SELECT nombre_compania, wms_bd_principal, wms_bd_integracion, wms_username_api, wms_token_api, wms_endpoint_db, wms_tipo_integracion, ruta_datos, api_endpoint, api_username, api_token FROM maestra_integradora WHERE wms_bd_principal=%s"
    cur.execute(call_table, (empresa,))
    conn.commit()
    datospsql = cur.fetchall()
    datarow = cur.rowcount
    if datarow == 1:
        datos_integracion = datospsql[0]
        return datos_integracion
    else:
        error = 'No existe la empresa'
        return error

    if conn:
        cur.close()
        conn.close()


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])