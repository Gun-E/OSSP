import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import sys
from wordcloud import WordCloud 
from collections import Counter


# 크롤링 결과 중 해시태그 데이터 불러오기
raw_total = pd.read_excel('C:/Users/rkdrj/OneDrive/바탕 화면/OSSP/files/크롤링 데이터/크롤링통합파일.xlsx',engine='openpyxl')
raw_total['tags'] [:3]

# 해시태그 통합 저장하기
tags_total = []

for tags in raw_total['tags']:
    tags_list = tags[2:-2].split("', '")
    for tag in tags_list:
        tags_total.append(tag)
        
# 빈도수 집계하기(Counter)
tag_counts = Counter(tags_total)

# 가장 많이 사용된 해시태그 살펴보기 
tag_counts.most_common(50)

# 데이터 정제하기
STOPWORDS = ['#제주도','#일상', '#선팔', '#광고', '#건강', '#반영구', '#제주자연눈썹','#다이어트','#협찬','#서귀포눈썹문신', '#제주눈썹문신', '#소통', '#맞팔']
tag_total_selected = []
for tag in tags_total:
    if tag not in STOPWORDS:
        tag_total_selected.append(tag)
        
tag_counts_selected = Counter(tag_total_selected)
tag_counts_selected.most_common(50)

# 시각화 라이브러리 호출 및 환경 설정(한글 폰트)
if sys.platform in ["win32", "win64"]:
    font_name = "malgun gothic"
rc('font',family=font_name)

# 데이터 준비하기
tag_counts_df = pd.DataFrame(tag_counts_selected.most_common(30))
tag_counts_df.columns = ['tags', 'counts']

# 막대 차트 만들기
plt.figure(figsize=(10,8)) 
sns.barplot(x='counts', y='tags', data = tag_counts_df)
font_path = "c:/Windows/Fonts/malgun.ttf"
plt.savefig('C:/Users/rkdrj/OneDrive/바탕 화면/OSSP/files/태그막대차트.png')

# 워드클라우드 만들기
wordcloud=WordCloud(font_path= font_path, 
                background_color="white",
                max_words=100,
                relative_scaling= 0.3,
                width = 800,
                height = 400
                ).generate_from_frequencies(tag_counts_selected)  
plt.figure(figsize=(15,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('C:/Users/rkdrj/OneDrive/바탕 화면/OSSP/files/태그워드클라우드.png')

