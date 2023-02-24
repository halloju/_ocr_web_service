from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from aioredis import create_redis_pool, Redis
from app.exceptions import CustomException, exception_handler
from app.routers import docs
from app.routers.ocr import gp_ocr, template_ocr
from app.routers.template_crud import create, read, update, delete
from dotenv import load_dotenv
import os

load_dotenv(".env.dev")

def register_redis(app: FastAPI) -> None:
    """
    把redis挂载到app对象上面
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
                  title="Backend")

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(CustomException, exception_handler)

    app.include_router(docs.router)

    app.include_router(
        create.router,
        prefix="/template_crud",
        tags=["template_crud"],
    )
    app.include_router(
        read.router,
        prefix="/template_crud",
        tags=["template_crud"],
    )
    app.include_router(
        update.router,
        prefix="/template_crud",
        tags=["template_crud"],
    )
    app.include_router(
        delete.router,
        prefix="/template_crud",
        tags=["template_crud"],
    )
    app.include_router(
        gp_ocr.router,
        prefix="/ocr",
        tags=["ocr"],
    )
    app.include_router(
        template_ocr.router,
        prefix="/ocr",
        tags=["ocr"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    register_redis(app)

    return app

app = get_application()
