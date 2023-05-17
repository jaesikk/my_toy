# 45482

import threading
from tkinter import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class App(threading.Thread):
    def __init__(self):
        print('@@@@@@@@@@@@@@@@@@@ @@@@@@@ @@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@@@ @@@@@@@@@@@@@@')
        super().__init__()
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('window-size=800,600')
        self.driver = webdriver.Chrome( options=self.opt)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://www.yes24.com/Templates/FTLogin.aspx"
        self.driver.get(self.url)

        # tkinter
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("yes24 티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()

        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, width=40)
        self.id_entry.grid(row=1, column=1)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, show='*',width=40)
        self.pw_entry.grid(row=2, column=1)
        self.login_button = Button(self.object_frame, text="Login", width=3, height=2, command=self.login)
        self.login_button.grid(row=3, column=1)
        self.showcode_label = Label(self.object_frame, text="공연번호")
        self.showcode_label.grid(row=4, column=0)
        self.showcode_entry = Entry(self.object_frame, width=40)
        self.showcode_entry.grid(row=4, column=1)
        self.showcode_button = Button(self.object_frame, text="직링", width=3, height=2, command=self.link_go)
        self.showcode_button.grid(row=5, column=1)
        self.dp.mainloop()

    # 로그인 하기
    def login(self):
        def task():
            #self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME,'iframe'))
            self.driver.find_element(By.NAME,'SMemberID').send_keys(self.id_entry.get())
            self.driver.find_element(By.ID,'SMemberPassword').send_keys(self.pw_entry.get())
            self.driver.find_element(By.ID,'btnLogin').click()

        newthread = threading.Thread(target=task)
        newthread.start()

    # 직링 바로가기
    def link_go(self):
        def task():
            # sample : 45482
            self.driver.get('http://ticket.yes24.com/Pages/Perf/Sale/PerfSaleProcess.aspx?IdPerf=' + self.showcode_entry.get())
            # self.driver.find_element(By.CLASS_NAME, 'rn-bb03').click()
            # while len(self.driver.window_handles) <= 1:
            #     self.driver.implicitly_wait(1)
            # self.driver.switch_to.window(self.driver.window_handles[1])  # 새 창으로 이동
        newthread = threading.Thread(target=task)
        newthread.start()


app = App()
app.start()
