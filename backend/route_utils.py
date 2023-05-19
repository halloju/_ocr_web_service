import json
import os
from datetime import datetime

import requests
from app.exceptions import MlaasRequestError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import jwt
from datetime import datetime


def call_mlaas_function(request, action: str, project, logger, timeout=5):
    logger.info({'call_mlaas_function': {'action': action, 'request_id': request['request_id']}})
    mlaas_url = os.environ.get(f'{project}_MLAAS_URL')
    if os.environ.get('MODE') == 'dev':
        connection_url = f'{mlaas_url}/{action}'
        inp_post_response = requests.post(connection_url, json=request)
    else:
        action = action.split('/')[1]
        connection_url = f'{mlaas_url}/{action}'
        headers = {
            'X-Client-Id': os.environ.get(f'{project}_MLAAS_XClient'),
            'Authorization': os.environ.get(f'{project}_MLAAS_JWT'),
            'Content-Type': 'application/json'
        }
        inp_post_response = requests.post(f'{connection_url}/v1', json=request, headers=headers, timeout=timeout, verify=False)
    logger.info({'call_mlaas_function': {
        'status_code': inp_post_response.status_code,
        'connection_url': connection_url,
        'request_input_keys': list(request['inputs'].keys())
    }})
    logger.debug({
        'call_mlaas_function': {'response': inp_post_response.json()}
    })
    if inp_post_response.status_code == 200:
        return json.loads(inp_post_response.content.decode('utf-8'))
    logger.error({'call_mlaas_function': {
        'error_msg': inp_post_response.text
    }})
    raise MlaasRequestError(inp_post_response.status_code, inp_post_response.text)


def init_log(action: str, logger, uid=None, rid=None):
    if not uid:
        uid = get_user_id()

    if not rid:
        rid = get_request_id()
    action = action
    log_main = {'user_id': uid, 'request_id': rid, 'action': action}
    logger.info(log_main)
    return uid, rid, log_main


def get_user_id() -> str:
    return '13520'


def get_request_id() -> str: # celery with task_id
    return datetime.now().strftime("%Y/%m/%d/%H/%M/%S/") + 'gpocr_system_test'

SECRET_KEY = "your-secret-key"  # Replace with your actual secret key
ALGORITHM = "HS256"  # Or another algorithm like "RS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return username
