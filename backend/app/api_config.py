from app.router_schema import MlaasErrorOutput

# http response description
http_responses = {
    500: {
        "model": MlaasErrorOutput,
        "description": "Mlaas Error",
        "content": {
            "application/json": {
                "example": {
                        "mlaas_code": "0001",
                        "msg": "API run failed"
                }
            }
        }
    },
}
