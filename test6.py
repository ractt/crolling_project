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
    #검색 단어 받기
    keyword = entry.get()
    # 크롬 옵션 설정
    chrome_options = Options()
    # 시크릿 모드 활성화
    chrome_options.add_argument("--incognito")  
    browser = webdriver.Chrome(options=chrome_options)
    
    
    #사이트 검색
    
    # 포셀 검색
    browser.get('http://forsell.co.kr/login/')
    time.sleep(2)
    id_input_forsell = browser.find_element(By.NAME, 'username')
    pw_input_forsell = browser.find_element(By.NAME, 'password')
    id_input_forsell.send_keys('aaa10130')
    pw_input_forsell.send_keys('tjgktjd123') #사용자화 필요함.(개인 아이디, 비번)
    login_button_forsell = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button_forsell.click()
    time.sleep(5)
    SearchTab_forsell = browser.find_element(By.LINK_TEXT, '연관키워드 검색')
    SearchTab_forsell.click()
    time.sleep(1)
    # 광고가 닫히는 동작
    try:
    # 아무 곳이나 한 번 클릭하여 광고를 닫음
        action_offad_forsell = ActionChains(browser)
    # 아무 곳이나 한 번 클릭하도록 설정
        action_offad_forsell.move_by_offset(100, 100).click().perform()
        
    except NoSuchElementException:
    # 해당 요소가 없는 경우 예외 처리
        print("닫기 없음________________________________________")
        pass
    time.sleep(4)
    #키워드 검색
    keyword_input_forsell = browser.find_element(By.ID, 'searchKeyword')
    keyword_input_forsell.send_keys(keyword)
    search_button_forsell = browser.find_element(By.ID, 'searchBtn')
    search_button_forsell.click()
    time.sleep(7)
    coupang1_inforsell = browser.find_element(By.ID, 'coupangReKeyword')
    coupang2_inforsell = browser.find_element(By.ID, 'coupangAutoKeyword')
    coupang1_inforsell.click()
    coupang2_inforsell.click()
    time.sleep(2)
    copy_forsell_keyword = browser.find_element(By.ID, 'copyKeyword')
    copy_forsell_keyword.click()
    clipboard_content_forsell = pyperclip.paste()
    result_forsell = clipboard_content_forsell.split(',')

    # 네이버 쇼핑 검색
    browser.get(f'https://search.shopping.naver.com/search/all?query={keyword}')
    time.sleep(2)
    # 스크롤 전 높이 
    before_h_naver = browser.execute_script("return window.scrollY")
    # 모든 상품명을 저장할 리스트 생성
    result_naver_raw = []

    # 무한 스크롤
    while True:
    # 맨 아래로 스크롤 내린다.
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # 스크롤 사이 페이지 로딩 시간 
        time.sleep(1)
    # 스크롤 후 높이 
        after_h_naver = browser.execute_script("return window.scrollY")
    # 스크롤 높이가 변하지 않으면 더 이상 스크롤할 필요 없음
        if after_h_naver == before_h_naver:
            break
    # 스크롤 이전 높이 업데이트
        before_h_naver = after_h_naver
    
    # 현재 페이지의 모든 상품명을 가져와서 리스트에 추가
    content_naver = browser.find_elements(By.CLASS_NAME, 'product_title__Mmw2K')
    for element_naver in content_naver:
        result_naver_raw.append(element_naver.text)

    # 지마켓 검색
    url_gmarket = f"https://browse.gmarket.co.kr/search?keyword={keyword}"
    response_gmarket = requests.get(url_gmarket)
    soup_gmarket = BeautifulSoup(response_gmarket.text, 'html.parser')
    items_gmarket_text_selected = soup_gmarket.select(".text__item")
    results_gmarket_raw = [item_gmarket_element.text.strip() for item_gmarket_element in items_gmarket_text_selected]
    browser.quit()


    #검색 결과 수정
    
    #네이버 
    result_naver_non_sorted = []
    result_naver = []
    # 단어 추출 및 정리
    for product_naver_raw in result_naver_raw:
        # 첫 번째 단어를 제외한 단어들 추출 first deleted
        products_naver_non_first = product_naver_raw.split()[1:]
        # 영어, 숫자, 특수기호를 포함한 단어 제거 및 소문자로 변환 non korean deleted 
        product_naver_organization = [re.sub(r'[^a-zA-Z가-힣]', '', product_naver_non_korean_deleted).lower() for product_naver_non_korean_deleted in products_naver_non_first if not re.match(r'[a-zA-Z0-9\W]+', product_naver_non_korean_deleted)]
        # 결과 리스트에 추가
        result_naver_non_sorted.extend(product_naver_organization)

    # 단어 빈도수 계산
    results_counted_naver = Counter(result_naver_non_sorted)

    # 빈도수에 따라 정렬
    results_sorted_naver = sorted(results_counted_naver.items(), key=lambda x: x[1], reverse=True)

    # 빈도수에 따라 결과 저장
    for word_naver, count_naver in results_sorted_naver:
        if count_naver > 0:
            result_naver.append((word_naver, count_naver))
    
    #지마켓  
    result_gmarket_non_sorted = []
    result_gmarket = []
    # 단어 추출 및 정리
    for product_gmarket_raw in results_gmarket_raw:
        # 첫 번째 단어를 제외한 단어들 추출 first deleted
        products_gmarket_non_first = product_gmarket_raw.split()#[2:]
        # 영어, 숫자, 특수기호를 포함한 단어 제거 및 소문자로 변환 non korean deleted 
        product_gmarket_organization = [re.sub(r'[^a-zA-Z가-힣]', '', product_gmarket_non_korean_deleted).lower() for product_gmarket_non_korean_deleted in products_gmarket_non_first if not re.match(r'[a-zA-Z0-9\W]+', product_gmarket_non_korean_deleted)]
        # 결과 리스트에 추가
        result_gmarket_non_sorted.extend(product_gmarket_organization)
        
    # 단어 빈도수 계산
    results_counted_gmarket = Counter(result_gmarket_non_sorted)

    # 빈도수에 따라 정렬
    results_sorted_gmarket = sorted(results_counted_gmarket.items(), key=lambda x: x[1], reverse=True)

    # 빈도수에 따라 결과 저장
    for word_gmarket, count_gmarket in results_sorted_gmarket:
        if count_gmarket > 0:
            result_gmarket.append((word_gmarket, count_gmarket))
    

    # 결과 출력
    
    result_text_n.delete(1.0, tk.END)
    result_text_n.insert(tk.END, "네이버 쇼핑 검색 결과:\n")
    for word, count in result_naver:
        # 괄호와 작은 따옴표 제거 후 출력
        word = word.strip("(),'") 
        result_text_n.insert(tk.END, f"{word}: {count}\n")
    result_text_g.insert(tk.END, "\n지마켓 검색 결과:\n")
    for product_name, count in result_gmarket:
        product_name = product_name.strip("(),'") 
        result_text_g.insert(tk.END, f"- {product_name}: {count}\n")
    result_text_f.insert(tk.END, "\n포셀 검색 결과:\n")
    for keyword in result_forsell:
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