from fastapi import FastAPI, Request
from lib.service.celery.celeryconfig import predict_task, celery_app
from celery.result import AsyncResult
from pydantic import BaseModel
from typing import List


class Series(BaseModel):
    date: str
    value: int

class RequestModel(BaseModel):
    series: List[Series]

app = FastAPI()


@app.post("/create_predict")
async def create_predict(horizont: int, body: RequestModel, request: Request, nCV: int=1):
    task = predict_task.delay(body.dict(), horizont, nCV)

    return {"predictID": task.id}


@app.get("/get_result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    task_result.get()

    if task_result == "PENDING":
        return {"status": "PENDING", "result": None}
    elif task_result.state == 'FAILURE':
        return {"status": task_result.state, "result": str(task_result.info)}
    else:
        return {"status": task_result.state, "result": task_result.result}
