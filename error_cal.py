import joblib
import matplotlib.pyplot as plt
import timeit

from sklearn.utils import shuffle
from solcast_frames.latlng import LatLng
from solcast_frames.radiationframehandler import RadiationFrameHandler
import pandas as pd
import numpy as np
import datetime
import measure
import predict

def error_cal(lat: str, lng: str, strSDate: str, strEDate: str, strOrgCd: str, pos_name: str) :
    measured = measure.measure(strSDate, strEDate, strOrgCd)
    predicted = predict.predict(lat, lng, pos_name, strOrgCd)
    print(measured.loc[strSDate:strEDate],predicted.loc[strSDate:strEDate] )
    error = measured.loc[strSDate:strEDate] - predicted.loc[strSDate:strEDate]
    abserror = abs(error)
    mae = np.mean(abserror)
    nmae = np.mean(abserror)/np.mean(measured.loc[strSDate:strEDate])
    nmae_hour = abserror.groupby(abserror.index.hour).mean()/measured.loc[strSDate:strEDate].groupby(measured.loc[strSDate:strEDate].index.hour).mean()
    nmae_date = abserror.groupby(abserror.index.date).mean()/measured.loc[strSDate:strEDate].groupby(measured.loc[strSDate:strEDate].index.date).mean()
    
    return mae, nmae, nmae_hour, nmae_date


print(error_cal(37.4772, 126.6249, '2021-08-14', '2021-08-20', '876', 'Incheon')) 