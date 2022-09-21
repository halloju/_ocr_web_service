from app.database import Base, engine, get_db
from app.models import register
from app.schema.common import Response
from app.services.users import HashPlain
from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter()


@router.get("/init")
def init():
    Base.metadata.create_all(bind=engine)

    db = next(get_db())
    objects = [
        register.Account(
            account = 'ESB12345',
            name = HashPlain.get_plain_hash('王大明'),
            hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash('esun1313'),
            is_active = True,
            birthday = HashPlain.get_plain_hash('1996-01-01')
            )
    ]

    for object in objects:
        db.add(object)
        db.commit()

    return Response(data={"msg": "success"})
