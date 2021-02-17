import win32com.client
import pandas as pd
from datetime import date, datetime, timedelta

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

    def today_info(self, code):
        datetime.today()  # 현재 날짜 가져오기
        year = datetime.today().year  # 현재 연도 가져오기
        month = datetime.today().month  # 현재 월 가져오기
        day = datetime.today().day  # 현재 일 가져오기

        today = str(year) + str(month) + str(day)

        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()

        # 현재가 객체 구하기
        objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        objStockMst.SetInputValue(0, 'A000660')  # 종목 코드 - sk하이닉스
        objStockMst.BlockRequest()

        # 현재가 통신 및 통신 에러 처리
        rqStatus = objStockMst.GetDibStatus()
        rqRet = objStockMst.GetDibMsg1()
        #print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()

        # 현재가 정보 조회
        #time = objStockMst.GetHeaderValue(4)  # 시간
        today_info = [today]
        open = objStockMst.GetHeaderValue(13)  # 시가
        today_info.append(open)
        high = objStockMst.GetHeaderValue(14)  # 고가
        today_info.append(high)
        low = objStockMst.GetHeaderValue(15)  # 저가
        today_info.append(low)
        cprice = objStockMst.GetHeaderValue(11)  # 종가
        today_info.append(cprice)
        vol = objStockMst.GetHeaderValue(18)  # 거래량
        today_info.append(vol)
        #        code = objStockMst.GetHeaderValue(0)  #종목코드
        name = objStockMst.GetHeaderValue(1)  # 종목명

        # 사용하는데이터 -> [날짜, 시간, 고가, 저가, 종가, 거래량] 나오는 API

        return name, today_info


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


class Result:
    def __init__(self):
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


def past_data(code, new):
    final = Result
    today = date.today()
    start = str(datetime.now() + timedelta(days=-3650))[:10]
    date_today = str(today).replace('-', '').replace(' ', '')
    date_start = str(start).replace('-', '').replace(' ', '')
    begins = new.RequestFromTo(code, int(date_start), int(date_today), final)
    iteration_num = len(begins.dates)
    print("코드: ", code)
    d = {'dates': [], 'opens': [], 'highs': [], 'lows': [], 'closes': [], 'vols': []}
    r = {'results': []}
    for i in range(1, iteration_num):
        d["dates"].append(begins.dates[i])
        d["opens"].append(begins.opens[i])
        d["highs"].append(begins.highs[i])
        d["lows"].append(begins.lows[i])
        d["closes"].append(begins.closes[i])
        d["vols"].append(begins.vols[i])
        if i+1 < iteration_num:
            r["results"].append(1 if begins.lows[i] > begins.closes[i+1] else 0)
        else:
            r["results"].append(0)

    # df = pd.DataFrame(d)
    # df.to_csv('./_5years_data.csv', sep=',', na_rep='NaN', index=False)

    return d, r

def foreign_info(code):
    come_on = temp
    others_new = Cp7210()
    fin = others_new.request(1, come_on)
    for i in range(len(fin.data7210)):
        if fin.data7210[i]["code"] == code:
            return fin.data7210[i]
