AUTO_COMMENT = False

import time
import sys
import random
import datetime

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
div_chat_message = "//div[contains(@class, 'DivChatMessage')]"
div_user_info = "//div[contains(@class, 'DivUserInfo')]"
div_comment = "//div[contains(@class, 'DivComment')]"

# To check if connected, if there like container = ok, else click on retry
div_like_container = "//div[contains(@class, 'DivLikeContainer')]"
retry_button = "//Button[contains(text(),'Retry')]"

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


options = webdriver.ChromeOptions()
if 'USER_PROFILE' in locals():
    options.add_argument("--user-data-dir="+str(USER_PROFILE)) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
else:
    options.add_argument("--user-data-dir=C:\\Users\\Kit\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 19")
options.add_argument(r'--remote-debugging-pipe')
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument("--headless=new")
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 
browser = webdriver.Chrome(options)

#browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')
browser.get('https://tiktok.com/@byprw_official/live')


#Check if connected
while True:
    try:
        DivLikeContainer = WebDriverWait(browser, 60).until(ExpectedConditions.presence_of_element_located((By.XPATH, div_like_container)))
        break
    except:
        RetryButton = browser.find_elements(By.XPATH, retry_button)
        if len(RetryButton) > 0:
            RetryButton[0].click()

def removeElement(element):
    browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)

#DivHeaderContainer = browser.find_elements(By.XPATH, div_header_container)
#removeElement(DivHeaderContainer)
DivSideNavContainer = browser.find_elements(By.XPATH, div_side_nav_container)
removeElement(DivSideNavContainer[0])
DivLiveContent = browser.find_elements(By.XPATH, div_live_content)
removeElement(DivLiveContent[1])


#   Input Text
# DivInputEditorContainer = browser.find_element(By.XPATH, div_input_editor_container)

last_comment_time_epoch = 0
def time_to_comment(last_comment_time_epoch):
    now_epoch = int(datetime.datetime.now().timestamp())
    next_pin_epoch = last_comment_time_epoch + (int(random.random()*1000)) % 300 + 300
    if(next_pin_epoch < now_epoch):
        return True
    else:
        return False

last_index = -1
chat_count = 0


comment_left = comment_list
while True:
    DivChatMessage = browser.find_elements(By.XPATH, div_chat_message)
    chat_count = len(DivChatMessage)
    #print("Count:", chat_count)
    #
    if(chat_count > last_index):
        user = DivChatMessage[last_index-1].find_elements(By.XPATH, div_user_info)
        user = user[last_index-1].text
        comment = DivChatMessage[last_index-1].find_elements(By.XPATH, div_comment)
        comment = comment[last_index-1].text
        #print(user, comment)
        print('['+time.strftime('%H:%M')+']['+user+"] " + comment)
        last_index = last_index + 1
        #print("Last Index :" , last_index)
    #
    if AUTO_COMMENT == True and time_to_comment(last_comment_time_epoch):
        try:
            if(len(comment_left) == 0):
                comment_left = comment_list
            pick_index = (random.random() * 100) % len(comment_left)
            to_comment = comment_left.pop(int(pick_index))

            #
            ContentEditable = browser.find_element(By.XPATH, content_editable)
            ContentEditable.send_keys(to_comment)
            ContentEditable.send_keys(Keys.RETURN)
            last_comment_time_epoch = int(datetime.datetime.now().timestamp())
        except:
            print('['+time.strftime('%H:%M')+'] cannot comment')
    #
    #   
    #if len(temp_comments):
    #    print("[Chat] Found", len(temp_comments), "chat(s)" )
    #
    time.sleep(1)


