from fastapi import Form
from pydantic import Field, BaseModel, create_model


# API default input schema
class DefaultInput(BaseModel):
    business_unit: str = Field(..., title="業管單位代碼",
                               description="The code of business unit, follow esun policy",
                               example="C170")
    request_id: str = Field(..., title="請求識別碼",
                            description="client-side UUID, must be unique", example="QAZWSXEDC")

    class Config:
        extra = 'forbid'


# API default output schema
class DefaultOutput(BaseModel):
    business_unit: str = Field(..., title="業管單位代碼",
                               description="The code of business unit, follow esun policy",
                               example="C170")
    request_id: str = Field(..., title="請求識別碼",
                            description="client-side UUID, must be unique", example="QAZWSXEDC")
    trace_id: str = Field(..., title="回應識別碼",
                          description="server-side UUID, must be unique", example="POILKJ")
    request_time: float = Field(..., title="收到請求時間點 (unix timestamp)",
                                description="Server receive time", example="1610093238.3967335")
    response_time: float = Field(..., title="回應結果時間點 (unix timestamp)",
                                 description="Server response time", example="1610093248.0620785")
    duration_time: float = Field(..., title="請求處理時間 (至小數點後四位)",
                                 description="Server compute time (response time - request time)",
                                 example="0.1234")

    class Config:
        extra = 'forbid'


# API final input / output schema generator
def mlaas_item_generator(name, api_inputs, api_outputs):
    """ Generator api input / output model class.

    Args:
      - name: action_name
      - project_inputs: proj input model class
      - project_outputs: proj output model class

    Returns:
      - mlaas_input: mlaas input final model class
      - mlaas_output: mlaas output final model class

    """

    mlaas_input = create_model(
        name + 'MlaasInput',
        inputs=(api_inputs, ...),
        __base__=DefaultInput
    )

    mlaas_output = create_model(
        name + 'MlaasOutput',
        outputs=(api_outputs, ...),
        __base__=DefaultOutput
    )
    return mlaas_input, mlaas_output
