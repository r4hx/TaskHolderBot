import json
import os

import boto3


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=os.getenv('SERVICE_USER_ACCESS_ID'),
    aws_secret_access_key=os.getenv('SERVICE_USER_ACCESS_SECRET'),
    region_name='ru-central1',
    endpoint_url='https://storage.yandexcloud.net'
)


def handler(event, context):
    data = json.loads(event["body"])
    body = {
        'method': 'sendMessage',
        'text': data['message']['text'],
        'chat_id': data['message']['chat']['id'],
    }
    s3.put_object(
        Bucket=os.getenv('YC_BUCKET'),
        Key=data['message']['chat']['id'],
        Body=data['message']['text'],
    )
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(body),
        "isBase64Encoded": False
    }


if __name__ == "__main__":
    pass
