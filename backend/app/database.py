from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

mode = os.environ["MODE"]

if mode=="dev":
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db/postgres"
    schema_name = "if_gp_ocr"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://XXXXX@10.240.205.109:5432/feature"
    schema_name = "AICLOUD_DB_SCHEMA"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"connect_timeout": 2})
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
