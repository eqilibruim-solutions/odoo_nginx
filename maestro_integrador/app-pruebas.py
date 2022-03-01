import sys
from connection_erp.siigo_api import create_customer_siigo
from main import integracion_data, init_integracion
from utils.tableCreate import *

def init(bd_principal):
    init_integracion(bd_principal)
    datos = integracion_data(bd_principal)

    if datos != 'No existe la empresa':
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


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])