from typing import List, Optional
from pydantic import BaseModel, Extra, Field


class DefaultInputs(BaseModel, extra=Extra.forbid):
    system_id: str = Field(
        title='資產代碼_系統簡稱',
        description='''
        ''',
        example='CH0052_OLIU'
    )
    business_category: List[str] = Field(
        title='業務別',
        description='''
        所有可能的選項:
        "CARDAPPLY": 申辦信用卡
        "FRAUD": 冒用聲明文件與報案單
        "OPEN_ACCOUNT_BANK": 開戶(玉銀)
        ''',
        example=['OPEN_ACCOUNT_BANK', 'UNSECURED_LOAN']
    )

    # @validator('business_category', allow_reuse=True)
    # def confirm_business_category(cls, field_value):
    #     if len(field_value) != len(set(field_value)):
    #         raise ValueError('business_category不能重複')
    #     else:
    #         return field_value


class CallBackInputs(BaseModel):
    callback_url: str = Field(
        title='請求callback伺服器的url',
        description='''
        OCR辨識完成後會向此url發送callback請求，請求方法為POST
        body為callback_body指定的內容
        headers為callback_headers指定的內容
        該url需要響應"HTTP/1.1 200 OK"，我們將以HTTP狀態碼確認callback成功與否
        ''',
        example='www.google.com'
    )
    callback_body: str = Field(
        title='callback的內容',
        description='''<pre><code><div class="renderedMarkdown">    必須為可被解譯成JSON格式的字串
    其內容必須包含${image_cv_id}與${recognition_status}兩個變數提供MLaaS API替換請求變數
    而${ocr_results}或${detection_results}必須擇一提供MLaaS API替換請求變數
    若需要辨識完成的時間，則可選擇在字串中包含${datetime}提供MLaaS API替換請求變數
    屆時在callback時，會將這兩個變數替換。內容說明如下
    image_cv_id: 影像註冊的 key 值
    recognition_status: 辨識狀態。成功為"SUCCESS"，失敗為"FAIL"
    datetime: 辨識完成的時間，e.g. "2022-04-06 18:11:52"
    ocr_results: OCR的辨識結果，其內容為List of JSON，範例與JSON的內容描述如下:
            當 predict_class 為 "ID_FRONT" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/ID_FRONT.txt">連結</a>
            當 predict_class 為 "ID_BACK" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/ID_BACK.txt">連結</a>
            當 predict_class 為 "ID_FULL" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/ID_FULL.txt">連結</a>
            當 predict_class 為 "WITHHOLDING_STATEMENT" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/WS.txt">連結</a>
            當 predict_class 為 "PASSBOOK_COVER" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/PBC.txt">連結</a>
            當 predict_class 為 "PASSBOOK_INNER" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/PBI.txt">連結</a>
            當 predict_class 為 "NTB_FINANCIAL_STATEMENT" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/FS.txt">連結</a>
            當 predict_class 為 "DRIVER_LICENSE" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/LICENSE.txt">連結</a>
            當 predict_class 為 "HEALTH_INSURANCE" 時，內容描述與範例如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/HEALTH.txt">連結</a>
    detection_results: 人臉與證件照的辨識結果，其內容為List of JSON，JSON的內容範例與描述如 <a href="https://esgarden.esunbank.com.tw/personal/esb21762/Documents/%E8%88%87%E6%89%80%E6%9C%89%E4%BA%BA%E5%85%B1%E7%94%A8/ID_FACE.txt">連結</a></div></code></pre>
        ''',
        example="{\"business_unit\": \"C170\", \"inputs\": {\"id\": \"${image_cv_id}\", \"status\": \"${recognition_status}\", \"results\": \"${ocr_results}\"}}"
    )
    callback_headers: str = Field(
        title='callback的headers',
        description='''
        必須為可被解譯成JSON格式的字串(若無headers, 請帶"{}")
        ''',
        example="{\"x-client-id\": \"abcde\"}"
    )

    # @validator('callback_body', allow_reuse=True)
    # def confirm_callback_body(cls, field_value):
    #     if field_value is not None:
    #         keyword_list = re.findall(r"\$\{(.*?)\}", field_value)
    #         if not all(x in keyword_list for x in ['image_cv_id', 'recognition_status']):
    #             raise ValueError('輸入的callbody字串中沒有包含${image_cv_id}或${recognition_status}')
    #         if not any(x in keyword_list for x in ['ocr_results', 'detection_results']):
    #             raise ValueError('輸入的callbody字串中沒有包含${ocr_results}或${detection_results}')
    #         try:
    #             json.loads(field_value)
    #         except json.decoder.JSONDecodeError:
    #             raise ValueError('輸入的callbody字串無法解譯成json格式')
    #     return field_value

    # @validator('callback_headers', allow_reuse=True)
    # def confirm_callback_headers(cls, field_value):
    #     if field_value is not None:
    #         try:
    #             json.loads(field_value)
    #         except json.decoder.JSONDecodeError:
    #             raise ValueError('輸入的headers字串無法解譯成json格式')
    #     return field_value


