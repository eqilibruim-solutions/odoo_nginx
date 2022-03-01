import requests
import json
import os
import shutil

# Conexión API
print("Generamos Token")
urlToken = "http://34.127.82.68:8000/api/token"
payload='username=simon.trillos%40bexsoluciones.com&password=Ui2tl7MoVO'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}
responseToken = requests.post(urlToken, headers=headers, data=payload)
commit_data = responseToken.json()
Token = commit_data['access_token']
print(Token)


def sendPedido(Token):
    print("Envio Factura")
    print("--- Encabezados ---")

    contenido = os.listdir('/home/simon_trillos/maestro_integrador/pedidos_connection/datosjson')
    print(contenido)
    for cont in contenido:
        origen = "/home/simon_trillos/maestro_integrador/pedidos_connection/datosjson/" + cont
        destino = "/home/simon_trillos/maestro_integrador/pedidos_connection/enviadas/" + cont

        urlFactura = "http://34.127.82.68:8000/pedidos"
        with open(origen) as file:
            data = json.load(file)
        payload = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Token}'
        }
        response = requests.post(urlFactura, headers=headers, data=payload)
        datajson = response.json()
        print("Respuesta: ", response.status_code)
        pedido = cont.replace('.json', '')

        try:
            print('Pedido_: ', pedido)
            shutil.move(origen, destino)
        except:
            print("Error con el pedido: ", pedido)

sendPedido(Token)