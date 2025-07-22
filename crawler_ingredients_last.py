# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json
# import time
# from selenium.common.exceptions import TimeoutException


# def load_json_top5():
#     with open("products_conditioner.json", encoding='utf-8') as f:
#         return json.load(f)[:5]


# def save_json(data, filename):
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)


# def setup_driver():
#     options = Options()
#     options.add_experimental_option("excludeSwitches", ["enable-logging"])
#     options.add_experimental_option("useAutomationExtension", False)
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

#     driver = webdriver.Chrome(options=options)

#     # Cloudflare 탐지 우회용 navigator.webdriver 삭제
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined
#         });
#         """
#     })
#     return driver


# def extract_ingredients_with_fresh_driver(url):
#     driver = setup_driver()
#     try:
#         driver.get(url)
#         time.sleep(2)

#         # 구매정보 탭 클릭
#         buy_info_btn = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "a.goods_buyinfo"))
#         )
#         buy_info_btn.click()

#         # 반복 스크롤 다운 (표 로딩 유도)
#         for _ in range(5):
#             driver.execute_script("window.scrollBy(0, 500);")
#             time.sleep(1)

#         # 디버깅용 HTML 저장
#         with open("debug_page.html", "w", encoding="utf-8") as f:
#             f.write(driver.page_source)

#         # 표에서 '성분' 항목 찾기 (전성분이라는 항목일 수도 있음)
#         td = WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.XPATH, "//th[contains(text(), '성분')]/following-sibling::td"))
#         )
#         return td.text.strip()

#     except TimeoutException:
#         print(f"❌ [Timeout] 성분 정보를 찾지 못함: {url}")
#         return ""
#     except Exception as e:
#         print(f"❌ [오류 발생] ({url}): {e}")
#         return ""
#     finally:
#         driver.quit()


# def main():
#     data = load_json_top5()
#     success, failed = [], []

#     for idx, item in enumerate(data):
#         full_url = item["link"] if item["link"].startswith("http") else "https://www.oliveyoung.co.kr" + item["link"]
#         print(f"[{idx+1}/5] {item['name']} 성분 가져오는 중...")

#         ingredients = extract_ingredients_with_fresh_driver(full_url)
#         item["ingredients"] = ingredients

#         if ingredients:
#             success.append(item)
#         else:
#             failed.append(item)

#         # Cloudflare 완화용 딜레이
#         time.sleep(2)

#     save_json(success, "products_conditioner_top5_with_ingredients.json")
#     save_json(failed, "products_conditioner_top5_failed.json")
#     print("✅ 저장 완료")


# if __name__ == "__main__":
#     main()



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time


def load_json_top5():
    with open("products_conditioner.json", encoding='utf-8') as f:
        return json.load(f)[:5]

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def setup_driver():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    # Cloudflare 우회용
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    })
    return driver

def extract_ingredients_with_fresh_driver(url):
    driver = setup_driver()
    try:
        driver.get(url)
        time.sleep(2)

        # "구매정보" 탭 클릭
        buy_info_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.goods_buyinfo"))
        )
        buy_info_btn.click()

        # 콘텐츠 로딩 기다리기 (최대 20초)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[contains(text(), '화장품법에 따라 기재해야 하는 모든 성분')]")
            )
        )

        # 성분 텍스트 추출
        dd = driver.find_element(By.XPATH, "//dt[contains(text(), '화장품법에 따라 기재해야 하는 모든 성분')]/following-sibling::dd[1]")
        return dd.text.strip()

    except TimeoutException:
        print(f"❌ [Timeout] 성분 정보를 찾지 못함: {url}")
        return ""
    except Exception as e:
        print(f"❌ [오류 발생] ({url}): {e}")
        return ""
    finally:
        driver.quit()

def main():
    data = load_json_top5()
    success, failed = [], []

    for idx, item in enumerate(data):
        full_url = item["link"] if item["link"].startswith("http") else "https://www.oliveyoung.co.kr" + item["link"]
        print(f"[{idx+1}/5] {item['name']} 성분 가져오는 중...")

        ingredients = extract_ingredients_with_fresh_driver(full_url)
        item["ingredients"] = ingredients

        if ingredients:
            success.append(item)
        else:
            failed.append(item)

        time.sleep(2)  # Cloudflare 차단 방지용

    save_json(success, "products_conditioner_top5_with_ingredients.json")
    save_json(failed, "products_conditioner_top5_failed.json")
    print("✅ 저장 완료")

if __name__ == "__main__":
    main()