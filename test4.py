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
# WebDriver 초기화
driver = webdriver.Chrome()
keyword = input("입력")
# 페이지 열기
driver.get(f"https://search.11st.co.kr/pc/total-search?kwd={keyword}&tabId=TOTAL_SEARCH")

# XPath를 사용하여 해당 ID를 가진 요소 찾기
element_11 = driver.find_element(By.XPATH, "//*[@id='section_commonPrd']/div[2]/ul")

# 해당 요소 내의 상품명 요소들을 찾기
st11_results = element_11.find_elements(By.CLASS_NAME, "c-card-item__name")

# 상품명을 저장할 리스트 생성
all_words = []

# 각 상품 요소를 순회하며 상품명 가져오기
for product_element_11 in st11_results:
    product_name_11 = product_element_11.text
    if "상품명" in product_name_11:
        product_name_11 = product_name_11.split("상품명")[1].strip()
    # 상품명의 첫 번째 단어 삭제
    first_space_index = product_name_11.find(" ")
    if first_space_index != -1:
        product_name_11 = product_name_11[first_space_index+1:].strip()
    # 영어, 숫자, 특수기호를 제외한 문자열만 남기기
    product_name_11 = re.sub(r'[^가-힣\s]', '', product_name_11)
    # 상품명을 공백을 기준으로 단어로 분리하여 리스트에 추가
    words = product_name_11.split()
    all_words.extend(words)


# 각 단어의 빈도수 계산
word_counter = Counter(all_words)

# 빈도수에 따라 내림차순으로 정렬
sorted_word_counts = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)

# 정렬된 결과 출력
for word, count in sorted_word_counts:
    print(f"{word}: {count}")

# WebDriver 종료
driver.quit()
