import re

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

URL_LOGIN_PAGE = "https://www.sbisec.co.jp/ETGate/"
URL_IPO_LIST = "https://m.sbisec.co.jp/oeliw011?type=21"


class Ipo:
    def __init__(self, headless=True, incognito=False, timeout=10):
        option = Options()
        if headless:
            option.add_argument("--headless")
        if incognito:
            option.add_argument("--incognito")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        self.timeout = timeout

    def login(self, user_id: str, user_password: str, trading_password: str) -> bool:
        self.trading_password = trading_password
        self.driver.get(URL_LOGIN_PAGE)
        try:  # ページロード完了まで待機
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.NAME, "ACT_login")))
        except TimeoutException as e:
            print(f"ログインページの表示に失敗しました。({e})")
        self.driver.find_element(By.NAME, "user_id").send_keys(user_id)
        self.driver.find_element(By.NAME, "user_password").send_keys(user_password)
        self.driver.find_element(By.NAME, "ACT_login").click()
        try:  # ページロード完了まで待機
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, "logoutM")))
        except TimeoutException as e:
            print(f"ログインに失敗しました。({e})")
            return False
        else:
            print("SBI証券にログインしました。")
        return True

    def logout(self):
        self.driver.find_element(By.ID, "logoutM").click()
        print("SBI証券からログアウトしました。")

    def order_all(self):
        while True:
            self.driver.get(URL_IPO_LIST)
            try:
                self.driver.find_element(By.XPATH, '//img[@alt="申込"]').click()
            except NoSuchElementException:
                print("申し込みできる銘柄がありません。")
                break
            else:
                try:
                    WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.NAME, "suryo")))
                except TimeoutException as e:
                    print(f"ページ読み込みに失敗しました。({e})")
                    break
                else:
                    self.driver.find_element(By.CLASS_NAME, "lbody").text
                    self.driver.find_element(By.NAME, "suryo").send_keys("100")
                    self.driver.find_element(By.ID, "strPriceRadio").click()
                    self.driver.find_element(By.NAME, "tr_pass").send_keys(self.trading_password)
                    self.driver.find_element(By.NAME, "order_kakunin").click()
                    try:
                        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.NAME, "order_btn")))
                        self.driver.find_element(By.NAME, "order_btn").click()
                    except TimeoutException as e:
                        print(f"抽選申し込みに失敗しました。({e})")
                    except NoSuchElementException as e:
                        print(f"抽選申し込みに失敗しました。({e})")
                    else:
                        print("抽選申し込みが完了しました。")

    def __del__(self):
        self.driver.quit()
