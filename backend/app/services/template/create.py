from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.orm import Session
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def create_template(template, db: Session):
    """
    將 template 影像寫入 MinIO
    將 template 其餘資訊寫入 DB
    """
    try:
        # Step 1. 將 template 影像寫入 MinIO

        # Step 2. 將 template 其餘資訊寫入 DB
        today = datetime.today()
        template_id=template.user_id+today.strftime('%y%m%d%H%M%S'),
        template_info = TemplateInfo(
            template_id=template_id,
            user_id=template.user_id,
            template_name=template.template_name,
            bbox=template.bbox,
            created_at=today,
            updated_at=today
        )
        db.add(template_info)
        db.commit()
        db.refresh(template_info)
        return template_id

    except OperationalError as e:
        logger.error("create_template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
