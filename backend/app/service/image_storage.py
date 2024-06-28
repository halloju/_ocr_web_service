import base64
from typing import Tuple
from datetime import timedelta
from route_utils import get_redis_filename
from utils.logger import Logger


class ImageStorage:
    def __init__(self, conn):
        self.conn = conn
        self.logger = Logger('image_storage')

    async def store_image_data(self, file, image_redis_key) -> Tuple[str, str]:
        image_data = await file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")
        
        # Store the encoded image data and filename in Redis
        ttl = timedelta(hours=1)
        await self.conn.setex(image_redis_key, int(ttl.total_seconds()), encoded_data)
        await self.conn.setex(get_redis_filename(image_redis_key), int(ttl.total_seconds()), file.filename)
        self.logger.info({'image_redis_key': image_redis_key, 'msg': 'Store the encoded image data and filename in Redis finished'})
        return image_redis_key, encoded_data
