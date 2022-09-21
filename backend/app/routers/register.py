import email
from app.exceptions import CustomException
from app.services import users as service_users
from app.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schema.users import UserCreate
from app.forms.register import UserCreateForm
from app.schema.common import Response
from app.schema.users import ResetRequest, RegisterRequest, ModifyRequest

router = APIRouter()

@router.post("")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    '''
    註冊帳號
    '''
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(account=form.account,
                          name=form.name,
                          birthday=form.birthday,
                          password=form.password)
        try:
            user = service_users.create_new_user(user=user, db=db)
            return Response(data={"status": 200})
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username")
            raise CustomException(status_code=400, message=form.errors)
    raise CustomException(status_code=400, message=form.errors)

@router.post("/reset")
def reset_password(request: ResetRequest, db: Session = Depends(get_db)):
    '''
    忘記密碼
    '''
    service_users.reset_password(db, request)
    return Response(data={"status": 200})

@router.post("/modify")
def modify_name(request: ModifyRequest, db: Session = Depends(get_db)):
    '''
    修改名字
    '''
    service_users.modify_name(db, request)
    return Response(data={"status": 200})

@router.get("/is_active/{account}")
def check_active(account: str, db: Session = Depends(get_db)):
    '''
    確認帳號是否啟用
    '''
    user = service_users.check_active(db, account)
    result = user.is_active
    return Response(data=result)

@router.post("/revoke/{account}")
def revoke(account: str, db: Session = Depends(get_db)):
    '''
    註銷帳號
    '''
    service_users.revoke(db, account)
    return Response(data={"status": 200})

@router.post("/activate/{account}")
def activate(account: str, db: Session = Depends(get_db)):
    '''
    啟用帳號
    '''
    service_users.activate(db, account)
    return Response(data={"status": 200})