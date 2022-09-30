from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.exceptions import CustomException, exception_handler
from app.routers import db, docs, template


def get_application():
    app = FastAPI(docs_url=None)

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
        template.router,
        prefix="/template",
        tags=["template"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    return app

app = get_application()
