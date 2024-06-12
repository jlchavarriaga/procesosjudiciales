# auth.py
from sqlalchemy import create_engine
from fastapi_users import BaseUserManager, schemas
from fastapi_users.authentication import JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from fastapi import Request
from fastapi_users.authentication import JWTAuthentication

DATABASE_URL = "sqlite:///./test.db"
SECRET = "SECRET"

Base = declarative_base()

class UserTable(Base, SQLAlchemyBaseUserTable[int]):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserManager(BaseUserManager[UserTable, int]):
    user_db_model = UserTable

    async def on_after_register(self, user: UserTable, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

def get_user_db():
    db = SessionLocal()
    yield SQLAlchemyUserDatabase(UserTable, db)

# Define the user schemas
class UserRead(schemas.BaseUser[int]):
    id: int
    email: str

class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str

# JWT Authentication
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
jwt_strategy = JWTStrategy(secret=SECRET)

