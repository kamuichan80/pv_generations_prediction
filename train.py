from data_load import load_data
from model import model
import joblib
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

def train(location_name: str, enddate: str, missing: bool, lat: str, lng: str, capacity: float):
    X_train2, y_train2, X_test2, y_test2 = load_data(location_name, enddate, missing, lat, lng)
    # start_time = time.time()
    model_xgb = model()
    print("model loaded", flush=True)
    
    fit_result_2 = model_xgb.fit(X_train2, y_train2)
    
    print(fit_result_2)
    joblib.dump(fit_result_2, "xgboost_%s.pickle" % location_name)
    
    load_2 = joblib.load('xgboost_%s.pickle' % location_name)
    

    y_2_pred_xgb = load_2.predict(X_test2).reshape(-1,1)

    df_y_2_pred_xgb = pd.DataFrame(data=y_2_pred_xgb, index=y_test2.index, columns=y_test2.columns)

    error_xgb_2 = y_test2 - df_y_2_pred_xgb
    abserror_xgb_2 = abs(error_xgb_2)
    
    capacity_2 = capacity
    
    nmae_2 = np.mean(abserror_xgb_2)/capacity_2
    nmae_2_hour = np.mean((abserror_xgb_2.groupby(abserror_xgb_2.index.hour).mean()/capacity_2))
    nmae_2_date = np.mean((abserror_xgb_2.groupby(abserror_xgb_2.index.date).mean()/capacity_2))
    
    print("%s validation MAE per capacity: %.5f" % (location_name,nmae_2))
    print("%s validation MAE per capacity by hour: %.5f" % (location_name,nmae_2_hour))
    print("%s validation MAE per capacity by date: %.5f" % (location_name,nmae_2_date))
    print("Done.", flush=True)
    
print(train('신인천소내','20200820',True,'37.4772','126.6249', 200))
print(train('부산복합자재창고','20200924',False,'35.10468','129.0323', 115))
print(train('부산신항','20200820',False,'35.10468','129.0332', 187))
