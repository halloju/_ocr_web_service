"""
task asyn ocr (like cv controller)
"""
import base64
import json
import os
import uuid

from route_utils import call_mlaas_function, get_redis_filename, get_redis_taskname


class AsyncPredictTask(object):
    def __init__(self, redis_pool, request):
        super().__init__()
        self.conn = redis_pool
        self.business_unit = "C170"
        self.project_names = {
            'cv-ocr': 'CV',
        }
        self.endpoints = {
            'cv-ocr': 'ocr/upload',
        }
        self.logger = request.state.logger
        self.rid = request.state.request_id

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    async def predict(self, image_id, action, input_params):
        try:
            encoded_data = await self.conn.get(image_id)
            input_data = {
                "business_unit": self.business_unit,
                "request_id": self.rid,
                "inputs": {
                    "system_id": "CH0052_OLIU",
                    "business_category": [
                        "OPEN_ACCOUNT_BANK",
                        "UNSECURED_LOAN"
                    ],
                    "image": encoded_data,
                    "action": "RECOGNITION",
                    "source": "INTERNAL",
                    "clearness_type": "MANUAL",
                    "clearness_threshold": 2,
                    "callback": [
                        {
                            "callback_url": f"{os.environ.get(f'GP_CALLBACK_MLAAS_URL')}/callback/controller_callback/v1",
                            "callback_body": "{\"business_unit\": \"B31\", \"request_id\": \"test\", \"inputs\": {\"image_cv_id\": \"${image_cv_id}\", \"recognition_status\": \"${recognition_status}\", \"ocr_results\": \"${ocr_results}\"}}",
                            "callback_headers": json.dumps({
                                "x-client-id": os.environ.get(f'MLAAS_XClient'),
                                "Authorization": os.environ.get(f'MLAAS_JWT')})
                        }
                    ],
                    **input_params  # "image_class": "PASSBOOK_COVER"
                }
            } 
            data_pred = call_mlaas_function(
                input_data,
                action=self.endpoints[action],
                project=self.project_names[action],
                logger=self.logger
            )
            self.logger.debug({'predict': {'image_id': image_id, 'response_index ': list(data_pred.keys())}})
            # Return the prediction result
            return data_pred
        except Exception as e:
            self.logger.error({'predict': {'error_msg': str(e), 'image_id': image_id, 'action': action, 'input_params': input_params}})
            raise e

    async def predict_image(self, image_id, action, input_params):
        file_name = await self.conn.get(get_redis_filename(image_id))
        image_cv_id = 'cv-'+str(uuid.uuid4())
        try:
            response = self.predict(image_id, action=action, input_params=input_params)
            status_code = response['outputs']['status_code']
            # Get the file name from Redis using the image ID as the key
            if (response['outputs']['image_cv_id']):
                image_cv_id = response['outputs']['image_cv_id']
            predict_class = response['outputs']['predict_class']
            if status_code == '0000':
                return {'status': 'PROCESSING', 'predict_class': predict_class, 'file_name': file_name, 'image_cv_id': image_cv_id}
            elif status_code == '5421':  # class check error
                return {'status': 'FAIL', 'predict_class': predict_class, 'file_name': file_name+'-image-check-error', 'image_cv_id': image_cv_id}
            else:
                self.logger.warning({'predict_image': {'image_id': image_id, 'response': response}})
        except Exception as e:
            self.logger.error({'predict_image': {'error_msg': str(e), 'image_id': image_id, 'action': action}})
        return {'status': 'FAIL', 'err_msg': str(response['outputs']['status_msg']), 'image_cv_id': image_cv_id, 'file_name': file_name}

    async def process_image(self, file, action: str, input_params: dict):
        
        image_id = str(uuid.uuid4())
        # Read and encode the file data as base64
        image_data = file.file.read()
        encoded_data = base64.b64encode(image_data).decode("utf-8")

        # Store the encoded image data in Redis using the image ID as the key
        await self.conn.set(image_id, encoded_data)
        # Store the file name in Redis using the image ID as the key
        await self.conn.set(get_redis_filename(image_id), file.filename)
        # start task prediction
        upload_result = await self.predict_image(image_id, action=action, input_params=input_params)
        task_id = str(upload_result["image_cv_id"]).replace('/', '-')  # 2022/10/11.../uuid  -< 2022-10-11...-uuid
        await self.conn.set(get_redis_taskname(task_id), json.dumps({'task_id': task_id, 'status': upload_result["status"], 'url_result': f'/ocr/result/{task_id}', 'image_id': image_id, 'result': '', 'file_name': upload_result["file_name"]}))
        return {'task_id': task_id, 'status': upload_result["status"], 'url_result': f'/ocr/result/{task_id}', 'image_id': image_id, 'file_name': upload_result["file_name"]}
