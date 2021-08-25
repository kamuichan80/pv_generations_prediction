import numpy as np
import datetime
import measure
import predict
import error_cal
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'AppleGothic'
import pandas as pd
from datetime import datetime,timedelta
import seaborn as sns
def test(strOrgCd : str, pred_strSDate: str, meas_strSDate: str, pred_strEDate: str, meas_strEDate: str, location_name: str, capacity: float, lat: str, lng: str):
    time_delta = timedelta(days=1)
    df_measure = measure.measure(meas_strSDate, meas_strEDate, strOrgCd)
    df_predict = predict.predict(lat, lng, location_name, strOrgCd, pred_strSDate, pred_strEDate)
    # df_measure = pd.read_csv('result_1/df_gens_876_2021-08-23.csv', index_col=0, parse_dates=True)
    # df_predict = pd.read_csv('result_1/df_pred_876_2021-08-23.csv', index_col=0, parse_dates=True)
    # df_measure = pd.read_csv('result_1/df_gens_%s_%s.csv' % (strOrgCd,(pd.to_datetime(meas_strEDate)+time_delta).strftime('%Y-%m-%d')), index_col=0, parse_dates=True)
    # df_predict = pd.read_csv('result_1/df_pred_%s_%s.csv' % (strOrgCd,(pd.to_datetime(meas_strEDate)+time_delta).strftime('%Y-%m-%d')), index_col=0, parse_dates=True)
    # print(df_measure, df_predict)
    err_cal = error_cal.error_cal(lat, lng, pred_strSDate, pred_strEDate, strOrgCd, location_name, capacity)
    plt.figure(figsize=(15,5))
    plt.plot(df_measure.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].index, df_measure.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].values, df_predict.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].index, df_predict.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].values)
    plt.title('%s의 태양광 발전량' % location_name)
    plt.legend(['실제발전량','예측발전량'])
    err_cal[2].plot.bar()
    plt.title('%s의 시간당 태양광 평균발전량 에러' % location_name)
    plt.legend(['시간당 평균발전량 에러'])
    # plt.figure(figsize=(5,5))
    err_cal[3].index = err_cal[3].index.date
    err_cal[3]
    err_cal_day = pd.concat([err_cal[3],err_cal[4]], axis=1)
    err_cal_day.plot.bar(color=['red','blue'],stacked=False)
    plt.title('%s의 일당 발전량 에러' % location_name)
    plt.legend(['하루 총발전량 에러','하루 평균발전량 에러'])
    # print(err_cal_day)
    plt.show()
    
    # print("총 조회시간 내의 설치용량 대 평균절대오차", err_cal_876[0])
    # print("총 조회시간 내의 설치용량 대 시간당 평균절대오차", err_cal_876[1])
    # print("총 조회시간 내의 설치용량 대 일당 평균절대오차", err_cal_876[2])
if __name__ == '__main__':
    test('876', '2021-08-19', '20210819', '2021-08-25', '20210825', '신인천소내', 200, '37.4772', '126.6249')
    test('997N', '2021-08-19', '20210819', '2021-08-25', '20210825', '부산복합자재창고', 115, '35.10468', '129.0323')
    test('997G', '2021-08-19', '20210819', '2021-08-25', '20210825', '부산신항', 187, '35.10468', '129.0323')
