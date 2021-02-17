from pykrx import stock
from datetime import datetime
import pandas as pd

def krx_info(start, code):
    today = str(datetime.now())[:10].replace('-', '').replace(' ', '')
    #BPS, PER, PBR, EPS, DIV, DPS
    cal_info = stock.get_market_fundamental_by_date(start, today, code)
    cal_info = pd.DataFrame(cal_info.values.tolist())

    #시가총액, 거래량, 거래대금, 상장주식수
    corp_info = stock.get_market_cap_by_date(start, today, code)
    corp_info = pd.DataFrame(corp_info.values.tolist())

    # KOSPI  시가, 고가, 저가, 종가, 거래량
    kospi = stock.get_index_ohlcv_by_date(start, today, "1001")
    kospi = pd.DataFrame(kospi.values.tolist())

    # KOSDAQ  시가, 고가, 저가, 종가, 거래량
    kosdaq = stock.get_index_ohlcv_by_date(start, today, "2001")
    kosdaq = pd.DataFrame(kosdaq.values.tolist())

    result = pd.concat([cal_info, corp_info, kospi, kosdaq], axis=1)

    return result