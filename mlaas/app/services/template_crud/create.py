from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from app.services import minio
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
import base64
from datetime import datetime, timedelta
from io import BytesIO
import logging
import pytz


logger = logging.getLogger(__name__)


def create_template(template, db: Session):
    """
    將 template 影像寫入 MinIO
    將 template 其餘資訊寫入 DB
    """
    try:
        today = datetime.now(pytz.timezone("Asia/Taipei"))
        print(f'datetime.now(): {datetime.now()}')
        print(f'datetime.now(pytz.timezone("Europe/London")): {datetime.now(pytz.timezone("Europe/London"))}')
        print(f'datetime.now(pytz.timezone("Asia/Taipei")): {datetime.now(pytz.timezone("Asia/Taipei"))}')
        print(f'today: {today}')
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
        print(f"service template create <template>: {template}")
        # Step 2. 將 template 其餘資訊寫入 DB
        expiration_time = (today + timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
        template_info = TemplateInfo(
            template_id=template_id,
            user_id=template.user_id,
            template_name=template.template_name,
            points_list=jsonable_encoder(template.points_list),
            creation_time=today.strftime("%Y-%m-%d %H:%M:%S"),
            expiration_time=expiration_time,
            is_no_ttl=False
        )
        db.add(template_info)
        db.commit()
        db.refresh(template_info)
        return template_id

    except OperationalError as e:
        logger.error("create_template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
