from minio import Minio
from minio.error import S3Error
import os
import sys
from dotenv import load_dotenv

load_dotenv()
URL_MINIO = os.getenv('LINK_MINIO')
ACCESS_KEY = os.getenv('ACCESS_KEY_MINIO')
SECRET_KEY = os.getenv('SECRECTE_KEY_MINIO')

def main(bucket, archivo):
    # Conexión al servidor de buckets
    client = Minio(
        URL_MINIO,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
    )

    # Valida si el bucket existe sino lo crea
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
    else:
        print(f"Bucket '{bucket}' already exists")

    # Carga un archivo de la ruta
    client.fput_object(
        bucket, archivo, 'imagenes/azurep.png'
    )

    print(
        "Successfully uploaded as "
        f"object '{archivo}' to bucket '{bucket}'."
    )

    #Lista los buckets que hay
    """
    buckets = client.list_buckets()
    for bucketl in buckets:
        print(bucketl.name, bucketl.creation_date)
    """


if __name__ == "__main__":
    try:
        main('pruebas','azurep.png')
    except S3Error as exc:
        print("error occurred.", exc)


