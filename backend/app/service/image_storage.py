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

    async def store_image_data(self, file) -> Dict:
            """
            Stores the image data and filename in Redis.

            Args:
                file: The image file to be stored.

            Returns:
                A dictionary containing the Redis keys and encoded image data.

            """
            image_dict = {}
            image_list = await self.transform_to_image(file)
            for image_data in image_list:
                image_redis_key = str(uuid.uuid4())
                encoded_data = base64.b64encode(image_data).decode("utf-8")        
            
                # Store the encoded image data and filename in Redis
                ttl = timedelta(hours=1)
                await self.conn.setex(image_redis_key, int(ttl.total_seconds()), encoded_data)
                await self.conn.setex(get_redis_filename(image_redis_key), int(ttl.total_seconds()), file.filename)
                self.logger.info({'image_redis_key': image_redis_key, 'msg': 'Store the encoded image data and filename in Redis finished'})
                image_dict[image_redis_key] = encoded_data

            return image_dict

    async def transform_to_image(self, file: UploadFile):
        """
        Transforms the given file into a list of images.

        Args:
            file: The file to be transformed.

        Returns:
            A list of images. Each image is represented as a byte string.

        Raises:
            ValueError: If the file type is invalid.
        """
        img_list = []
        file_raw = await file.read()
        file_kind = filetype.guess(file_raw)
        if file_kind:
            if file_kind.extension == 'pdf':
                doc = fitz.open('pdf', file_raw)
                for img in doc:
                    pix = img.get_pixmap(dpi=300).tobytes('PNG')
                    img_list.append(pix)
                doc.close()
                fitz.TOOLS.store_shrink(100)
            elif file_kind.mime.startswith('image'):
                img_list.append(file_raw)
            else:
                raise ValueError('Invalid file type')
            return img_list
        else:
            raise ValueError('Invalid file type')