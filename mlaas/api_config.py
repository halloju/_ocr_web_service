# http response description
http_responses = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated"
                }
            }
        }
    },
    500: {
        "model": MlaasHttpOutput,
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "business_unit": "IF_C170", "request_id": "ckn56cRs8f1KS12345",
                    "trace_id": "82cbe90c-18a7-447f-996b-612b654f1db8",
                    "request_time": 1615785636.8845854, "response_time": 1615785636.8863857,
                    "duration_time": 0.0018, "outputs": {
                        "status_code": "0001", "status_msg": "API run failed"
                    }
                }
            }
        },
    },
    507: {
        "model": MlaasHttpOutput,
        "description": "Insufficient Storage",
        "content": {
            "application/json": {
                "example": {
                    "business_unit": "IF_C170", "request_id": "ckn56cRs8f1KS12345",
                    "trace_id": "82cbe90c-18a7-447f-996b-612b654f1db8",
                    "request_time": 1615785636.8845854, "response_time": 1615785636.8863857,
                    "duration_time": 0.0018, "outputs": {
                        "status_code": "0002", "status_msg": "MLaaS DB Error"
                    }
                }
            }
        },
    },
    510: {
        "model": MlaasHttpOutput,
        "description": "Not Extended",
        "content": {
            "application/json": {
                "example": {
                    "business_unit": "IF_C170", "request_id": "ckn56cRs8f1KS12345",
                    "trace_id": "82cbe90c-18a7-447f-996b-612b654f1db8",
                    "request_time": 1615785636.8845854, "response_time": 1615785636.8863857,
                    "duration_time": 0.0018, "outputs": {
                        "status_code": "0004", "status_msg": "ESIP API failed"
                    }
                }
            }
        },
    },
    512: {
        "model": MlaasHttpOutput,
        "description": "Model Serving Failed",
        "content": {
            "application/json": {
                "example": {
                    "business_unit": "IF_C170", "request_id": "ckn56cRs8f1KS12345",
                    "trace_id": "82cbe90c-18a7-447f-996b-612b654f1db8",
                    "request_time": 1615785636.8845854, "response_time": 1615785636.8863857,
                    "duration_time": 0.0018, "outputs": {
                        "status_code": "0001", "status_msg": "API run failed"
                    }
                }
            }
        },
    }
}
