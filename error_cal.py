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
import pandas as pd
def error_cal(lat: str, lng: str, strSDate: str, strEDate: str, strOrgCd: str, pos_name: str, capacity: float) :
    measured = measure.measure(strSDate, strEDate, strOrgCd)
    predicted = predict.predict(lat, lng, pos_name, strOrgCd, strSDate, strEDate)
    error = measured.loc[strSDate:strEDate] - predicted.loc[strSDate:strEDate]
    abserror = abs(error)
    nmae = np.mean(abserror)/capacity
    nmae_hour = abserror.groupby(abserror.index.hour).mean()/capacity
    nmae_date = abserror.groupby(abserror.index.date).mean()/capacity
    
    df_nmae = pd.DataFrame(data=nmae)
    df_nmae_hour = pd.DataFrame(data=nmae_hour)
    df_nmae_date = pd.DataFrame(data=nmae_date)
    
    return df_nmae, df_nmae_hour, df_nmae_date


print(error_cal(37.4772, 126.6249, '2021-08-16', '2021-08-22', '876', 'Incheon', 200))
# print(error_cal(35.10468, 129.0323, '2021-08-16', '2021-08-22', '997N', 'Busan_1', 115)) 
# print(error_cal(35.10468, 129.0323, '2021-08-16', '2021-08-22', '997G', 'Busan_2', 187)) 
