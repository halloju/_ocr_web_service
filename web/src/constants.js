export const FILE_SIZE_LIMIT = 10 * 1024 * 1024; // 10 MB
export const TEMPLATE_FILE_SIZE_LIMIT = 5 * 1024 * 1024; // 5 MB
export const TOTAL_FILE_SIZE_LIMIT = 200
export const API_TIMEOUT = 600000; // 5 minutes (in milliseconds)
export const PULL_INTERVAL = 3000; // xx second (in milliseconds)
export const MAX_RETRIES = 30; // 30 times
export const MIN_PIXEL = 100; // create template
export const default_error_msg = '系統非預期錯誤，請聯絡管理員';
export const templateLimit = 20; // 模板上限
export const error_table = {
    // '0001': '系統非預期錯誤，請聯絡管理員',
    // '0002':  '系統非預期錯誤，請聯絡管理員',
    5401: '同一員工編號在同一秒內上傳或更新模板',
    5402: '檔案格式錯誤',
    5407: '模板編號不存在',
    // '5415': '系統非預期錯誤，請聯絡管理員',
    // '5416': '系統非預期錯誤，請聯絡管理員',
    // '5001': '網頁系統非預期錯誤，請聯絡管理員', // web unknown error
    // '5002': '網頁系統非預期錯誤，請聯絡管理員', // web redis unknown error
    // '5003': '網頁系統非預期錯誤，請聯絡管理員', // web redis result find error
    5004: '要求逾時，請重新上傳圖片',
    5420: '圖片品質不佳，請重新上傳圖片',
    5421: '上傳錯誤圖片非服務辨識類別/系統無法辨識該種類的類別'
};
