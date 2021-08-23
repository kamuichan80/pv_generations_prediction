import joblib
import matplotlib.pyplot as plt
import timeit
from solcast_frames.latlng import LatLng
from solcast_frames.radiationframehandler import RadiationFrameHandler
import pandas as pd
from datetime import datetime

def predict(lat: float, lng: float, pos_name: str,strOrgCd: str):

    present_time = datetime.now().date()
    # print(present_time)
    # quit()
    location = LatLng(lat=lat, lng=lng, name=pos_name, tag="", timezone="Asia/Seoul")
    # print(location.desc())
    load = joblib.load('xgboost_%s.pickle' % pos_name)
    radiation_estimated_actuals = RadiationFrameHandler.estimated_actuals(location,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI').sort_index(ascending=True).tz_convert('Asia/Seoul')
    fx_solcast_radiation = RadiationFrameHandler.forecast(location,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI').tz_convert('Asia/Seoul')
    
    radiation_location = pd.concat([radiation_estimated_actuals,fx_solcast_radiation], axis=0)
    
    radiation_location_resample = radiation_location.resample('1H',closed='right').sum()
    
    # radiation_location_1_resample['month'] = radiation_location_1_resample.index.month
    # radiation_location_1_resample['day'] = radiation_location_1_resample.index.day
    # radiation_location_1_resample['hour'] = radiation_location_1_resample.index.hour
    # radiation_location_1_resample['dayofyear'] = radiation_location_1_resample.index.dayofyear
    
    pred = load.predict(radiation_location_resample[['ghi','ebh','dni','dhi','cloud_opacity']]).reshape(-1,1)
    
    df_pred = pd.DataFrame(data=pred, index=radiation_location_resample.index)
    df_pred.index.name = None
    df_pred.columns = ['gens']
    df_pred.to_csv('df_pred_%s_%s.csv' % (strOrgCd,f"{datetime.now():%Y-%m-%d}"))
    
    return df_pred

print(predict(37.4772, 126.6249, 'Incheon', '876'))
print(predict(35.10468, 129.0323, 'Busan_1', '997N'))
print(predict(35.10468, 129.0323, 'Busan_2', '997G'))