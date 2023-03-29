import requests
import json
from fastapi import Request
from app.exceptions import MlaasRequestError
import os


def call_mlaas_function(request, action: str, timeout=5):
    mlaas_url = os.environ.get("MLAAS_URL")
    
    if os.environ.get('MODE') == 'dev':
        connection_url = f'{mlaas_url}/{action}'
        inp_post_response = requests.post(connection_url, json=request)
    else:
        action = action.split('/')[1]
        connection_url = f'{mlaas_url}/{action}'
        headers = {
            'X-Client-Id': os.environ.get('MLAAS_XClient'),
            'Authorization': os.environ.get('MLAAS_JWT'),
            'Content-Type': 'application/json'
        }
        inp_post_response = requests.post(connection_url+'/v1', json=request, headers=headers, timeout=timeout, verify=False)
    if inp_post_response.status_code == 200:
        return json.loads(inp_post_response.content.decode('utf-8'))
    raise MlaasRequestError()

def get_user_id() -> str:
    return '13520'

def get_request_id() -> str:
    return 'gpocr_system_test'