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
    if data['message']['text'] == '/start':
        yc.upload(data['message']['from']['id'], 'info.txt', '')
        yc.upload(data['message']['from']['id'], 'tasks.txt', '')
        return SendMessage(data['message']['from']['id'], messages['welcome'])
    else:
        last_message = yc.get_user_info(data).get('last_message', 0)
        yc.update_user_info(data)
        if data['message']['text'] == 'Добавить задачу':
            return SendMessage(data['message']['from']['id'], messages['task_add'])
        elif data['message']['text'] == 'Посмотреть список':
            return SendMessage(data['message']['from']['id'], messages['task_list'])
        elif data['message']['text'] == 'Удалить':
            return SendMessage(data['message']['from']['id'], messages['task_delete'])
        else:
            if last_message == 'Добавить задачу':
                yc.task_add(data)
                return SendMessage(data['message']['from']['id'], messages['task_added'])
            else:
                return SendMessage(data['message']['from']['id'], data['message']['text'])
