import joblib
import matplotlib.pyplot as plt
import timeit
from solcast_frames.latlng import LatLng
from solcast_frames.radiationframehandler import RadiationFrameHandler
import pandas as pd
import datetime

location1 = LatLng(lat=37.4772, lng=126.6249, name="Incheon", tag="", timezone="Asia/Seoul")
location2 = LatLng(lat=35.10468, lng=129.0323, name="Busan", tag="", timezone="Asia/Seoul")
print(location1.desc())
print(location2.desc())
if __name__ == '__main__':
    load_2 = joblib.load('xgboost_2.pickle')
    load_3 = joblib.load('xgboost_3.pickle')
    load_4 = joblib.load('xgboost_4.pickle')
    radiation_estimated_actuals1 = RadiationFrameHandler.estimated_actuals(location1,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI')
    radiation_estimated_actuals2 = RadiationFrameHandler.estimated_actuals(location2,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI')
    fx_solcast_radiation1 = RadiationFrameHandler.forecast(location1,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI')
    fx_solcast_radiation2 = RadiationFrameHandler.forecast(location2,api_key = 'NxDhssBnedzmAcBBG0z54OfuzbVhZzKI')

    radiation_location_1 = pd.concat([radiation_estimated_actuals1,fx_solcast_radiation1], axis=0)
    radiation_location_2 = pd.concat([radiation_estimated_actuals2,fx_solcast_radiation2], axis=0)
    
    radiation_location_1_resample = radiation_location_1.resample('1H').sum()
    radiation_location_2_resample = radiation_location_2.resample('1H').sum()
    
    # radiation_location_1_resample['month'] = radiation_location_1_resample.index.month
    # radiation_location_1_resample['day'] = radiation_location_1_resample.index.day
    # radiation_location_1_resample['hour'] = radiation_location_1_resample.index.hour
    # radiation_location_1_resample['dayofyear'] = radiation_location_1_resample.index.dayofyear
    
    
    #radiation_location_1.ghi.plot()
    #radiation_location_2.ghi.plot()
    pred_2 = load_2.predict(radiation_location_1_resample[['ghi','ebh','dni','dhi','air_temp','zenith','azimuth','cloud_opacity']]).reshape(-1,1)
    pred_3 = load_3.predict(radiation_location_2_resample[['ghi','ebh','dni','dhi','air_temp','zenith','azimuth','cloud_opacity']]).reshape(-1,1)
    pred_4 = load_4.predict(radiation_location_2_resample[['ghi','ebh','dni','dhi','air_temp','zenith','azimuth','cloud_opacity']]).reshape(-1,1)
    
    df_pred_2 = pd.DataFrame(data=pred_2, index=radiation_location_1_resample.index)
    df_pred_3 = pd.DataFrame(data=pred_3, index=radiation_location_2_resample.index)
    df_pred_4 = pd.DataFrame(data=pred_4, index=radiation_location_2_resample.index)
    plt.figure(1)
    plt.subplot(311)        
    df_pred_2.plot()
    plt.subplot(312)
    df_pred_3.plot()
    plt.subplot(313)
    df_pred_4.plot()
    plt.show()
    df_pred_2.to_csv('df_pred_2_%s.csv' % f"{datetime.datetime.now():%Y-%m-%d}")
    df_pred_2.to_csv('df_pred_3_%s.csv' % f"{datetime.datetime.now():%Y-%m-%d}")
    df_pred_2.to_csv('df_pred_4_%s.csv' % f"{datetime.datetime.now():%Y-%m-%d}")
