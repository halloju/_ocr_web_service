from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from aioredis import create_redis_pool
from app.exceptions import CustomException, exception_handler
from app.exceptions import MlaasRequestError, mlaas_request_handler
from app.routers import docs
from app.routers.ocr import gp_ocr, template_ocr
from app.routers.image_tools import pdf_transform
from app.routers.template_crud import create, read, update, delete
from app.api_config import http_responses
import os
import logging
from datetime import datetime

log_filename = "./app/logger/" + datetime.now().strftime('%Y-%m-%d') + ".log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=log_filename,
    filemode='a'
)
# 設定 logger
logger = logging.getLogger(__name__)

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

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        Close Redis Connection
        :return:
        """
        app.state.redis.close()
        await app.state.redis.wait_closed()

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
        gp_ocr.router,
        prefix="/gp_ocr",
        tags=["gp_ocr"],
    )
    app.include_router(
        template_ocr.router,
        prefix="/template_ocr",
        tags=["template_ocr"],
    )
    app.include_router(
        pdf_transform.router,
        prefix="/image_tools",
        tags=["image_tools"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    register_redis(app)

    return app

app = get_application()
