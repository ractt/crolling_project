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

def search(event=None):
    keyword = entry.get()
    # 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # 시크릿 모드 활성화
    browser = webdriver.Chrome(options=chrome_options)
    # 포셀 검색
    browser.get('http://forsell.co.kr/login/')
    time.sleep(2)
    id_input = browser.find_element(By.NAME, 'username')
    pw_input = browser.find_element(By.NAME, 'password')
    id_input.send_keys('aaa10130')
    pw_input.send_keys('tjgktjd123')
    login_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    time.sleep(5)
    SearchTab = browser.find_element(By.LINK_TEXT, '연관키워드 검색')
    SearchTab.click()
    time.sleep(3)
    # 광고가 닫히는 동작
    try:
    # 아무 곳이나 한 번 클릭하여 광고를 닫음
        action = ActionChains(browser)
    # 아무 곳이나 한 번 클릭하도록 설정
        action.move_by_offset(100, 100).click().perform()
        
    except NoSuchElementException:
    # 해당 요소가 없는 경우 예외 처리
        print("닫기 없음________________________________________")
        pass
    time.sleep(4)
    keyword_input = browser.find_element(By.ID, 'searchKeyword')
    keyword_input.send_keys(keyword)
    search_button = browser.find_element(By.ID, 'searchBtn')
    search_button.click()
    time.sleep(7)
    coupang1 = browser.find_element(By.ID, 'coupangReKeyword')
    coupang2 = browser.find_element(By.ID, 'coupangAutoKeyword')
    coupang1.click()
    coupang2.click()
    time.sleep(2)
    copy = browser.find_element(By.ID, 'copyKeyword')
    copy.click()
    clipboard_content = pyperclip.paste()
    forsell_keywords = clipboard_content.split(',')
    

    # 네이버 쇼핑 검색
    
    browser.get('https://shopping.naver.com/')
    time.sleep(2)
    search_box = browser.find_element(By.CLASS_NAME, '_searchInput_search_text_3CUDs')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    # 스크롤 전 높이 
    before_h = browser.execute_script("return window.scrollY")
    # 모든 상품명을 저장할 리스트 생성
    naver_product_names = []

    # 무한 스크롤
    while True:
    # 맨 아래로 스크롤 내린다.
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    
    # 스크롤 사이 페이지 로딩 시간 
        time.sleep(1)
    
    # 스크롤 후 높이 
        after_h = browser.execute_script("return window.scrollY")
    
    # 스크롤 높이가 변하지 않으면 더 이상 스크롤할 필요 없음
        if after_h == before_h:
            break
    
    # 스크롤 이전 높이 업데이트
        before_h = after_h
    
    # 현재 페이지의 모든 상품명을 가져와서 리스트에 추가
    naver_results = browser.find_elements(By.CLASS_NAME, 'product_title__Mmw2K')
    for element_n in naver_results:
        naver_product_names.append(element_n.text)
        


    # 지마켓 검색
    url_g = f"https://browse.gmarket.co.kr/search?keyword={keyword}"
    response_g = requests.get(url_g)
    soup_g = BeautifulSoup(response_g.text, 'html.parser')
    items_g = soup_g.select(".text__item")
    gmarket_results = [item.text.strip() for item in items_g]

    browser.quit()


    #검색 결과 수정
    #네이버 
    # 결과 리스트
    result_list_n = []
    naver_product_results = []
    # 단어 추출 및 정리
    for product_n in naver_product_names:
        # 첫 번째 단어를 제외한 단어들 추출
        words_n = product_n.split()[1:]
        # 영어, 숫자, 특수기호를 포함한 단어 제거 및 소문자로 변환
        words_n = [re.sub(r'[^a-zA-Z가-힣]', '', word_n).lower() for word_n in words_n if not re.match(r'[a-zA-Z0-9\W]+', word_n)]
        # 결과 리스트에 추가
        result_list_n.extend(words_n)

    # 단어 빈도수 계산
    word_counts_n = Counter(result_list_n)

    # 빈도수에 따라 정렬
    sorted_words_n = sorted(word_counts_n.items(), key=lambda x: x[1], reverse=True)

    # 빈도수에 따라 결과 출력
    for word_n, count_n in sorted_words_n:
        if count_n > 0:
            naver_product_results.append((word_n, count_n))
    
    #지마켓
    # 각 상품명의 첫 번째와 두 번째 단어를 제외하고 단어들 추출
    words_g = []
    gmarket_product_results = []
    for phrase in gmarket_results:
        # 상품명을 공백을 기준으로 단어로 분리
        words_in_phrase = phrase.split()
        # 첫 번째와 두 번째 단어를 제외한 나머지 단어들을 words 리스트에 추가
        words_g.extend(words_in_phrase[2:])

    # 영어, 숫자, 특수기호를 공백으로 바꾸기
    pattern = re.compile('[a-zA-Z0-9\W]+')
    modified_list = [pattern.sub(' ', word) for word in words_g]

    # 모든 단어를 하나의 문자열로 합치기
    combined_string = ' '.join(modified_list)

    # 단어 빈도수 계산
    word_count = Counter(combined_string.split())

    # 빈도수가 1 이상인 단어들만 추출
    filtered_words = {word: count for word, count in word_count.items() if count > 1}

    # 빈도수에 따라 내림차순으로 정렬
    sorted_words_g = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)
    
    # 빈도수에 따라 결과 입력
    for word_g, count_g in sorted_words_g:
        if count_g > 0:
            gmarket_product_results.append((word_g, count_g))
    

    # 결과 출력
    result_text_n.delete(1.0, tk.END)
    result_text_n.insert(tk.END, "네이버 쇼핑 검색 결과:\n")
    for word, count in naver_product_results:
        # 괄호와 작은 따옴표 제거 후 출력
        word = word.strip("(),'") 
        result_text_n.insert(tk.END, f"{word}: {count}\n")
    result_text_g.insert(tk.END, "\n지마켓 검색 결과:\n")
    for product_name, count in gmarket_product_results:
        product_name = product_name.strip("(),'") 
        result_text_g.insert(tk.END, f"- {product_name}: {count}\n")
    result_text_f.insert(tk.END, "\n포셀 검색 결과:\n")
    for keyword in forsell_keywords:
        result_text_f.insert(tk.END, f"- {keyword}\n")

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("검색 앱")

