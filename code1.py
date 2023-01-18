from selenium import webdriver
from selenium.webdriver.common.by import By
from webdrivermanager import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import unicodedata
import pandas as pd


from folium.plugins import MarkerCluster

# 검색결과 URL 만드는 함수
def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    return url    

# 인스타그램 로그인
def login(driver):
        # 인스타그램 접속
        driver.get("https://www.instagram.com")
        time.sleep(2)

        # 인스타그램 로그인
        email = '********'   ### 계정 정보 
        input_id = driver.find_element(By.NAME, "username")
        input_id.clear()
        input_id.send_keys(email)

        password = '********' ### 비밀번호 정보 
        input_pw = driver.find_element(By.NAME, "password")
        input_pw.clear()
        input_pw.send_keys(password)
        input_pw.submit()

        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, 'button._acan._acao._acas._aj1-').click() # 계정 정보 저장 넘어가기
        driver.find_element(By.CSS_SELECTOR, 'button._a9--._a9_1').click() # 알림 설정 넘어가기

        print('로그인 성공')

# HTML에서 첫번째 게시글 찾아 클릭하는 함수
def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR, "div._aabd._aa8k._aanf")
    first.click()
    time.sleep(3)

# 게시글 정보 가져오는 함수
def get_content(driver):
    # 현재 페이지 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 본문 내용 가져오기
    try:
        content = soup.select('div._a9zs > span')[0].text  
        content = unicodedata.normalize('NFC', content) 
    except:
        content = ' '
    # 본문 내용에서 해시태그 가져오기(정규식 활용)
    tags = re.findall(r'#[^\s#,\\]+', content)  
    # 작성일자 정보 가져오기
    date = soup.select('time._a9ze._a9zf')[0]['datetime'][:10]
    # 좋아요 수 가져오기
    try:
        like = soup.select('div._aacl._aaco._aacw._aacx._aada._aade > span')[0].text
    except:
        like = 0
    # 위치정보 가져오기
    try: 
        place = soup.select('div._aaqm')[0].text
        place = unicodedata.normalize('NFC', place)
    except:
        place = ''
    # 수집한 정보 저장하기
    data = [content, date, like, place, tags]
    return data

# 다음 게시글로 이동하는 함수
def move_next(driver):
    right = driver.find_elements('css selector', 'div._aaqg._aaqh > button._abl-')[0]
    right.click()
    time.sleep(3)

def crawling(driver, url):
    driver.get(url)
    time.sleep(5)

    # 첫 번째 게시글 열기
    select_first(driver)
    
    # 게시글 수집하기
    target = 1000      # 크롤링할 게시글 수
    for i in range(target):
        # 게시글 수집에 오류 발생시(네트워크 문제 등의 이유로)  2초 대기 후, 다음 게시글로 넘어가도록 try, except 구문 활용
        try:
            data = get_content(driver)    # 게시글 정보 가져오기
            results.append(data)
            move_next(driver)
        except:
            time.sleep(2)
            move_next(driver)
    print('크롤링 성공')
    return results

# 크롤링 결과 저장하기
def savefile(word,results):
    results_df = pd.DataFrame(results)
    results_df.columns = ['content','data','like','place','tags']
    results_df.to_excel(f'./files/크롤링 데이터/{word}.xlsx', index = False)
    print('크롤링 파일 저장 성공')
# 여러 개의 저장파일 통합하기
def mergefile(word):
    jeju_insta_df = pd.DataFrame( [ ] )

    folder = './files/크롤링 데이터/'
    f_list = [f'{word[0]}.xlsx', f'{word[1]}.xlsx', f'{word[2]}.xlsx', f'{word[3]}.xlsx']
    for fname in f_list:
        fpath = folder + fname
        temp = pd.read_excel(fpath)
        jeju_insta_df = jeju_insta_df.append(temp)
    jeju_insta_df.columns =['content','data','like','place','tags']
    print('크롤링 파일 통합 성공')

    # 중복 데이터 제거하고 엑셀 파일로 저장하기
    jeju_insta_df.drop_duplicates(subset = [ "content"] , inplace = True)
    jeju_insta_df.to_excel('./files/크롤링 데이터/크롤링통합파일.xlsx', index = False)
    print('중복 데이터 제거 성공')
    
# 메인 인스타그램 크롤링

# 크롬 브라우저 열기
driver = webdriver.Chrome('./files/chromedriver.exe') 

# 인스타그램 로그인
login(driver)

#검색어
word = ["제주핫플", "제주카페","제주맛집","제주바다"] 
     
  
# 크롤링
for i in range(4):
    url = insta_searching(word[i]) # 인스타그램 검색페이지 URL 만들기
    results = [ ]
    results = crawling(driver, url)
    savefile(word[i], results)

# 여러 개의 저장파일 통합하기
mergefile(word)
