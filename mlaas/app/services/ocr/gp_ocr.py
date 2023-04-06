from app.exceptions import CustomException, ImageTypeError
from app.models.ocr_results import OCRResults
from app.services import minio
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from PIL import Image
import base64
import numpy as np
from datetime import datetime
from io import BytesIO
import logging
import random
import uuid


logger = logging.getLogger(__name__)


def gp_ocr(ocr_image_info, db: Session):
    """
    辨識圖片中的文字
    """
    try:
        today = datetime.today()
        request_id = str(uuid.uuid4())
        image_cv_id = datetime.now().strftime("%Y/%m/%d/%H/%M/%S/") + request_id
        image_base64_binary = ocr_image_info.image.encode('utf-8')
        image_binary = base64.b64decode(image_base64_binary)
        # Step 1. 將 template 影像寫入 MinIO
        client = minio.get_minio_client()
        minio.check_bucket(client)
        client.put_object(
            minio.BUCKET_NAME,
            image_cv_id,
            BytesIO(image_binary),
            len(image_binary)
        )

        # Step 2. fake ocr results
        img_pil = Image.open(BytesIO(image_binary))
        if not type(img_pil).__name__.endswith('ImageFile'):
            raise ImageTypeError(type(img_pil).__name__)
        img_arr = np.array(img_pil.convert('RGB'))
        img_width, img_height = img_arr.shape[:2]
        random_points = [(random.randint(0, img_width), random.randint(0, img_height)) for times in range(3)]
        max_random_points = [(random.randint(point_width, img_width), random.randint(point_height, img_height)) for point_width, point_height in random_points]
        text_list = ['2023.01.16', ocr_image_info.model_name, ocr_image_info.image_complexity]
        fake_ocr_results = []
        for i in range(3):
            fake_ocr_results.append({
                'points': [
                    [random_points[i][0], random_points[i][1]],
                    [max_random_points[i][0], random_points[i][1]],
                    [max_random_points[i][0], max_random_points[i][1]],
                    [random_points[i][0], max_random_points[i][1]]
                ],
                'text': text_list[i],
                'det_prob': round(random.random(), 4),
                'rec_prob': round(random.random(), 4)

            })
        ocr_results = [i for i in fake_ocr_results if i['text']]
        for ocr_result in ocr_results:
            insert_ocr_results = OCRResults(
                image_cv_id=image_cv_id,
                text=ocr_result['text'],
                det_model='example',
                rec_model='example',
                det_prob=ocr_result['det_prob'],
                rec_prob=ocr_result['rec_prob'],
                x_1=ocr_result['points'][0][0],
                y_1=ocr_result['points'][0][1],
                x_2=ocr_result['points'][1][0],
                y_2=ocr_result['points'][1][1],
                x_3=ocr_result['points'][2][0],
                y_3=ocr_result['points'][2][1],
                x_4=ocr_result['points'][3][0],
                y_4=ocr_result['points'][3][1],
                etl_dt=today
            )
            db.add(insert_ocr_results)
            db.commit()
            db.refresh(insert_ocr_results)
        return image_cv_id, ocr_results
    except OperationalError as e:
        logger.error("gpocr db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
    except ImageTypeError as e:
        logger.error("image type error:{}".format(e))
        raise ImageTypeError(status_code=5402, message="上傳圖片格式錯誤，請確認上傳檔案格式是否為 .jpg, .png")
