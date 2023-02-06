from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from app.services import minio
from io import BytesIO
from copy import deepcopy
from datetime import datetime
import logging
import pytz

logger = logging.getLogger(__name__)


def update_template(template, db: Session):
    try:
        today = datetime.now(pytz.timezone("Asia/Taipei"))
        template_id = template.template_id
        new_template_id=template.user_id+today.strftime('%Y%m%d%H%M%S')
         # Step 1. 將 template 影像寫入 db
        record = db.query(TemplateInfo).\
            filter(TemplateInfo.template_id == template.template_id).one()
        template_info = TemplateInfo(
            template_id=new_template_id,
            user_id=template.user_id,
            template_name=template.template_name,
            bbox=template.bbox,
            updated_at=today,
            is_public=record.is_public,
            is_no_ttl=record.is_no_ttl
        )
        db.add(template_info)
        db.commit()

        # Step 2. 將 template 影像寫入 MinIO
        client = minio.get_minio_client()
        minio.check_bucket(client)
        response = client.get_object(
            minio.BUCKET_NAME,
            f'template/{template_id[5:9]}/{template_id[9:11]}/{template_id[11:13]}/{template_id[13:15]}/{template_id[15:17]}/{template_id}'
        )
        image_binary = response.read()
        response.close()
        client.put_object(
            minio.BUCKET_NAME,
            f'template/{today.year:04}/{today.month:02}/{today.day:02}/{today.hour:02}/{today.minute:02}/{new_template_id}',
            BytesIO(image_binary),
            len(image_binary)
        )

        response.release_conn()
        return new_template_id
    except OperationalError as e:
        logger.error("update template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
