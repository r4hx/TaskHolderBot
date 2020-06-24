import json


def send(chat_id, text, last_message):
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
        'text': "{}\n\nПредыдущее сообщение: {}".format(text, last_message),
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


text = {
    'welcome': "Привет. Я трекер задач. Моя основная цель - победить твою прокрастинацию. \
            \n\nДавай составим список задач и посмотрим что из этого выйдет?",
    'task_add': "Что нужно сделать?",
    'task_list': "Это список наших задач, выполним что нибудь?",
    'task_delete': "Уже закончил?😀",
    'task_added': "Задача добавлена",
    'task_list_empty': "Список задач пуст",
    'not_response': "На ваш запрос у меня нет ответа"
}
