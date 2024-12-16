from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import time
import os
import pickle

cookie_file_path = "platform/shopee_cookie.pkl"

def save_cookies(browser):
    pickle.dump(browser.get_cookies(), open(cookie_file_path,"wb"))

def load_cookies(browser):
    if(not os.path.exists(cookie_file_path)):
        print('['+time.strftime('%H:%M')+'][WARNING][Shopee] Cannot Load cookies')
        return
    else:
        cookies = pickle.load(open(cookie_file_path, "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.refresh()
        print('['+time.strftime('%H:%M')+'][Shopee] Cookies Loaded')

removingElements = [
    "//header[@class='_container_fa00w_1']",
    "//div[@class='_overviewContainer_hwlot_5 liveOverviewContainer']",
    "//div[@id='player']",
    "//div[@class='_titleMask_1pvjx_48']",
    "//div[@class='_titleWrap_1pvjx_57']",
    "//div[@class='_cardContainer_1pvjx_140']",
    "//div[@class='_indicatorContainer_1pvjx_158']",
    "//div[@class='_violation_1a9hg_5']",
]

##########################
# Element
##########################

list_live_title_elements = "//span[contains(@class, '_titlePre_15qqm_81')]"

chat_container_xpath = "//div[@class='_commentContainer_1pvjx_226']" # for waiting container to load

chat_count_xpath = "//div[@class='_comment_1pvjx_226']"
chat_user_xpath = "//span[@class='_commentUser_1pvjx_254']"
chat_comment_xpath = "//span[@class='_commentContent_1pvjx_258']"

##########################
# Initiate
##########################
def initialize(browser):
    while True:
        try:
            browser.get('https://seller.shopee.co.th/creator-center/insight/live/list#')
            load_cookies(browser)
            browser.get('https://seller.shopee.co.th/creator-center/insight/live/list#')
            live_session_xpath = "//tr[@class='eds-react-table-row eds-react-table-row-level-0']"
            live_session = WebDriverWait(browser, 180).until(ExpectedConditions.presence_of_element_located((By.XPATH, live_session_xpath)))
            real_time = live_session.find_elements(By.XPATH, '//div[contains(text(), "Real-Time")]')

            if(len(real_time) > 0):
                live_id = live_session.get_attribute('data-row-key')
                browser.get('https://creator.shopee.co.th/dashboard/live/'+live_id+'?lang=th')
                break
        except:
            print("Trying to Get Live Session Error")
            time.sleep(5)

#####################
# Removing Element
#####################
def clean_up(browser):
    for element in removingElements:
        try:
            el = WebDriverWait(browser, 5).until(ExpectedConditions.presence_of_element_located((By.XPATH, element)))
            browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", el)
        except:
            print('Cannot Remove ', element)

#####################
# Getting Comment
#####################
def get_chat_count(browser):
    try:
        chat_container = WebDriverWait(browser, 5).until(ExpectedConditions.presence_of_element_located((By.XPATH, chat_container_xpath)))
        chats = chat_container.find_elements(By.XPATH, chat_count_xpath)
        return len(chats)
    except:
        print('[ERROR] shopee : get_chat_count')
        return 0
    
def get_chat(browser, target_index):
    try:
        chat_container = WebDriverWait(browser, 5).until(ExpectedConditions.presence_of_element_located((By.XPATH, chat_container_xpath)))
        user = chat_container.find_elements(By.XPATH, chat_user_xpath)
        user = user[target_index].text[:-1]
        comment = chat_container.find_elements(By.XPATH, chat_comment_xpath)
        comment = comment[target_index].text
        return (user, comment)
    except:
        print('[ERROR] shopee : get_chat_at ', target_index)
        return 0
    