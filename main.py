import time
from funciones_consulta import obtener_numero_registros, obtener_registros, obtener_detalle_registro


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
                id_juicio = registro.get('idJuicio')
                if id_juicio:
                    detalles = obtener_detalle_registro(id_juicio)
                    if detalles:
                        registro['detalles'] = detalles
                        registros_con_detalles.append(registro)
                    else:
                        print(f"Error al obtener detalles para el idJuicio {id_juicio}")
                else:
                    print("El registro no tiene idJuicio")

            time.sleep(2)  # Pausa de 2 segundos entre cada solicitud
        else:
            print(f"Error al obtener la página {pagina}")

    return registros_con_detalles

if __name__ == "__main__":
    cedula_actor = '0968599020001'
    cedula_demandado = ''

    registros_con_detalles = obtener_registros_con_detalles(cedula_actor, cedula_demandado)
    if registros_con_detalles:
        print("Registros con detalles obtenidos exitosamente:")
        for registro in registros_con_detalles:
            print(registro)
    else:
        print("No se pudieron obtener registros con detalles.")
