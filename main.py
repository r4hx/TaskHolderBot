import json
from yasdk import ObjectStorage


def handler(event, context):
    yc = ObjectStorage()
    data = json.loads(event["body"])
    yc.update_user_info(data)
    print(data)
    if data['message']['text'] == '/start':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json'
            },
            "body": 'Здарова ёпта 😀',
            "isBase64Encoded": False,
        }
    else:
        body = {
            'method': 'sendMessage',
            'text': data['message']['text'],
            'chat_id': data['message']['from']['id'],
        }
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json'
            },
            "body": json.dumps(body),
            "isBase64Encoded": False,
        }
