from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.exceptions import CustomException, exception_handler
from app.routers import register, login, db, docs


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
        db.router,
        prefix="/db",
        tags=["db"],
    )

    app.include_router(
        register.router,
        prefix="/register",
        tags=["register"],
    )

    app.include_router(
        login.router,
        prefix="/login",
        tags=["login"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    return app

app = get_application()


