export const FILE_SIZE_LIMIT = 5 * 1024 * 1024; // 5 MB
export const API_TIMEOUT = 600000; // 5 minutes (in milliseconds)
export const PULL_INTERVAL = 3000; // xx second (in milliseconds)
export const MAX_RETRIES = 30; // 30 times
export const MIN_PIXEL = 100; // create template
export const default_error_msg = '系統非預期錯誤，請聯絡管理員';
export const error_table = {
    // '0001': '系統非預期錯誤，請聯絡管理員',
    // '0002':  '系統非預期錯誤，請聯絡管理員',
    '5401': '該帳號同時在創建模板，請稍後再試',
    // '5402': '系統非預期錯誤，請聯絡管理員',
    // '5407': '系統非預期錯誤，請聯絡管理員',
    '5413': '圖檔過大，請縮小影像尺寸再次上傳',
    // '5415': '系統非預期錯誤，請聯絡管理員',
    // '5416': '系統非預期錯誤，請聯絡管理員',
    // '5001': '網頁系統非預期錯誤，請聯絡管理員', // web unknown error
    // '5002': '網頁系統非預期錯誤，請聯絡管理員', // web redis unknown error
    // '5003': '網頁系統非預期錯誤，請聯絡管理員', // web redis result find error
    '5004': '要求逾時，請重新上傳圖片'
};
