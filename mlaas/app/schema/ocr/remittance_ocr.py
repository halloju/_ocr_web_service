from pydantic import BaseModel, Field
from app.common.schema import img_base64_string


class PredictInput(BaseModel):
    image: str = Field(...,
                       description='''base64 字串的影像<br /><br />''',
                       example=img_base64_string)


class PredictOutput(BaseModel):
    status_code: str = Field(...,
                             description='''服務狀態碼<br /><br />
                                            狀態碼：<br />
                                            API 服務正常："0000"<br />
                                            程式碼錯誤："0001"<br />
                                            DB相關錯誤："0002"<br />
                                            request_id 重複呼叫："5401"<br />
                                            ''',
                             example="0000")
    status_msg: str = Field(...,
                            description='''服務狀態內容<br /><br />
                                           狀態內容<br />
                                           API 服務正常："OK"<br />
                                           程式碼錯誤："code error"<br />
                                           DB相關錯誤："DB error"<br />
                                           request_id 重複呼叫："unique violation"<br />
                                           ''',
                            example="OK")
    remitno: str = Field(...,
                         description='''匯款序號<br /><br />
                                        1. 回辨識過後的匯款序號<br />
                                        2. 非六位數則回傳空值<br />
                                        3. 英數字<br />
                                        ''',
                         example="I90002")
    amount: str = Field(...,
                        description='''匯款金額<br /><br />
                                        1. 回辨識過後的匯款金額<br />
                                        2. 右靠左補零<br />
                                        3. 純數字<br />
                                        ''',
                        example="0000000000500")
    receiveacc: str = Field(...,
                            description='''收款帳號<br /><br />
                                            1. 回辨識過後的收款帳號<br />
                                            2. 右靠左補零<br />
                                            3. 純數字<br />
                                            ''',
                            example="00015979150388")
    remitterid: str = Field(...,
                            description='''匯款人ID<br /><br />
                                            1. 回辨識過後的匯款人ID<br />
                                            2. 英數字<br />
                                            3. 8碼(公司)或10碼(個人)<br />
                                            ''',
                            example="A123456789")
    agentid: str = Field(...,
                         description='''代理人ID<br /><br />
                                        1. 回辨識過後的代理人ID<br />
                                        2. 英數字<br />
                                        3. 若辨識不出或顧客無填寫則為空<br />
                                        4. 10碼(個人)<br />
                                        ''',
                         example="B123456789")
    receivebank: str = Field(...,
                             description='''收款行代號<br /><br />
                                            1. 回辨識過後的收款行編碼<br />
                                            2. 純數字<br />
                                            3. 7 碼<br />
                                            ''',
                             example="5210116")
    remark: str = Field(...,
                        description='''是否有附言<br /><br />
                                        回辨識過後的附言是否有值(Y/N)<br />
                                        ''',
                        example="Y")
    receiver_name: str = Field(...,
                               description='''收款人戶名<br /><br />
                                              最多 40 字<br />
                                              ''',
                               example="王曉明")
    remit_name: str = Field(...,
                            description='''匯款人戶名<br /><br />
                                           最多 40 字<br />
                                           ''',
                            example="黃大強")
    agent_name: str = Field(...,
                            description='''代理人姓名<br /><br />
                                           1. 若辨識不出或顧客無填寫則為空<br />
                                           2. 最多 40 字<br />
                                           ''',
                            example="陳玉珊")
