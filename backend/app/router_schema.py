from pydantic import Field, BaseModel


# API default output schema
class MlaasErrorOutput(BaseModel):
    mlaas_code: str = Field(
        ..., title="Mlaas的錯誤代碼",
        description="The code of mlaas error code（only 4 digit）",
        example="5401"
    )
    message: str = Field(..., title="Mlaas的錯誤訊息", example="template_id 不存在")
