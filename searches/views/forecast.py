import json
import pandas as pd

from django.http import JsonResponse


def forecast(request, **kwargs):
    from fbprophet import Prophet

    values = request.POST.getlist('values[]')
    timestamps = request.POST.getlist('timestamps[]')

    if not values or not timestamps:
        return JsonResponse(data={})

    df = pd.DataFrame([timestamps, values], index=['ds', 'y']).T
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    fc = m.predict(future)

    predicted_timestamps = fc['ds'].to_list()
    predicted_values = fc['yhat'].to_list()

    return JsonResponse(data={'timestamps': predicted_timestamps, 'values': predicted_values})
