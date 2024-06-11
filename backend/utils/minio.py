import os
from minio import Minio
from minio.error import ResponseError

class MinioStorage:
    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False
        )

    def save_image(self, image_path, object_name):
        try:
            self.client.fput_object(
                self.bucket_name,
                object_name,
                image_path
            )
            print(f"Image {object_name} saved successfully.")
        except ResponseError as err:
            print(f"Error saving image: {err}")

    def load_image(self, object_name, destination_path):
        try:
            self.client.fget_object(
                self.bucket_name,
                object_name,
                destination_path
            )
            print(f"Image {object_name} loaded successfully.")
        except ResponseError as err:
            print(f"Error loading image: {err}")

# Example usage
if __name__ == "__main__":
    # Initialize MinioStorage object
    minio_storage = MinioStorage(
        endpoint="your-minio-endpoint",
        access_key="your-access-key",
        secret_key="your-secret-key",
        bucket_name="your-bucket-name"
    )

    # Save an image
    minio_storage.save_image("path/to/image.jpg", "image.jpg")

    # Load an image
    minio_storage.load_image("image.jpg", "path/to/destination.jpg")