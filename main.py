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
    last_message = yc.get_user_info(data).get('last_message')
    print(last_message)
    print(type(last_message))
    yc.update_user_info(data)
    print(data)
    if data['message']['text'] == '/start':
        return SendMessage(data['message']['from']['id'], messages['welcome'])
    elif data['message']['text'] == 'Добавить задачу':
        return SendMessage(data['message']['from']['id'], messages['task_add'])
    elif data['message']['text'] == 'Посмотреть список':
        return SendMessage(data['message']['from']['id'], messages['task_list'])
    elif data['message']['text'] == 'Удалить':
        return SendMessage(data['message']['from']['id'], messages['task_delete'])
    else:
        if last_message == 'Добавить задачу':
            pass
        else:
            return SendMessage(data['message']['from']['id'], data['message']['text'])
