from app.schema.users import UserCreate
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json

def test_register(app: FastAPI, db_session: Session, client: TestClient):
    user_schema = UserCreate(account="ESB19999",
                            password="Steve_Rogers",
                            name="美國隊長",
                            birthday="19180704")
    req_data = jsonable_encoder(user_schema)
    response = client.post("http://localhost:5000/register", json=req_data)
    data = response.json()
    print(data)
    assert response.status_code == 200
    user_schema = UserCreate(account="ESB19999",
                            password="Steve_Rogers",
                            name="美國隊長",
                            birthday="19180704")
    req_data = jsonable_encoder(user_schema)
    response = client.post("http://localhost:5000/register", json=req_data)
    data = response.json()
    print(data)
    assert response.status_code == 400
    assert json.loads(response.text)["msg"] == ['Duplicate username']
