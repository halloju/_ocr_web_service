import base64
import logging
from app.models.register import Account
from app.models.login_hist import LoginHist
from app.schema.users import UserCreate
from sqlalchemy.orm import Session
from app.exceptions import CustomException
from sqlalchemy.exc import IntegrityError, OperationalError
from passlib.context import CryptContext
from app.schema.users import ResetRequest, ModifyRequest, LoginRequest
from app.models.register import Account

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

SALT = 'Z&sg6nu7A79tP#g#a6Q@&1UejtVo^&ys*SH^sOtTW*!WiUGmS19LaBBFs!IlvS*!9u3Ht@qKVum'

class HashPlain:
    @staticmethod
    def get_plain_hash(plain):
        encry_str = ""
        for i,j in zip(plain, SALT):
            temp = str(ord(i)+ord(j)) + '_'
            encry_str = encry_str + temp
        s1 = base64.b64encode(encry_str.encode("utf-8"))
        return s1.decode("utf-8")

    @staticmethod
    def dectry(hashed):
        p = base64.b64decode(hashed).decode("utf-8")
        dec_str = ""
        for i,j in zip(p.split("_")[:-1], SALT):
            temp = chr(int(i) - ord(j))
            dec_str = dec_str+temp
        return dec_str

def create_new_user(user: UserCreate, db: Session):
    try:
        user = Account(
            account=user.account.upper(),
            name=HashPlain.get_plain_hash(user.name),
            birthday=HashPlain.get_plain_hash(user.birthday),
            hashed_password=Hasher.get_password_hash(user.password),
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except OperationalError as e:
        logger.error("create_new_user db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")

def modify_name(db: Session, request: ModifyRequest):

    try:

        user = db.query(Account).filter(Account.account == request.account.upper())

        if not user.first():
            raise CustomException(status_code=400, message="account is not found")
        if not user.first().is_active:
            raise CustomException(status_code=400, message="the account is not activated")
        if user.first().name == request.name:
            raise CustomException(status_code=400, message="the name is same")
        if not Hasher.verify_password(request.password, user.first().hashed_password):
            raise CustomException(status_code=400, message="the password is not valid")
        update_info = dict(name=HashPlain.get_plain_hash(request.name))
        user.update(update_info)
        db.commit()

    except OperationalError as e:
        logger.error("modify_name db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")

def check_active(db: Session, account: str):

    try:

        user = db.query(Account).filter(Account.account == account.upper())

        if not user.first():
            raise CustomException(status_code=400, message="account is not found")

    except OperationalError as e:
        logger.error("check_active db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")

    return user.first()

def revoke(db: Session, account: str):

    try:

        user = db.query(Account).filter(Account.account == account.upper())

        if not user.first():
            raise CustomException(status_code=400, message="account is not found")
        if not user.first().is_active:
            raise CustomException(status_code=400, message="the account is already revoked")
        update_info = dict(is_active = False)
        user.update(update_info)
        db.commit()

    except OperationalError as e:
        logger.error("revoke db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")

def reset_password(db: Session, request: ResetRequest):

    try:

        user = db.query(Account).filter(Account.account == request.account.upper())
        if not user.first():
            raise CustomException(status_code=400, message="account is not found")
        if not user.first().is_active:
            raise CustomException(status_code=400, message="the account is not activated")
        if not user.first().birthday == HashPlain.get_plain_hash(request.birthday):
            raise CustomException(status_code=400, message="the birthday is not valid")
        update_info = dict(hashed_password=Hasher.get_password_hash(request.password))
        user.update(update_info)
        db.commit()

    except OperationalError as e:
        logger.error("reset_password db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")

def activate(db: Session, account: str):

    try:

        user = db.query(Account).filter(Account.account == account.upper())

        if not user.first():
            raise CustomException(status_code=400, message="email is not found")
        if user.first().is_active:
            raise CustomException(status_code=400, message="the account is already activated")
        update_info = dict(is_active = True)
        user.update(update_info)
        db.commit()

    except OperationalError as e:
        logger.error("activate db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")

def login(db: Session, request: LoginRequest):

    try:

        user = db.query(Account).filter(Account.account == request.account.upper())
        # Account Not Found
        if not user.first():
            login_hist = LoginHist(account=request.account.upper(),
                                   status="Account Not Found")
            db.add(login_hist)
            db.commit()
            raise CustomException(status_code=400, message="未註冊的帳號")
        # Inactive Account
        if not user.first().is_active:
            login_hist = LoginHist(account=request.account.upper(),
                                   status="Inactive Account")
            db.add(login_hist)
            db.commit()
            raise CustomException(status_code=400, message="該帳號未被啟用")
        # Invalid Password
        if not Hasher.verify_password(request.password, user.first().hashed_password):
            login_hist = LoginHist(account=request.account.upper(),
                                   status="Invalid Password")
            db.add(login_hist)
            db.commit()
            raise CustomException(status_code=400, message="密碼錯誤")
        # Login Success
        login_hist = LoginHist(account=request.account.upper(),
                               status="Login Success")
        db.add(login_hist)
        db.commit()
        return user.first()

    except OperationalError as e:
        logger.error("login db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
