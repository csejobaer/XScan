# js_render.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def js_render_test(url, payloads):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    for payload in payloads:
        test = url + "?x=" + payload
        try:
            driver.get(test)
            time.sleep(1)
            src = driver.page_source
            if payload in src:
                print(f"[DOM XSS POSSIBLE] {test}")
        except:
            continue
    driver.quit()
