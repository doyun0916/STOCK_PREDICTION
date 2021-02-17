from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 




def crawler(company_code, maxpage):
 
    page = 1
    up_list = ['기대','강세','개선','수주','상승세','상승','선전','이익','증가','투자','특허','회복','확대']
    up_list_count=[0,0,0,0,0,0,0,0,0,0,0,0,0] #키워드 갯수만큼 초기화 필요
    down_list = ['불확실성','충격하락세','하락','추락','불가피','부진']
    down_list_count=[0,0,0,0,0,0] #키워드 갯수만큼 초기화 필요
 
    while page <= int(maxpage): 
    
        #네이버 파이낸스 뉴스란
        url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page) 
        source_code = requests.get(url).text
        html = BeautifulSoup(source_code, "lxml")
             
        # 뉴스 제목 
        titles = html.select('.title')
        for title in titles: 
            title = title.get_text() 
            title = re.sub('\n','',title)
            for i in range(0,len(up_list)-1):
                if title.find(up_list[i])>=0:  
                    up_list_count[i]+=1
            for j in range(0,len(down_list)-1):
                if title.find(down_list[j])>=0:
                    down_list_count[j]+=1
                    
        print("up_list_count :"+ str(up_list_count))

        print("down_list_count :"+ str(down_list_count))

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
    maxpage = 100  # 증권사 원파는 페이지만큼 돌리기 
    convert_to_code(company, maxpage)
 
main() 