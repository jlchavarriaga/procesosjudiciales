import requests


def obtener_numero_registros(cedula_actor='', cedula_demandado=''):
    url = 'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/contarCausas'
    payload = {
        "numeroCausa": "",
        "actor": {
            "cedulaActor": cedula_actor,
            "nombreActor": ""
        },
        "demandado": {
            "cedulaDemandado": cedula_demandado,
            "nombreDemandado": ""
        },
        "provincia": "",
        "numeroFiscalia": "",
        "recaptcha": "verdad"
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-419,es-US;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': str(len(str(payload))),
        'Content-Type': 'application/json',
        'Host': 'api.funcionjudicial.gob.ec',
        'Origin': 'https://procesosjudiciales.funcionjudicial.gob.ec',
        'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error en la solicitud:', response.status_code)
        print('Detalle:', response.text)
        return 0


def obtener_registros(pagina, tamano, cedula_actor='', cedula_demandado=''):
    url = f'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page={pagina}&size={tamano}'
    payload = {
        "numeroCausa": "",
        "actor": {
            "cedulaActor": cedula_actor,
            "nombreActor": ""
        },
        "demandado": {
            "cedulaDemandado": cedula_demandado,
            "nombreDemandado": ""
        },
        "provincia": "",
        "numeroFiscalia": "",
        "recaptcha": "verdad",
        "first": pagina,
        "pageSize": tamano
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-419,es-US;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': str(len(str(payload))),
        'Content-Type': 'application/json',
        'Host': 'api.funcionjudicial.gob.ec',
        'Origin': 'https://procesosjudiciales.funcionjudicial.gob.ec',
        'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error en la solicitud:', response.status_code)
        print('Detalle:', response.text)
        return None


# No implementado por seguridad
def obtener_todos_los_registros(cedula_actor='', cedula_demandado=''):
    total_registros = obtener_numero_registros(cedula_actor, cedula_demandado)
    if total_registros == 0:
        print("No se encontraron registros.")
        return None

    url = f'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page=1&size={total_registros}'
    payload = {
        "numeroCausa": "",
        "actor": {
            "cedulaActor": cedula_actor,
            "nombreActor": ""
        },
        "demandado": {
            "cedulaDemandado": cedula_demandado,
            "nombreDemandado": ""
        },
        "provincia": "",
        "numeroFiscalia": "",
        "recaptcha": "verdad",
        "first": 1,
        "pageSize": total_registros
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-419,es-US;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': str(len(str(payload))),
        'Content-Type': 'application/json',
        'Host': 'api.funcionjudicial.gob.ec',
        'Origin': 'https://procesosjudiciales.funcionjudicial.gob.ec',
        'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Ajusta esto según el formato de la respuesta
    else:
        print('Error en la solicitud:', response.status_code)
        print('Detalle:', response.text)
        return None


def obtener_detalle_registro(id_juicio):
    url = f'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{id_juicio}'
    headers = {
        'Accept': 'application/vnd.api.v1+json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-419,es-US;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'api.funcionjudicial.gob.ec',
        'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Ajusta esto según el formato de la respuesta
    else:
        print('Error en la solicitud:', response.status_code)
        print('Detalle:', response.text)
        return None