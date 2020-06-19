import json
from yasdk import ObjectStorage


def handler(event, context):
    yc = ObjectStorage()
    data = json.loads(event["body"])
    body = {
        'method': 'sendMessage',
        'text': data['message']['text'],
        'id': data['message']['from']['id'],
    }
    yc.upload(str(body.get('id')), 'messages.txt', str(body.get('text')))
    print(data)
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json'
        },
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
