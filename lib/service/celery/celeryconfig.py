from celery import Celery
from lib.service.predictor.predict_algh import create_prediction



celery_app = Celery(
    'predict_task',
    broker='redis://redis:6379/0', 
    backend='redis://redis:6379/0'
)

@celery_app.task
def predict_task(data, horizont, nCV):
    print("Predict Task called")
    prediction = create_prediction(data, horizont, nCV)
    return prediction