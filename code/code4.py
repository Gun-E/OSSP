
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud 
import sys

# 예제 5-44 크롤링 데이터 불러오기
raw_total = pd.read_excel('./files/크롤링 데이터/크롤링통합파일.xlsx')
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
    fpath = f'./files/태그 데이터/태그데이터_{select_word}.xlsx'
    select_df.to_excel(fpath, index = False)  



# 시각화 라이브러리 호출 및 환경 설정(한글 폰트)
if sys.platform in ["win32", "win64"]:
    font_name = "malgun gothic"
rc('font',family=font_name)

# 여행지 추천 막대 그래프
raw_travel = pd.read_excel('./files/태그 데이터/태그데이터_카페.xlsx')
travel_counts_selected = Counter(raw_travel['place'])

STOPWORDS = ['제주','제주도','jeju','제주도 제주', 'Jeju Island, Korea'] # 데이터 정제하기
travel_data = []
for place in travel_counts_selected:
    if place not in STOPWORDS:
        travel_data.append(place)
        
travel_counts = Counter(travel_data)
location_counts_df = pd.DataFrame(travel_counts.most_common(10))
location_counts_df.columns = ['place', 'counts']

# 막대 차트 만들기
plt.figure(figsize=(20,10)) 
sns.barplot(x='counts', y='place', data = location_counts_df)
font_path = "c:/Windows/Fonts/malgun.ttf"
plt.savefig('./files/추천/트랜디한 여행지 추천 막대차트.png')




# 맛집 추천 막대 그래프
raw_travel = pd.read_excel('./files/태그 데이터/태그데이터_맛집.xlsx')
travel_counts_selected = Counter(raw_travel['place'])

STOPWORDS = ['제주','제주도','jeju','제주도 제주', 'Jeju Island, Korea'] # 데이터 정제하기
travel_data = []
for place in travel_counts_selected:
    if place not in STOPWORDS:
        travel_data.append(place)
        
travel_counts = Counter(travel_data)
location_counts_df = pd.DataFrame(travel_counts.most_common(10))
location_counts_df.columns = ['place', 'counts']

# 막대 차트 만들기
plt.figure(figsize=(20,10)) 
sns.barplot(x='counts', y='place', data = location_counts_df)
font_path = "c:/Windows/Fonts/malgun.ttf"
plt.savefig('./files/추천/맛집 추천 막대차트.png')


