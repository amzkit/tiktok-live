import time
import sys
import random
import datetime
import sys
sys.path.append('platform')

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
#UIDS = json.loads(os.getenv('UIDS', 'True').replace('\n', '').replace('\\',''))
ACCOUNTS = json.loads(os.getenv('ACCOUNTS', 'True').replace('\n', '').replace('\\','').replace(' ',''))
USER_PROFILE = os.getenv('USER_PROFILE', 'True')
LINE_NOTIFY_URL = os.getenv('LINE_NOTIFY_URL')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import shopee
import tiktok

lives = {}
options = webdriver.ChromeOptions()
if 'USER_PROFILE' in locals():
    options.add_argument("--user-data-dir="+str(USER_PROFILE)) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
else:
    options.add_argument("--user-data-dir=C:\\Users\\Decoz\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
options.add_argument(r'--remote-debugging-pipe')
options.add_argument("--log-level=3")
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
        #removeElement(DivSideNavContainer)
        #DivLiveContent = browser.find_elements(By.XPATH, div_live_content)
        #removeElement(DivLiveContent[1])
        print('['+time.strftime('%H:%M')+']['+unique_id+'] Connected')
        #
        lives[unique_id]['shown_connection_error'] = True

def notify(unique_id, message):
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + TOKEN[unique_id]}
    try:
        r = requests.post(LINE_NOTIFY_URL, headers=headers, data = {'message':message})
    except:
        print('['+time.strftime('%H:%M')+'][ERROR] Line Notify Error')

def siri(unique_id, user, comment):
    #print('['+time.strftime('%H:%M')+']['+unique_id+'][Comment] ' + user + ' : ' + comment)
    message = user + ':' + comment
    #notify(unique_id, message)
    #
    if len(comment) > 0 and comment[0] == "@" and len(comment.split()) > 1:
        comment = comment.split()[1:]
        comment = ' '.join(comment)
    
    tts = gTTS(comment, lang='th')
    filename = str(int(time.time())) + '_' + comment
    comment_path = 'comment'
    if not os.path.exists(comment_path):
        os.makedirs(comment_path)
    tts.save(os.path.join(comment_path, filename +'.ogg'))
    
    #    print('['+time.strftime('%H:%M')+']['+uid+'][Error] gtts')
    #    lives[uid]['shown_connection_error'] = True

account_count = 0
for account in ACCOUNTS:
    platform = account["platform"]
    uid = account["uid"]
    
    #
    if account_count > 0:
        browser.switch_to.new_window('tab')
    print('['+time.strftime('%H:%M')+']['+platform+']['+uid+'] Connecting')
    #
    if platform == "shopee":
        shopee.initialize(browser)
        shopee.clean_up(browser)
    if platform == "tiktok":
        tiktok.initialize(browser, uid)
        tiktok.clean_up(browser)
    #
    print('['+time.strftime('%H:%M')+']['+platform+']['+uid+'] Connected')
    #
    #
    lives[uid] = {
        'platform'  :   platform,
        'window_id' :   browser.window_handles[account_count],
        'chat_processed_index':   0,
        'chat_count':   0,
        'last_connected_epoch_time' :   int(datetime.datetime.now().timestamp()),
        'waiting_until_reconnect'   :   1500,
        'shown_connection_error'    :   False,
    }
    account_count = account_count + 1
    #
    time.sleep(1)



while True:
    for account in ACCOUNTS:
        platform = account["platform"]
        uid = account["uid"]
        #
        if(len(ACCOUNTS) > 1):
            switch(uid)
        #
        try:
            if platform == 'tiktok':
                chat_count = tiktok.get_chat_count(browser)
            elif platform == 'shopee':
                chat_count = shopee.get_chat_count(browser)
            
            lives[uid]['chat_count'] = chat_count
            #print("Count:", chat_count)
            #
            if(lives[uid]['chat_count'] > lives[uid]['chat_processed_index']):
                user = ''
                comment = ''
                if platform == 'tiktok':
                    (user, comment) = tiktok.get_chat(browser, lives[uid]['chat_processed_index'])
                elif platform == 'shopee':
                    (user, comment) = shopee.get_chat(browser, lives[uid]['chat_processed_index'])
                print('['+time.strftime('%H:%M')+']['+platform+']['+uid+']['+user+"] " + comment)
                #
                if(comment != ''):
                    siri(uid, user, comment)
                lives[uid]['chat_processed_index'] = lives[uid]['chat_processed_index'] + 1
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