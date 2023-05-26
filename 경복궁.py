import time
import telegram
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://ticket.11st.co.kr/Product/Detail?id=267448&prdNo=5626407961'
cnt = 0
def check():
    global cnt
    cnt+=1
    print(f'= = >> {cnt}회차 조회를 시작합니다.')
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, '2023-05-27'))
    ).click()
    print('2023-05-27 날짜 클릭')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'c_ticket_seat'))
    ).click()

    tmp = driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div/div[1]/div/div[2]/div[2]/dl/div/dd')
    print(tmp.text)
    res = tmp.text
    if res != '매진':
        print('here')
        bot = telegram.Bot(token='AAEiIChMcVgFuCO3ZPr6AFhe03o2z745t')
        bot.send_message(chat_id=-721609842,
                         text=f"경복궁 클릭 확인 완료."
                              f"https://ticket.11st.co.kr/Product/Detail?id=267448&prdNo=5626407961")
        driver.quit()

    print('---------------end point -----------------')

    time.sleep(randint(2, 4))
    check()

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    # driver = open_browser()
    check()