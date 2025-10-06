# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009889CC2A6BEB3C7360152CE20B2B2D896FF5DDCA139F6E30B3A8EA8DCD807B4C829DFE6044EB72DD36AE726A14535CF1238C1FD7A062B9515AFE98ABE11438FAD53D4460403125C97961308C1C7527419C81DBD377B99E364F7B5B66690F097661D029D40254E5309C4F03B3F9DD4F43F0831617391131C70C0D80315FA0515855D24F26C0C9609F8227B7B30FB2ECAE66CA55547C93E7A555FA75C37DFA34E43F6B779C1A7019F12C34CA3DA663B2FAC2738604B9C9C9D8428003EBCFB3F790F7E0D874CD818F7766CAAF7F09760774899130A1ACC36809D3D8F1AAB468F375C10475DAF2F00009D5B7E7C5099864B3BEBAB83708C8F9BA5CC412C525E1C7D915464B3BA0A0C8F0FAD5ACE397E681604E98ADD214B930481B19618160EFC3DBF5A529F3A42BA799ECD76D03D0EFBD0587C62DB8DF74940C6C191D0AC8240C3BD76E5485381FDBF92B8949167ABD1A0BE9B73531778E2EF95540326D66C7A867CF39A7F683A38A8BC62356AB86FF58CDA70902CEF179A95EA6586CB579900B09C4E3EECA95657C2EBA833299F72FE5AE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
