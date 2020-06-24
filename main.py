import json
import os
from yasdk import User, Task
from messages import text, send

user = User()
task = Task()


def handler(event, context):
    data = json.loads(event["body"])
    json.dumps(data, indent=4, ensure_ascii=False)
    from_id = data['message']['from']['id']
    if data['message']['text'] == '/start':
        user.upload(from_id, os.getenv('INFO_FILENAME'), '')
        user.upload(from_id, os.getenv('TASK_FILENAME'), '')
        user.update_info(data)
        return send(from_id, text.get('welcome'), 'null')
    else:
        try:
            last_message = user.get_info(data)['last_message']
        except KeyError:
            last_message = None
        finally:
            user.update_info(data)
        if data['message']['text'] == 'Добавить задачу':
            return send(from_id, text.get('task_add'), last_message)
        elif data['message']['text'] == 'Посмотреть список':
            task_list = task.all(data)
            if task_list is None:
                return send(
                    from_id,
                    text.get("task_list_empty"),
                    last_message,
                )
            else:
                return send(
                    from_id,
                    "{} \n{}".format(text.get('task_list'), task_list),
                    last_message
                )
        elif data['message']['text'] == 'Удалить':
            return send(from_id, text.get('task_delete'), last_message)
        else:
            if data['message']['text']:
                task.add(data)
                return send(from_id, text.get('task_added'), last_message)
            else:
                return send(from_id, text.get('not_response'), last_message)
