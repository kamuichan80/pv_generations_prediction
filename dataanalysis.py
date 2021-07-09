# coding: utf-8
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'AppleGothic'
import pandas as pd
import numpy as np
from pandas.core.indexes.datetimes import date_range
import seaborn as sns

data = pd.read_csv("한국남부발전(주)_인천수산정수장 태양광발전실적_20201119.csv",encoding='CP949',index_col=0,parse_dates=True)
preprocessed_data = data[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']]
preprocessed_data.columns = ['1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','0']
preprocessed_redata = preprocessed_data[['0','1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']]
preprocessed_redata = preprocessed_redata.reindex(pd.date_range(start='2013-01-01', end='2020-12-31'), fill_value=0)
preprocessed_redata.loc['2018-11-24'] = preprocessed_redata.loc['2018-11-23'].values

# print(preprocessed_redata.shape)
# print(len(preprocessed_redata.values.flatten()), len(pd.date_range(start='2013-01-01 00:00:00', end='2020-12-31 23:00:00', freq='H')))
generations_data = pd.DataFrame(index=pd.date_range(start='2013-01-01 00:00:00', end='2020-12-31 23:00:00', freq='H'), data=preprocessed_redata.values.flatten())
generations_data.columns = ['발전량']
generations_data = generations_data.fillna(0)
# print(generations_data)
# generations_data.loc['2020-07-31'].plot()
# plt.show()

weather_data2013 = pd.read_csv('weather2013.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2013 = weather_data2013.fillna(0)
index2013 = pd.date_range(start='2013-01-01 00:00:00',end='2013-12-31 23:00:00', freq='H')
weather_data2013 = weather_data2013.reindex(index=index2013, fill_value=0)
weather_data2013.loc['2013-03-19 20:00:00'] = weather_data2013.loc['2013-03-19 19:00:00'].values
weather_data2014 = pd.read_csv('weather2014.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2014 = weather_data2014.fillna(0)
weather_data2015 = pd.read_csv('weather2015.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2015 = weather_data2015.fillna(0)
weather_data2016 = pd.read_csv('weather2016.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2016 = weather_data2016.fillna(0)
weather_data2017 = pd.read_csv('weather2017.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2017 = weather_data2017.fillna(0)
weather_data2018 = pd.read_csv('weather2018.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2018 = weather_data2018.fillna(0)
index2018 = pd.date_range(start='2018-01-01 00:00:00',end='2018-12-31 23:00:00', freq='H')
weather_data2018 = weather_data2018.reindex(index=index2018, fill_value=0)
weather_data2018.loc['2018-11-24 00:00:00':'2018-11-24 23:00:00'] = weather_data2018.loc['2018-11-23 00:00:00':'2018-11-23 23:00:00'].values
weather_data2019 = pd.read_csv('weather2019.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2019 = weather_data2019.fillna(0)
weather_data2020 = pd.read_csv('weather2020.csv',index_col=2,encoding='CP949', parse_dates=True)
weather_data2020 = weather_data2020.fillna(0)
index2020 = pd.date_range(start='2020-01-01 00:00:00',end='2020-12-31 23:00:00', freq='H')
weather_data2020 = weather_data2020.reindex(index=index2020, fill_value=0)

# print(len(weather_data2013),len(weather_data2014),len(weather_data2015),len(weather_data2016),len(weather_data2017),len(weather_data2018),len(weather_data2019),len(weather_data2020) )
# print((weather_data2013.head(24)),(weather_data2014.head(24)),(weather_data2015.head(24)),(weather_data2016.head(24)),(weather_data2017.head(24)),(weather_data2018.head(24)),(weather_data2019.head(24)),(weather_data2020.head(24)) )


weather_data_list = [weather_data2013, weather_data2014, weather_data2015, weather_data2016, weather_data2017, weather_data2018, weather_data2019, weather_data2020]
weather_data_full = pd.concat(weather_data_list, axis=0)
# print(weather_data_full.head(24), weather_data_full.tail(24))
# print(len(generations_data), len(weather_data_full))

X = weather_data_full.drop(columns=['지점명', '지점', '운형(운형약어)'])
# print(X.index)
X['month'] = X.index.month
X['day'] = X.index.day
X['hour'] = X.index.hour
y = generations_data

# print(type(X.index))
dropThis2016 = pd.date_range(start='2016-02-29 00:00:00', end='2016-02-29 23:00', freq='H')
dropThis2020 = pd.date_range(start='2020-02-29 00:00:00', end='2020-02-29 23:00', freq='H')
dropThis = dropThis2016.union(dropThis2020)
# print(type(dropThis))
# print(dropThis)
X_new = X.drop(dropThis)
y_new = y.drop(dropThis)
# print(len(X_new), len(y_new))


X_selected = X_new.loc[:'2019']
y_selected = y_new.loc[:'2019']


# print(X_selected.tail(24), y_selected.tail(24))
# corr_df = pd.concat([X,y], axis=1)
# print(corr_df.head(24))
# pal = sns.color_palette("icefire", 24)

# sns.scatterplot(x = '발전량', y='일me사(MJ/m2)', data=corr_df, hue=corr_df.index.hour, palette=pal)
# plt.show()

# plt.figure(1)
# plt.plot(y.loc['2013'].resample('M').mean().values, '-o', label='2013')
# plt.plot(y.loc['2014'].resample('M').mean().values, '-v', label='2014')
# plt.plot(y.loc['2015'].resample('M').mean().values, '-^', label='2015')
# plt.plot(y.loc['2016'].resample('M').mean().values, '-<', label='2016')
# plt.plot(y.loc['2017'].resample('M').mean().values, '->', label='2017')
# plt.plot(y.loc['2018'].resample('M').mean().values, '-8', label='2018')
# plt.plot(y.loc['2019'].resample('M').mean().values, '-s', label='2019')
# plt.legend(title='발전량')
# plt.show()
# print(len(X.columns))


# for name, values in X.iteritems():
#     # print(name)
#     plt.figure(2)
#     plt.plot(X.loc['2013'][name].resample('M').mean().values, '-o', label='2013')
#     plt.plot(X.loc['2014'][name].resample('M').mean().values, '-v', label='2014')
#     plt.plot(X.loc['2015'][name].resample('M').mean().values, '-^', label='2015')
#     plt.plot(X.loc['2016'][name].resample('M').mean().values, '-<', label='2016')
#     plt.plot(X.loc['2017'][name].resample('M').mean().values, '->', label='2017')
#     plt.plot(X.loc['2018'][name].resample('M').mean().values, '-8', label='2018')
#     plt.plot(X.loc['2019'][name].resample('M').mean().values, '-s', label='2019')
#     plt.legend(title=name)
#     plt.show()
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
# Fit regression model
# tscv = TimeSeriesSplit(n_splits=7)
# for train_index, test_index in tscv.split(X_selected):
    # print("TRAIN:", train_index, "TEST:", test_index)
    # X_train, X_test = X_selected.loc[train_index], X_selected.loc[test_index]
    # y_train, y_test = y_selected.loc[train_index], y_selected.loc[test_index]

X_train, X_test, y_train, y_test = train_test_split(X_selected, y_selected, test_size=0.3, random_state = 42)
print(X_train, y_train, X_test, y_test)
ridge = Ridge(alpha=.5)
gb = GradientBoostingRegressor(n_estimators= 500, max_depth = 4, min_samples_split = 5, learning_rate = 0.01, loss = 'ls')

print(X_selected.describe(), y_selected.describe())


plt.plot(ridge.fit(X_train, y_train).predict(X_test))
plt.plot(gb.fit(X_train, y_train).predict(X_test))
plt.plot(y_test.values)
plt.show()

error_lr = y_test - ridge.fit(X_train, y_train).predict(X_test).reshape(-1,1)
abserror_lr = abs(error_lr)
error_gb = y_test - gb.fit(X_train, y_train).predict(X_test).reshape(-1,1)
abserror_gb = abs(error_gb)
print(abserror_lr.groupby(abserror_lr.index.hour).mean()/10, abserror_gb.groupby(abserror_gb.index.hour).mean()/10)


print(abserror_lr.groupby(abserror_lr.index.month).mean()/10, abserror_gb.groupby(abserror_gb.index.month).mean()/10)
