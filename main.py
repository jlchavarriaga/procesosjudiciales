from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from fastapi_users.auth import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi_users.models import BaseOAuthAccount
from fastapi_users import FastAPIUsers
from service import (
    obtener_solo_registros,
    obtener_registros_con_detalles,
    obtener_registros_con_detalles_y_actuaciones,
    obtener_detalle_y_actuaciones_de_proceso
)

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
SECRET = "SECRET"

Base: DeclarativeMeta = declarative_base()

class UserTable(Base, SQLAlchemyBaseUserTable):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserManager(BaseUserManager):
    user_db_model = UserTable

    async def on_after_register(self, user: UserTable, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

def get_user_db():
    db = SessionLocal()
    yield SQLAlchemyUserDatabase(UserTable, db)

# Define the JWT authentication
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

fastapi_users = FastAPIUsers(
    user_manager=get_user_db(),
    auth_backends=[jwt_authentication]
)

@app.post("/procesos/basicos")
async def get_solo_procesos(payload: Payload, user: UserTable = Depends(jwt_authentication.get_current_user)):
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
async def get_detalle_y_actuaciones(id_juicio: str, user: UserTable = Depends(fastapi_users.current_user())):
    try:
        print(f"Recibido id_juicio: {id_juicio}")
        detalle = obtener_detalle_y_actuaciones_de_proceso(id_juicio)
        if not detalle:
            raise HTTPException(status_code=404, detail="No se encontraron detalles para el proceso.")
        return detalle
    except Exception as e:
        print(f"Error en get_detalle_y_actuaciones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
