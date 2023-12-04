import base64
from typing import Tuple
from route_utils import get_redis_filename
from utils.logger import Logger


class ImageStorage:
    def __init__(self, conn):
        self.conn = conn
        self.logger = Logger('image_storage')

    async def store_image_data(self, file, image_id) -> Tuple[str, str]:
        image_data = await file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data and filename in Redis
        await self.conn.set(image_id, encoded_data)
        await self.conn.set(get_redis_filename(image_id), file.filename)
        self.logger.info({'image_id': image_id, 'msg': 'Store the encoded image data and filename in Redis finished'})
        return image_id, encoded_data
