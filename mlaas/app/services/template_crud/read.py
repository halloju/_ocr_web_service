from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from app.services import minio
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
import base64
import logging
from minio.error import S3Error
from fastapi.encoders import jsonable_encoder


logger = logging.getLogger(__name__)


def get_available_templates(template, db: Session):
    """
    從 DB 取得公開的 templates 以及該 user_id 自定義的 templates
    """
    try:
        available_templates = db.query(
            TemplateInfo.template_id,
            TemplateInfo.template_name,
            TemplateInfo.creation_time,
            TemplateInfo.expiration_time).filter(TemplateInfo.user_id == template.user_id)
        if not available_templates.first():
            logger.info({'msg': "available_templates are not found"})
        #     raise CustomException(status_code=400, message=)
        return available_templates.all()
    except OperationalError as e:
        logger.error("db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")


def get_template_detail(template, db: Session):
    """
    從 MinIO 拉圖檔
    從 DB 拉 template 相關資訊
    """
    try:
        # Step 1. 從 MinIO 拉圖出來
        client = minio.get_minio_client()
        template_id = template.template_id
        response = client.get_object(
            minio.BUCKET_NAME,
            f'template/{template_id[5:9]}/{template_id[9:11]}/{template_id[11:13]}/{template_id[13:15]}/{template_id[15:17]}/{template_id}'
        )
        image_binary = response.read()
        response.close()
        response.release_conn()
        base64_binary = base64.b64encode(image_binary)
        image_base64 = base64_binary.decode('utf-8')

        # Step 2. 從 DB 拉座標點等資訊
        template_detail = db.query(
            TemplateInfo.is_no_ttl,
            TemplateInfo.template_name,
            TemplateInfo.points_list,
            TemplateInfo.creation_time,
            TemplateInfo.expiration_time).filter(TemplateInfo.template_id == template_id)
        if not template_detail.first():
            raise CustomException(status_code=400, message="template_detail is not found")
        detail_dict = jsonable_encoder(template_detail.first())
        template_detail = {
            "image": image_base64,
            "is_no_ttl": detail_dict['is_no_ttl'],
            "points_list": detail_dict["points_list"],
            "template_name": detail_dict["template_name"],
            "creation_time": detail_dict["creation_time"],
            "expiration_time": detail_dict["expiration_time"]
        }
        return template_detail
    except Exception as e:
        logger.error("error: {}".format(e))
        raise CustomException(status_code=424, message=f"查無此 template_id: {template_id}")

