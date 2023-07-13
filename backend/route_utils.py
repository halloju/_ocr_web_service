import os

import httpx
from aioredis import Redis
from app.exceptions import MlaasRequestError
from starlette.requests import Request


def perform_mlaas_request(post_func, request, action: str, project, logger, timeout=5):
    logger.info({'call_mlaas_function': {'action': action, 'request_id': request['request_id']}})
    mlaas_url = os.environ.get(f'{project}_MLAAS_URL')
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
        inp_post_response = post_func(
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

def call_mlaas_function(request, action: str, project, logger, timeout=5):
    with httpx.Client(verify=False) as client:
        return perform_mlaas_request(client.post, request, action, project, logger, timeout)

async def async_call_mlaas_function(request, action: str, project, logger, timeout=5):
    async with httpx.AsyncClient(verify=False) as client:
        return await perform_mlaas_request(client.post, request, action, project, logger, timeout)


def get_redis_filename(image_id: str) -> str:
    return f'celery-upload-img-meta-{image_id}'

def get_redis_taskname(task_id: str) -> str:
    return f'celery-task-meta-{task_id}'


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
