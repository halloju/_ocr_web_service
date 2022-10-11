from app.models.template_info import TemplateInfo
from app.exceptions import CustomException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger(__name__)


def get_available_templates(db: Session, user_id: str):
    """
    從 DB 取得公開的 templates 以及該 user_id 自定義的 templates
    """
    try:
        available_templates = db.query(
            TemplateInfo.template_id,
            TemplateInfo.template_name,
            TemplateInfo.updated_at).filter(TemplateInfo.user_id == user_id)
        if not available_templates.first():
            raise CustomException(status_code=400, message="available_templates are not found")
        return available_templates.all()
    except OperationalError as e:
        logger.error("db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")


def get_template_detail(db: Session, template_id: str):
    """
    從 MinIO 拉圖檔
    從 DB 拉 template 相關資訊
    """
    try:
        # Step 1. 從 MinIO 拉圖出來

        # Step 2. 從 DB 拉座標點等資訊
        template_detail = db.query(
            TemplateInfo.template_name,
            TemplateInfo.bbox).filter(TemplateInfo.template_id == template_id)
        if not template_detail.first():
            raise CustomException(status_code=400, message="template_detail is not found")
        return template_detail.first()
    except OperationalError as e:
        logger.error("db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
