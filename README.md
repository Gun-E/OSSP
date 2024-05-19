# 제주 맛집 트랜드

## Set up
1. Install Requirements
    ```dotnetcli
    pip install -r requirements.txt
    ```
2. Instargram Crawling
    - Chrome version check
        > chrome 실행 후 chrome://settings/help 접속하여 version 확인
    - ChromeDriver Download
        > https://chromedriver.chromium.org/downloads 접속 후 자신의 chrome version과 맞는 것을 찾아 download
    - 해당 경로에 위치
        ```dotnetcli
        ./files/chromedriver.exe
        ```
    - Enter email & password
        - code1.py
            ```python
            def login(driver):
            # 인스타그램 접속
            driver.get("https://www.instagram.com")
            time.sleep(2)

            # 인스타그램 로그인
            email = '********'   ### 계정 정보 입력!!
            input_id = driver.find_element(By.NAME, "username")
            input_id.clear()
            input_id.send_keys(email)

            password = '********' ### 비밀번호 정보 입력!! 
            input_pw = driver.find_element(By.NAME, "password")
            input_pw.clear()
            input_pw.send_keys(password)
            input_pw.submit()

            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'button._acan._acao._acas._aj1-').click() # 계정 정보 저장 넘어가기
            driver.find_element(By.CSS_SELECTOR, 'button._a9--._a9_1').click() # 알림 설정 넘어가기

            print('로그인 성공')
            ```
    - 코드 해당 위치에 본인 인스타그램 아이디와 비밀번호 입력
3. kakao API setting
    - Get API key
        > 1. https://developers.kakao.com/ 접속
        > 2. 로그인 후 개발자 등록, 앱 생성
        > 3. REST API Key 복사
    - Enter REST API Key
        - code3.py
            ```python
            def find_places(searching):
                # ① 접속URL 만들기
                url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
                # ② headers 입력하기
                headers = {
                "Authorization": "KakaoAK *******" ### REST API Key 입력!!
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
            ```
     - 코드 해당 위치에 본인 REST API Key 입력
## Order of execution
1. code1.py
2. code2.py
3. code3.py
4. code4.py
