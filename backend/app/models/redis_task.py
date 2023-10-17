import json
from app.models.task import Task


class RedisTaskRepository:
    def __init__(self, redis_pool):
        self.conn = redis_pool

    async def save(self, task):
        """
        Save the task data into Redis.
        """
        task_data = task.to_dict()
        await self.conn.set(self._task_key(task.task_id), json.dumps(task_data))

        # If you also need to save image data or other associated data,
        # you can add more set operations here.

    async def get(self, task_id):
        """
        Retrieve the task data from Redis.
        """
        task_data_str = await self.conn.get(self._task_key(task_id))
        if not task_data_str:
            return None

        task_data = json.loads(task_data_str)
        # Construct a Task object from the stored data.
        task = Task(
            task_data['image_id'],
            task_data['file_name'],
            task_data['predict_class'],
            task_data['status'],
            task_data['image_cv_id'],
            task_data['err_msg']
        )
        return task

    async def delete(self, task_id):
        """
        Remove the task data from Redis.
        """
        await self.conn.delete(self._task_key(task_id))

    def _task_key(self, task_id):
        """
        Generate a Redis key for the task based on its ID.
        """
        return f'task:{task_id}'

    # Add more methods if you need to manage other related data,
    # such as image data, associated with the task.
