import joblib
import matplotlib.pyplot as plt
import timeit
from solcast_frames.latlng import LatLng
from solcast_frames.radiationframehandler import RadiationFrameHandler
import pandas as pd
from datetime import datetime, timedelta

def predict(lat: str, lng: str, location_name: str,strOrgCd: str, strSDate: str, strEDate: str):

    # present_time = datetime.now().date()
    # print(present_time)
    # quit()
    location = LatLng(lat=lat, lng=lng, name=location_name, tag="", timezone="Asia/Seoul")
    # print(location.desc())
    load = joblib.load('./xgboost_%s.pickle' % location_name)
    # load = joblib.load('./pickle_save/xgboost_%s.pickle' % pos_name)
    # load = joblib.load('./pickle_save_addtimeindex/xgboost_%s.pickle' % pos_name)
    radiation_estimated_actuals = RadiationFrameHandler.estimated_actuals(location,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI').sort_index(ascending=True).tz_convert('Asia/Seoul')
    fx_solcast_radiation = RadiationFrameHandler.forecast(location,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI').tz_convert('Asia/Seoul')
    
    radiation_location = pd.concat([radiation_estimated_actuals,fx_solcast_radiation], axis=0)
    
    radiation_location_resample = radiation_location.resample('1H',closed='right').sum()
    
    # radiation_location_resample.ghi.plot()
    # plt.show()
    radiation_location_resample['month'] = radiation_location_resample.index.month
    radiation_location_resample['day'] = radiation_location_resample.index.day
    radiation_location_resample['hour'] = radiation_location_resample.index.hour
    radiation_location_resample['dayofyear'] = radiation_location_resample.index.dayofyear
    radiation_location_resample_re =  radiation_location_resample
    # print(radiation_location_resample_re.index)
    time_delta1 = timedelta(days=1)
    time_delta2 = timedelta(days=4)
    # print(((pd.to_datetime(strSDate)+time_delta1).strftime('%Y-%m-%d %H:%M:%S')))
    # print(((pd.to_datetime(strEDate)+time_delta2).strftime('%Y-%m-%d %H:%M:%S')))
    pred = load.predict(radiation_location_resample_re[['ghi','ebh','dni','dhi','cloud_opacity','month','day','hour','dayofyear']].loc[(pd.to_datetime(strSDate)+time_delta1).strftime('%Y-%m-%d %H:%M:%S'):(pd.to_datetime(strEDate)+time_delta2).strftime('%Y-%m-%d %H:%M:%S')]).reshape(-1,1)
    # print(pred)
    # pred = load.predict(radiation_location_resample_re[['ghi','ebh','dni','dhi','cloud_opacity']].loc[pd.to_datetime(strSDate)+time_delta1:pd.to_datetime(strEDate)+time_delta2]).reshape(-1,1)
    
    df_pred = pd.DataFrame(data=abs(pred), index=radiation_location_resample_re.loc[(pd.to_datetime(strSDate)+time_delta1).strftime('%Y-%m-%d %H:%M:%S'):(pd.to_datetime(strEDate)+time_delta2).strftime('%Y-%m-%d %H:%M:%S')].index)
    df_pred.index.name = None
    df_pred.columns = ['gens']
    # print(df_pred)
    # df_pred.plot()
    # plt.show()
    # quit()
    df_pred.to_csv('df_pred_%s_%s.csv' % (strOrgCd,f"{datetime.now():%Y-%m-%d}"))
    
    return df_pred

# print(predict('37.4772', '126.6249', '신인천소내', '876', '2021-08-17', '2021-08-23'))
# print(predict('35.10468', '129.0323', '부산복합자재창고', '997N', '2021-08-17', '2021-08-23'))
# print(predict('35.10468', '129.0323', '부산신항', '997G', '2021-08-17', '2021-08-23'))
