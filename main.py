import json


def handler(event, context):
    data = json.loads(event["body"])
    body = {
        'method': 'sendMessage',
        'text': data['message']['text'],
        'chat_id': data['message']['chat']['id'],
    }
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(body),
        "isBase64Encoded": False
    }
