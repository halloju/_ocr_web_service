from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.exceptions import CustomException, exception_handler
from app.routers import docs
from app.routers.ocr import gp_ocr, template_ocr, check_back_ocr, check_front_ocr, remittance_ocr, callback, cv_upload
from app.routers.user import auth
from app.routers.template_crud import create, read, update, delete


def get_application():
    app = FastAPI(docs_url=None,
                  title="MLaaS")

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
    app.include_router(
        check_back_ocr.router,
        prefix="/ocr",
        tags=["ocr"],
    )
    app.include_router(
        check_front_ocr.router,
        prefix="/ocr",
        tags=["ocr"],
    )
    app.include_router(
        remittance_ocr.router,
        prefix="/REMIT",
        tags=["REMIT"],
    )

    app.include_router(
        callback.router,
        prefix="/ocr",
        tags=["ocr"],
    )

    app.include_router(
        cv_upload.router,
        prefix="/ocr",
        tags=["ocr"],
    )
    app.include_router(
        auth.router,
        prefix="/user-access-control",
        tags=["user-access-control"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    return app


app = get_application()
