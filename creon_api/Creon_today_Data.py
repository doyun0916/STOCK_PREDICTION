import win32com.client
from datetime import datetime

datetime.today()            # 현재 날짜 가져오기
year=datetime.today().year        # 현재 연도 가져오기
month=datetime.today().month      # 현재 월 가져오기
day=datetime.today().day        # 현재 일 가져오기 



today =str(year) +str(month)+str(day)        

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
    
# 현재가 객체 구하기
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
objStockMst.SetInputValue(0, 'A000660')   #종목 코드 - sk하이닉스
objStockMst.BlockRequest()

# 현재가 통신 및 통신 에러 처리 
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0:
    exit()

# 현재가 정보 조회
time= objStockMst.GetHeaderValue(4)  # 시간
high= objStockMst.GetHeaderValue(14)  # 고가
low= objStockMst.GetHeaderValue(15)   # 저가
cprice= objStockMst.GetHeaderValue(11) # 종가
vol= objStockMst.GetHeaderValue(18)   #거래량

#        code = objStockMst.GetHeaderValue(0)  #종목코드
#        name= objStockMst.GetHeaderValue(1)  # 종목명             
#        open= objStockMst.GetHeaderValue(13)  # 시가        
# 사용하는데이터 -> [날짜, 시간, 고가, 저가, 종가, 거래량] 나오는 API

print("오늘 : "+ today)
print("시간", time)
print("고가", high)
print("저가", low)
print("종가", cprice)
print("거래량", vol)
        
