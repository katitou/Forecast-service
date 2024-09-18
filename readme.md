# Forecast Service

## Обзор проекта

**Forecast Service** предназначен для создания прогнозов для заданного временного ряда с использованием [Naive forecasting method](https://otexts.com/fpp2/simple-methods.html). Оценка точности прогнозов определяется средней абсолютной процентной ошибки [MAPE](https://en.wikipedia.org/wiki/Mean_absolute_percentage_error). 



## Работа сервиса
- FastAPI - предоставляет API для взаимодействия с сервисом
- Celery - управляет асинхронной обработкой задач для создания прогнозов
- Redis - брокер для celery


## Запуск сервиса

### Сборка контейнеров

Для создания и запуска всех сервисов:

```sh
docker-compose up --build
```

### FastAPI-Swagger UI

```
http://0.0.0.0:8000/docs
```


## 1. Create Prediction

Инициирует задачу прогнозирования для заданных данных временного ряда.
```
POST /create_predict
```

**Параметры запроса**:
- `horizont (int)`: количество точек прогноза;
- `nCV (int)`: количество окон - сколько раз необходимо построить прогноз с заданным горизонтом в прошлом.




### Request Body
```json
{
  "series": [
    {"date": "2022-10-01", "value": 100},
    {"date": "2022-10-02", "value": 110},
    {"date": "2022-10-03", "value": 105},
    {"date": "2022-10-04", "value": 101}
  ]
}

```
### Response Body
- `predictID` - *id* для получения результатов прогноза.

```json
{
  "result": {
    "predictID": "5e6b467c-e385-47eb-b541-18e4376a01c7"
  }
}
```




## 2. Get Result

Получает результат прогноза по предоставленному *predictID*.

```
GET /get_result/{task_id}
```


**Параметры запроса**:
- `task_id (string)`: *ID* задачи прогнозирования.

### Response Body

```json
{
  "status": "SUCCESS",
  "result": {
    "prediction": [
      {
        "date": "2022-10-05",
        "value": 101
      },
      {
        "date": "2022-10-06",
        "value": 101
      }
    ],
    "accuracy": {
      "kind": "MAPE",
      "value": 1.9047619047619049
    }
  }
}
```
