import time
import telegram
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By

def search(driver):
    driver.get('https://booking.stayfolio.com/places/nuwa/bookings/plugin')
    available = driver.find_element(By.CLASS_NAME, 'available')
    print(available.text)
    time.sleep(5)

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    # driver = open_browser()
    search(driver)