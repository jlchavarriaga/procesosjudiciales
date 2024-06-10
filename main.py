import requests

url = 'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page=1&size=20'

payload = {
    "numeroCausa": "",
    "actor": {
        "cedulaActor": "0968599020001",
        "nombreActor": ""
    },
    "demandado": {
        "cedulaDemandado": "",
        "nombreDemandado": ""
    },
    "provincia": "",
    "numeroFiscalia": "",
    "recaptcha": "verdad",
    "first": 1,
    "pageSize": 10
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
    print('Solicitud enviada con éxito')
    print('Respuesta:', response.json())
else:
    print('Error en la solicitud:', response.status_code)
    print('Detalle:', response.text)
