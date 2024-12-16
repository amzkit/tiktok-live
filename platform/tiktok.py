from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import pickle
import time
import os

cookie_file_path = "platform/tiktok_cookie.pkl"

def save_cookies(browser):
    pickle.dump(browser.get_cookies(), open(cookie_file_path,"wb"))

def load_cookies(browser):
    if(not os.path.exists(cookie_file_path)):
        print('['+time.strftime('%H:%M')+'][WARNING][Tiktok] Cannot Load cookies')
        return
    else:
        cookies = pickle.load(open(cookie_file_path, "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.refresh()
        print('['+time.strftime('%H:%M')+'][Tiktok] Cookies Loaded')

# To remove
div_side_nav_container = "//div[contains(@class, 'DivSideNavContainer')]"
div_live_content = "//div[contains(@class, 'DivLiveContent')]"

removingElements = [
    div_side_nav_container,
    div_live_content
]

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

def initialize(browser, uid):
    browser.get('https://tiktok.com/@'+uid+'/live')
    load_cookies(browser)
    clean_up(browser)

def clean_up(browser):
    DivSideNavContainer = WebDriverWait(browser, 60).until(ExpectedConditions.presence_of_element_located((By.XPATH, div_side_nav_container)))
    browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", DivSideNavContainer)
    DivLiveContent = browser.find_elements(By.XPATH, div_live_content)
    browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", DivLiveContent[1])

#######################################
#   Chat
#######################################

def get_chat_count(browser):
    DivChatMessages = browser.find_elements(By.XPATH, div_chat_messages)
    return len(DivChatMessages)

def get_chat(browser, target_index):
    DivChatMessages = browser.find_elements(By.XPATH, div_chat_messages)
    user = DivChatMessages[target_index].find_elements(By.XPATH, div_user_info)
    user = user[target_index].text
    comment = DivChatMessages[target_index].find_elements(By.XPATH, div_comment)
    comment = comment[target_index].text
    return (user, comment)
