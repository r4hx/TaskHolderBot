import json
import os

import boto3


class YandexCloudS3:

    def __init__(self):
        self.session = boto3.session.Session()
        self.s3 = self.session.client(
            service_name='s3',
            aws_access_key_id=os.getenv('USER_ACCESS_ID'),
            aws_secret_access_key=os.getenv('USER_ACCESS_SECRET'),
            region_name='ru-central1',
            endpoint_url='https://storage.yandexcloud.net'
        )
        self.bucket = os.getenv('BUCKET')

    def upload(self, user_id, filename, body):
        self.user_id = user_id
        self.filename = filename
        self.body = body
        self.result = self.s3.put_object(
            Bucket=self.bucket,
            Key="users/{}/{}".format(self.user_id, self.filename),
            Body=self.body,
        )
        return self.result

    def download(self, user_id, filename):
        self.user_id = user_id
        self.filename = filename
        self.result = self.s3.get_object(
            Bucket=self.bucket,
            Key="users/{}/{}".format(self.user_id, self.filename)
        )
        return self.result

    def delete(self, user_id, filename):
        self.user_id = user_id
        self.filename = filename
        self.result = self.s3.delete_object(
            Bucket=self.bucket,
            Key="users/{}/{}".format(self.user_id, self.filename)
        )
        return self.result


def handler(event, context):
    yc = YandexCloudS3()
    data = json.loads(event["body"])
    body = {
        'method': 'sendMessage',
        'text': data['message']['text'],
        'chat_id': data['message']['chat']['id'],
    }
    yc.upload(str(body.get('chat_id')), 'messages.txt', str(body.get('text')))
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json'
        },
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
