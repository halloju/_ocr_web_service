from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import pytz

logger = logging.getLogger(__name__)


def update_template(template, db: Session):
    try:
        db.query(TemplateInfo).\
            filter(TemplateInfo.template_id == template.template_id).\
            update({'bbox': template.bbox, "template_name": template.template_name, "updated_at": datetime.today()})
        db.commit()
        today = datetime.now(pytz.timezone("Asia/Taipei"))
        new_template_id=template.user_id+today.strftime('%Y%m%d%H%M%S')
        return new_template_id
    except OperationalError as e:
        logger.error("update template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
