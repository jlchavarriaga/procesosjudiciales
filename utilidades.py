import json
import csv


def guardar_en_csv(registros):
    with open('procesos_judiciales.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)


def guardar_en_json(registros):
    with open('procesos_judiciales.json', 'w', encoding='utf-8') as file:
        json.dump(registros, file, indent=4)
