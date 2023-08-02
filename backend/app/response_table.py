"""
response status code detail info
"""

status_ok = {
    'status_code': '0000',
    'status_msg': 'OK'
}

status_codeerror = {
    'status_code': '0001',
    'status_msg': 'code error'
}

status_unexpected = {
    'status_code': '0002',
    'status_msg': 'unexpected error'
}

status_uniqueviolation = {
    'status_code': '5401',
    'status_msg': 'unique violation',
}

status_image_type_error = {
    'status_code': '5402',
    'status_msg': 'image type error',
}

status_templateerror = {
    'status_code': '5404',
    'status_msg': 'template error'
}

status_templateexisterror = {
    'status_code': '5407',
    'status_msg': 'template_id not exist'
}

status_parametererror = {
    'status_code': '5415',
    'status_msg': 'parameter error'
}

status_boxrerror = {
    'status_code': '5416',
    'status_msg': 'widthheight error'
}

status_bad_quality = {
    'status_code': '5429',
    'status_msg': 'bad image quality error'
}

status_class_error = {
    'status_code': '5429',
    'status_msg': 'confirm image class check error'
}

response_table = {
    '0000': status_ok,
    '0001': status_codeerror,
    '0002': status_unexpected, 
    '5401': status_uniqueviolation,
    '5402': status_image_type_error,
    '5404': status_templateerror,
    '5407': status_templateexisterror,
    '5415': status_parametererror,
    '5416': status_boxrerror,
    '5420': status_bad_quality,
    '5421': status_class_error
}