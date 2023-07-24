import { error_table, default_error_msg } from '../constants.js';

export const handleErrorMsg = (res) => {
    let error_msg = default_error_msg;
    if ( typeof(res.data) === 'object' && 'mlaas_code' in res.data) {
        console.log(res.data.mlaas_code);
        if (res.data.mlaas_code in error_table) error_msg = error_table[res.data.mlaas_code] + ' (' + res.data.mlaas_code + ')';
    }
    return error_msg;
};