
import pandas as pd

# 예제 5-44 크롤링 데이터 불러오기
raw_total = pd.read_excel('C:/Users/rkdrj/OneDrive/바탕 화면/OSSP/files/크롤링 데이터/크롤링통합파일.xlsx')
raw_total.head()

# 예제 5-48 여러개의 단어 선택/추출/저장하기
select_word_list = ['커피','맛집','카페','포토존','핫플']

for select_word in select_word_list:
    check_list = []
    for content in raw_total['content']:
        if select_word in content:
            check_list.append(True)
        else:
            check_list.append(False)

    select_df = raw_total[check_list]
    fpath = f'C:/Users/rkdrj/OneDrive/바탕 화면/OSSP/files/태그 데이터/태그데이터_{select_word}.xlsx'
    select_df.to_excel(fpath)    