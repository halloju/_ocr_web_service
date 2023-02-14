from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from app.services import minio
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger(__name__)


def delete_template(template, db: Session):
    """
    將 MinIO 中的 template 影像刪除
    將 DB 中的 template 資訊刪除
    """
    try:
        template_id = template.template_id

        # Step 1. 將 MinIO 中的 template 影像刪除
        client = minio.get_minio_client()
        client.remove_object(
            minio.BUCKET_NAME,
            f'template/{template_id[5:9]}/{template_id[9:11]}/{template_id[11:13]}/{template_id[13:15]}/{template_id[15:17]}/{template_id}'
        )

        # Step 2. 將 DB 中的 template 資訊刪除
        db.query(TemplateInfo).filter(TemplateInfo.template_id==template_id).delete()
        db.commit()
    except OperationalError as e:
        logger.error("delete template db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
