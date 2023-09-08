import os

import httpx
from aioredis import Redis
from app.exceptions import MlaasRequestError, CustomException
from starlette.requests import Request
from typing import Optional
from app.response_table import response_table


def get_mlaas_result(logger, res: dict) -> Optional[dict]:
    outputs = res['outputs']
    status_code = outputs['status_code']
    image_cv_id = outputs['image_cv_id'] if 'image_cv_id' in outputs else ''
    if status_code == '0000':
        return outputs
    if status_code in response_table:
        status = response_table[status_code]
        logger.info({'image_cv_id': image_cv_id, 'mlaas_error_msg': status})
        raise MlaasRequestError(**status, image_cv_id=image_cv_id)
    else:
        status = {'status_code': status_code, 'status_msg': 'unknown error'}
        logger.info({'image_cv_id': image_cv_id, 'mlaas_error_msg': status})
        raise MlaasRequestError(**status, image_cv_id=image_cv_id)


def get_mode_conn_info(project, mode, action):
    mlaas_url = os.environ.get(f'{project}_MLAAS_URL')
    headers = {}
    if mode == 'dev':
        connection_url = f'{mlaas_url}/{action}'
    else:
        action = action.split('/')[1]
        connection_url = f'{mlaas_url}/{action}/v1'
        headers = {
            'X-Client-Id': os.environ.get('MLAAS_XClient'),
            'Authorization': os.environ.get('MLAAS_JWT'),
            'Content-Type': 'application/json'
        }
    return action, connection_url, headers


def call_mlaas_function(request, action: str, project, logger, timeout=5):
    log_act = 'call_mlaas_function'
    logger.info(
        {log_act: {'action': action, 'request_id': request['request_id']}})
    with httpx.Client(verify=False) as client:
        action, connection_url, headers = get_mode_conn_info(
            project, os.environ.get('MODE'), action)

        try:
            inp_post_response = client.post(
                connection_url,
                json=request,
                headers=headers if os.environ.get('MODE') != 'dev' else None,
                timeout=timeout
            )
            inp_post_response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error({log_act: {
                'error_msg': str(exc),
                'status_code': exc.response.status_code
            }})
            raise CustomException(exc.response.status_code, str(exc)) from exc
        except httpx.RequestError as exc:
            logger.error({log_act: {
                'error_msg': str(exc)
            }})
            raise CustomException(None, str(exc)) from exc

        # logger.info({log_act: {
        #     'status_code': inp_post_response.status_code,
        #     'connection_url': connection_url,
        #     'request_input_keys': list(request['inputs'].keys())
        # }})

        return get_mlaas_result(logger, inp_post_response.json())


async def async_call_mlaas_function(request, action: str, project, logger, timeout=5):
    log_act = 'async_call_mlaas_function'
    logger.info(
        {log_act: {'action': action, 'request_id': request['request_id']}})
    async with httpx.AsyncClient(verify=False) as client:
        action, connection_url, headers = get_mode_conn_info(
            project, os.environ.get('MODE'), action)

        try:
            inp_post_response = await client.post(
                connection_url,
                json=request,
                headers=headers if os.environ.get('MODE') != 'dev' else None,
                timeout=timeout,
            )
            inp_post_response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error({log_act: {
                'error_msg': str(exc),
                'status_code': exc.response.status_code
            }})
            raise CustomException(exc.response.status_code, str(exc)) from exc
        except httpx.RequestError as exc:
            logger.error({log_act: {
                'error_msg': str(exc)
            }})
            raise CustomException(None, str(exc)) from exc

        # logger.info({log_act: {
        #     'status_code': inp_post_response.status_code,
        #     'connection_url': connection_url,
        #     'request_input_keys': list(request['inputs'].keys())
        # }})

        return get_mlaas_result(logger, inp_post_response.json())


def get_redis_filename(image_id: str) -> str:
    return f'celery-upload-img-meta-{image_id}'


def get_redis_taskname(task_id: str) -> str:
    return f'celery-task-meta-{task_id}'


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
