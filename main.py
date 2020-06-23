import json
from yasdk import ObjectStorage
from messages import messages


def SendMessage(chat_id, text, last_message):
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
        'text': "{}\n\nПоследнее сообщение: {}".format(text, last_message),
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
        yc.update_user_info(data)
        return SendMessage(data['message']['from']['id'], messages.get('welcome'), 'null')
    else:
        try:
            last_message = yc.get_user_info(data)['last_message']
        except KeyError:
            last_message = None
        finally:
            yc.update_user_info(data)
        if data['message']['text'] == 'Добавить задачу':
            return SendMessage(data['message']['from']['id'], messages.get('task_add'), last_message)
        elif data['message']['text'] == 'Посмотреть список':
            task_list = yc.task_list(data)
            if task_list is None:
                return SendMessage(
                    data['message']['from']['id'],
                    messages.get("task_list_empty"),
                    last_message,
                )
            else:
                return SendMessage(
                    data['message']['from']['id'],
                    "{} \n{}".format(messages.get('task_list'), task_list),
                    last_message
                )
        elif data['message']['text'] == 'Удалить':
            return SendMessage(data['message']['from']['id'], messages.get('task_delete'), last_message)
        else:
            yc.task_add(data)
            return SendMessage(data['message']['from']['id'], messages.get('task_added'), last_message)
