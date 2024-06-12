import time
from funciones_consulta import obtener_numero_registros, obtener_registros, obtener_detalle_registro, obtener_actuaciones_judiciales, obtener_info_proceso
from utilidades import guardar_en_csv, guardar_en_json

def obtener_solo_registros(cedula_actor='', cedula_demandado=''):
    total_registros = obtener_numero_registros(cedula_actor, cedula_demandado)
    if total_registros == 0:
        print("No se encontraron registros.")
        return None

    tamano_pagina = 10
    total_paginas = (total_registros + tamano_pagina - 1) // tamano_pagina  # Redondeo hacia arriba

    print(f"Total de registros: {total_registros}")
    print(f"Total de páginas: {total_paginas}")

    registros_basicos = []

    for pagina in range(1, total_paginas + 1):
        registros = obtener_registros(pagina, tamano_pagina, cedula_actor, cedula_demandado)
        if registros is not None:
            print(f"Obteniendo la página {pagina}...")
            registros_basicos.extend(registros)
        else:
            print(f"Error al obtener la página {pagina}")

    return registros_basicos


def obtener_registros_con_detalles(cedula_actor='', cedula_demandado=''):
    total_registros = obtener_numero_registros(cedula_actor, cedula_demandado)
    if total_registros == 0:
        print("No se encontraron registros.")
        return None

    tamano_pagina = 10
    total_paginas = (total_registros + tamano_pagina - 1) // tamano_pagina  # Redondeo hacia arriba

    print(f"Total de registros: {total_registros}")
    print(f"Total de páginas: {total_paginas}")

    registros_con_detalles = []

    for pagina in range(1, total_paginas + 1):
        registros = obtener_registros(pagina, tamano_pagina, cedula_actor, cedula_demandado)
        if registros is not None:
            print(f"Obteniendo detalles de la página {pagina}...")
            for registro in registros:
                detalles = obtener_detalle_registro(registro['idJuicio'])
                if detalles:
                    registro['detalles'] = detalles
                    registros_con_detalles.append(registro)
                else:
                    print(f"Error al obtener detalles para el registro con idJuicio {registro['idJuicio']}")
        else:
            print(f"Error al obtener la página {pagina}")

    return registros_con_detalles


def obtener_detalle_y_actuaciones_de_proceso(id_juicio):
    try:
        info_proceso = obtener_info_proceso(id_juicio)
        detalle = obtener_detalle_registro(id_juicio)
        if detalle:
            print(f"Detalle obtenido: {detalle}")
            if isinstance(detalle, list):
                for item in detalle:
                    procesar_detalle(item, id_juicio)
            elif isinstance(detalle, dict):
                procesar_detalle(detalle, id_juicio)
            else:
                print(f"Tipo inesperado de detalle: {type(detalle)}")
        resultado = {
            'info_proceso': info_proceso,
            'detalle': detalle
        }
        return resultado
    except Exception as e:
        print(f"Error en obtener_detalle_y_actuaciones_de_proceso: {str(e)}")
        return None

def procesar_detalle(detalle, id_juicio):
    try:
        print(f"Procesando detalle: {detalle}")
        if isinstance(detalle, dict):
            for incidente_judicatura in detalle.get('lstIncidenteJudicatura', []):
                id_movimiento_juicio_incidente = incidente_judicatura.get('idMovimientoJuicioIncidente')
                id_judicatura = incidente_judicatura.get('idJudicaturaDestino')
                id_incidente_judicatura = incidente_judicatura.get('idIncidenteJudicatura')
                nombre_judicatura = incidente_judicatura.get('nombreJudicatura')

                actuaciones_judiciales = obtener_actuaciones_judiciales(
                    id_movimiento_juicio_incidente,
                    id_juicio,
                    id_judicatura,
                    id_incidente_judicatura,
                    nombre_judicatura
                )
                if actuaciones_judiciales:
                    incidente_judicatura['actuacionesJudiciales'] = actuaciones_judiciales
                else:
                    print(f"Error al obtener actuaciones judiciales para el incidente judicatura con id {id_incidente_judicatura}")
        else:
            print(f"El detalle no es un diccionario: {detalle}")
    except Exception as e:
        print(f"Error en procesar_detalle: {str(e)}")

def obtener_registros_con_detalles_y_actuaciones(cedula_actor='', cedula_demandado=''):
    registros_con_detalles = obtener_registros_con_detalles(cedula_actor, cedula_demandado)
    if registros_con_detalles:
        for registro in registros_con_detalles:
            if isinstance(registro['detalles'], list):
                for detalle in registro['detalles']:
                    procesar_detalle(detalle, registro.get('idJuicio'))
            elif isinstance(registro['detalles'], dict):
                procesar_detalle(registro['detalles'], registro.get('idJuicio'))
            else:
                print(f"Tipo inesperado de detalles: {type(registro['detalles'])}")
            time.sleep(2)  # Pausa de 2 segundos entre cada solicitud

    return registros_con_detalles


if __name__ == "__main__":
    cedula_actor = '0968599020001'
    cedula_demandado = ''

    registros_con_detalles_y_actuaciones = obtener_registros_con_detalles_y_actuaciones(cedula_actor, cedula_demandado)

    guardar_en_csv(registros_con_detalles_y_actuaciones)
    guardar_en_json(registros_con_detalles_y_actuaciones)

    if registros_con_detalles_y_actuaciones:
        print("Registros con detalles y actuaciones judiciales obtenidos exitosamente:")
        for registro in registros_con_detalles_y_actuaciones:
            print(registro)
    else:
        print("No se pudieron obtener registros con detalles y actuaciones judiciales.")
