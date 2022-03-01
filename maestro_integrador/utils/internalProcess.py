import psycopg2
import xmlrpc.client
from main import integracion_data
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')

def procesos_internos_productos(bd_integracion, bd_principal):
    datos = integracion_data(bd_principal)

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(datos[5]))
    uid = common.authenticate(datos[1], datos[3], datos[4], {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(datos[5]))

    connection = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    # Datos bd integracion
    with connection:
        with connection.cursor() as cursor:
            try:
                validacion = "SELECT name FROM pg_available_extensions WHERE name='dblink'"
                cursor.execute(validacion)
                val = cursor.fetchall()
                if val == False:
                    cursor.execute("CREATE EXTENSION dblink;")
                    connection.commit()                    
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                datosreplace = ['price', 'cost', 'peso', 'volumen']
                for dator in datosreplace:
                    query = "update productos_wms SET "+ dator +"=replace("+ dator +", ',', '.')"
                    cursor.execute(query)
                    connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("INSERT INTO categorias_wms(name_category, id) select distinct category, 0 as id from productos_wms")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE categorias_wms a SET id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name FROM product_category') AS b (id integer, name text)) as b WHERE a.name_category=b.name;")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("SELECT name_category FROM categorias_wms WHERE id=0")
                datosc = cursor.fetchall()
                for datc in datosc:
                    categoria = models.execute_kw(datos[1], uid, datos[4], 'product.category', 'create', [{
                        'name': str(datc[0])
                    }])
            except Exception as e:
                print("Error en el proceso create category: ", e)
            
            try:
                cursor.execute("UPDATE categorias_wms a SET id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name FROM product_category') AS b (id integer, name text)) as b WHERE a.name_category=b.name;")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)
            
            try:
                cursor.execute("INSERT INTO t_iva(id, iva) VALUES(9, '19'), (10, '5'), (11, '0')")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)            

            try:
                cursor.execute("UPDATE productos_wms SET iva=b.id FROM t_iva as b WHERE productos_wms.iva=b.iva")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("INSERT INTO unidad_medida(id, name) SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name FROM uom_uom') AS b (id integer, name text)")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)  

            try:
                cursor.execute("UPDATE productos_wms SET unidad=b.id FROM unidad_medida as b WHERE productos_wms.unidad=b.name;")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE productos_wms a SET category=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name FROM product_category') AS b (id integer, name text)) as b WHERE a.category=b.name;")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                query = "UPDATE productos_wms a SET id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name, default_code FROM product_template') AS b (id integer, name text, default_code text)) as b WHERE a.name=b.name or a.referencia=b.default_code;" 
                cursor.execute(query)
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            """
            try:
                conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_principal +" user="+ USERNAME +" password=" + PASS)
                cur = conn.cursor()
                cur.execute("UPDATE product_taxes_rel a SET tax_id=b.taxes_rel FROM (SELECT * FROM dblink('dbname="+ bd_integracion +"','SELECT product_tmpl_id, taxes_rel, supplier_taxes_rel FROM T_IVA_WMS') AS b (product_tmpl_id integer, taxes_rel integer, supplier_taxes_rel integer)) as b WHERE a.prod_id=b.product_tmpl_id;")
                conn.commit()
                cur.execute("UPDATE product_supplier_taxes_rel a SET tax_id=b.supplier_taxes_rel FROM (SELECT * FROM dblink('dbname="+ bd_integracion +"','SELECT product_tmpl_id, taxes_rel, supplier_taxes_rel FROM T_IVA_WMS') AS b (product_tmpl_id integer, taxes_rel integer, supplier_taxes_rel integer)) as b WHERE a.prod_id=b.product_tmpl_id;")
                conn.commit()           
            except Exception as e:
                conn.close()
                print("Error en proceso actualizacion iva : ", e) 
            """

    connection.close()
    cursor.close()

def procesos_internos_clientes(bd_integracion, bd_principal):
    connection = psycopg2.connect("host="+ HOST +" dbname="+ bd_principal +" user="+ USERNAME +" password="+ PASS +"")
    # Actualizacion principal controlador DIAN
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("UPDATE l10n_latam_identification_type SET is_vat=false WHERE id=4")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)
    connection.close()
    cursor.close()

    connection = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    # Datos bd integracion
    with connection:
        with connection.cursor() as cursor:
            try:
                validacion = "SELECT name FROM pg_available_extensions WHERE name='dblink'"
                cursor.execute(validacion)
                val = cursor.fetchall()
                if val == False:
                    cursor.execute("CREATE EXTENSION dblink;")
                    connection.commit()                    
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE clientes_wms a SET state_id=b.id FROM (SELECT * FROM dblink('dbname=" + bd_principal + "','SELECT id, name FROM res_country_state') AS b (id integer, name text)) as b WHERE a.state_id=b.name")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE clientes_wms SET country_id=49")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE clientes_wms SET state_id='656' WHERE state_id='COR'")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE clientes_wms a SET id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, vat FROM res_partner') AS b (id integer, vat text)) as b WHERE a.vat=b.vat")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)
            
            try:
                cursor.execute("UPDATE clientes_wms a SET l10n_latam_identification_type_id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name FROM l10n_latam_identification_type') AS b (id integer, name text)) as b WHERE a.l10n_latam_identification_type_id=b.name")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

    connection.close()
    cursor.close()
    

def procesos_internos_proveedores(bd_integracion, bd_principal):
    connection = psycopg2.connect("host="+ HOST +" dbname="+ bd_principal +" user="+ USERNAME +" password="+ PASS +"")
    # Actualizacion principal controlador DIAN
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("UPDATE l10n_latam_identification_type SET is_vat=false WHERE id=4")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)
    connection.close()
    cursor.close()

    connection = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    # Datos bd integracion
    with connection:
        with connection.cursor() as cursor:
            try:
                validacion = "SELECT name FROM pg_available_extensions WHERE name='dblink'"
                cursor.execute(validacion)
                val = cursor.fetchall()
                if val == False:
                    cursor.execute("CREATE EXTENSION dblink;")
                    connection.commit()                    
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE proveedores_wms a SET state_id=b.id FROM (SELECT * FROM dblink('dbname=" + bd_principal + "','SELECT id, name FROM res_country_state') AS b (id integer, name text)) as b WHERE a.state_id=b.name")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE proveedores_wms SET country_id=49")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE proveedores_wms SET state_id='656' WHERE state_id='COR'")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE proveedores_wms a SET id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, vat FROM res_partner') AS b (id integer, vat text)) as b WHERE a.vat=b.vat")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

            try:
                cursor.execute("UPDATE proveedores_wms a SET l10n_latam_identification_type_id=b.id FROM (SELECT * FROM dblink('dbname="+ bd_principal +"','SELECT id, name FROM l10n_latam_identification_type') AS b (id integer, name text)) as b WHERE a.l10n_latam_identification_type_id=b.name")
                connection.commit()
            except Exception as e:
                print("Error en el proceso: ", e)

    connection.close()
    cursor.close()

    