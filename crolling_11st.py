import subprocess
import sys
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

keyword = input("검색할 단어를 입력하세요: ")
url_11 = f"https://search.11st.co.kr/pc/total-search?kwd={keyword}&tabId=TOTAL_SEARCH"
response_11 = requests.get(url_11)
soup_11 = BeautifulSoup(response_11.text, 'html.parser')
items_11 = soup_11.select(".c-card-item__name")
my_list_11 = [item.text.strip() for item in items_11]

# 각 상품명의 첫 번째와 두 번째 단어를 제외하고 단어들 추출
words_11 = []
st11_product_results = []
for phrase in my_list_11:
    # 상품명을 공백을 기준으로 단어로 분리
    words_in_phrase_11 = phrase.split()
    # 첫 번째와 두 번째 단어를 제외한 나머지 단어들을 words 리스트에 추가
    words_11.extend(words_in_phrase_11[1:])

# 영어, 숫자, 특수기호를 공백으로 바꾸기
pattern = re.compile('[a-zA-Z0-9\W]+')
modified_list_11 = [pattern.sub(' ', word) for word in words_11]

# 모든 단어를 하나의 문자열로 합치기
combined_string_11 = ' '.join(modified_list_11)

# 단어 빈도수 계산
word_count_11 = Counter(combined_string_11.split())

# 빈도수가 1 이상인 단어들만 추출
filtered_words_11 = {word: count for word, count in word_count_11.items() if count > 1}

# 빈도수에 따라 내림차순으로 정렬
sorted_words_11 = sorted(filtered_words_11.items(), key=lambda x: x[1], reverse=True)

# 빈도수에 따라 결과 입력
for word_11, count_11 in sorted_words_11:
    if count_11 > 0:
        st11_product_results.append((word_11, count_11))

print(st11_product_results)
print(items_11)