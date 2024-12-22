import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image
from io import BytesIO

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    s3_target = "thumbnail-invokelambda-sandesh"
    key_target = "thumbnails/" + key
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        upload_image = response['Body'].read()

        image = Image.open(BytesIO(upload_image))
        image.thumbnail((1280, 720))
        thumbnail_buffer = BytesIO()
        image.save(thumbnail_buffer, 'JPEG')
        thumbnail_buffer.seek(0)


        s3.put_object(
            Bucket= s3_target,
            Key= key_target,
            Body= thumbnail_buffer,
            ContentType= 'image/jpg'
            )

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
