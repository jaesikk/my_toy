# -*- coding: utf-8 -*-
import time
import telegram
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import os
# load_dotenv()
import tkinter as tk

# 입력값을 파일에 저장하는 함수
def save_input_values(id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check):
    with open("input_values.txt", "w") as file:
        file.write(f"ID: {id}\n")
        file.write(f"Password: {pw}\n")
        file.write(f"Name: {nm}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        file.write(f"Date: {yyyymmdd}\n")
        file.write(f"Time: {t}\n")
        file.write(f"Number of trains to check: {num_trains_to_check}\n")
    print("Input values saved successfully.")

# 파일에서 입력값을 읽어오는 함수
def load_input_values():
    input_values = {}
    with open("input_values.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split(": ")
            input_values[key] = value
    return input_values

# Submit 버튼 클릭 시 실행되는 함수
def submit_callback():
    global n
    # 입력값 받기
    id = id_entry.get()
    pw = pw_entry.get()
    nm = nm_entry.get()
    start = start_entry.get()
    end = end_entry.get()
    yyyymmdd = yyyymmdd_entry.get()
    t = t_entry.get()
    num_trains_to_check = num_trains_to_check_entry.get()

    # 입력값 저장
    save_input_values(id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check)

    # 파일에서 입력값 읽어오기
    input_values = load_input_values()

    # 결과 텍스트 업데이트
    result_text.configure(state='normal')
    result_text.delete('1.0', tk.END)
    n +=1
    result_text.insert(tk.END, f'{n}번째 log입니다.\n')
    for key, value in input_values.items():
        result_text.insert(tk.END, f"{key}: {value}\n")
    result_text.configure(state='disabled')

    #main 실행
    main(id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check)

def main(id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check):
    browser = webdriver.Chrome()
    # driver = open_browser()
    driver = login(browser, id, pw)
    search_train(driver, start, end, yyyymmdd, t) #기차 출발 시간은 반드시 짝수

def open_browser():
    driver = webdriver.Chrome("chromedriver")
    return driver


def login(driver, login_id, login_psw):
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    print('login 진입완료: ', login_id, login_psw)
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
    bot = telegram.Bot(token='5949014838:AAEiIChMcVgFuCO3ZPr6AFhe03o2z745t-k')
    bot.send_message(chat_id=-721609842, text=f"{nm}님의 {end}행/{t}시 이후 {num_trains_to_check}개의 SRT 조회를 시작합니다.")
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

n = 0
# tkinter 윈도우 생성
window = tk.Tk()
window.title("Input Values")

# 입력값을 불러오기 위해 파일에서 입력값 읽어오기
input_values = load_input_values()

# ID 입력 필드
id_label = tk.Label(window, text="ID:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.insert(tk.END, input_values.get("ID", ""))  # 이전 값이 있으면 입력 창에 표시
id_entry.pack()

# Password 입력 필드
pw_label = tk.Label(window, text="Password:")
pw_label.pack()
pw_entry = tk.Entry(window)
pw_entry.insert(tk.END, input_values.get("Password", ""))
pw_entry.pack()

# Name 입력 필드
nm_label = tk.Label(window, text="Name:")
nm_label.pack()
nm_entry = tk.Entry(window)
nm_entry.insert(tk.END, input_values.get("Name", ""))
nm_entry.pack()

# Start 입력 필드
start_label = tk.Label(window, text="Start:")
start_label.pack()
start_entry = tk.Entry(window)
start_entry.insert(tk.END, input_values.get("Start", ""))
start_entry.pack()

# End 입력 필드
end_label = tk.Label(window, text="End:")
end_label.pack()
end_entry = tk.Entry(window)
end_entry.insert(tk.END, input_values.get("End", ""))
end_entry.pack()

# Date 입력 필드
yyyymmdd_label = tk.Label(window, text="Date (YYYYMMDD):")
yyyymmdd_label.pack()
yyyymmdd_entry = tk.Entry(window)
yyyymmdd_entry.insert(tk.END, input_values.get("Date", ""))
yyyymmdd_entry.pack()

# Time 입력 필드
t_label = tk.Label(window, text="Time (even number):")
t_label.pack()
t_entry = tk.Entry(window)
t_entry.insert(tk.END, input_values.get("Time", ""))
t_entry.pack()

# Number of trains to check 입력 필드
num_trains_to_check_label = tk.Label(window, text="Number of trains to check:")
num_trains_to_check_label.pack()
num_trains_to_check_entry = tk.Entry(window)
num_trains_to_check_entry.insert(tk.END, input_values.get("Number of trains to check", ""))
num_trains_to_check_entry.pack()

# Submit 버튼
submit_button = tk.Button(window, text="Submit", command=submit_callback)
submit_button.pack()

# 결과 텍스트 박스
result_text = tk.Text(window, height=10, width=50)
result_text.configure(state='disabled')
result_text.pack()

# 이벤트 루프 실행
window.mainloop()




# id = os.environ.get("ID1")
# pw = os.environ.get("PW1")
# nm = os.environ.get("NAME1")
# start = '통도사'
# end = '수서'
# yyyymmdd = '20230519'
# t = '14' # only 짝수
# num_trains_to_check=4
want_reserve=False

### ID, PW : SRT 계정
### 23행 search_train에서 세부 조정
# if __name__ == "__main__":
#     options = webdriver.ChromeOptions()
#     # options.add_experimental_option("excludeSwitches", ["enable-logging"])
#     # browser = webdriver.Chrome(options=options)
#     browser = webdriver.Chrome()
#     # driver = open_browser()
#     driver = login(browser, id, pw)
#     search_train(driver, start, end, yyyymmdd, t) #기차 출발 시간은 반드시 짝수

###############################
# def submit():
#     global id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check
#     id = entry_id.get()
#     pw = entry_pw.get()
#     nm = entry_nm.get()
#     start = entry_start.get()
#     end = entry_end.get()
#     yyyymmdd = entry_yyyymmdd.get()
#     t = entry_t.get()
#     num_trains_to_check = int(entry_num_trains_to_check.get()) if entry_num_trains_to_check.get() else 0
#
#     root.destroy()
#     # if __name__ == "__main__":
#     # options = webdriver.ChromeOptions()
#     # options.add_experimental_option("excludeSwitches", ["enable-logging"])
#     # browser = webdriver.Chrome(options=options)
#     browser = webdriver.Chrome()
#     # driver = open_browser()
#     driver = login(browser, id, pw)
#     search_train(driver, start, end, yyyymmdd, t)  # 기차 출발 시간은 반드시 짝수
#
#
# #
# # root = tk.Tk()
# # root.title("입력값 설정")
# # root.geometry("300x400")
# #
# # label_id = tk.Label(root, text="ID:")
# # label_id.pack()
# # entry_id = tk.Entry(root)
# # entry_id.pack()
# #
# # label_pw = tk.Label(root, text="PW:")
# # label_pw.pack()
# # entry_pw = tk.Entry(root, show="*")
# # entry_pw.pack()
# #
# # label_nm = tk.Label(root, text="NAME:")
# # label_nm.pack()
# # entry_nm = tk.Entry(root)
# # entry_nm.pack()
# #
# # label_start = tk.Label(root, text="출발역:")
# # label_start.pack()
# # entry_start = tk.Entry(root)
# # entry_start.pack()
# #
# # label_end = tk.Label(root, text="도착역:")
# # label_end.pack()
# # entry_end = tk.Entry(root)
# # entry_end.pack()
# #
# # label_yyyymmdd = tk.Label(root, text="날짜 (YYYYMMDD):")
# # label_yyyymmdd.pack()
# # entry_yyyymmdd = tk.Entry(root)
# # entry_yyyymmdd.pack()
# #
# # label_t = tk.Label(root, text="시간 (짝수):")
# # label_t.pack()
# # entry_t = tk.Entry(root)
# # entry_t.pack()
# #
# # label_num_trains_to_check = tk.Label(root, text="확인할 열차 수:")
# # label_num_trains_to_check.pack()
# # entry_num_trains_to_check = tk.Entry(root)
# # entry_num_trains_to_check.pack()
# #
# # button_submit = tk.Button(root, text="Submit", command=submit)
# # button_submit.pack()
# #
# # root.mainloop()
# #
# # print("입력된 값:")
# # print("ID:", id)
# # print("PW:", pw)
# # print("NAME:", nm)
# # print("출발역:", start)
# # print("도착역:", end)
# # print("날짜:", yyyymmdd)
# # print("시간:", t)
# # print("확인할 열차 수:", num_trains_to_check)
