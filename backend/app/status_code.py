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

status_dberror = {
    'status_code': '0002',
    'status_msg': 'DB error',
    'err_detail': {'error_message': 'Feature DB error'}
}

status_minioerror = {
    'status_code': '0002',
    'status_msg': 'DB error',
    'err_detail': {'error_message': 'MinIO error'}
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
