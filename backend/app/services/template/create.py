from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from app.services import minio
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
import base64
from datetime import datetime
from io import BytesIO
import logging


logger = logging.getLogger(__name__)


def create_template(template, db: Session):
    """
    將 template 影像寫入 MinIO
    將 template 其餘資訊寫入 DB
    """
    try:
        today = datetime.today()
        template_id=template.user_id+today.strftime('%Y%m%d%H%M%S')

        image_base64_binary = template.image.encode('utf-8')
        image_binary = base64.b64decode(image_base64_binary)

        # Step 1. 將 template 影像寫入 MinIO
        client = minio.get_minio_client()
        minio.check_bucket(client)
        client.put_object(
            minio.BUCKET_NAME,
            f'template/{today.year:04}/{today.month:02}/{today.day:02}/{today.hour:02}/{today.minute:02}/{template_id}',
            BytesIO(image_binary),
            len(image_binary)
        )

        # Step 2. 將 template 其餘資訊寫入 DB
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
