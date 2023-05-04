# -*- coding: utf-8 -*-
import time
import telegram
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import os

load_dotenv()

id = os.environ.get("ID")
pw = os.environ.get("PW")
nm = os.environ.get("NAME")
start = '김천구미'
end = '수서'
yyyymmdd = '20230507'
t = '12' # only 짝수
num_trains_to_check=4
want_reserve=False
def open_browser():
    driver = webdriver.Chrome("chromedriver")
    return driver


def login(driver, login_id, login_psw):
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    driver.implicitly_wait(15)
    driver.find_element(By.ID, 'srchDvNm01').send_keys(str(login_id))
    driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(str(login_psw))
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
    driver.implicitly_wait(5)
    return driver

###################################################  num_trains_to_check : 조회리스트 사이즈, want_reserve : 예약대기 기능 활성화 여부
def search_train(driver, dpt_stn, arr_stn, dpt_dt, dpt_tm):
    global num_trains_to_check, want_reserve
    is_booked = False # 예약 완료 되었는지 확인용
    cnt_refresh = 0 # 새로고침 회수 기록

    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do') # 기차 조회 페이지로 이동
    driver.implicitly_wait(5)
    # 출발지/도착지/출발날짜/출발시간 입력
    elm_dpt_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
    elm_dpt_stn.clear()
    elm_dpt_stn.send_keys(dpt_stn) # 출발지
    elm_arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
    elm_arr_stn.clear()
    elm_arr_stn.send_keys(arr_stn) # 도착지
    elm_dptDt = driver.find_element(By.ID, "dptDt")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
    Select(driver.find_element(By.ID,"dptDt")).select_by_value(dpt_dt) # 출발날짜
    elm_dptTm = driver.find_element(By.ID, "dptTm")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
    Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(dpt_tm) # 출발시간

    print("기차를 조회합니다")
    print(f"출발역:{dpt_stn} , 도착역:{arr_stn}\n날짜:{dpt_dt}, 시간: {dpt_tm}시 이후\n{num_trains_to_check}개의 기차 중 예약")
    print(f"예약 대기 사용: {want_reserve}")

    driver.find_element(By.XPATH, "//input[@value='조회하기']").click() # 조회하기 버튼 클릭
    driver.implicitly_wait(5)
    time.sleep(1)
    # bot = telegram.Bot(token='5949014838:AAEiIChMcVgFuCO3ZPr6AFhe03o2z745t-k')
    # bot.send_message(chat_id=-721609842, text=f"{nm}님의 {end}행/{t}시 이후 {num_trains_to_check}개의 SRT 조회를 시작합니다.")
    while True:
        for i in range(1, num_trains_to_check+1):
            standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
            reservation = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text
            # print('======================= log1 ============= > > > >>', standard_seat)
            if "예약하기" in standard_seat:
                print("예약 가능 클릭")
                driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
                driver.implicitly_wait(3)

                if driver.find_elements(By.ID, 'isFalseGotoMain'):
                    is_booked = True
                    print("예약 성공")
                    bot = telegram.Bot(token='5949014838:AAEiIChMcVgFuCO3ZPr6AFhe03o2z745t-k')
                    bot.send_message(chat_id=-721609842, text=f"{nm}님의 {end}행 기차가 예약되었습니다 결제하세요")
                    break
                else:
                    print("잔여석 없음. 다시 검색")
                    driver.back()  # 뒤로가기
                    driver.implicitly_wait(5)

            if want_reserve:
                if "신청하기" in reservation:
                    driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8) > a").click()
                    is_booked = True
                    print("예약 대기 완료")
                    bot = telegram.Bot(token='5949014838:AAEiIChMcVgFuCO3ZPr6AFhe03o2z745t-k')
                    bot.send_message(chat_id="-721609842", text=f"{nm}님의 {end}행 기차 예약 대기가 신청되었습니다. 확인해주세요.")
                    break

        if not is_booked:
            time.sleep(randint(1, 3)) #2~4초 랜덤으로 기다리기

            # 다시 조회하기
            submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
            driver.execute_script("arguments[0].click();", submit)
            cnt_refresh += 1
            print(f"새로고침 {cnt_refresh}회")
            driver.implicitly_wait(10)
            time.sleep(0.5)
        else:
            break
    return driver

### ID, PW : SRT 계정
### 23행 search_train에서 세부 조정
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # browser = webdriver.Chrome(options=options)
    browser = webdriver.Chrome()
    driver = open_browser()
    driver = login(driver, id, pw)
    search_train(driver, start, end, yyyymmdd, t) #기차 출발 시간은 반드시 짝수