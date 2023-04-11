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
date_list = ['20230415','20230422'] #원하는 일자
exhibit = 2 #원하는 전시회 (n번째)
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
    time.sleep(0.2)
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
    print('문자 전송 완료')
    driver.quit()
    return 1

def select_ticket(n):# 일반으로만 끊습니다. 조건 더 열기 귀찮,,
    flag = 0
    if n == 2:
        ticket_doub = driver.find_element(By.XPATH, f'//*[@id="peopleType01"]/label[3]')
        ticket_doub.click()
        flag = 2

    elif n == 1:
        ticket_mono = driver.find_element(By.XPATH, f'//*[@id="peopleType01"]/label[2]')
        ticket_mono.click()
        flag = 1

    else: print("selectTicket_Error !!")
    return flag

def click_refresh():
    global refresh_cnt

    refresh_btn = driver.find_element(By.XPATH, '//*[@id="step0"]/div/div/div[1]/ul[1]/li/button')
    refresh_btn.click()
    time.sleep(randint(3, 4))
    refresh_cnt += 1
    print('재검색에 돌입합니다.')
    search_date()

def search_time():
    global date_cnt
    time.sleep(0.1)
    print('2')
    for i in range(1,5):
        # test : 시간 무조건 오후거만 본다는 전제 (변경 원할 시 for문 range만 수정)
        time.sleep(0.2) # 런타임 에러 주포인트 2
        time_btn = driver.find_element(By.XPATH, f'//*[@id="time_body2"]/ul[2]/li[{i}]/a')
        time.sleep(0.2) # 런타임 에러 주포인트 3
        left_tickets = driver.find_element(By.XPATH, f'//*[@id="time_body2"]/ul[2]/li[{i}]/a/input')
        left = left_tickets.get_attribute("value")
        driver.implicitly_wait(10)
        if int(left) > 1:
            time_btn.click()
            driver.implicitly_wait(10)
            if select_ticket(2):
                print('=========final step2')
                time.sleep(0.1)
                next_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[3]/div[2]/div[2]/a')
                next_btn.click()
                final_confirm()
        elif int(left) == 1:
            time_btn.click()
            if select_ticket(1):
                print('=========final step1')
                driver.implicitly_wait(10)
                driver.quit()
                # next_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[3]/div[2]/div[2]/a')
                # next_btn.click()
                # final_confirm()
        elif int(left) == 0: # 리프레쉬 포인트
            date_cnt += 1
            print('잔여표::', left, '  //refresh까지:: ', date_cnt, ' :: ', (len(date_list)*4))
        else: print('알 수 없는 오류')
    if date_cnt == (len(date_list)*4):
        date_cnt = 0
        click_refresh()


def search_date():
    global refresh_cnt
    # 달력 일자 선택
    print(f'----- {refresh_cnt}회차 조회를 시작합니다. -----')

    time.sleep(0.6) # 런타임 에러 주포인트 1
    for week in range(1,7):
        # time.sleep(0.1)
        for day in range(1,8):
            time.sleep(0.1)
            td_class = driver.find_element(By.XPATH, f'//*[@id="calendar_body"]/tr[{week}]/td[{day}]')
            if td_class.get_attribute("class") == 'select_day': # 활성화된 날 체크
                time.sleep(0.1)
                td_date = driver.find_element(By.XPATH, f'//*[@id="calendar_body"]/tr[{week}]/td[{day}]/input[1]')
                driver.implicitly_wait(10)
                date_val = td_date.get_attribute("value")
                driver.implicitly_wait(5)
                print('1')
                time.sleep(0.1)
                if date_val in date_list:
                    btn = driver.find_element(By.XPATH, f'//*[@id="calendar_body"]/tr[{week}]/td[{day}]/a')
                    btn.click()
                    time.sleep(0.2)
                    print('select_date::', date_val, ' || date_lst::', date_list)
                    search_time()
    return driver

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # browser = webdriver.Chrome(options=options)

    browser = webdriver.Chrome()
    driver = open_browser()
    driver = login(driver, id, pw)
    select_exhibit(exhibit)

    search_date()