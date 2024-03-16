import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import pyperclip
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# 사용자로부터 검색어 입력 받기
search_query = input("검색어를 입력하세요: ")
# 브라우저 생성
browser = webdriver.Chrome()
# 웹 사이트 열기
browser.get(f'https://search.11st.co.kr/pc/total-search?kwd={search_query}&tabId=TOTAL_SEARCH')

time.sleep(3)
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
    
    
    
#일반 상품 추출 xpath 이용할 듯
    
    
# 현재 페이지의 모든 상품명을 가져와서 리스트에 추가
product_elements = browser.find_elements(By.CLASS_NAME, 'c-card-item__name')







for element in product_elements:
    product_names.append(element.text)

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

# 빈도수에 따라 결과 출력
for word, count in sorted_words:
    if count > 0:
        print(f'{word}: {count}')