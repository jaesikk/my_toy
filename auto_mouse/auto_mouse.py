import mouse, keyboard, time, pyautogui


while True:
    if keyboard.is_pressed("shift+f7"):
        while True:
            mouse.click()
            time.sleep(0.0005)
            if keyboard.is_pressed("shift+f8"):
                break
            if keyboard.is_pressed("shift+f9"):
                exit()
    if keyboard.is_pressed("shift+f9"):
        exit()


