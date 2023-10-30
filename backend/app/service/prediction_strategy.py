from typing import Any, Dict
import os
import json
from route_utils import async_call_mlaas_function, get_redis_filename, get_redis_taskname


class PredictionStrategy:
    async def call_api(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Any:
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def construct_payload(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class CVOcrPredictionStrategy(PredictionStrategy):
    def __init__(self, logger):
        self.callback_url = os.environ.get('GP_CALLBACK_MLAAS_URL', '')
        self.x_client_id = os.environ.get('MLAAS_XClient', '')
        self.authorization = os.environ.get('MLAAS_JWT', '')
        self.business_unit = "C170"
        self.endpoint = "ocr/upload"
        self.project_name = "CV"
        self.logger = logger

    async def call_api(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Any:
        payload = self.construct_payload(
            encoded_data, input_params, request_id)
        response = await async_call_mlaas_function(payload, action=self.endpoint, project=self.project_name, logger=self.logger)
        return response

    def construct_payload(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        callback_body = json.dumps({
            "business_unit": "C170",
            "request_id": "test",
            "inputs": {
                "image_cv_id": "${image_cv_id}",
                "recognition_status": "${recognition_status}",
                "ocr_results": "${ocr_results}"
            }
        })

        callback_headers = json.dumps({
            "x-client-id": self.x_client_id,
            "Authorization": self.authorization
        })

        payload = {
            "business_unit": self.business_unit,
            "request_id": request_id,
            "inputs": {
                "system_id": "CH0052_OLIU",
                "image": encoded_data,
                "source": "INTERNAL",
                "callback": [{
                    "callback_url": f"{self.callback_url}/callback/controller_callback/v1",
                    "callback_body": callback_body,
                    "callback_headers": callback_headers
                }],
                "business_category": ["OPEN_ACCOUNT_BANK", "UNSECURED_LOAN"],
                "action": "RECOGNITION",
                "clearness_type": "MANUAL",
                "clearness_threshold": 2,
                **input_params
            }
        }
        return payload


class GPOcrPredictionStrategy(PredictionStrategy):
    def __init__(self):
        self.callback_url = os.environ.get('GP_CALLBACK_MLAAS_URL', '')
        self.x_client_id = os.environ.get('MLAAS_XClient', '')
        self.authorization = os.environ.get('MLAAS_JWT', '')
        self.business_unit = "C170"
        self.endpoint = "ocr/upload"
        self.project_name = "CV"

    async def call_api(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Any:
        payload = self.construct_payload(
            encoded_data, input_params, request_id)
        response = await async_call_mlaas_function(payload, action=self.endpoint, project=self.project_name, logger=self.logger)
        return response

    def construct_payload(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        callback_body = json.dumps({
            "business_unit": "B31",
            "request_id": "test",
            "inputs": {
                "image_cv_id": "${image_cv_id}",
                "recognition_status": "${recognition_status}",
                "ocr_results": "${ocr_results}"
            }
        })

        callback_headers = json.dumps({
            "x-client-id": self.x_client_id,
            "Authorization": self.authorization
        })

        payload = {
            "system_id": "CH0052_OLIU",
            "business_unit": self.business_unit,
            "request_id": request_id,
            "inputs": {
                "system_id": "CH0052_OLIU",
                "image": encoded_data,
                "source": "INTERNAL",
                "callback": [{
                    "callback_url": f"{self.callback_url}/callback/controller_callback/v1",
                    "callback_body": callback_body,
                    "callback_headers": callback_headers
                }],
                "business_category": ["OPEN_ACCOUNT_BANK", "UNSECURED_LOAN"],
                "action": "RECOGNITION",
                "clearness_type": "MANUAL",
                "clearness_threshold": 2,
                **input_params
            }
        }
        return payload


class PredictionAPI:
    def __init__(self, strategy: PredictionStrategy, logger):
        self.strategy = strategy
        self.logger = logger

    async def call_prediction_api(self, encoded_data: str, input_params: Dict[str, Any], request_id: str) -> Any:
        return await self.strategy.call_api(encoded_data, input_params, request_id)