class CVInputs(DefaultInputs):
    image: str = Field(
        title='base64 字串的影像',
        description='''
        ''',
        example='/9j/4AAQSkZJRgABAQEBLAEsAAD/2w'
    )
    action: str = Field(
        title='執行動作',
        description='''
        "RECOGNITION": 執行全部的辨識流程(辨識結果需再利用 ASSEMBLE SERVICE 取得)
        "ONLY_CLASSIFY_CLEARNESS": 僅做影像分類與影像清晰度
        ''',
        example='RECOGNITION'
    )
    source: Optional[str] = Field(
        'EXTERNAL',
        title='請求來源',
        description='''
        "EXTERNAL": 此請求來自外部顧客
        "INTERNAL": 此請求來自行員
        ''',
        example='EXTERNAL'
    )
    callback: Optional[List[CallBackInputs]] = Field(
        title='請求callback時的相關參數',
        description='''
        當執行動作為RECOGNITION時，才需設定其相關參數，可設定多個 callback 伺服器
        ''',
        nullable=True,
        example=[{'callback_url': 'www.google.com',
                  'callback_body': "{\"business_unit\": \"C170\", \"inputs\": {\"id\": \"${image_cv_id}\", \"status\": \"${recognition_status}\", \"results\": \"${ocr_results}\"}}",
                  'callback_headers': "{\"x-client-id\": \"abcde\"}"},
                 {'callback_url': 'tw.yahoo.com',
                  'callback_body': "{\"system_id\": \"OULU\", \"inputs\": {\"image_id\": \"${image_cv_id}\", \"status\": \"${recognition_status}\", \"results\": \"${ocr_results}\"}}",
                  'callback_headers': "{\"client-id\": \"abcde\"}"}]
    )
    clearness_type: str = Field(
        title='判斷影像是否清晰的種類',
        description='''
        當執行動作為RECOGNITION時，
        "DISABLE": 不論影像是否清晰，都會做RECOGNITION
        "DEFAULT": 使用預設的門檻值 (預設門檻值為 1) 判斷影像是否清晰，若影像清晰，才會做RECOGNITION
        "MANUAL": 手動設定門檻值判斷影像是否清晰，若影像清晰，才會做RECOGNITION
        當執行動作為ONLY_CLASSIFY_CLEARNESS時，
        "DEFAULT": 使用預設的門檻值 (預設門檻值為 1) 判斷影像是否清晰
        "MANUAL": 手動設定門檻值判斷影像是否清晰
        ''',
        example='MANUAL'
    )
    clearness_threshold: Optional[float] = Field(
        title='判斷影像是否清晰的門檻值',
        description='''
        ''',
        nullable=True,
        example=2
    )
    image_class: Optional[str] = Field(
        title='欲確認的影像類別',
        description='''
        支援的圖片類型:
        "ID": 身分證正面or反面
        "ID_FRONT": 身分證正面
        "ID_BACK": 身分證反面
        "ID_FACE": 人臉與證件照(不做分類)
        "ID_FULL": 身分證正反影本(不做分類)
        "NTB_FINANCIAL_STATEMENT": 國稅局個人所得清單
        "PASSBOOK": 存摺封面or內頁
        "PASSBOOK_COVER": 存摺封面
        "PASSBOOK_INNER": 存摺內頁
        "WITHHOLDING_STATEMENT": 扣繳憑單
        "SECOND_ID": 第二證件(駕照or健保卡)
        "DRIVER_LICENSE": 駕照
        "HEALTH_INSURANCE": 健保卡
        ''',
        nullable=True,
        example='PASSBOOK_COVER'
    )

    # @validator('action', allow_reuse=True)
    # def confirm_action(cls, field_value):
    #     if field_value not in ['RECOGNITION', 'ONLY_CLASSIFY_CLEARNESS']:
    #         raise ValueError('不支援此執行動作')
    #     else:
    #         return field_value

    # @validator('source', allow_reuse=True)
    # def confirm_source(cls, field_value, values, field, config):
    #     if field_value not in ['EXTERNAL', 'INTERNAL']:
    #         raise ValueError('不支援此來源')
    #     return field_value.lower()

    # @validator('clearness_type', allow_reuse=True)
    # def confirm_clearness_type(cls, field_value, values, field, config):
    #     if field_value not in ['DISABLE', 'MANUAL', 'DEFAULT']:
    #         raise ValueError('不支援此清晰度種類')
    #     else:
    #         return field_value

    # @validator('clearness_threshold', allow_reuse=True)
    # def confirm_clearness_threshold(cls, field_value, values, field, config):
    #     if 'clearness_type' in values:
    #         if values['clearness_type'] == 'MANUAL':
    #             if field_value is None:
    #                 raise ValueError('當清晰度種類為 MANUAL 時，clearness_threshold 必須存在')
    #             if field_value <= 0:
    #                 raise ValueError('清晰度的門檻值必大於0')
    #         else:
    #             if field_value is not None:
    #                 raise ValueError('當清晰度種類為 DEFAULT 和 DISABLE 時，clearness_threshold 不需設定')
    #     return field_value

    # @validator('image_class', allow_reuse=True)
    # def image_class_check(cls, field_value):
    #     if field_value not in cfg.CLASS_CANDIDATE:
    #         if field_value is not None:
    #             raise ValueError('不支援此影像類別')
    #     return field_value


