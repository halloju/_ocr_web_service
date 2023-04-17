import os

from aioredis import create_redis_pool
from app.api_config import http_responses
from app.exceptions import (CustomException, MlaasRequestError,
                            exception_handler, mlaas_request_handler)
from app.routers import docs
from app.routers.image_tools import pdf_transform
from app.routers.ocr import ocr
from app.routers.task import task
from app.routers.template_crud import create, delete, read, update
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from logger import Logger

# 設定 logger
logger = Logger('main')

def register_redis(app: FastAPI) -> None:
    """
    把 redis 掛載到 app 上面
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        Get Redis Connection
        :return:
        """
        app.state.redis = await create_redis_pool(os.getenv("LOCAL_REDIS_URL"))
        logger.info({'register_redis': 'startup'})

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        Close Redis Connection
        :return:
        """
        app.state.redis.close()
        await app.state.redis.wait_closed()
        logger.info({'register_redis': 'shutdown'})

def get_application():
    app = FastAPI(docs_url=None,
                  title="Web Backend")

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(CustomException, exception_handler)
    app.add_exception_handler(MlaasRequestError, mlaas_request_handler)

    app.include_router(docs.router)

    app.include_router(
        create.router,
        prefix="/template_crud",
        tags=["template_crud"],
        responses=http_responses
    )
    app.include_router(
        read.router,
        prefix="/template_crud",
        tags=["template_crud"],
        responses=http_responses
    )
    app.include_router(
        update.router,
        prefix="/template_crud",
        tags=["template_crud"],
        responses=http_responses
    )
    app.include_router(
        delete.router,
        prefix="/template_crud",
        tags=["template_crud"],
        responses=http_responses
    )
    app.include_router(
        ocr.router,
        prefix="/ocr",
        tags=["ocr"],
    )
    app.include_router(
        task.router,
        prefix="/task",
        tags=["task"],
    )
    app.include_router(
        pdf_transform.router,
        prefix="/image_tools",
        tags=["image_tools"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    register_redis(app)
    logger.info({'get_application': 'finish'})

    return app


app = get_application()
