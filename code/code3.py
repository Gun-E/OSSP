import time
import pandas as pd
from tqdm.notebook import tqdm
import requests
import time
import folium
from folium.plugins import MarkerCluster


# 크롤링 데이터 불러오기
raw_total = pd.read_excel('./files/크롤링 데이터/크롤링통합파일.xlsx')
raw_total.head()

# 위치정보 가져오기
location_counts = raw_total['place'].value_counts( )
location_counts

# 등록된 위치정보별 빈도수 데이터
location_counts_df = pd.DataFrame(location_counts)
location_counts_df.head()

# 위치정보 빈도수 데이터 저장하기
location_counts_df.to_excel('./files/위치 데이터/장소위치정보빈도수.xlsx')

# 위치정보 종류 확인하기
locations = list( location_counts.index )
locations 


# 카카오 로컬 API를 활용한 장소 검색 함수 만들기
def find_places(searching):
    # ① 접속URL 만들기
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
    # ② headers 입력하기
    headers = {
    "Authorization": "KakaoAK *******"
    }
    # ③ API 요청&정보 받기
    places = requests.get(url, headers = headers).json()['documents']
    # ④ 필요한 정보 선택하기
    place = places[0] 
    name = place['place_name']
    x=place['x']
    y=place['y']
    data = [name, x, y, searching] 

    return data

locations_inform = [ ]
for location in tqdm(locations):
    try:
        data = find_places(location)       
        locations_inform.append(data) 
        time.sleep(0.5) 
    except:
        pass
locations_inform

# 위치정보 저장하기
locations_inform_df = pd.DataFrame(locations_inform)
locations_inform_df.columns = ['name_official','경도','위도','인스타위치명']
locations_inform_df.to_excel('./files/위치 데이터/장소의정확한위치정보.xlsx', index=False)


# 인스타 게시량 및 위치정보 데이터 불러오기
location_counts_df = pd.read_excel('./files/위치 데이터/장소위치정보빈도수.xlsx', index_col = 0)
locations_inform_df = pd.read_excel('./files/위치 데이터/장소의정확한위치정보.xlsx')

# 위치 데이터 병합하기
location_data = pd.merge(locations_inform_df, location_counts_df, 
                         how = 'inner', left_on = 'name_official', right_index=True)

location_data.head()

# 데이터 중복 점검하기
location_data['name_official'].value_counts()

# 병합한 데이터 저장하기
location_data.to_excel('./files/위치 데이터/위치병합데이터.xlsx')

# 데이터 불러오기
location_data = pd.read_excel('./files/위치 데이터/위치병합데이터.xlsx')
location_data.info()

# 지도 표시하기
Mt_Hanla =[33.362500, 126.533694]
map_jeju = folium.Map(location = Mt_Hanla, zoom_start = 11)

for i in range(len(location_data)):
    name = location_data ['name_official'][i]    # 공식명칭
    count = location_data ['place'][i]           # 게시글 개수
    size = int(count)*2
    long = float(location_data['위도'][i])      
    lat = float(location_data['경도'][i])       
    folium.CircleMarker((long,lat), radius = size, color='red', popup=name).add_to(map_jeju)
    
map_jeju

# 지도 저장하기
map_jeju.save('./files/위치데이터지도.html') 

# 지도 표시하기(마커 집합)

locations = []
names = []

for i in range(len(location_data)):
    data = location_data.iloc[i]  # 행 하나씩
    locations.append((float(data['위도']),float(data['경도'])))    # 위도 , 경도 순으로..
    names.append(data['name_official'])


Mt_Hanla =[33.362500, 126.533694]
map_jeju2 = folium.Map(location = Mt_Hanla, zoom_start = 11)
                       
marker_cluster = MarkerCluster(
    locations=locations, popups=names,
    name='Jeju',
    overlay=True,
    control=True,

)

marker_cluster.add_to(map_jeju2)
folium.LayerControl().add_to(map_jeju2)

map_jeju2

# 지도 저장하기
map_jeju2.save('./files/위치 데이터/장소위치.html') 