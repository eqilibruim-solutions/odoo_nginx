import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')

# Borrado de tablas
def deletetab(bd_integracion, datadel):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    dropt = "DROP TABLE IF EXISTS "+ datadel +";"
    cur.execute(dropt)
    conn.commit()
    conn.close()
    cur.close()


#### Creacion de tablas ####
# Tabla productos
def m_productos(bd_integracion):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    try:
        tabla = "productos"
        productos = """
                    CREATE TABLE IF NOT EXISTS productos_wms
                    (
                        id integer,
                        referencia character varying(150),
                        barcode character varying(250),
                        name character varying(250),
                        category character varying(150),
                        price character varying(100),
                        cost character varying(100),
                        unidad character varying(150),
                        peso character varying(50),
                        volumen character varying(50),
                        iva character varying(50),
                        lote character varying(50),
                        vencimiento character varying(50)
                    );
        """
        cur.execute(productos)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)

    # Tabla categorias
    try:
        tabla = "categorias"
        categorias = """
                    CREATE TABLE IF NOT EXISTS categorias_wms
                    (
                        id integer,
                        name_category character varying(150)
                    );
        """
        cur.execute(categorias)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)

    # Tabla unidad medida
    try:
        tabla = "und_medida"
        und_medida = """
                    CREATE TABLE IF NOT EXISTS unidad_medida
                    (
                        id integer NOT NULL,
                        name character varying(150)
                    );
        """
        cur.execute(und_medida)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)

    # Tabla iva
    try:
        tabla = "iva"
        t_iva = """
                CREATE TABLE IF NOT EXISTS t_iva
                (
                    id integer NOT NULL,
                    iva character varying(50),
                    CONSTRAINT t_iva_pkey PRIMARY KEY (id)
                );
        """
        cur.execute(t_iva)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)

    # Tabla iva wms
    try:
        tabla = "iva_wms"
        t_iva_wms = """
                CREATE TABLE IF NOT EXISTS t_iva_wms
                (
                    product_tmpl integer,
                    taxes_rel integer,
                    supplier_taxes integer                    
                );
        """
        cur.execute(t_iva)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)
    conn.close()
    cur.close()


def m_clientes(bd_integracion):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    try:
        tabla = "clientes"
        clientes = """
                    CREATE TABLE IF NOT EXISTS clientes_wms
                    (
                        id integer,
                        vat character varying(150) NOT NULL,
                        l10n_latam_identification_type_id character varying(100),
                        customer_rank character varying(20),
                        name character varying(255),
                        email character varying(255),
                        phone character varying(100),
                        mobile character varying(50),
                        street character varying(250),
                        zip character varying(50),
                        city character varying(150),
                        state_id character varying(255),
                        country_id character varying(50)
                    );
        """
        cur.execute(clientes)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)
    conn.close()
    cur.close()

def m_proveedores(bd_integracion):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    try:
        tabla = "proveedores"
        proveedores = """
                        CREATE TABLE IF NOT EXISTS proveedores_wms
                        (
                            id integer NOT NULL,
                            vat character varying(150) NOT NULL,
                            l10n_latam_identification_type_id character varying(100),
                            customer_rank character varying(20),
                            name character varying(255),
                            email character varying(255),
                            phone character varying(100),
                            mobile character varying(50),
                            street character varying(250),
                            zip character varying(50),
                            city character varying(150),
                            state_id character varying(50),
                            country_id character varying(50)
                        );
        """
        cur.execute(proveedores)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)
    conn.close()
    cur.close()

def m_pedidos(bd_integracion):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    try:
        tabla = "pedidos"
        pedidos = """
                        CREATE TABLE IF NOT EXISTS pedidos_wms
                        (
                            compania character varying(150) NOT NULL,
                            num_ped character varying(150) NOT NULL,
                            nit_cliente character varying(150) NOT NULL,
                            cod_vendedor character varying(150),
                            cond_pago character varying(150),
                            observacion character varying(150),
                            fecha_pedido character varying(150),
                            cod_producto character varying(150),
                            cant_pedida character varying(150),
                            precio_unitario character varying(150),
                            descuento character varying(150)
                        );
        """
        cur.execute(pedidos)
        conn.commit()
    except Exception as e:
        print("Error creando la tabla: ", tabla, " Error_: ", e)
    conn.close()
    cur.close()