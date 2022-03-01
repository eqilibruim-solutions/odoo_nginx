import requests
import json
from main import integracion_data

def generate_token(bd_principal):
    datos = integracion_data(bd_principal)

    patch = 'auth'
    if datos[8] is not None and datos[9] is not None and datos[10] is not None:
        urlToken = datos[8] + patch
        payload = json.dumps({
            "username": datos[9],
            "access_key": datos[10]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        responseToken = requests.post(urlToken, headers=headers, data=payload)
        commit_data = responseToken.json()
        Token = commit_data['access_token']

        return Token
    else:
        Token = None
        return Token
