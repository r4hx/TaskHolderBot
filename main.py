import json
import os

import boto3


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=os.getenv('USER_ACCESS_ID'),
    aws_secret_access_key=os.getenv('USER_ACCESS_SECRET'),
    region_name='ru-central1',
    endpoint_url='https://storage.yandexcloud.net'
)


def handler(event, context):
    data = json.loads(event["body"])
    body = {
        'method': 'sendMessage',
        'text': data['message']['text'],
        'chat': data['message']['chat']['id'],
    }
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(body),
        "isBase64Encoded": False
    }
