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

# 네이버 쇼핑 검색 함수
def search_naver(keyword, browser):
    browser.get(f'https://search.shopping.naver.com/search/all?query={keyword}')
    time.sleep(2)
    before_h_naver = browser.execute_script("return window.scrollY")
    result_naver_raw = []

    while True:
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)
        after_h_naver = browser.execute_script("return window.scrollY")

        if after_h_naver == before_h_naver:
            break

        before_h_naver = after_h_naver

    content_naver = browser.find_elements(By.CLASS_NAME, 'product_title__Mmw2K')
    for element_naver in content_naver:
        result_naver_raw.append(element_naver.text)

    return result_naver_raw

#11번가 검색 함수
def search_11st(keyword, browser):
    browser.get(f'https://search.11st.co.kr/pc/total-search?kwd={keyword}&tabId=TOTAL_SEARCH')
    time.sleep(2)
    # 모든 상품명을 저장할 리스트 생성
    result_11st_raw = []

    # XPath를 사용하여 해당 ID를 가진 요소 찾기
    element_11 = browser.find_element(By.XPATH, "//*[@id='section_commonPrd']/div[2]/ul")
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
# 지마켓 검색 함수
def search_gmarket(keyword):
    url_gmarket = f"https://browse.gmarket.co.kr/search?keyword={keyword}"
    response_gmarket = requests.get(url_gmarket)
    soup_gmarket = BeautifulSoup(response_gmarket.text, 'html.parser')
    items_gmarket_text_selected = soup_gmarket.select(".text__item")
    results_gmarket_raw = [item_gmarket_element.text.strip() for item_gmarket_element in items_gmarket_text_selected]
    return results_gmarket_raw

# 검색 함수
def search(event=None):
    keyword = entry.get()
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    browser = webdriver.Chrome(options=chrome_options)

    try:
        # 포셀 사이트 로그인 및 검색
        browser.get('http://forsell.co.kr/login/')
        time.sleep(2)
        id_input_forsell = browser.find_element(By.NAME, 'username')
        pw_input_forsell = browser.find_element(By.NAME, 'password')
        id_input_forsell.send_keys('aaa10130')
        pw_input_forsell.send_keys('tjgktjd123')
        login_button_forsell = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button_forsell.click()
        time.sleep(5)
        SearchTab_forsell = browser.find_element(By.LINK_TEXT, '연관키워드 검색')
        SearchTab_forsell.click()
        time.sleep(1)

        try:
            # 광고 닫기
            action_offad_forsell = ActionChains(browser)
            action_offad_forsell.move_by_offset(100, 100).click().perform()
        except NoSuchElementException:
            print("닫기 없음________________________________________")
            pass

        time.sleep(4)
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
        result_naver_raw = search_naver(keyword, browser)
        
        # 지마켓 검색
        results_gmarket_raw = search_gmarket(keyword)

        result_naver_non_sorted = []
        result_naver = []
        for product_naver_raw in result_naver_raw:
            products_naver_non_first = product_naver_raw.split()[1:]
            product_naver_organization = [re.sub(r'[^a-zA-Z가-힣]', '', product_naver_non_korean_deleted).lower() for product_naver_non_korean_deleted in products_naver_non_first if not re.match(r'[a-zA-Z0-9\W]+', product_naver_non_korean_deleted)]
            result_naver_non_sorted.extend(product_naver_organization)

        results_counted_naver = Counter(result_naver_non_sorted)
        results_sorted_naver = sorted(results_counted_naver.items(), key=lambda x: x[1], reverse=True)

        for word_naver, count_naver in results_sorted_naver:
            if count_naver > 0:
                result_naver.append((word_naver, count_naver))

        result_gmarket_non_sorted = []
        result_gmarket = []
        for product_gmarket_raw in results_gmarket_raw:
            products_gmarket_non_first = product_gmarket_raw.split()#[2:]
            product_gmarket_organization = [re.sub(r'[^a-zA-Z가-힣]', '', product_gmarket_non_korean_deleted).lower() for product_gmarket_non_korean_deleted in products_gmarket_non_first if not re.match(r'[a-zA-Z0-9\W]+', product_gmarket_non_korean_deleted)]
            result_gmarket_non_sorted.extend(product_gmarket_organization)

        results_counted_gmarket = Counter(result_gmarket_non_sorted)
        results_sorted_gmarket = sorted(results_counted_gmarket.items(), key=lambda x: x[1], reverse=True)

        for word_gmarket, count_gmarket in results_sorted_gmarket:
            if count_gmarket > 0:
                result_gmarket.append((word_gmarket, count_gmarket))

        # 검색 결과 출력
        result_text_n.delete(1.0, tk.END)
        result_text_n.insert(tk.END, "네이버 쇼핑 검색 결과:\n")
        for word, count in result_naver:
            word = word.strip("(),'") 
            result_text_n.insert(tk.END, f"{word}: {count}\n")
        result_text_g.delete(1.0, tk.END)
        result_text_g.insert(tk.END, "\n지마켓 검색 결과:\n")
        for product_name, count in result_gmarket:
            product_name = product_name.strip("(),'") 
            result_text_g.insert(tk.END, f"- {product_name}: {count}\n")
        result_text_f.delete(1.0, tk.END)
        result_text_f.insert(tk.END, "\n포셀 검색 결과:\n")
        for keyword in result_forsell:
            result_text_f.insert(tk.END, f"- {keyword}\n")
    finally:
        browser.quit()

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("검색 앱")
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
