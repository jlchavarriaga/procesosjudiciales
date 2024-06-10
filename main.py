import time

from funciones_consulta import obtener_numero_registros, obtener_registros


def main(cedula_actor='', cedula_demandado=''):
    total_registros = obtener_numero_registros(cedula_actor, cedula_demandado)
    if total_registros == 0:
        print("No se encontraron registros.")
        return

    tamano_pagina = 10
    total_paginas = (total_registros + tamano_pagina - 1) // tamano_pagina  # Redondeo hacia arriba

    print(f"Total de registros: {total_registros}")
    print(f"Total de páginas: {total_paginas}")

    for pagina in range(1, total_paginas + 1):
        registros = obtener_registros(pagina, tamano_pagina, cedula_actor, cedula_demandado)
        if registros is not None:
            print(f"Página {pagina}:")
            print(registros)
        else:
            print(f"Error al obtener la página {pagina}")

        time.sleep(2) # Pausa de 2 segundos entre cada solicitud

if __name__ == "__main__":
    cedula_actor = '0968599020001'
    cedula_demandado = ''
    main(cedula_actor, cedula_demandado)
