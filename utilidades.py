import csv
import json


def guardar_en_csv(registros):
    if not registros:
        print("No hay registros para guardar en CSV.")
        return

    keys = registros[0].keys()
    with open('procesos_judiciales.csv', 'w', newline='', encoding='utf-8') as file:
        dict_writer = csv.DictWriter(file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(registros)


def guardar_en_json(registros):
    if not registros:
        print("No hay registros para guardar en JSON.")
        return

    with open('procesos_judiciales.json', 'w', encoding='utf-8') as file:
        json.dump(registros, file, indent=4, ensure_ascii=False)
