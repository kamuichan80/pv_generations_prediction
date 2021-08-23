from pandas.core.frame import DataFrame
import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import re
import numpy as np
from datetime import datetime, timedelta

def measure(strSdate: str, strEdate: str, strOrgCd: str):
    
    xmlUrl = 'http://dataopen.kospo.co.kr/openApi/Gene/pwrGenTran'
    My_API_Key = unquote('xXcVSpRYdLQ17Ah8ywRY71aNXMVNT1p5MnZu1U%2B2pbyEo0AIb1ykDMkOiYpdrXCQUuHTFVhypkLuRpd628kpaw%3D%3D')
    queryParams = '?' + urlencode(
            {
            quote_plus('ServiceKey') : My_API_Key,
            quote_plus('pageNo') : '1',
            quote_plus('numOfRows') : '10',
            quote_plus('strSdate') : strSdate,
            quote_plus('strEdate') : strEdate,
            quote_plus('strType') : '1',
            quote_plus('strOrgCd') : strOrgCd,
            quote_plus('strHoki') : '01',
            }
        )
    response = requests.post(xmlUrl+queryParams).text.encode('utf-8')
    xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
    rows_date = xmlobj.find_all(re.compile("ymd"))
    rows_generations = xmlobj.find_all(re.compile("qhorgen[0-9]"))
    df_date = pd.DataFrame(pd.to_datetime(rows_date[row].text) for row in range(0, len(rows_date)))
    generations = pd.DataFrame(float(rows_generations[row].text) for row in range(0, len(rows_generations)))
    reshape_gen = generations.values.reshape(-1, 24)
    df_reshape_gen = pd.DataFrame(data=reshape_gen, index=df_date[0].values).sort_index(ascending=True)
    time_delta = timedelta(days=1)
    index_date = pd.date_range(start=strSdate, end=pd.to_datetime(strEdate)+time_delta,closed='right',freq='1H',tz='Asia/Seoul')
    df_gens = pd.DataFrame(data=df_reshape_gen.stack().values, index=index_date, columns=['gens'])
    df_gens.to_csv('df_gens_%s_%s.csv' % (strOrgCd,f"{datetime.now():%Y-%m-%d}"))
    # print(df_reshape_gen.stack().loc['2021-08-13'])
    # print(df_gens.loc['2021-08-13'])
    return df_gens

print(measure('20210816','20210822','876'))
print(measure('20210816','20210822','997N'))
print(measure('20210816','20210822','997G'))