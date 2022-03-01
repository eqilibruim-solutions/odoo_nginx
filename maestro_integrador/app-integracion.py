#Integracion por medio de archivos planos
import json
from datetime import datetime
from os import getcwd
import os
import sys
from main import integracion_data, init_integracion
from utils.tableCreate import *
from utils.load_data import *
from utils.internalProcess import *
from utils.productos_wms import create_product, update_product
from utils.clientes_wms import create_customer, update_customer
from utils.proveedores_wms import create_supplier, update_supplier
from connection_erp.siigo_api import create_customer_siigo, create_product_siigo
from datetime import datetime, timedelta
from log_sincronizacion import sincronizaciones_log

# integracion productos txt
def integracion_productos_wms_txt(bd_principal):
    inicio = datetime.now()
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)

    if datos != 'No existe la empresa':
        empresa = datos[0]
        #Borrado datos
        datDelete = ['t_iva', 'productos_wms', 'unidad_medida', 'categorias_wms']
        for dat in datDelete:
            deletetab(datos[2], dat)
        m_productos(datos[2])
        load_data(datos[1], 'productos_wms', datos[7])
        procesos_internos_productos(datos[2], datos[1])

        # Insert productos wms
        creados = create_product(datos[2], datos[1])
        if creados is None:
            creados = 'No hay archivo'
        
        # Actualizar productos wms
        actualizados = update_product(datos[2], datos[1])
        if actualizados is None:
            actualizados = ' No hay archivo'

        # Insertando datos en log
        datos_sincronizados = creados+actualizados
        fin = now = datetime.now()   
        sincronizaciones_log(empresa, 'productos_wms', str(datos_sincronizados), inicio, fin)
        return 'Correcta'
    else:
        return 'Empresa no existe'


def integracion_clientes_wms_txt(bd_principal):
    inicio = datetime.now()
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)

    if datos != 'No existe la empresa':
        empresa = datos[0]
        #Borrado datos
        datDelete = ['clientes_wms']
        for dat in datDelete:
            deletetab(datos[2], dat)
        m_clientes(datos[2])
        load_data(datos[1], 'clientes_wms', datos[7])
        procesos_internos_clientes(datos[2], datos[1])

        # Insert clientes wms
        creados = create_customer(datos[2], datos[1])
        if creados is None:
            creados = 'No hay archivo'
        
        # Actualizar cliente wms
        actualizados = update_customer(datos[2], datos[1])
        if actualizados is None:
            actualizados = ' No hay archivo'

        # Insertando datos en log
        datos_sincronizados = creados+actualizados
        fin = now = datetime.now()   
        sincronizaciones_log(empresa, 'clientes_wms', str(datos_sincronizados), inicio, fin)   
        return 'Correcta'
    else:
        return 'Empresa no existe'


def integracion_proveedores_wms_txt(bd_principal):
    inicio = datetime.now()
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)

    if datos != 'No existe la empresa':
        empresa = datos[0]
        #Borrado datos
        datDelete = ['proveedores_wms']
        for dat in datDelete:
            deletetab(datos[2], dat)
        m_proveedores(datos[2])
        load_data(datos[1], 'proveedores_wms', datos[7])
        procesos_internos_proveedores(datos[2], datos[1])

        # Insert proovedores wms
        creados = create_supplier(datos[2], datos[1])
        if creados is None:
            creados = 'No hay archivo'
        
        # Actualizar proovedores wms
        actualizados = update_supplier(datos[2], datos[1])
        if actualizados is None:
            actualizados = ' No hay archivo'

        # Insertando datos en log
        datos_sincronizados = creados+actualizados
        fin = now = datetime.now()   
        sincronizaciones_log(empresa, 'proveedores_wms', str(datos_sincronizados), inicio, fin) 
        return 'Correcta'
    else:
        return 'Empresa no existe'


# Conexion por API
def integracion_productos_wms_api(bd_principal):
    inicio = datetime.now()
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)

    if datos != 'No existe la empresa':
        empresa = datos[0]
        # Borrado datos
        datDelete = ['t_iva', 'productos_wms', 'unidad_medida', 'categorias_wms']
        for dat in datDelete:
            deletetab(datos[2], dat)
        # Creacion tablas
        m_productos(datos[2])
        create_product_siigo(datos[2], datos[1])
        # Procesado y organizacion datos
        procesos_internos_productos(datos[2], datos[1])

        
        # Insert productos wms
        creados = create_product(datos[2], datos[1])
        if creados is None:
            creados = 'No hay credenciales API'

        # Actualizar productos wms
        actualizados = update_product(datos[2], datos[1])
        if actualizados is None:
            actualizados = ' No hay credenciales API'

        # Insertando datos en log
        datos_sincronizados = creados+actualizados
        fin = now = datetime.now()   
        sincronizaciones_log(empresa, 'productos_wms', str(datos_sincronizados), inicio, fin)
        return 'Correcta'
    else:
        return 'Empresa no existe'


def integracion_clientes_wms_api(bd_principal):
    inicio = datetime.now()
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)

    if datos != 'No existe la empresa':
        empresa = datos[0]
        # Borrado datos
        datDelete = ['clientes_wms']
        for dat in datDelete:
            deletetab(datos[2], dat)
        # Creacion tablas
        m_clientes(datos[2])
        # Insertando datos tablas
        create_customer_siigo(datos[2], datos[1])
        # Depurando y organizando datos
        procesos_internos_clientes(datos[2], datos[1])

        # Insert clientes wms
        creados = create_customer(datos[2], datos[1])
        if creados is None:
            creados = 'No hay credenciales API'
        
        # Actualizar cliente wms
        actualizados = update_customer(datos[2], datos[1])
        if actualizados is None:
            actualizados = ' No hay credenciales API'

        # Insertando datos en log
        datos_sincronizados = creados+actualizados
        fin = now = datetime.now()   
        sincronizaciones_log(empresa, 'clientes_wms', str(datos_sincronizados), inicio, fin)
        return 'Correcta'
    else:
        return 'Empresa no existe'


def integracion_proveedores_wms_api(bd_principal):
    print('No hay API sincronizacion proveedores...')

def integracion_pedidos_wms(bd_principal):
    inicio = datetime.now()
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)
    cargar_data = load_data(datos[1], 'pedidos_wms', datos[7])

    


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])