from collections import Counter
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# 사용자로부터 검색어 입력 받기
search_query = input("검색어를 입력하세요: ")
# 브라우저 생성
browser = webdriver.Chrome()
# 웹 사이트 열기
browser.get('https://shopping.naver.com/home')
# 로딩 대기
time.sleep(3)
# 검색어 창을 찾아 search 변수에 저장 (By.CLASS_NAME 방식)
search_box = browser.find_element(By.CLASS_NAME, '_searchInput_search_text_3CUDs')
# 검색어 입력
search_box.send_keys(search_query)
# 검색 실행
search_box.send_keys(Keys.RETURN)
# 스크롤 전 높이 
before_h = browser.execute_script("return window.scrollY")
# 모든 상품명을 저장할 리스트 생성
product_names = []

# 무한 스크롤
while True:
    # 맨 아래로 스크롤 내린다.
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    
    # 스크롤 사이 페이지 로딩 시간 
    time.sleep(2)
    
    # 스크롤 후 높이 
    after_h = browser.execute_script("return window.scrollY")
    
    # 스크롤 높이가 변하지 않으면 더 이상 스크롤할 필요 없음
    if after_h == before_h:
        break
    
    # 스크롤 이전 높이 업데이트
    before_h = after_h
    
# 현재 페이지의 모든 상품명을 가져와서 리스트에 추가
product_elements = browser.find_elements(By.CLASS_NAME, 'product_title__Mmw2K')
for element in product_elements:
    product_names.append(element.text)

#결과를 출력
#print(product_names)

# 브라우저 종료
browser.quit()

# 결과 리스트
result_list = []
# 단어 추출 및 정리
for product in product_names:
    # 첫 번째 단어를 제외한 단어들 추출
    words = product.split()[1:]
    # 영어, 숫자, 특수기호를 포함한 단어 제거 및 소문자로 변환
    words = [re.sub(r'[^a-zA-Z가-힣]', '', word).lower() for word in words if not re.match(r'[a-zA-Z0-9\W]+', word)]
    # 결과 리스트에 추가
    result_list.extend(words)

# 단어 빈도수 계산
word_counts = Counter(result_list)

# 빈도수에 따라 정렬
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# 결과 출력
for word, count in sorted_words:
    if count > 1:
        print(f'{word}: {count}')