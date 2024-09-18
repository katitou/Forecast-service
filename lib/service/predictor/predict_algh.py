import pickle
import joblib
import numpy as np 
import pandas as pd 


def load_model(path='lib/service/predictor/naive_model.pkl'):
    model = joblib.load(path)
    return model


def create_prediction(data, horizont, nCV):
    df = pd.DataFrame(data['series'])
    df.rename(columns={'date': 'ds', 'value': 'y'},  inplace=True)
    df['unique_id'] = 'series_1'

    model = load_model()
    current_df = df.copy()
    forecasts = []
    map_values = []

    for i in range (nCV):
        forecast_df = model.forecast(df = current_df, h=horizont)
        forecast_df = forecast_df.astype({'Naive': 'float'})

        # данные для рассчета mape
        actual = df['y'].tail(horizont).tolist()
        predict = forecast_df['Naive'].head(horizont).tolist()

        mape = np.mean(np.abs((np.array(actual) - np.array(predict)) / np.array(actual))) * 100
        map_values.append(mape)
        
        # добавление новых прдсказаний в итоговый df
        for j in range(horizont):
            forecasts.append({
                'date': forecast_df['ds'].iloc[j].strftime('%Y-%m-%d'),
                'value': float(forecast_df['Naive'].iloc[j])
            })

        # df исключительно из новых точек 
        horizont_data = {
            'ds': forecast_df['ds'],
            'y': forecast_df['Naive'].astype(float),
            'unique_id': ['series_1'] * horizont
        }

        horizont_df = pd.DataFrame(horizont_data)

        # слияние: исходный + новые точки 
        current_df = pd.concat([current_df, horizont_df]).reset_index(drop=True)

    avg_mape = np.mean(map_values)

    return {
        'prediction': forecasts,
        'accuracy': {
            'kind': 'MAPE',
            'value': avg_mape
        }
    }

