import os 
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

load_dotenv ()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de la base de datos 

try:
    engine = create_engine(DATABASE_URL, echo= False, client_encoding= 'utf8')

    print("Motor de base de datos SQLAlchemy creado exitosamente para Docker (local).")
except Exception as e:
    print(f"Error al crear el motor de base de datos (local): {e}")
    raise

Base = declarative_base()
DBSession = sessionmaker(bind=engine)

def get_db_engine():
    return engine

def get_db_session():
    return DBSession()

def get_db_connection():
    return engine.connect()  