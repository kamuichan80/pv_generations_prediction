from pandas.core.frame import DataFrame
import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import re
import numpy as np
from datetime import datetime, timedelta

xmlUrl = 'http://dataopen.kospo.co.kr/openApi/Gene/pwrGenTran'
My_API_Key = unquote('xXcVSpRYdLQ17Ah8ywRY71aNXMVNT1p5MnZu1U%2B2pbyEo0AIb1ykDMkOiYpdrXCQUuHTFVhypkLuRpd628kpaw%3D%3D')
# My_API_Key = unquote('uAeoLlrQxF6ksUubkstds%2BXrPna5e6F5PEBWm7MiXXXMCHe%2FLZIbpGhJV5XWVnhawq7UebOw00vsBLMMNiS2SQ%3D%3D')

def measure(strSDate: str, strEDate: str, strOrgCd: str):
    
    queryParams = '?' + urlencode(
            {
            quote_plus('ServiceKey') : My_API_Key,
            quote_plus('pageNo') : '1',
            quote_plus('numOfRows') : '10',
            quote_plus('strSdate') : strSDate,
            quote_plus('strEdate') : strEDate,
            quote_plus('strType') : '1',
            quote_plus('strOrgCd') : strOrgCd,
            quote_plus('strHoki') : '01',
            }
        )
    # print(xmlUrl+queryParams)
    response = requests.post(xmlUrl+queryParams).text.encode('utf-8')
    # print(response)
    xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
    # print(xmlobj)
    rows_date = xmlobj.find_all(re.compile("ymd"))
    # print(rows_date)
    rows_generations = xmlobj.find_all(re.compile("qhorgen[0-9]"))
    df_date = pd.DataFrame(pd.to_datetime(rows_date[row].text) for row in range(0, len(rows_date)))
    generations = pd.DataFrame(float(rows_generations[row].text) for row in range(0, len(rows_generations)))
    reshape_gen = generations.values.reshape(-1, 24)
    # print(reshape_gen)
    df_reshape_gen = pd.DataFrame(data=reshape_gen, index=df_date[0].values).sort_index(ascending=True)
    time_delta = timedelta(days=1)
    # index_date = pd.date_range(start=strSDate, end=(pd.to_datetime(strEDate)+time_delta).strftime('%Y-%m-%d %H:%M:%S'),closed='right',freq='1H',tz='Asia/Seoul')
    index_date = pd.date_range(start=strSDate, end=strEDate,closed='right',freq='1H',tz='Asia/Seoul')
    # print(index_date)
    df_gens = pd.DataFrame(data=df_reshape_gen.stack().values, index=index_date, columns=['gens'])
    df_gens.to_csv('df_gens_%s_%s.csv' % (strOrgCd,f"{datetime.now():%Y-%m-%d}"))
    return df_gens.loc[(pd.to_datetime(strSDate)+time_delta):]
    # return df_gens

# print(measure('20210819','20210825','876'))
# print(measure('20210817','20210823','997N'))
# print(measure('20210817','20210823','997G'))
