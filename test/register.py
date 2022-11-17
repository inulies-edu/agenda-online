import pyautogui as auto
import time

cont = 0
time.sleep(5)
for i in range(5):
    auto.PAUSE = 0.5
    auto.click(x=1355, y=540)
    auto.click(x=1209, y=438)
    auto.write('teste' + str(cont))
    auto.press('tab')
    auto.write('teste' + str(cont) + '@email.com')
    auto.press('tab')
    auto.write('1z9jsdasjd!@#')
    auto.press('enter')
    cont += 1




