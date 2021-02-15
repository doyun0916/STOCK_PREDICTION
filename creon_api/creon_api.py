import sys
from PyQt5.QtWidgets import *
import win32com.client
import pandas as pd
import os
from datetime import date

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')


class CpStockChart:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    # 차트 요청 - 기간 기준으로
    def RequestFromTo(self, code, fromDate, toDate, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('1'))  # 기간으로 받기
        self.objStockChart.SetInputValue(2, toDate)  # To 날짜
        self.objStockChart.SetInputValue(3, fromDate)  # From 날짜
        # self.objStockChart.SetInputValue(4, 500)  # 최근 500일치
        self.objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 날짜,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('D'))  # '차트 주기 - 일간 차트 요청
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        if rqStatus != 0:
            exit()

        len = self.objStockChart.GetHeaderValue(3)

        caller.dates = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.opens.append(self.objStockChart.GetDataValue(1, i))
            caller.highs.append(self.objStockChart.GetDataValue(2, i))
            caller.lows.append(self.objStockChart.GetDataValue(3, i))
            caller.closes.append(self.objStockChart.GetDataValue(4, i))
            caller.vols.append(self.objStockChart.GetDataValue(5, i))

        return caller

    # 차트 요청 - 최근일 부터 개수 기준
    def RequestDWM(self, code, dwm, count, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 받기
        self.objStockChart.SetInputValue(4, count)  # 최근 500일치
        self.objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 요청항목 - 날짜,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 일/주/월
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()

        len = self.objStockChart.GetHeaderValue(3)

        caller.dates = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        caller.times = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.opens.append(self.objStockChart.GetDataValue(1, i))
            caller.highs.append(self.objStockChart.GetDataValue(2, i))
            caller.lows.append(self.objStockChart.GetDataValue(3, i))
            caller.closes.append(self.objStockChart.GetDataValue(4, i))
            caller.vols.append(self.objStockChart.GetDataValue(5, i))

        return

    # 차트 요청 - 분간, 틱 차트
    def RequestMT(self, code, dwm, count, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 받기
        self.objStockChart.SetInputValue(4, count)  # 조회 개수
        self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 분/틱
        self.objStockChart.SetInputValue(7, 1)  # 분틱차트 주기
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        if rqStatus != 0:
            exit()

        len = self.objStockChart.GetHeaderValue(3)

        caller.dates = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        caller.times = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.times.append(self.objStockChart.GetDataValue(1, i))
            caller.opens.append(self.objStockChart.GetDataValue(2, i))
            caller.highs.append(self.objStockChart.GetDataValue(3, i))
            caller.lows.append(self.objStockChart.GetDataValue(4, i))
            caller.closes.append(self.objStockChart.GetDataValue(5, i))
            caller.vols.append(self.objStockChart.GetDataValue(6, i))

        print(len)

        return caller

class Cp7210:
    def __init__(self):
        self.objRq = None
        return

    def request(self, investFlag, caller):
        maxRqCont = 1
        rqCnt = 0
        caller.data7210 = []
        self.objRq = None
        self.objRq = win32com.client.Dispatch("CpSysDib.CpSvr7210d")

        self.objRq.SetInputValue(0, '0')  # 0 전체 1 거래소 2 코스닥 3 업종 4 관심종목
        self.objRq.SetInputValue(1, ord('0'))  # 0 수량 1 금액
        self.objRq.SetInputValue(2, investFlag)  # 0 종목 1 외국인 2 기관계 3 보험기타 4 투신..
        self.objRq.SetInputValue(3, ord('0'))  # 0 상위순 1 하위순

        self.objRq.BlockRequest()
        rqCnt += 1

        # 통신 및 통신 에러 처리
        rqStatus = self.objRq.GetDibStatus()
        rqRet = self.objRq.GetDibMsg1()
        if rqStatus != 0:
            return False

        cnt = self.objRq.GetHeaderValue(0)
        date = self.objRq.GetHeaderValue(1)  # 집계날짜
        time = self.objRq.GetHeaderValue(2)  # 집계시간

        for i in range(cnt):
            item = {}
            item['code'] = self.objRq.GetDataValue(0, i)
            item['종목명'] = self.objRq.GetDataValue(1, i)
            item['현재가'] = self.objRq.GetDataValue(2, i)
            item['대비'] = self.objRq.GetDataValue(3, i)
            item['대비율'] = self.objRq.GetDataValue(4, i)
            item['거래량'] = self.objRq.GetDataValue(5, i)
            item['외국인'] = self.objRq.GetDataValue(6, i)
            item['기관계'] = self.objRq.GetDataValue(7, i)
            item['보험기타금융'] = self.objRq.GetDataValue(8, i)
            item['투신'] = self.objRq.GetDataValue(9, i)
            item['은행'] = self.objRq.GetDataValue(10, i)
            item['연기금'] = self.objRq.GetDataValue(11, i)
            item['국가지자체'] = self.objRq.GetDataValue(12, i)
            item['기타법인'] = self.objRq.GetDataValue(13, i)
            caller.data7210.append(item)

        return caller

if __name__ == "__main__":
    class Result:
        def __init__(self):
            # 기본 변수들
            self.dates = []
            self.opens = []
            self.highs = []
            self.lows = []
            self.closes = []
            self.vols = []
            self.times = []

    class temp:
        def __init__(self):
            self.data7210 = []

    new = CpStockChart()
    final = Result
    code = input("코드명: ")
    today = date.today()
    date_today = str(today).replace('-', '').replace(' ', '')
    begins = new.RequestFromTo(code, int(date_today)-50000, int(date_today), final)
    iteration_num = len(begins.dates)
    print("코드: ", code)
    d = {'dates': [], 'opens': [], 'highs': [], 'lows': [], 'closes': [], 'vols': [], 'results': []}
    yesterday = begins.highs[0]
    for i in range(1, iteration_num):
        #print("날짜: ", begins.dates[i], "시가: ", begins.opens[i], "고가: ", begins.highs[i], "저가: ", begins.lows[i], "종가: ", begins.closes[i], "거래량: ", begins.vols[i],)
        d["dates"].append(begins.dates[i])
        d["opens"].append(begins.opens[i])
        d["highs"].append(begins.highs[i])
        d["lows"].append(begins.lows[i])
        d["closes"].append(begins.closes[i])
        d["vols"].append(begins.vols[i])
        d["results"].append(1 if (begins.highs[i] - yesterday) > 0 else 0)
        yesterday = begins.highs[i]

    Df = pd.DataFrame(d)
    Df.to_csv('./_5years_data.csv', sep=',', na_rep='NaN', index=False)

    print("")
    print("************ 외국인, 기관계 등등 지표 ****************")

    come_on = temp
    others_new = Cp7210()
    fin = others_new.request(1, come_on)
    for i in range(len(fin.data7210)):
        if fin.data7210[i]["code"] == code:
            print(fin.data7210[i])