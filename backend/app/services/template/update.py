from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.orm import Session
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def update_template(template, db: Session):
    try:
        template_info = db.query(
            TemplateInfo.template_name,
            TemplateInfo.bbox).filter(TemplateInfo.template_id == template.template_id).first()
        if not template_info:
            raise CustomException(status_code=400, message="template_info is not found")
        today = datetime.today()
        template_info.update({"bbox": template.bbox, "updated_at": today})
        db.commit()
    except OperationalError as e:
        logger.error("update template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
