import requests
import json
from fastapi import Request
from app.exceptions import MlaasRequestError


def call_mlaas_function(request, action: str):

    connection_url = f"http://mlaas:7777/template_crud/{action}"
    inp_post_response = requests.post(connection_url, json=request)
    if inp_post_response.status_code == 200:
        return json.loads(inp_post_response.content.decode('utf-8'))
    raise MlaasRequestError()

def get_user_id() -> str:
    return '13520'

def get_request_id() -> str:
    return 'gpocr_system'