import json


def handler(event, context):
    print(event)
    if 'queryStringParameters' in event and 'name' in event['queryStringParameters']:
        name = event['queryStringParameters']['name']
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/plain'
            },
            "body": name,
            "isBase64Encoded": True,
        }
    else:
        data = json.loads(event["body"])
        body = {
            'method': 'sendMessage',
            'text': data['message']['text'],
            'chat_id': data['message']['chat']['id'],
        }
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/plain'
            },
            "body": json.dumps(body),
            "isBase64Encoded": True,
        }
