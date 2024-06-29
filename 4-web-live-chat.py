import time
import sys
import random
import datetime
import sys

HEADLESS = False
AUTO_COMMENT = False

#GTTS Speech
from gtts import gTTS
from io import BytesIO

#Line Notify
import requests

import json
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = json.loads(os.getenv('TOKEN', 'True').replace('\n', '').replace('\\',''))
UIDS = json.loads(os.getenv('LIVE_CHAT_IDS', 'True').replace('\n', '').replace('\\','').replace(' ',''))
USER_PROFILE = os.getenv('USER_PROFILE_0', 'True')
LINE_NOTIFY_URL = os.getenv('LINE_NOTIFY_URL')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

#v202405
#chat_div = "//div[@class='py-2 px-4 rounded-full bg-brand-hover bg-opacity-[.14] break-words mb-4']"
#v20240606


# To remove
div_header_container = "//div[contains(@class, 'DivHeaderContainer')]"
div_side_nav_container = "//div[contains(@class, 'DivSideNavContainer')]"
div_live_content = "//div[contains(@class, 'DivLiveContent')]"

# Chat Element
div_chat_message_list = "//div[contains(@class, 'DivChatMessageList')]"
#div_chat_message = "//div[contains(@class,'DivChatMessageList')]/div[contains(@class, 'DivChatMessage')]"

div_chat_messages = "//div[@data-e2e='chat-message']"
div_user_info = "//div[contains(@class, 'DivUserInfo')]"
div_comment = "//div[contains(@class, 'DivComment')]"

# To check if connected, method 1: if there like container = ok, else click on retry
div_like_container = "//div[contains(@class, 'DivLikeContainer')]"
retry_button = "//Button[contains(text(),'Retry')]"

# To check if connected, method 2: check DivContent (there will be message 'username joined')
div_content = "//div[contains(@class,'DivContent')]"

# Insert Chat
div_input_editor_container = "//div[contains(@class, 'DivInputEditorContainer')]"
content_editable = "//div[@contenteditable='plaintext-only']"

comment_list = [
    'แนะนำกลิ่น passion love หน่อยค่ะ','กลิ่น dreamy cloud หน่อยค่ะ',
    'แนะนำ kiss me more หน่อยค่ะ', 'ขอกลิ่น mine wish หน่อยค่ะ',
    'แนะนำกลิ่นสำหรับผู้ชายหน่อยค่ะ','กลิ่นสดชื่นๆ',
    'ไปเที่ยวกลางคืนกลิ่นไหนดีคะ', 'กลิ่นหวานๆ หน่อยค่ะ'
    'ปิคนิค','woodsand','ไปทะเลกลิ่นไหน','มีกลิ่นคล้ายเค้าเตอร์แบรนด์ไหมคะ',
    'ส่งวันไหน',
]
lives = {}

options = webdriver.ChromeOptions()
if 'USER_PROFILE' in locals():
    options.add_argument("--user-data-dir="+str(USER_PROFILE)) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
else:
    options.add_argument("--user-data-dir=C:\\Users\\Kit\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 21")
options.add_argument(r'--remote-debugging-pipe')

options.add_argument("--disable-blink-features=AutomationControlled")
if HEADLESS:
    options.add_argument("--headless=new")
######################
# Attempt to disable error stun.l.google.com message
#options.add_argument(r'--disable-logging')
#options.add_argument(r'--allow-running-insecure-content')
#options.add_argument(r'--ignore-certificate-errors')
######################
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 

browser = webdriver.Chrome(options)

#browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')

def removeElement(element):
    browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)

def switch(unique_id):
    browser.switch_to.window(lives[unique_id]['window_id'])

