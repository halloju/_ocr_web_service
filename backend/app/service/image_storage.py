import base64
import uuid
from typing import Tuple
from route_utils import  get_redis_filename


class ImageStorage:
    def __init__(self, conn):
        self.conn = conn

    async def store_image_data(self, file) -> Tuple[str, str]:
        image_id = str(uuid.uuid4())
        image_data = await file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data and filename in Redis
        await self.conn.set(image_id, encoded_data)
        await self.conn.set(get_redis_filename(image_id), file.filename)

        return image_id, encoded_data
