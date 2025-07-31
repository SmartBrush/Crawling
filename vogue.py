from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# 1. 크롬 옵션 설정
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

# 2. VOGUE 검색 결과 페이지 접속
url = "https://www.vogue.co.kr/search/탈모"
driver.get(url)

# 3. 첫 번째 로딩 대기
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ul#post_list > li"))
)

# ✅ 4. 스크롤 4회 반복 (스크롤 후 2초 대기)
for _ in range(4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 5. 기사 요소들 수집
items = driver.find_elements(By.CSS_SELECTOR, "ul#post_list > li")

result = []
for item in items:
    try:
        image = item.find_element(By.CSS_SELECTOR, "div.thum img").get_attribute("src")
        title = item.find_element(By.CSS_SELECTOR, "h3.s_tit").text.strip()
        category = item.find_element(By.CSS_SELECTOR, "p.category").text.strip()

        # 날짜 및 작성자 분리
        date_elem = item.find_element(By.CSS_SELECTOR, "p.date")
        date_full = date_elem.get_attribute("innerText").strip()
        date = date_full.split('\n')[0].strip()

        try:
            writer_text = date_elem.find_element(By.CSS_SELECTOR, "span").text.strip()
            writer = writer_text.replace("by", "").strip()
        except:
            writer = None

        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        result.append({
            "title": title,
            "category": category,
            "date": date,
            "writer": writer,
            "image": image,
            "link": link
        })

    except Exception as e:
        print("오류 발생:", e)
        
# 6. JSON 저장
with open("vogue_talmo_articles.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"{len(result)}개 기사 저장 완료")
driver.quit()
