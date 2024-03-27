import time
import random
import datetime
import threading
import json
from queue import Queue
from dotenv import load_dotenv
import os
from distutils.util import strtobool

load_dotenv()


#PRODUCTS = os.getenv('PRODUCTS', 'True')
#print(PRODUCTS)
USER_PROFILE = os.getenv('USER_PROFILE')
LIVE_CHAT_IDS = json.loads(os.getenv('LIVE_CHAT_IDS', 'True').replace('\n', '').replace('\\',''))
TOKEN = json.loads(os.getenv('TOKEN', 'True').replace('\n', '').replace('\\',''))
LINE_NOTIFY_URL = os.getenv('LINE_NOTIFY_URL')

#19 byprw
#21 perfumex

print("Environment :")
print("USER_PROFILE :", USER_PROFILE)
print("LIVE_CHAT_IDS :", LIVE_CHAT_IDS)

#GTTS Speech
from gtts import gTTS

#To hide pygame welcome message

#Line Notify
import requests

def notify(unique_id, message):
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + TOKEN[unique_id]}
    r = requests.post(LINE_NOTIFY_URL, headers=headers, data = {'message':message})

def notify_before_end(unique_id, time_diff):
    #number of second to be waited until end - 300 (before 5 mins)
    waiting_seconds = 14400 - (time_diff % 14400) - 300
    if waiting_seconds > 0:
        # sleep exactly the right amount of time
        m, s = divmod(waiting_seconds, 60)
        h, m = divmod(m, 60)
        #print('['+time.strftime('%H:%M')+']['+unique_id+'] set notification in', f'{h:02d}:{m:02d}', 'hours')
        time.sleep(waiting_seconds)
        message = unique_id + ' is ending in 5 mins'
        notify(unique_id, message)
        time.sleep(300)
        message = unique_id + ' is ended'
        notify(unique_id, message)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
#options.add_argument("--user-data-dir="+str(USER_PROFILE)) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
#options.add_argument(r'--remote-debugging-pipe')
options.add_argument(r'--headless')
options.add_argument(r'--disable-gpu')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options)



#browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')
id = LIVE_CHAT_IDS[0]
url_str = "https://tiktok.com/@" + id + "/live"
driver.get(url_str)

#id = LIVE_CHAT_IDS[1]
#url_str = "https://tiktok.com/@" + id + "/live"
#driver.execute_script("window.open('"+url_str+"','_blank');")

def removeElement(element):
    driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
def removeClass(element):
    driver.execute_script("arguments[0].setAttribute('class','')", element)

top_bar = WebDriverWait(driver, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@class='tiktok-1lhjsdw-DivHeaderContainer e10win0d0']")))
left_bar = WebDriverWait(driver, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@class='tiktok-1wt3i5h-DivSideNavContainer e15sbjlu0']")))
live_video = WebDriverWait(driver, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@class='tiktok-10q5o1z-DivLiveContent e14c6d574']")))
hide_chat_button = WebDriverWait(driver, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@class='tiktok-1dnj95g-DivChatRoomHeaderIconContainer erwvzsp2']")))

removeElement(top_bar)
removeElement(left_bar)
removeElement(live_video)
removeElement(hide_chat_button)


chats = driver.find_elements(By.XPATH, "//div[@data-e2e='chat-message']/div[2]/div[2]")


while True:

    time.sleep(1)

    #driver.execute_script("window.open('"+url_str+"','_blank');")


