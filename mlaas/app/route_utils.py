from fastapi import Form


def get_output_template():
    return {
        'business_unit': '',
        'request_id': '',
        'trace_id': '',
        'request_time': '',
        'duration_time': ''
}
