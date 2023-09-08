from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

mode = os.environ["MODE"]

if mode == "dev":
    load_dotenv(".env.dev")
    schema_name = "if_gp_ocr"
else:
    load_dotenv()
    schema_name = "AICLOUD_DB_SCHEMA"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"connect_timeout": 2})
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
