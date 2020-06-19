import json
from yasdk import ObjectStorage


def SendMessage(chat_id, text):
    keyboard = {
        "keyboard":
            [
                ["Добавить", "Посмотреть"],
                ["Удалить"],
            ],
        "one_time_keyboard": True
    }
    body = {
        'method': 'sendMessage',
        'text': text,
        'chat_id': chat_id,
        'reply_markup': json.dumps(keyboard),
    }
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json'
        },
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }


def handler(event, context):
    yc = ObjectStorage()
    data = json.loads(event["body"])
    yc.update_user_info(data)
    print(data)
    if data['message']['text'] == '/start':
        return SendMessage(data['message']['from']['id'], 'Здарова ёпта 😀')
    else:
        return SendMessage(data['message']['from']['id'], data['message']['text'])
