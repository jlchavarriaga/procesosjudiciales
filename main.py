from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from service import (
    obtener_solo_registros,
    obtener_registros_con_detalles,
    obtener_registros_con_detalles_y_actuaciones,
    obtener_detalle_y_actuaciones_de_proceso
)

app = FastAPI()

class Payload(BaseModel):
    cedula_actor: Optional[str] = ''
    cedula_demandado: Optional[str] = ''

@app.post("/procesos/basicos")
def get_solo_procesos(payload: Payload):
    try:
        registros = obtener_solo_registros(payload.cedula_actor, payload.cedula_demandado)
        if not registros:
            raise HTTPException(status_code=404, detail="No se encontraron registros.")
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/procesos/detalles")
def get_procesos_con_detalles(payload: Payload):
    try:
        registros = obtener_registros_con_detalles(payload.cedula_actor, payload.cedula_demandado)
        if not registros:
            raise HTTPException(status_code=404, detail="No se encontraron registros.")
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/procesos/detalles_actuaciones")
def get_procesos_con_detalles_y_actuaciones(payload: Payload):
    try:
        registros = obtener_registros_con_detalles_y_actuaciones(payload.cedula_actor, payload.cedula_demandado)
        if not registros:
            raise HTTPException(status_code=404, detail="No se encontraron registros.")
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/procesos/{id_juicio}")
def get_detalle_y_actuaciones(id_juicio: str):
    try:
        print(f"Recibido id_juicio: {id_juicio}")
        detalle = obtener_detalle_y_actuaciones_de_proceso(id_juicio)
        if not detalle:
            raise HTTPException(status_code=404, detail="No se encontraron detalles para el proceso.")
        return detalle
    except Exception as e:
        print(f"Error en get_detalle_y_actuaciones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
