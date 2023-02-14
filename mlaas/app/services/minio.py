from minio import Minio


BUCKET_NAME = 'if-gp-ocr'


def check_bucket(client):
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
    else:
        print('Bucket already exists')


def get_minio_client():
    client = Minio(
        endpoint='minio:9000',
        access_key='admin',
        secret_key='admin123',
        secure=False
        # **default_minio_args
    )
    return client
