# -*- coding: utf-8 -*-
'''
셀레니움 공식문서 : https://www.selenium.dev/documentation/webdriver/elements/information/#get-css-value
'''

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
load_dotenv()

'''
********인풋값을 설정해주세요.**************
1) .env파일을 생성하고, ID를 기재해주세요.       ex) ID=nickname
2) .env파일에 PW를 기재해주세요.               ex) PW=password
3) 아래 date_list에 원하시는 일자를 적어주세요.
4) 리움미술관 페이지에서 n번째에 있는 exhibit을 조회합니다.
+) 조회는 오후타임대만 합니다.
'''
####################### input value ###########################
id = os.environ.get("ID") #리움미술관 ID
pw = os.environ.get("PW") #리움미술관 PW
date_list = ['6','14'] #원하는 일자
time_list = ['10','11','13','16','17']
exhibit = 2 #원하는 전시회 (n번째)
n_month = False # 다음달 조회여부
###############################################################

date_cnt = 0
refresh_cnt = 1
def open_browser():
    driver = webdriver.Chrome("chromedriver")
    return driver


def login(driver, login_id, login_psw):
    driver.get('https://ticket.leeum.org/leeum/logoutProc.do')
    driver.implicitly_wait(5)
    driver.find_element(By.ID, 'memberid').send_keys(str(login_id))
    driver.find_element(By.ID, 'memberpw').send_keys(str(login_psw))
    driver.find_element(By.XPATH, '//*[@id="loginForm2"]/div/button').click()
    driver.implicitly_wait(5)
    return driver

def select_exhibit(n):
    driver.get('https://ticket.leeum.org/leeum/personal/exhibitList.do#none')
    driver.find_element(By.XPATH, f'//*[@id="exhlist_item_{n-1}"]').click()
    driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/a').click()
    driver.implicitly_wait(5)

def final_confirm():
    time.sleep(0.1)
    confrim_btn = driver.find_element(By.XPATH,'//*[@id="payConfirm"]')
    confrim_btn.click()
    print("예약이 확정되었습니다.")

    # 문자전송
    time.sleep(1)
    close_btn = driver.find_element(By.XPATH,'//*[@id="first_Giude"]/div/div/div[3]/button')
    close_btn.click()
    time.sleep(1)
    sms_btn = driver.find_element(By.XPATH,'//*[@id="container"]/div/div/div[2]/ul/li[2]/a')
    sms_btn.click()
    time.sleep(1)
    send_btn = driver.find_element(By.XPATH,'//*[@id="m_2"]/div/div/div[3]/button[2]')
    send_btn.click()
    print('문자전송완료')
    driver.quit()
    return 1

def click_refresh():
    global refresh_cnt

    refresh_btn = driver.find_element(By.XPATH, '//*[@id="step0"]/div/div/div[1]/ul[1]/li/button')
    refresh_btn.click()
    time.sleep(randint(2, 4))
    refresh_cnt += 1
    # print('재검색에 돌입합니다.')
    search_date()

def search_time():
    global date_cnt
    ########################################################
    driver.implicitly_wait(10)
    time.sleep(0.5)
    times = driver.find_elements(By.CLASS_NAME, 'select_time')
    for idx in range(len(times)):

        # print('idx::',idx+1, times[idx].text)
        for wt in time_list:
            if wt in times[idx].text:
                # print('wishTime:: ', wt)
                if '예약 가능' in times[idx].text:
                    # print('예약가능&&wishTime',idx)
                    if idx <4:
                        c1, c2 = 1, idx
                    else:
                        c1, c2 = 2, idx-4
                    # 여기는 예약가능한 열만 온다. (동시성 오류 배제)
                    print(wt,'시 예약 가능')
                    val, ticket = '', ''
                    val = driver.find_element(By.XPATH,f'//*[@id="time_body2"]/ul[{c1}]/li[{c2+1}]/a/input')
                    lefts = val.get_attribute("value")
                    n= int(lefts)
                    times[idx].click()
                    print(wt, '시 클릭 완료')
                    # time.sleep(3)
                    if n > 2: # 3
                        print('>>>>> 3매 예약')
                        ticket = driver.find_element(By.XPATH, f'//*[@id="peopleType01"]/label[4]')
                    elif n > 1: # 2매
                        print('>> 2매 예약')
                        ticket = driver.find_element(By.XPATH, f'//*[@id="peopleType01"]/label[3]')
                    else: # 1매
                        # print('>> 1매는 필요 없어')
                        # click_refresh()
                        ticket = driver.find_element(By.XPATH, f'//*[@id="peopleType01"]/label[2]')
                    ticket.click()
                    print('인원 선택 완료')

                    # time.sleep(10)
                    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[3]/div[2]/div[2]/a')
                    next_btn.click()
                    final_confirm()

    times.clear()
    # 예약은 가능하나, wishTime 포문 다 돌아도 없으면
    date_cnt += 1
    if date_cnt == len(date_list):
        print('===================refreshPoint')
        date_cnt = 0
        click_refresh()
    ########################################################


def search_date():
    global refresh_cnt, n_month
    # 달력 일자 선택
    if n_month:
        nm_btn = driver.find_element(By.ID, 'calendar_nextBtn')
        nm_btn.click()
        print('@ @ @@ @   next month btn is clicked!!')
        time.sleep(0.5)
        n_month = False

    print(f'----- {refresh_cnt}회차 조회를 시작합니다. -----')

    days = driver.find_elements(By.CLASS_NAME, 'select_day')
    time.sleep(0.2)
    for day in days:
        date = day.text
        if date in date_list:
            day.click()
            print(date,'일 선택 완료! 시간 조회 시작')
            time.sleep(0.3)
            search_time()
    return driver

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.headless = True
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    browser = webdriver.Chrome()
    # driver = open_browser()
    driver = login(browser, id, pw)
    select_exhibit(exhibit)

    search_date()