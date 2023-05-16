"""
Kafka parameters of ocr results
"""
from pydantic import BaseModel, Extra, Field, StrictStr
from typing import List, Optional
from datetime import datetime


class OcrPredict(BaseModel, extra=Extra.allow):
    image_cv_id: StrictStr = Field(...,
                                   description='''影像編號<br /><br />''',
                                   example="test_ws_encrypt")
    ocr_type: StrictStr = Field(...,
                                description='''辨識結果對應圖檔<br /><br />''',
                                example="WITHHOLDING_STATEMENT")
    tag: StrictStr = Field(...,
                           description='''辨識要項<br /><br />''',
                           example="id")
    model: Optional[str] = Field(...,
                                 description='''模型名稱<br /><br />''',
                                 example="attention")
    label: Optional[str] = Field(...,
                                 description='''辨識結果<br /><br />''',
                                 example="F1234567")
    prob: Optional[List] = Field(...,
                                 description='''辨識機率值<br /><br />''',
                                 example=[0.9586760401725769, 0.9515883326530457, 0.9507707953453064, 0.9577591419219971, 0.952286422252655, 0.9467113018035889, 0.9480671286582947])
    x_min: Optional[int] = Field(...,
                                 description='''BBOX X軸最小值<br /><br />''',
                                 example=89)
    y_min: Optional[int] = Field(...,
                                 description='''BBOX Y軸最小值<br /><br />''',
                                 example=226)
    x_max: Optional[int] = Field(...,
                                 description='''BBOX X軸最大值<br /><br />''',
                                 example=213)
    y_max: Optional[int] = Field(...,
                                 description='''BBOX Y軸最大值<br /><br />''',
                                 example=253)
    etl_dt: datetime = Field(...,
                             description='''時間戳記<br /><br />''',
                             example='2022-04-06 18:11:52')


class CALLBACKInput(BaseModel, extra=Extra.allow):
    ocr_results: List[OcrPredict]


class CALLBACKOutput(BaseModel, extra=Extra.allow):
    status_code: str = Field(
        title='服務狀況',
        description='''
        所有可能的選項:
        "0000": 正常
        "0001": 程式碼錯誤
        ''',
        example='0000'
    )
    status_msg: str = Field(
        title='服務狀況內容',
        description='''
        所有可能的選項:
        "OK": 正常
        "code error": 程式碼錯誤
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        ''',
    )
