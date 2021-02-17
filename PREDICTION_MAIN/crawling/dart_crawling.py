import dart_fss as dart
from datetime import datetime, timedelta

def corp_info(name):
    # Open DART API KEY 설정
    api_key='8a21428e7aff607d8bfb0963894c7a030650cf4e'
    dart.set_api_key(api_key=api_key)

    # DART 에 공시된 회사 리스트 불러오기
    corp_list = dart.get_corp_list()

    # 검색
    corp_name = corp_list.find_by_corp_name(name, exactly=True)[0]
    corp_name = str(corp_name)
    corp_nums = None                           # 회사고유코드 담을 변수
    for i in range(1, len(corp_name)):
        if corp_name[i] == "]":
            corp_nums = corp_name[1:i]
            break
    start = str(datetime.now() + timedelta(days=-30))[:10]          # (-30, 즉 지금으로부터 한달전 공시자료부터 최신까지 검색을 위한 기간 설정)
    date_start = str(start).replace('-', '').replace(' ', '')
    titles = []
    for i in range(1, 3):
        result = dart.filings.search(corp_code=corp_nums, bgn_de=str(date_start), last_reprt_at='N',
                                     pblntf_ty=None, pblntf_detail_ty=None,
                                     sort='date', sort_mth='desc',
                                     page_no=i, page_count=100)                            # page_no, page_count로 양 조절 (몇번째 페이지에서 몇개 가져올지)

        for i in range(len(result)):                                                    # 검색 결과를 제목만 뽑아내기
            print(result.report_list[i].report_nm)
