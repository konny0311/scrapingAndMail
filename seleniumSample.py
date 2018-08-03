from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import re

#スクレイピングのためのサンプル
driver = webdriver.Chrome(chromedriver path) #driver保存path入力
loginUrl = "URL" #開きたいurl
driver.get(loginUrl)
user = os.environ["userFrom"]
pin = ""
driver.find_element_by_id("username").send_keys(user)
driver.find_element_by_id("password").send_keys(pin)
driver.find_element_by_id("Login").send_keys(Keys.ENTER)

patternAuth = "url"
m = re.match(patternAuth, driver.current_url)
if m is not None:
    print("認証画面が出ました")
    #id認証画面
    code = input("メールに記載されているコードを入力してください。")
    driver.find_element_by_id("emc").send_keys(code)
    driver.find_element_by_id("save").send_keys(Keys.ENTER)

patternSuccess = "url"
m2 = re.match(patternSuccess, driver.current_url)
if m2 is not None:
    print("ログインできました")
print(driver.current_url)
driver.find_element_by_xpath("//a[@title='勤務表タブ']").click()
# sleep(5)
# driver.close()
