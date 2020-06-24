import json
import os
from yasdk import ObjectStorage
from messages import text, send


def handler(event, context):
    yc = ObjectStorage()
    data = json.loads(event["body"])
    json.dumps(data, indent=4, ensure_ascii=False)
    if data['message']['text'] == '/start':
        yc.upload(data['message']['from']['id'], os.getenv('INFO_FILENAME'), '')
        yc.upload(data['message']['from']['id'], os.getenv('INFO_FILENAME'), '')
        yc.update_user_info(data)
        return send(data['message']['from']['id'], text.get('welcome'), 'null')
    else:
        try:
            last_message = yc.get_user_info(data)['last_message']
        except KeyError:
            last_message = None
        finally:
            yc.update_user_info(data)
        if data['message']['text'] == 'Добавить задачу':
            return send(data['message']['from']['id'], text.get('task_add'), last_message)
        elif data['message']['text'] == 'Посмотреть список':
            task_list = yc.task_list(data)
            if task_list is None:
                return send(
                    data['message']['from']['id'],
                    text.get("task_list_empty"),
                    last_message,
                )
            else:
                return send(
                    data['message']['from']['id'],
                    "{} \n{}".format(text.get('task_list'), task_list),
                    last_message
                )
        elif data['message']['text'] == 'Удалить':
            return send(data['message']['from']['id'], text.get('task_delete'), last_message)
        else:
            if data['message']['text']:
                yc.task_add(data)
                return send(data['message']['from']['id'], text.get('task_added'), last_message)
            else:
                return send(data['message']['from']['id'], text.get('not_response'), last_message)
