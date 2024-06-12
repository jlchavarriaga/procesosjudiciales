# procesosjudiciales
Servicio para extraer información de la página web "Consulta de Procesos Judiciales" utilizando técnicas de Web Scraping

Crear el entorno virtual:
    python -m venv venv


Activar el entorno virtual:
    En Windows:
    .\venv\Scripts\activate

    En macOS y Linux:
    source venv/bin/activate


Ejecutar las Pruebas
    python tests.py

Ejecutar la Aplicación
    uvicorn main:app --reload

    1. Obtener solo los procesos básicos:
        Ruta: POST /procesos/basicos
        {
            "cedula_actor": "0968599020001",
            "cedula_demandado": ""
        }
    2. Obtener procesos con detalles:
        Ruta: POST /procesos/detalles
        {
            "cedula_actor": "0968599020001",
            "cedula_demandado": ""
        }
    3. Obtener procesos con detalles y actuaciones judiciales:
        Ruta: POST /procesos/detalles_actuaciones
        {
            "cedula_actor": "0968599020001",
            "cedula_demandado": ""
        }
    4. Obtener detalle de un proceso específico junto con sus actuaciones judiciales:
        Ruta: GET /procesos/{id_juicio}
        Ejemplo de URL: GET /procesos/12345



