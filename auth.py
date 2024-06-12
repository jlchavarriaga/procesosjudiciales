from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers, BaseUserManager, schemas
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

DATABASE_URL = "sqlite:///./test.db"
SECRET = "SECRET"

Base: DeclarativeMeta = declarative_base()

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

# Define the Bearer transport
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Define the user schemas
class UserRead(schemas.BaseUser[int]):
    id: int
    email: str

class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str

fastapi_users = FastAPIUsers(
    get_user_manager=get_user_db,
    auth_backends=[auth_backend]
)

app = FastAPI()

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

