from app.exceptions import CustomException
from app.services import users as service_users
from app.database import get_db
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.forms.login import LoginForm
from app.schema.common import Response
from app.schema.users import LoginRequest

router = APIRouter()

@router.post("")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    '''
    登入帳號
    '''
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        user = service_users.login(request=request, db=db)
        if user:
            return Response(data={"status": 200})
    raise CustomException(status_code=403, message=form.errors)
 