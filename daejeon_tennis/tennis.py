import time
import telegram
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import timedelta

load_dotenv()
id = os.environ.get("ID")
pw = os.environ.get("PW")

import urllib.request
month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', \
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

url = 'https://www.djsiseol.or.kr'
date = urllib.request.urlopen(url).headers['Date']
# date = urllib.request.urlopen(url).headers['Date'][5:-4]
# print('date: ', date)
date = date.rstrip(' GMT')[5:]
date = datetime.strptime(date, '%d %b %Y %H:%M:%S') + timedelta(hours=9)
print('date : ', date)
# d, m, y, hour, min, sec = date[:2], month[date[3:6]], date[7:11], date[12:14], date[15:17], date[18:]
# print(f'[{url}]의 서버시간\n{y}년 {m}월 {d}일 {hour}시 {min}분 {sec}초')

def login(driver, login_id, login_pw):
    login_url = 'https://www.djsiseol.or.kr/portal/login.asp?site=reserve'
    driver.get(login_url)
    driver.implicitly_wait(5)
    driver.find_element(By.ID, 'user_id').send_keys(str(login_id))
    driver.find_element(By.ID, 'password').send_keys(str(login_pw))
    driver.find_element(By.CLASS_NAME, 'sub_login_bt').click()
    driver.implicitly_wait(5)
    return driver

def search_date():
    search_date_url = 'https://www.djsiseol.or.kr/reserve/sub0201_02.asp?selectDate=2023.06.09&selectYear=2023&selectMonth=06&siseol_cd=HS&usss_cd=HS_TC3&session_user=com32350&holidayYn=n&holidayYname=&closedCheck=n&use_tm=2&use_cnt=1&select_check=07%3A00-08%3A00-0&select_check=08%3A00-09%3A00-0&select_check=09%3A00-10%3A00-0&select_check=10%3A00-11%3A00-0&select_check=11%3A00-12%3A00-0&select_check=14%3A00-15%3A00-0&select_check=15%3A00-16%3A00-0&select_check=16%3A00-17%3A00-0&select_check=17%3A00-18%3A00-0&select_check=18%3A00-19%3A00-0&select_check=19%3A00-20%3A00-0&select_check=20%3A00-21%3A00-0&select_check=21%3A00-22%3A00-0&spa_fee=&spa_fee_type=D'
    driver.get(search_date_url)
    test = driver.find_element(By.XPATH,'//*[@id="calendar"]/div[1]/div[1]/div[2]/table/tbody/tr[3]/td[3]')
    print("<> > > > > > >testText :: ",test.text)
    # '//*[@id="calendar"]/div[1]/div[1]/div[2]/table/tbody/tr[3]/td[2]/span[4]'
    time.sleep(3)
    return driver
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.headless = True
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    browser = webdriver.Chrome()
    driver = login(browser, id, pw)
    search_date()

