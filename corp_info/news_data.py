from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 
from datetime import datetime


year= datetime.today().year       # 현재 연도 가져오기
month= datetime.today().month      # 현재 월 가져오기
day=datetime.today().day         # 현재 일 가져오기

def crawler(company_code, maxpage):
 
    page = 1
    global point
    point = 100
    up_list = ['기대','회복','상승세','상승','개선','선전','수혜플러스','확대','증가','투자','확대','강세','수주','특허','이익']
    down_list = ['불확실성','충격하락세','하락','추락','불가피','부진']

 
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
            for i in up_list:
                if title.find(i)!= -1:
                    point += 1
            for j in down_list:
                if title.find(j)!= -1:
                    point -= 1
          
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
        page += 1 
 

 
 
# 종목 리스트 파일 열기  
# 회사명을 종목코드로 변환 
        
def convert_to_code(company, maxpage):
    data = pd.read_csv('company_list.txt', dtype=str, sep='\t')   # 종목코드 추출  
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
        
           
def main():
    info_main = input("="*50+"\n"+"실시간 뉴스기사 다운받기."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    company = input("종목 이름이나 코드 입력: ") 
    maxpage = 3  # 증권사 3페이지까지 파일을 만듬
    convert_to_code(company, maxpage)
    print(str(point)+"점")
 
main() 