import base64
from typing import Dict
from datetime import timedelta
import filetype
import fitz
import uuid
from fastapi import UploadFile
from route_utils import get_redis_filename
from utils.logger import Logger


class ImageStorage:
    def __init__(self, conn):
        self.conn = conn
        self.logger = Logger('image_storage')

    async def store_image_data(self, file: UploadFile):
        async for img_list in self.transform_to_image(file):
            for img_data in img_list:
                image_redis_key = str(uuid.uuid4())
                encoded_data = base64.b64encode(img_data).decode("utf-8")
                try:
                    await self.conn.setex(image_redis_key, int(timedelta(hours=1).total_seconds()), encoded_data)
                    yield image_redis_key, encoded_data
                except Exception as e:
                    self.logger.error({'image_redis_key': image_redis_key, 'error': str(e), 'msg': 'Failed to store image in Redis'})
                    yield image_redis_key, None
                
    async def transform_to_image(self, file: UploadFile, chunk_size=10):
        file_raw = await file.read()
        file_kind = filetype.guess(file_raw)
        if file_kind is None:
            raise ValueError('Cannot guess file type')
        if file_kind.extension == 'pdf':
            try:
                doc = fitz.open('pdf', file_raw)
                self.logger.info({'msg': 'Transforming PDF to image'})
                
                for i in range(0, len(doc), chunk_size):
                    img_list = []
                    self.logger.info({'msg': f'Processing chunk of PDF pages {i} to {min(i+chunk_size, len(doc))}'})
                    
                    for page_num in range(i, min(i+chunk_size, len(doc))):
                        page = doc[page_num]
                        pix = page.get_pixmap(dpi=300).tobytes('PNG')
                        img_list.append(pix)
                    
                    self.logger.info({'msg': f'Yielding image list for pages {i} to {min(i+chunk_size, len(doc))}'})
                    yield img_list
                
                doc.close()
            except Exception as e:
                self.logger.error({'error': str(e), 'msg': 'Failed to transform PDF to image'})
                yield []
        elif file_kind.mime.startswith('image'):
            self.logger.info({'msg': 'Transforming image to image'})
            yield [file_raw]