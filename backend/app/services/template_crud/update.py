from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def update_template(template, db: Session):
    try:
        db.query(TemplateInfo).\
            filter(TemplateInfo.template_id == template.template_id).\
            update({'bbox': template.bbox, "template_name": template.template_name, "updated_at": datetime.today()})
        db.commit()
    except OperationalError as e:
        logger.error("update template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
