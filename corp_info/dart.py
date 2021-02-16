import dart_fss as dart

# Open DART API KEY 설정
api_key='8a21428e7aff607d8bfb0963894c7a030650cf4e'
dart.set_api_key(api_key=api_key)

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

# 삼성전자 검색
corp_name = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]
corp_nums = None
corp_name = str(corp_name)
for i in range(1, len(corp_name)):
    if corp_name[i] == "]":
        corp_nums = corp_name[1:i]
        break
print(corp_nums)
result = dart.filings.search(corp_code=corp_nums, bgn_de='20200101', last_reprt_at='N', pblntf_ty=None, pblntf_detail_ty=None, sort='date', sort_mth='desc', page_no=3, page_count=50)
print(result)
# 2012년부터 연간 연결재무제표 불러오기
#fs = samsung.extract_fs(bgn_de='20120101')

# 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
#fs.save()