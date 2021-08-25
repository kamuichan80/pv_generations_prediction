import joblib
import matplotlib.pyplot as plt
import timeit

from sklearn.utils import shuffle
from solcast_frames.latlng import LatLng
from solcast_frames.radiationframehandler import RadiationFrameHandler
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import measure
import predict
import pandas as pd
def error_cal(lat: str, lng: str, strSDate: str, strEDate: str, strOrgCd: str, pos_name: str, capacity: float) :
    time_delta = timedelta(days=1)
    measured = measure.measure(strSDate, strEDate, strOrgCd)
    predicted = predict.predict(lat, lng, pos_name, strOrgCd, strSDate, strEDate)
    # measured = pd.read_csv('result_1/df_gens_%s_%s.csv' % (strOrgCd, (pd.to_datetime(strEDate)+time_delta).strftime('%Y-%m-%d')), index_col=0, parse_dates=True)
    # predicted = pd.read_csv('result_1/df_pred_%s_%s.csv' % (strOrgCd, (pd.to_datetime(strEDate)+time_delta).strftime('%Y-%m-%d')), index_col=0, parse_dates=True)
    # print(measured.index, predicted.index)
    error = measured.loc[(pd.to_datetime(strSDate)+time_delta).strftime('%Y-%m-%d %H:%M:%S'):strEDate] - predicted.loc[(pd.to_datetime(strSDate)+time_delta).strftime('%Y-%m-%d %H:%M:%S'):strEDate]
    abserror = abs(error)
    abserror_6h = abserror.resample('6H').sum()
    abserror_1day = abserror.resample('D').sum()
    nmae = np.mean(abserror)/capacity
    nmae_6h = abserror_6h/capacity
    nmae_1d = abserror_1day/capacity
    
    nmae_hour = abserror.groupby(abserror.index.hour).mean()/capacity
    nmae_date = abserror.groupby(abserror.index.date).mean()/capacity
    
    df_nmae = pd.DataFrame(data=nmae)
    df_nmae_6h = pd.DataFrame(data=nmae_6h)
    df_nmae_1d = pd.DataFrame(data=nmae_1d)
    df_nmae_hour = pd.DataFrame(data=nmae_hour)
    df_nmae_date = pd.DataFrame(data=nmae_date)
    
    return df_nmae, df_nmae_6h, df_nmae_hour, df_nmae_1d, df_nmae_date


# print(error_cal(37.4772, 126.6249, '2021-08-16', '2021-08-22', '876', '신인천소내', 200))
# print(error_cal(35.10468, 129.0323, '2021-08-17', '2021-08-23', '997N', '부산복합자재창고',, 115)) 
# print(error_cal(35.10468, 129.0323, '2021-08-17', '2021-08-23', '997G', '부산신항', 187)) 
