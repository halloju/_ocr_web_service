import json
from app.schema.users import UserCreate
from app.schema.campaign import Request as RequestCampaign
from app.schema.list import Request as RequestList
from app.schema.list import Request
from app.schema.list import RequestStatus
from app.schema.queue import RequestSqlQueue
from app.services import lead as service_lead
from app.services import list as service_list
from app.services import queue as service_queue
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_list(app: FastAPI, db_session: Session, client: TestClient):
    response = client.get("http://localhost:5000/lists")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data == {'error': False, 'data': []}


def test_update_list(app: FastAPI, db_session: Session, client: TestClient):
    # add account
    user_schema = UserCreate(account="ESB18888",
                             password="Steve_Rogers",
                             name="美國隊長",
                             birthday="19180704")
    response = client.post("http://localhost:5000/register",
                           json=jsonable_encoder(user_schema))
    assert response.status_code == 200
    # add campaign
    campaign_schemas = RequestCampaign(name="活躍客群信用卡申辦轉換率",
                                       campaignID="20200828A00101000005",
                                       expected_date="2099-12-12")
    response = client.post("http://localhost:5000/campaigns",
                           json=jsonable_encoder(campaign_schemas))
    assert response.status_code == 200
    # init data
    response = client.get("http://localhost:5000/db/init")
    # get tags
    response = client.get("http://localhost:5000/tags")
    assert json.loads(response.text) == ""
    # # create list
    # list_schemas = RequestList(campaign_id=1,
    #                            user_id="ESB18888",
    #                            intent=["貸款", "理財"],
    #                            status="編輯中",
    #                            leads=[{"leadID": "LNSMSA0003",
    #                                    "channel": "SMS",
    #                                    "version": 1,
    #                                    "status": "pending",
    #                                    "tags": {
    #                                             "selected_block": [
    #                                                 {
    #                                                     "tag_id": 14,
    #                                                     "condition": ""
    #                                                 },
    #                                                 {
    #                                                     "tag_id": 15,
    #                                                     "condition": ""
    #                                                 }
    #                                             ],
    #                                             "input_block": {
    #                                                 "indep_var": "14",
    #                                                 "operator": "AND",
    #                                                 "ctrl_var": "(15)"
    #                                             }
    #                                     }}])
    # response = client.post("http://localhost:5000/campaigns", json=jsonable_encoder(list_schemas))
    # assert response.status_code == 200
