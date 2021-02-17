import ml.ml_main as ml
import crawling.crawling_news as crawling_news
import crawling.dart_crawling as dart_crawling
import pandas as pd

code = input("종목 코드: ")
result, name = ml.prediction(code)
print("\n\n", result)

maxpage = 3  # 증권사 3 페이지까지 파일을 만듬
allpage = 100  # 증권사 100 페이지까지 분석
data = pd.read_csv('./crawling/company_list.txt', dtype=str, sep='\t')  # 종목코드 추출

crawling_news.convert_to_code_data(code[1:], 2, data)  # 이틀동안의 뉴스 분석 함수
print("")
print(" 공시정보:")
dart_crawling.corp_info(name)
# 아쉬운 점: 반도체쪽만 봐서..., 각 산업별 키워드를 찾아서, 가중치 재배치해도 성능이 좋아질 것 같습니다.