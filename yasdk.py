import os
import json
import time

import boto3
from messages import messages
from botocore.exceptions import ClientError


class ObjectStorage:

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
        self.users_dir = 'users'

    def upload(self, user_id, filename, body):
        self.user_id = user_id
        self.filename = filename
        self.body = body
        self.result = self.s3.put_object(
            Bucket=self.bucket,
            Key="{}/{}/{}".format(self.users_dir, self.user_id, self.filename),
            Body=self.body.encode('utf8'),
        )
        return self.result

    def download(self, user_id, filename):
        self.user_id = user_id
        self.filename = filename
        self.result = self.s3.get_object(
            Bucket=self.bucket,
            Key="{}/{}/{}".format(self.users_dir, self.user_id, self.filename)
        )
        return self.result

    def delete(self, user_id, filename):
        self.user_id = user_id
        self.filename = filename
        self.result = self.s3.delete_object(
            Bucket=self.bucket,
            Key="{}/{}/{}".format(self.users_dir, self.user_id, self.filename)
        )
        return self.result

    def update_user_info(self, data):
        self.info = {
            'id': data['message']['from']['id'],
            'first_name': data['message']['from']['first_name'],
            'last_name': data['message']['from']['last_name'],
            'language_code': data['message']['from']['language_code'],
            'paid': 0,
            'last_message': data['message']['text'],
            'last_activity': data['message']['date'],
        }
        self.upload(
            data['message']['from']['id'],
            'info.txt',
            json.dumps(self.info, indent=4, ensure_ascii=False)
        )

    def get_user_info(self, data):
        self.result = self.download(
            data['message']['from']['id'],
            "info.txt"
        )
        return json.loads(self.result['Body'].read().decode('utf-8'))

    def task_list(self, data):
        self.data = data
        self.user_id = self.data['message']['from']['id']
        self.filename = "tasks.txt"
        try:
            self.result = self.download(self.user_id, self.filename)
            self.task_list = json.loads(
                self.result['Body'].read().decode('utf-8')
            )
        except ClientError:
            pass
        return self.task_list

    def task_add(self, data):
        self.data = data
        self.user_id = self.data['message']['from']['id']
        self.filename = "tasks.txt"
        self.task_list = {}
        try:
            self.result = self.download(self.user_id, self.filename)
            self.task_list = json.loads(
                self.result['Body'].read().decode('utf-8')
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print("Created new tasks.txt file")
        finally:
            self.text = self.data['message']['text']
            self.num_task = len(self.task_list) + 1
            self.task_list[self.num_task] = {
                'created': int(time.time()),
                'text': self.text,
                'active': True,
                'finished': '',
            }
            self.upload(
                self.user_id, self.filename,
                json.dumps(self.task_list, indent=4, ensure_ascii=False)
            )

    def task_delete(self, data):
        pass