def reconnect(unique_id):
    switch(unique_id)
    now_epoch = int(datetime.datetime.now().timestamp())
    reconnect_epoch = lives[unique_id]['last_connected_epoch_time'] + lives[unique_id]['waiting_until_reconnect']
    if(reconnect_epoch < now_epoch):
        print('['+time.strftime('%H:%M')+']['+unique_id+'] Reconnecting...')
        browser.get('https://tiktok.com/@'+unique_id+'/live')
        #
        DivSideNavContainer = WebDriverWait(browser, 60).until(ExpectedConditions.presence_of_element_located((By.XPATH, div_side_nav_container)))
        #DivSideNavContainer = browser.find_elements(By.XPATH, div_side_nav_container)
        removeElement(DivSideNavContainer)
        DivLiveContent = browser.find_elements(By.XPATH, div_live_content)
        removeElement(DivLiveContent[1])
        print('['+time.strftime('%H:%M')+']['+unique_id+'] Connected')
        #
        lives[unique_id]['shown_connection_error'] = True

def notify(unique_id, message):
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + TOKEN[unique_id]}
    r = requests.post(LINE_NOTIFY_URL, headers=headers, data = {'message':message})

def siri(unique_id, user, comment):
    #print('['+time.strftime('%H:%M')+']['+unique_id+'][Comment] ' + user + ' : ' + comment)
    message = user + ':' + comment
    notify(unique_id, message)
    #
    if len(comment) > 0 and comment[0] == "@" and len(comment.split()) > 1:
        comment = comment.split()[1:]
        comment = ' '.join(comment)
    try:
        tts = gTTS(comment, lang='th')
        filename = str(int(time.time())) + '_' + comment
        tts.save(os.path.join('comment', filename +'.ogg'))
    except:
        print('['+time.strftime('%H:%M')+']['+uid+'][Error] gtts')
        lives[uid]['shown_connection_error'] = True

for i in range(len(UIDS)):
    uid = UIDS[i]
    if i > 0:
        browser.switch_to.new_window('tab')
    print('['+time.strftime('%H:%M')+']['+uid+'] Connecting')
    browser.get('https://tiktok.com/@'+uid+'/live')
    #
    DivSideNavContainer = WebDriverWait(browser, 60).until(ExpectedConditions.presence_of_element_located((By.XPATH, div_side_nav_container)))
    #DivSideNavContainer = browser.find_elements(By.XPATH, div_side_nav_container)
    removeElement(DivSideNavContainer)
    DivLiveContent = browser.find_elements(By.XPATH, div_live_content)
    removeElement(DivLiveContent[1])
    #
    lives[uid] = {
        'window_id': browser.window_handles[i],
        'next_index': 0,
        'chat_count': 0,
        'last_connected_epoch_time': int(datetime.datetime.now().timestamp()),
        'waiting_until_reconnect': 1500,
        'shown_connection_error': False,
    }
    print('['+time.strftime('%H:%M')+']['+uid+'] Connected')
    time.sleep(1)

while True:
    for i in range(len(UIDS)):
        uid = UIDS[i]
        if(len(UIDS) > 1):
            switch(uid)
        #
        try:
            DivChatMessages = browser.find_elements(By.XPATH, div_chat_messages)
            lives[uid]['chat_count'] = len(DivChatMessages)
            #print("Count:", chat_count)
            #
            if(lives[uid]['chat_count'] > lives[uid]['next_index']):
                user = DivChatMessages[lives[uid]['next_index']].find_elements(By.XPATH, div_user_info)
                user = user[lives[uid]['next_index']].text
                comment = DivChatMessages[lives[uid]['next_index']].find_elements(By.XPATH, div_comment)
                comment = comment[lives[uid]['next_index']].text
                #print(user, comment)
                print('['+time.strftime('%H:%M')+']['+uid+']['+user+"] " + comment)
                if(comment != ''):
                    siri(uid, user, comment)
                lives[uid]['next_index'] = lives[uid]['next_index'] + 1
                #print("Last Index :" , last_index)
            #   
            #if len(temp_comments):
            #    print("[Chat] Found", len(temp_comments), "chat(s)" )
            #
        except:
            # ERROR remove from the list
            if(lives[uid]['shown_connection_error'] == False):
                print('['+time.strftime('%H:%M')+']['+uid+'] ERROR')
                lives[uid]['shown_connection_error'] = True
            reconnect(uid)
        #
        time.sleep(1)


