import json
from yasdk import ObjectStorage
from messages import messages


def SendMessage(chat_id, text):
    keyboard = {
        "keyboard":
            [
                ["Добавить задачу", "Посмотреть список"],
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
        return SendMessage(data['message']['from']['id'], messages['welcome'])
    elif data['message']['text'] == 'Добавить задачу':
        pass
    elif data['message']['text'] == 'Посмотреть список':
        pass
    elif data['message']['text'] == 'Удалить':
        pass
    else:
        return SendMessage(data['message']['from']['id'], data['message']['text'])
