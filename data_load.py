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

def load_data():
    data2 = pd.read_csv("./한국남부발전(주)_신인천소내 태양광발전실적_20200820.csv",encoding='CP949',index_col=0,parse_dates=True)
    data2 = data2.loc[:'2019']
    preprocessed_data2 = data2[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
    preprocessed_data2.columns = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    preprocessed_redata2 = preprocessed_data2[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
    preprocessed_redata2 = preprocessed_redata2.reindex(pd.date_range(start='2013-01-01', end='2019-12-31'), fill_value=0)
    preprocessed_redata2.loc['2016-05-04'] = preprocessed_redata2.loc['2016-05-03'].values
    preprocessed_redata2.loc['2016-06-01'] = preprocessed_redata2.loc['2016-06-02'].values

    data3 = pd.read_csv("./한국남부발전(주)_부산복합자재창고 태양광발전실적_20200924.csv",encoding='CP949',index_col=0,parse_dates=True)
    data3_1 = data3[data3['호기'] == 1]
    data3_1 = data3_1.loc[:'2019']
    preprocessed_data3_1 = data3_1[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
    preprocessed_data3_1.columns = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    preprocessed_redata3_1 = preprocessed_data3_1[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]

    data4 = pd.read_csv("./한국남부발전(주)_부산신항 태양광발전실적_20200820.csv",encoding='CP949',index_col=0,parse_dates=True)
    data4 = data4.loc[:'2019']
    preprocessed_data4 = data4[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
    preprocessed_data4.columns = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    preprocessed_redata4 = preprocessed_data4[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]

    preprocessed_redata2_flat = preprocessed_redata2.stack(dropna=False)
    preprocessed_redata3_1_flat = preprocessed_redata3_1.stack(dropna=False)
    preprocessed_redata4_flat = preprocessed_redata4.stack(dropna=False)

    index_date =pd.date_range(start='2013-01-01 00:00:00', end='2020-01-01 00:00:00', closed='right', freq='H', tz='Asia/Seoul')

    df_pre2 = pd.DataFrame(data=preprocessed_redata2_flat.values, index=index_date)

    df_pre3_1 = pd.DataFrame(data=preprocessed_redata3_1_flat.values, index=index_date)

    df_pre4 = pd.DataFrame(data=preprocessed_redata4_flat.values, index=index_date)

    generations_data2 = df_pre2
    generations_data2 = generations_data2.fillna(0)

    generations_data3 = df_pre3_1
    generations_data3 = generations_data3.fillna(0)

    generations_data4 = df_pre4
    generations_data4 = generations_data4.fillna(0)

    df_generations_data2 = pd.DataFrame(data=generations_data2)
    df_generations_data3 = pd.DataFrame(data=generations_data3)
    df_generations_data4 = pd.DataFrame(data=generations_data4)

    generations_data_2 = df_generations_data2
    generations_data_3 = df_generations_data3
    generations_data_4 = df_generations_data4

    selected_gens_2 = generations_data_2
    selected_gens_3 = generations_data_3
    selected_gens_4 = generations_data_4

    weather_data_2 = pd.read_csv('37.4772_126.6249_Solcast_PT60M.csv', parse_dates=True, index_col='PeriodEnd')
    weather_data_3 = pd.read_csv('35.10468_129.0323_Solcast_PT60M.csv', parse_dates=True, index_col='PeriodEnd')
    weather_data_4 = pd.read_csv('35.10468_129.0323_Solcast_PT60M.csv', parse_dates=True, index_col='PeriodEnd')

    X_2 = weather_data_2.drop(columns=['AirTemp','Azimuth','DewpointTemp','WindSpeed10m','WindDirection10m', 'RelativeHumidity','PrecipitableWater','SnowWater','SurfacePressure', 'GtiFixedTilt','GtiTracking','Zenith', 'AlbedoDaily'])
    y_2 = pd.DataFrame(data=selected_gens_2, index=generations_data_2.index, columns=generations_data_2.columns)
    X_3 = weather_data_3.drop(columns=['AirTemp','Azimuth','DewpointTemp','WindSpeed10m','WindDirection10m', 'RelativeHumidity','PrecipitableWater','SnowWater','SurfacePressure', 'GtiFixedTilt','GtiTracking','Zenith', 'AlbedoDaily'])
    y_3 = pd.DataFrame(data=selected_gens_3, index=generations_data_3.index, columns=generations_data_3.columns)
    X_4 = weather_data_4.drop(columns=['AirTemp','Azimuth','DewpointTemp','WindSpeed10m','WindDirection10m', 'RelativeHumidity','PrecipitableWater','SnowWater','SurfacePressure', 'GtiFixedTilt','GtiTracking','Zenith', 'AlbedoDaily'])
    y_4 = pd.DataFrame(data=selected_gens_4, index=generations_data_4.index, columns=generations_data_4.columns)

    X_2_new = X_2
    X_2_new.index = X_2.index.tz_convert(tz='Asia/Seoul') # forecast
    X_2_new = X_2_new.drop(['PeriodStart', 'Period'], axis=1) # forecast
    X_2_new = X_2_new.loc['2013-01-01 01:00:00+09:00':'2020-01-01 00:00:00+09:00']
    y_2_new = y_2
    X_3_new = X_3
    X_3_new.index = X_3.index.tz_convert(tz='Asia/Seoul') # forecast
    X_3_new = X_3_new.drop(['PeriodStart', 'Period'], axis=1) # forecast
    X_3_new = X_3_new.loc['2013-01-01 01:00:00+09:00':'2020-01-01 00:00:00+09:00']
    y_3_new = y_3
    X_4_new = X_4
    X_4_new.index = X_4.index.tz_convert(tz='Asia/Seoul') # forecast
    X_4_new = X_4_new.drop(['PeriodStart', 'Period'], axis=1) # forecast
    X_4_new = X_4_new.loc['2013-01-01 01:00:00+09:00':'2020-01-01 00:00:00+09:00']
    y_4_new = y_4

    # X_2_new['month'] = X_2_new.index.month
    # X_2_new['day'] = X_2_new.index.day
    # X_2_new['hour'] = X_2_new.index.hour
    # X_2_new['dayofyear'] = X_2_new.index.dayofyear
    # X_3_new['month'] = X_3_new.index.month
    # X_3_new['day'] = X_3_new.index.day
    # X_3_new['hour'] = X_3_new.index.hour
    # X_3_new['dayofyear'] = X_3_new.index.dayofyear
    # X_4_new['month'] = X_4_new.index.month
    # X_4_new['day'] = X_4_new.index.day
    # X_4_new['hour'] = X_4_new.index.hour
    # X_4_new['dayofyear'] = X_4_new.index.dayofyear

    # X_2_new.loc['2016-03':'2016-12']['dayofyear'] =  X_2_new.loc['2016-03':'2016-12']['dayofyear'] - 1
    # X_3_new.loc['2016-03':'2016-12']['dayofyear'] =  X_3_new.loc['2016-03':'2016-12']['dayofyear'] - 1
    # X_4_new.loc['2016-03':'2016-12']['dayofyear'] =  X_4_new.loc['2016-03':'2016-12']['dayofyear'] - 1

    dropThis2016 = pd.date_range(start='2016-02-29 00:00:00+09:00', end='2016-02-29 23:00+09:00', freq='H')
    X_2_renew = X_2_new.drop(dropThis2016)
    y_2_renew = y_2_new.drop(dropThis2016)
    X_2_selected = X_2_renew
    y_2_selected = y_2_renew
    X_3_renew = X_3_new.drop(dropThis2016)
    y_3_renew = y_3_new.drop(dropThis2016)
    X_3_selected = X_3_renew
    y_3_selected = y_3_renew
    X_4_renew = X_4_new.drop(dropThis2016)
    y_4_renew = y_4_new.drop(dropThis2016)
    X_4_selected = X_4_renew
    y_4_selected = y_4_renew

    X_train2, X_test2, y_train2, y_test2 = train_test_split(X_2_selected, y_2_selected, test_size=0.14285714285714285714, shuffle=False)
    X_train3, X_test3, y_train3, y_test3 = train_test_split(X_3_selected, y_3_selected, test_size=0.14285714285714285714, shuffle=False)
    X_train4, X_test4, y_train4, y_test4 = train_test_split(X_4_selected, y_4_selected, test_size=0.14285714285714285714, shuffle=False)

    # X_train2 = np.ascontiguousarray(X_train2)
    # y_train2 = np.ascontiguousarray(y_train2)
    # X_train3 = np.ascontiguousarray(X_train3)
    # y_train3 = np.ascontiguousarray(y_train3)
    # X_train4 = np.ascontiguousarray(X_train4)
    # y_train4 = np.ascontiguousarray(y_train4)
    return X_train2, y_train2, X_train3, y_train3, X_train4, y_train4, X_test2, y_test2, X_test3, y_test3, X_test4, y_test4

if __name__ == '__main__':
    start_time = time()
    print("Data loaded start", flush=True)
    load_data()
    print("Data loaded done.", flush=True)