import requests
import json
import psycopg2
import os
from dotenv import load_dotenv
from .token import generate_token

load_dotenv()
HOST = os.getenv('HOST_WMS')
USERNAME = os.getenv('USERNAME_WMS')
PASS = os.getenv('PASS_WMS')

def create_customer_siigo(bd_integracion, bd_principal):

    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()

    Token = generate_token(bd_principal)
    if Token is not None:
        parametros = {'page': 1, 'page_size': 1}
        urlCliente = "https://api.siigo.com/v1/customers"
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': Token
        }
        response = requests.get(urlCliente, params=parametros, headers=headers, data=payload)
        datajson = response.json()
        total_results = datajson[u'pagination'][u'total_results']
        iteracciones = round((total_results / 100) + 1)
        
        print("Respuesta: ", response.status_code)
        print('Total Clientes: ', total_results)
        print('Iteracciones: ', iteracciones)
        
        datapage = 1
        while datapage <= iteracciones:
            parametros = {'page': datapage, 'page_size': 100}
            urlCliente = "https://api.siigo.com/v1/customers"
            payload={}
            headers = {
            'Content-Type': 'application/json',
            'Authorization': Token
            }
            response = requests.get(urlCliente, params=parametros, headers=headers, data=payload)
            datajson = response.json()  
            # Inserta de a 100 items
            for dat in datajson['results']:
            
                ident = str(dat['identification'])
                vat = "CO" + ident
                
                if dat['id_type'] == {}:
                    typeident = 'Cédula de ciudadanía'
                else:
                    typeident = str(dat['id_type']['name'])
                    
                try: 
                    if dat['contacts'] is None:
                        if dat['name'] == 'N/A':
                            if dat['commercial_name'] is not None:
                                first_name = str(dat['commercial_name'])
                                last_name = str(dat['commercial_name'])
                            else:
                                first_name = " "
                                last_name = " "
                        else:
                            first_name = str(dat['name'])
                            last_name = str(dat['name'])
                            email = ""
                    else:
                        if dat['contacts'][0]['first_name'] == 'N/A':
                            if dat['commercial_name'] is not None:
                                first_name = str(dat['commercial_name'])
                                last_name = str(dat['commercial_name'])
                        else:
                            first_name = str(dat['contacts'][0]['first_name'])
                            last_name = str(dat['contacts'][0]['last_name'])
                            email = str(dat['contacts'][0]['email'])

                    name = first_name + " " + last_name
                except:
                    first_name = str(dat['name'])
                    last_name = str(dat['name'])
                    email = ""
                    name = first_name + " " + last_name

                try:
                    if dat['phones'][0]['number'] is None:
                        phone = ""
                    else:
                        phone = str(dat['phones'][0]['number'])
                except:
                    phone = ""
                
                try:
                    if dat['contacts'][0]['phone'] is None:
                        mobile = ""
                    else:
                        mobile = str(dat['contacts'][0]['phone']['number'])
                except:
                    mobile = ""   

                street = str(dat['address']['address'])
                if dat['address']['city'] == {}:
                    zip = ""
                    city = ""
                    state_id = "Sin Estado"
                    country_id = "49"
                else:
                    zip = str(dat['address']['city']['city_code'])
                    city = str(dat['address']['city']['city_name'])
                    state_id = str(dat['address']['city']['state_name'])
                    country_id = str(dat['address']['city']['country_name'])
                
                sql = "INSERT INTO clientes_wms(id, vat, l10n_latam_identification_type_id, name, email, phone, mobile, street, zip, city, state_id, country_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (0, vat, typeident, name, email, phone, mobile, street, zip, city, state_id, country_id))
                conn.commit()
            
            datapage += 1
        conn.close()
        cur.close()
    else:
        conn.close()
        cur.close()


def create_product_siigo(bd_integracion, bd_principal):
    conn = psycopg2.connect("host="+ HOST +" dbname="+ bd_integracion +" user="+ USERNAME +" password="+ PASS +"")
    cur = conn.cursor()
    Token = generate_token(bd_principal)
    if Token is not None:
        parametros = {'page': 1, 'page_size': 1}
        urlProduct = "https://api.siigo.com/v1/products"
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': Token
        }
        try:
            response = requests.get(urlProduct, params=parametros, headers=headers, data=payload)
            datajson = response.json()
            total_results = datajson[u'pagination'][u'total_results']
            iteracciones = round((total_results / 100) + 1)
        
            print("Respuesta: ", response.status_code)
            print('Total Productos: ', total_results)
            print('Iteracciones: ', iteracciones)
        except Exception as e:
            print("Error API_: ", e)
    
        datapage = 1
        while datapage <= iteracciones:
            parametros = {'page': datapage, 'page_size': 100}
            urlProduct = "https://api.siigo.com/v1/products"
            payload={}
            headers = {
            'Content-Type': 'application/json',
            'Authorization': Token
            }
            response = requests.get(urlProduct, params=parametros, headers=headers, data=payload)
            datajson = response.json() 
            # Inserta de a 100 items
            for dat in datajson['results']:
                code = str(dat['code'])
                name = str(dat['name'])
                category = str(dat[u'account_group'][u'name'])
                #price = 0
                #iva = 0
                try:
                    if dat['prices'][0]['price_list'] is None:
                        price = 0
                    else:
                        price = dat['prices'][0]['price_list'][0]['value']
                except:
                    price = 0
                finally:
                    price = price

                if dat['taxes'] == []:
                    iva = 0
                else:
                    iva = int(dat['taxes'][0]['percentage'])

                available_quantity = int(dat['available_quantity'])
                
                # Validación codigo de barras
                if dat['additional_fields'] is None:
                    barcode = str(dat[u'additional_fields'][u'barcode'])
                else:
                    barcode = ""

                sql = "INSERT INTO productos_wms(id, referencia, barcode, name, category, price, cost, unidad, peso, volumen, iva, lote) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (0, code, barcode, name, category, price, 0, 'UND', 0, 0, iva, 'none'))
                conn.commit()
            
            datapage += 1