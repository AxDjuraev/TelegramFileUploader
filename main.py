from fastapi import FastAPI
from settings import Settings
from uuid import uuid4
from asyncio import create_task, Task
from pydantic import BaseModel
from requests import post

app = FastAPI(debug=(not Settings.IS_PROD))
tasks_list = {}


class FileUploadingRequestBody(BaseModel):
    file_absolute_path: str
    user_id: int
    webhook: str = None


async def upload_file(file_path, chat_id, webhook = None):
    response = {}
    try:
        client = await Settings.get_client()
        res = await client.send_file(chat_id, file_path)
    except Exception as e:
        response['is_error'] = True
        response['error_message'] = str(e)
    else:
        response['res'] = res.to_json()
    finally:
        if webhook is not None:
            try:
                post(webhook, json=response)
            except Exception as e:
                print(e)
    return response


@app.post('/start_uploading')
async def start_uploading(request_body: FileUploadingRequestBody):
    task = create_task(
        upload_file(
            request_body.file_absolute_path,
            request_body.user_id,
            request_body.webhook
        )
    )

    if request_body.webhook is None:
        uid = str(uuid4())
        tasks_list[uid] = task
        return {
            'result': uid
        }

    return {
        'result': 'started'
    }


@app.get('/get_uploading_status/{task_id}')
async def get_uploading_status(task_id: str):
    task: Task = tasks_list.get(task_id)
    if not task:
        return {
            'result': 'NotFound'
        }
    response = {
        'result': {
            'is_done': task.done()
        }
    }

    if task.done():
        res = await task
        response['result'].update(res)

    return response


