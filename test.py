import numpy as np
import datetime
import measure
import predict
import error_cal
import matplotlib.pyplot as plt
import pandas as pd
if __name__ == '__main__':
    df_measure_876 = measure.measure('20210816', '20210820', '876')
    df_predict_876 = predict.predict(37.4772, 126.6249, 'Incheon', '876', '2021-08-16', '2021-08-20')
    # df_measure_997N = measure.measure('20210816', '20210820', '997N')
    # df_predict_997N = predict.predict(35.10468, 129.0323, 'Busan_1', '997N',  '2021-08-16', '2021-08-20')
    # df_measure_997G = measure.measure('20210816', '20210820', '997G')
    # df_predict_997G = predict.predict(35.10468, 129.0323, 'Busan_2', '997G',  '2021-08-16', '2021-08-20')
    
    plt.figure(1)
    ax_876 = df_predict_876.plot()
    df_measure_876.plot(ax=ax_876)
    # ax_997N = df_predict_997N.plot()
    # df_measure_997N.plot(ax=ax_997N)
    # ax_997G = df_predict_997G.plot(label='gens(predict)')
    # df_measure_997G.plot(ax=ax_997G,label='gens(measure)')
    # plt.legend()
    
    err_cal_876 = error_cal.error_cal(37.4772, 126.6249, '2021-08-16', '2021-08-22', '876', 'Incheon', 200)
    # err_cal_997N = error_cal.error_cal(35.10468, 129.0323, '2021-08-16', '2021-08-22', '997N', 'Busan_1', 115)
    # err_cal_997G = error_cal.error_cal(35.10468, 129.0323, '2021-08-16', '2021-08-22', '997G', 'Busan_2', 187)
    plt.figure(2)
    err_cal_876[1].plot.bar()
    plt.figure(3)
    err_cal_876[2].plot.bar()
    plt.show()
    
    print("총 조회시간 내의 설치용량 대 평균절대오차", err_cal_876[0])
    print("총 조회시간 내의 설치용량 대 시간당 평균절대오차", err_cal_876[1])
    print("총 조회시간 내의 설치용량 대 일당 평균절대오차", err_cal_876[2])
    # print("총 조회시간 내의 설치용량 대 평균절대오차", err_cal_997N[0])
    # print("총 조회시간 내의 설치용량 대 시간당 평균절대오차", err_cal_997N[1])
    # print("총 조회시간 내의 설치용량 대 일당 평균절대오차", err_cal_997N[2])
    # print("총 조회시간 내의 설치용량 대 평균절대오차", err_cal_997G[0])
    # print("총 조회시간 내의 설치용량 대 시간당 평균절대오차", err_cal_997G[1])
    # print("총 조회시간 내의 설치용량 대 일당 평균절대오차", err_cal_997G[2])