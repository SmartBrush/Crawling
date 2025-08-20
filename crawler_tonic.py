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

# 2. 접속할 URL (사용자 UI 페이지)
url = "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100040014&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=150"
driver.get(url)

# 3. 로딩 기다리기
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.prd_info"))
)

# 4. 제품 정보 추출
items = driver.find_elements(By.CSS_SELECTOR, "div.prd_info")

result = []
for item in items:
    try:
        brand = item.find_element(By.CSS_SELECTOR, "span.tx_brand").text.strip()
        name = item.find_element(By.CSS_SELECTOR, "p.tx_name").text.strip()
        price = item.find_element(By.CSS_SELECTOR, "span.tx_cur > span.tx_num").text.strip()
        image = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        result.append({
            "brand": brand,
            "name": name,
            "price": price,
            "image": image,
            "link": link
        })
    except Exception as e:
        print("오류 발생:", e)

# 5. JSON으로 저장
with open("products_tonic.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"{len(result)}개 상품 저장 완료")
driver.quit()