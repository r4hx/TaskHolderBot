import json
import os

import boto3


class YandexCloudS3:

    def __init__(self):
        self.session = boto3.session.Session()
        self.s3 = self.session.client(
            service_name='s3',
            aws_access_key_id=os.getenv('SERVICE_USER_ACCESS_ID'),
            aws_secret_access_key=os.getenv('SERVICE_USER_ACCESS_SECRET'),
            region_name='ru-central1',
            endpoint_url='https://storage.yandexcloud.net'
        )
        self.bucket = os.getenv('YC_BUCKET')

    def put(self, key, body):
        self.key = key
        self.body = body
        self.s3.put_object(
            Bucket=self.bucket, Key=self.key, Body=self.body,
        )


def handler(event, context):
    yc = YandexCloudS3()
    data = json.loads(event["body"])
    body = {
        'method': 'sendMessage',
        'text': data['message']['text'],
        'chat_id': data['message']['chat']['id'],
    }
    yc.put(body.get('chat_id', default='_'), body.get('text', default='_'))
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json'
        },
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