class CVOutputs(BaseModel, extra=Extra.forbid):
    status_code: str = Field(
        title='服務狀況',
        description='''
        所有可能的選項:
        "0000": 正常
        "0002": 資料庫錯誤
        "5402": 圖檔格式錯誤
        "5420": 圖檔品質不佳(執行動作為 RECOGNITION 時才會出現此服務狀況)
        "5421": 圖檔類別確認失敗(執行動作為 RECOGNITION 時才會出現此服務狀況)
        "5499": 未預期錯誤
        ''',
        example='0000'
    )
    status_msg: str = Field(
        title='服務狀況內容',
        description='''
        所有可能的選項:
        "OK": 正常
        "DB error": 資料庫錯誤
        "image type error": 圖檔格式錯誤
        "bad image quality error": 圖檔品質不佳(執行動作為 RECOGNITION 時才會出現此服務狀況)
        "confirm image class check error": 圖檔類別確認失敗(執行動作為 RECOGNITION 時才會出現此服務狀況)
        "unexpected error": 未預期錯誤
        ''',
        example='OK'
    )
    err_detail: Optional[dict] = Field(
        title='錯誤訊息',
        description='''
        ''',
    )
    image_cv_id: Optional[str] = Field(
        title='影像註冊的 key 值',
        description='''
        ''',
        example='438ffd10-1090-4687-be84-8f6c36be463a'
    )
    predict_class: Optional[str] = Field(
        title='模型預測的影像種類',
        description='''
        "ID_FRONT": 身分證正面
        "ID_BACK": 身分證反面
        "NTB_FINANCIAL_STATEMENT": 國稅局個人所得清單
        "OTHERS": 其他
        "PASSBOOK_COVER": 存摺封面
        "PASSBOOK_INNER": 存摺內頁
        "WITHHOLDING_STATEMENT": 扣繳憑單
        "DRIVER_LICENSE": 駕照
        "HEALTH_INSURANCE": 健保卡
        ''',
        example='ID_FRONT'
    )
    predict_class_prob: Optional[float] = Field(
        title='模型信心水準 (機率值)',
        description='''
        最小值: 0
        最大值: 1
        ''',
        example=0.99
    )
    clearness_status: Optional[str] = Field(
        title='影像清晰度狀態',
        description='''
        "blur": 影像模糊
        "clear": 影像清晰
        ''',
        example='blur'
    )
    clearness_value: Optional[float] = Field(
        title='影像清晰度',
        description='''
        ''',
        example=8.0
    )

