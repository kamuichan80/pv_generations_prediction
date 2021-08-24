# coding: utf-8
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'sans-serif'
import pandas as pd
import numpy as np
import joblib
from pandas.core.indexes.datetimes import date_range
from time import time
from sklearn.model_selection import train_test_split

def load_data(location_name: str, enddate: str, missing: bool, lat: str, lng: str):
    data2 = pd.read_csv("./한국남부발전(주)_%s 태양광발전실적_%s.csv" % (location_name, enddate),encoding='CP949',index_col=0,parse_dates=True)
    data2 = data2.loc[:'2019']
    preprocessed_data2 = data2[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
    preprocessed_data2.columns = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    preprocessed_redata2 = preprocessed_data2[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
    if missing == True:
        preprocessed_redata2 = preprocessed_redata2.reindex(pd.date_range(start='2013-01-01', end='2020-01-01', closed='right'), fill_value=0)
    else:
        pass
    preprocessed_redata2_flat = preprocessed_redata2.stack(dropna=False)

    index_date =pd.date_range(start='2013-01-01 00:00:00', end='2020-01-01 00:00:00', closed='right', freq='H', tz='Asia/Seoul')

    df_pre2 = pd.DataFrame(data=preprocessed_redata2_flat.values, index=index_date)


    generations_data2 = df_pre2
    generations_data2 = generations_data2.fillna(0)

    df_generations_data2 = pd.DataFrame(data=generations_data2)

    generations_data_2 = df_generations_data2

    selected_gens_2 = generations_data_2

    weather_data_2 = pd.read_csv('%s_%s_Solcast_PT60M.csv' % ('37.4772','126.6249'), parse_dates=True, index_col='PeriodEnd')

    X_2 = weather_data_2.drop(columns=['AirTemp','Azimuth','DewpointTemp','WindSpeed10m','WindDirection10m', 'RelativeHumidity','PrecipitableWater','SnowWater','SurfacePressure', 'GtiFixedTilt','GtiTracking','Zenith', 'AlbedoDaily'])
    y_2 = pd.DataFrame(data=selected_gens_2, index=generations_data_2.index, columns=generations_data_2.columns)

    X_2_new = X_2
    X_2_new.index = X_2.index.tz_convert(tz='Asia/Seoul') # forecast
    X_2_new = X_2_new.drop(['PeriodStart', 'Period'], axis=1) # forecast
    X_2_new = X_2_new.loc['2013-01-01 01:00:00+09:00':'2020-01-01 00:00:00+09:00']
    y_2_new = y_2

    X_2_new['month'] = X_2_new.index.month
    X_2_new['day'] = X_2_new.index.day
    X_2_new['hour'] = X_2_new.index.hour
    X_2_new['dayofyear'] = X_2_new.index.dayofyear

    X_2_new.loc['2016-03':'2016-12']['dayofyear'] =  X_2_new.loc['2016-03':'2016-12']['dayofyear'] - 1

    dropThis2016 = pd.date_range(start='2016-02-29 00:00:00+09:00', end='2016-02-29 23:00+09:00', freq='H')
    X_2_renew = X_2_new.drop(dropThis2016)
    y_2_renew = y_2_new.drop(dropThis2016)
    X_2_selected = X_2_renew
    y_2_selected = y_2_renew

    X_train2, X_test2, y_train2, y_test2 = train_test_split(X_2_selected, y_2_selected, test_size=0.14285714285714285714, shuffle=False)

    # X_train2 = np.ascontiguousarray(X_train2)
    # y_train2 = np.ascontiguousarray(y_train2)
    return X_train2, y_train2, X_test2, y_test2

if __name__ == '__main__':
    start_time = time()
    print("Data loaded start", flush=True)
    print("Data loaded done.", flush=True)
    
# print(load_data('신인천소내','20200820',True,'37.4772','126.6249'))
# print(load_data('부산복합자재창고','20200924',False,'35.10468','129.0323'))
# print(load_data('부산신항','20200820',False,'35.10468','129.0323'))