# 창 크기 조절
root.geometry("1500x800")

# 라벨과 엔트리 위젯 생성
label = ttk.Label(root, text="검색어를 입력하세요:")
label.grid(row=0, column=0, padx=5, pady=5)

entry = ttk.Entry(root, width=30)
entry.grid(row=0, column=1, padx=5, pady=5)

# 검색 버튼 생성
search_button = ttk.Button(root, text="검색", command=search)
search_button.grid(row=0, column=2, padx=5, pady=5)

# 네이버 검색 결과를 표시할 텍스트 박스 생성
result_text_n = tk.Text(root, height=20, width=40)
result_text_n.grid(row=1, column=0, padx=5, pady=5)

# 지마켓 검색 결과를 표시할 텍스트 박스 생성
result_text_g = tk.Text(root, height=20, width=40)
result_text_g.grid(row=1, column=1, padx=5, pady=5)

# 포셀 검색 결과를 표시할 텍스트 박스 생성
result_text_f = tk.Text(root, height=20, width=40)
result_text_f.grid(row=1, column=2, padx=5, pady=5)


# 텍스트의 글자 크기 설정
result_text_n.config(font=("Courier", 15))
result_text_g.config(font=("Courier", 15))
result_text_f.config(font=("Courier", 15))

# 엔터 키를 누르면 검색 버튼 클릭
root.bind('<Return>', search)

# GUI 실행
root.mainloop()
