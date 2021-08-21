from data_load import load_data
from model import model
import joblib
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

X_train2, y_train2, X_train3, y_train3, X_train4, y_train4, X_test2, y_test2, X_test3, y_test3, X_test4, y_test4 = load_data()
if __name__ == '__main__':
    start_time = time.time()
    model = model()
    print("model loaded", flush=True)
    
    fit_result_2 = model.fit(X_train2, y_train2)
    fit_result_3 = model.fit(X_train3, y_train3)
    fit_result_4 = model.fit(X_train4, y_train4)
    
    joblib.dump(fit_result_2, "xgboost_Incheon.pickle")
    joblib.dump(fit_result_3, "xgboost_Busan_1.pickle")
    joblib.dump(fit_result_4, "xgboost_Busan_2.pickle")
    
    
    load_2 = joblib.load('xgboost_Incheon.pickle')
    load_3 = joblib.load('xgboost_Busan_1.pickle')
    load_4 = joblib.load('xgboost_Busan_2.pickle')
    

    y_2_pred_xgb = load_2.predict(X_test2).reshape(-1,1)
    y_3_pred_xgb = load_3.predict(X_test3).reshape(-1,1)
    y_4_pred_xgb = load_4.predict(X_test4).reshape(-1,1)
    # y_2_pred_xgb = fit_result_2.predict(X_test2).reshape(-1,1)
    # y_3_pred_xgb = fit_result_3.predict(X_test3).reshape(-1,1)
    # y_4_pred_xgb = fit_result_4.predict(X_test4).reshape(-1,1)

    df_y_2_pred_xgb = pd.DataFrame(data=y_2_pred_xgb, index=y_test2.index, columns=y_test2.columns)
    df_y_3_pred_xgb = pd.DataFrame(data=y_3_pred_xgb, index=y_test3.index, columns=y_test3.columns)
    df_y_4_pred_xgb = pd.DataFrame(data=y_4_pred_xgb, index=y_test4.index, columns=y_test4.columns)

    error_xgb_2 = y_test2 - df_y_2_pred_xgb
    error_xgb_3 = y_test3 - df_y_3_pred_xgb
    error_xgb_4 = y_test4 - df_y_4_pred_xgb
    abserror_xgb_2 = abs(error_xgb_2)
    abserror_xgb_3 = abs(error_xgb_3)
    abserror_xgb_4 = abs(error_xgb_4)
    
    nmae_2 = np.mean(abserror_xgb_2)/np.mean(y_test2)
    nmae_3 = np.mean(abserror_xgb_3)/np.mean(y_test3)
    nmae_4 = np.mean(abserror_xgb_4)/np.mean(y_test4)
    
    print(abserror_xgb_2.groupby(abserror_xgb_2.index.hour).mean())
    print(abserror_xgb_3.groupby(abserror_xgb_3.index.hour).mean())
    print(abserror_xgb_4.groupby(abserror_xgb_4.index.hour).mean())
    # print(abserror_xgb_2.groupby(abserror_xgb_2.index.date).mean())
    # df_y_2_pred_xgb.plot()
    # y_test2.plot()
    # df_y_3_pred_xgb.loc['2019-01-01'].plot()
    # y_test3.loc['2019-01-01'].plot()
    # plt.show()
    # print("신인천소내 validation normailized MAE: %.5f" % nmae_2)
    # print("부산복합자재창고 validation normailized MAE: %.5f" % nmae_3)
    # print("부산신항 validation normailized MAE: %.5f" % nmae_4)
    # print("신인천소내 validation normailized MAE: %.5f", abserror_xgb_2.groupby(abserror_xgb_2.index.hour).mean()/y_test2.groupby(y_test2.index.hour).mean())
    # print("부산복합자재창고 validation normailized MAE: %.5f", np.mean(abserror_xgb_3)/np.mean(y_test3))
    # print("부산신항 validation normailized MAE: %.5f", np.mean(abserror_xgb_4)/np.mean(y_test4))
    
    
    
    print("Done.", flush=True)
    
