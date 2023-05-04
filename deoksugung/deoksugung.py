import time
import telegram
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

date_list = [
    '2023-05-06',
    '2023-05-07'
]
n_list = [
    2,4,6
]
cnt = 0
def search():
    global cnt
    cnt+=1
    print(f'= = >> {cnt}회차 조회를 시작합니다.')
    driver.get('https://www.deoksugung.go.kr/schedule/list?scheduleid=SB')
    for date in date_list:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, date))
        ).click()
        time.sleep(0.1)
        print(f'-- date : {date} --')
        for n in n_list:
            tmp = ''
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,f'//*[@id="schedule_listbydate"]/table/tbody/tr[{n}]/td[4]'))
            )
            tmp = element.text
            time.sleep(0.3)
            print(f'@@ {n}회차 element :: {tmp}')
            if tmp == '신청하기':
                # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@ == >> 신 청 가 능 ')
                bot = telegram.Bot(token='6280492134:AAGYt7Go7X18r_9TZp32-4aKGztHMjBL2B4')
                bot.send_message(chat_id=-872595952,
                                 text=f"덕수궁 {date}일 {n}회차 신청이 확인되었습니다."
                                      f"https://www.deoksugung.go.kr/schedule/list?scheduleid=SB")
                driver.quit()

    time.sleep(randint(2, 4))
    search()

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    # driver = open_browser()
    search()