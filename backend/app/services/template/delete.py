from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger(__name__)


def delete_template(template, db: Session):
    try:
        db.query(TemplateInfo).filter(TemplateInfo.template_id==template.template_id).delete()
        db.commit()
    except OperationalError as e:
        logger.error("delete template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
