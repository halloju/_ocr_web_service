import os
from aioredis import create_redis_pool
from app.api_config import http_responses
from app.exceptions import (CustomException, MlaasRequestError,
                            exception_handler, mlaas_request_handler)
from app.routers import docs
from app.routers.ocr import ocr
from app.routers.task import task
from app.routers.template_crud import create, delete, read, update
from app.routers import login
from app.routers.ocr import async_ocr
from app.routers import feedback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.logger import Logger
from utils.minio import MinioStorage


# 設定 logger
logger = Logger('main', uid='main', rid='main')


def register_redis(app: FastAPI) -> None:
    """
    Register Redis with the FastAPI application.
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        Get Redis Connection Pool
        :return:
        """
        try:
            app.state.redis = await create_redis_pool(os.getenv("LOCAL_REDIS_URL", "redis://localhost:6379"))
            # Create MinIO client
            app.state.minio = MinioStorage(
                endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
                access_key=os.getenv("MINIO_ACCESS KEY", "minio"),
                secret_key=os.getenv("MINIO_SECRET, KEY", "minio123"),
                bucket_name=os.getenv("MINIO_BUCKET_NAME", "ocr")
            )
            logger.info({'register_redis': 'startup'})
        except Exception as e:
            logger.error({'register_redis': 'startup failed', 'error': str(e)})

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        Close Redis Connection Pool
        :return:
        """
        try:
            app.state.redis.close()
            await app.state.redis.wait_closed()
            logger.info({'register_redis': 'shutdown'})
        except Exception as e:
            logger.error(
                {'register_redis': 'shutdown failed', 'error': str(e)})


def register_minio(app: FastAPI) -> None:
    """
    Register Minio with the FastAPI application.
    :param app:
    :return:
    """
    @app.on_event('startup')
    async def startup_event():
        """
        Get Minio Connection Pool
        :return:
        """
        try:
            app.state.minio = await create_minio_pool()
            logger.info({'register_minio': 'startup'})
        except Exception as e:
            logger.error({'register_minio': 'startup failed', 'error': str(e)})


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
        responses=http_responses
    )

    app.include_router(
        async_ocr.router,
        prefix="/ocr",
        tags=["ocr"],
        responses=http_responses
    )

    app.include_router(
        task.router,
        prefix="/task",
        tags=["task"],
    )
    app.include_router(
        login.router,
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        feedback.router,
        prefix="/feedback",
        tags=["feedback"],
    )
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    register_redis(app)
    logger.info({'get_application': 'finish'})

    return app


app = get_application()
