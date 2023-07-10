import json
import os
from datetime import datetime
import httpx
from app.exceptions import MlaasRequestError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import jwt
from starlette.requests import Request
from aioredis import Redis
import requests


def call_mlaas_function(request, action: str, project, logger, timeout=5):
    logger.info({'call_mlaas_function': {'action': action, 'request_id': request['request_id']}})
    mlaas_url = os.environ.get(f'{project}_MLAAS_URL')
    with httpx.Client() as client:
        if os.environ.get('MODE') == 'dev':
            connection_url = f'{mlaas_url}/{action}'
        else:
            action = action.split('/')[1]
            connection_url = f'{mlaas_url}/{action}/v1'
            headers = {
                'X-Client-Id': os.environ.get(f'MLAAS_XClient'),
                'Authorization': os.environ.get(f'MLAAS_JWT'),
                'Content-Type': 'application/json'
            }

        try:
            inp_post_response = client.post(
                connection_url, 
                json=request, 
                headers=headers if os.environ.get('MODE') != 'dev' else None,
                timeout=timeout
            )
            inp_post_response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error({'call_mlaas_function': {
                'error_msg': str(exc),
                'status_code': exc.response.status_code
            }})
            raise MlaasRequestError(exc.response.status_code, str(exc)) from exc
        except httpx.RequestError as exc:
            logger.error({'call_mlaas_function': {
                'error_msg': str(exc)
            }})
            raise MlaasRequestError(None, str(exc)) from exc

        logger.info({'call_mlaas_function': {
            'status_code': inp_post_response.status_code,
            'connection_url': connection_url,
            'request_input_keys': list(request['inputs'].keys())
        }})
        logger.debug({
            'call_mlaas_function': {'response': inp_post_response.json()}
        })

        return inp_post_response.json()


async def async_call_mlaas_function(request, action: str, project, logger, timeout=5):
    logger.info({'call_mlaas_function': {'action': action, 'request_id': request['request_id']}})
    mlaas_url = os.environ.get(f'{project}_MLAAS_URL')
    async with httpx.AsyncClient() as client:
        if os.environ.get('MODE') == 'dev':
            connection_url = f'{mlaas_url}/{action}'
        else:
            action = action.split('/')[1]
            connection_url = f'{mlaas_url}/{action}/v1'
            headers = {
                'X-Client-Id': os.environ.get(f'MLAAS_XClient'),
                'Authorization': os.environ.get(f'MLAAS_JWT'),
                'Content-Type': 'application/json'
            }

        try:
            inp_post_response = await client.post(
                connection_url, 
                json=request, 
                headers=headers if os.environ.get('MODE') != 'dev' else None,
                timeout=timeout,
            )
            inp_post_response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error({'call_mlaas_function': {
                'error_msg': str(exc),
                'status_code': exc.response.status_code
            }})
            raise MlaasRequestError(exc.response.status_code, str(exc)) from exc
        except httpx.RequestError as exc:
            logger.error({'call_mlaas_function': {
                'error_msg': str(exc)
            }})
            raise MlaasRequestError(None, str(exc)) from exc

        logger.info({'call_mlaas_function': {
            'status_code': inp_post_response.status_code,
            'connection_url': connection_url,
            'request_input_keys': list(request['inputs'].keys())
        }})
        logger.debug({
            'call_mlaas_function': {'response': inp_post_response.json()}
        })

        return inp_post_response.json()


def get_redis_filename(image_id: str) -> str:
    return f'celery-upload-img-meta-{image_id}'

def get_redis_taskname(task_id: str) -> str:
    return f'celery-task-meta-{task_id}'


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
