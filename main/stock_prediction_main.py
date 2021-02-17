#import ml.ml_main as ml_main
import win32com.client  # 크레온 api
from bs4 import BeautifulSoup  # 크롤링 
import requests
import re
import pandas as pd
import os 
from datetime import datetime #현재 시간

os.getcwd()
year= datetime.today().year       # 현재 연도 가져오기
month= datetime.today().month      # 현재 월 가져오기
day=datetime.today().day         # 현재 일 가져오기



#------------------------------------------------------------------------------------------------------------
# 크레온 api 실시간 값 받아오기 

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


print("오늘 : "+ today)
print("시간", time)
print("고가", high)
print("저가", low)
print("종가", cprice)
print("거래량", vol)


#------------------------------------------------------------------------------------------------------------

###  키워드 카운트 함수 
def crawler_data(company_code, allpage): #100페이지까지 분석하는 함수
 
    page = 1
    up_list = ['기대','강세','개선','수주','상승세','상승','선전','이익','증가','투자','특허','회복','확대']
    up_list_count=[0,0,0,0,0,0,0,0,0,0,0,0,0] #키워드 갯수만큼 초기화 필요
    down_list = ['불확실성','충격하락세','하락','추락','불가피','부진']
    down_list_count=[0,0,0,0,0,0] #키워드 갯수만큼 초기화 필요
 
    while page <= int(allpage): 
    
        #네이버 파이낸스 뉴스란
        url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page) 
        source_code = requests.get(url).text
        html = BeautifulSoup(source_code, "lxml")
             
        # 뉴스 제목    
        titles = html.select('.title')
        title_result=[]
        for title in titles: 
            title = title.get_text() 
            title = re.sub('\n','',title)
            title_result.append(title)
            for i in range(0,len(up_list)-1):  # 키워드 카운트
                if title.find(up_list[i])>=0:  
                    up_list_count[i]+=1
            for j in range(0,len(down_list)-1):
                if title.find(down_list[j])>=0:
                    down_list_count[j]+=1
       
        print( "up_list_count : " +   str(up_list_count))
        print( "down_list_count : " +   str(down_list_count))
        page += 1 

# ------------------------------------------------------------------------------

### 뉴스 csv 만드는 함수
def crawler(company_code, maxpage): #3페이지까지 엑셀 만드는함수
 
    page = 1

 
    while page <= int(maxpage): 
    
        #네이버 파이낸스 뉴스란
        url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page) 
        source_code = requests.get(url).text
        html = BeautifulSoup(source_code, "lxml")
             
        # 뉴스 제목    
        titles = html.select('.title')
        title_result=[]
        for title in titles: 
            title = title.get_text() 
            title = re.sub('\n','',title)
            title_result.append(title)
          
        # 뉴스 날짜 
        dates = html.select('.date') 
        date_result = [date.get_text() for date in dates] 
 
        # 뉴스 매체     
        sources = html.select('.info')
        source_result = [source.get_text() for source in sources] 
 
        # 변수들 합쳐서 해당 디렉토리에 csv파일로 저장하기 
        result= {"날짜" : date_result, "언론사" : source_result, "기사제목" : title_result} 
        df_result = pd.DataFrame(result)
        df_result.to_csv(str(year)+'_'+str(month)+'_'+str(day) +'_' + str(page) + '.csv', mode='w', encoding='utf-8-sig') 
        print("여기 지나가는 가?")
        page += 1 


# 종목 리스트 파일 열기  
# 회사명을 종목코드로 변환 
        
def convert_to_code_data(company, allpage): # 100페이지 분석하는 함수 
    data = pd.read_csv('C:\stockauto\company_list.txt', dtype=str, sep='\t')   # 종목코드 추출  
    company_name = data['회사명']
    keys = [i for i in company_name]    #데이터프레임에서 리스트로 바꾸기 
    company_code = data['종목코드']
    values = [j for j in company_code]
    dict_result = dict(zip(keys, values))  # 딕셔너리 형태로 회사이름과 종목코드 묶기 
    pattern = '[a-zA-Z가-힣]+' 
    if bool(re.match(pattern, company)) == True:         # Input에 이름으로 넣었을 때  
        company_code = dict_result.get(str(company))
        crawler_data(company_code, allpage)
 
    else:                                                # Input에 종목코드로 넣었을 때       
        company_code = str(company)      
        crawler_data(company_code, allpage)

# -----------------------------------------------------------------------------------------


def convert_to_code(company, maxpage): # 3페이지 엑셀로 만드는 함수 
    data = pd.read_csv(r'C:\stockauto\company_list.txt', dtype=str, sep='\t')   # 종목코드 추출  git Company.txt 파일 다운로드 후 경로 지정 필요합니다.
    company_name = data['회사명']
    keys = [i for i in company_name]    #데이터프레임에서 리스트로 바꾸기 
    company_code = data['종목코드']
    values = [j for j in company_code]
    dict_result = dict(zip(keys, values))  # 딕셔너리 형태로 회사이름과 종목코드 묶기 
    pattern = '[a-zA-Z가-힣]+' 
    if bool(re.match(pattern, company)) == True:         # Input에 이름으로 넣었을 때  
        company_code = dict_result.get(str(company))
        crawler(company_code, maxpage)
 
    else:                                                # Input에 종목코드로 넣었을 때       
        company_code = str(company)      
        crawler(company_code, maxpage)
        
# -------------------------------------- main --------------------------------------------------------------           
def main():
    info_main = input("="*50+"\n"+"실시간 뉴스기사 다운받기."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    company = input("코드명: ")  # Main 소스  code 가 크레온 api code와 겹쳐서 company 사용
  #  print("\n\n", ml_main.prediction(company)) # Main 소스
    maxpage = 3  # 증권사 3 페이지까지 파일을 만듬
    allpage = 100 # 증권사 100 페이지까지 분석

    convert_to_code(company, maxpage) #엑셀 페이지 만드는 함수 호출
    convert_to_code_data(company, allpage) # 100페이지 분석 함수 호출

 
main() 
