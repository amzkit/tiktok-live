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

USER_PROFILE = os.getenv('USER_PROFILE')
FLASHSALE_ENABLED = bool(strtobool(os.getenv('FLASHSALE_ENABLED', 'True')))
COMMENT_ENABLED = bool(strtobool(os.getenv('COMMENT_ENABLED', 'True')))
PINNING_ENABLED = bool(strtobool(os.getenv('PINNING_ENABLED', 'True')))
TOKEN = json.loads(os.getenv('TOKEN', 'True').replace('\n', '').replace('\\',''))
LINE_NOTIFY_URL = os.getenv('LINE_NOTIFY_URL')
#PRODUCTS = os.getenv('PRODUCTS', 'True')
#print(PRODUCTS)
#PRODUCTS = json.loads(os.getenv('PRODUCTS', 'True').replace('\n', '').replace('\\',''))

print("Environment :")
print("USER_PROFILE :", USER_PROFILE)
print("FLASHSALE_ENABLED :", FLASHSALE_ENABLED)
print("COMMENT_ENABLED :", COMMENT_ENABLED)
print("PINNING_ENABLED :", PINNING_ENABLED)

#GTTS Speech
from gtts import gTTS

from io import BytesIO
from pygame import mixer

#To hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

def remove(browser, element):
    browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir="+str(USER_PROFILE)) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--remote-debugging-pipe')
browser = webdriver.Chrome(options)

browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')


#login_with_email_btn = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Email_Panel_Button")
#login_with_email_btn.click()
#email_input = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Email_Input")
#email_input.send_keys("khotcham.perfumexlab@gmail.com")
#password_input = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Pwd_Input")
#password_input.send_keys("Euei@1440")
#login_btn = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Btn")
#login_btn.click()

print("Finding Logo for dashboard page")
navbar = WebDriverWait(browser, 120).until(ExpectedConditions.presence_of_element_located((By.ID, "top_nav_menu_compass_v2")))
#navbar = browser.find_element(By.ID, "top_nav_menu_compass_v2")
navbar.click()

print("Finding a live analysis link")
link = WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, '//a[contains(@href,"/compass/live-analysis")]')))
#link = browser.find_element(By.XPATH, '//a[contains(@href,"/compass/live-analysis")]')
link.click()

#browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')



# page after live-analysis
#live_board_menu = WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, '//button[text()="ไลฟ์บอร์ด"]')))
#live_board_button_xpath = "//div[@class='theme-arco-tabs-content theme-arco-tabs-content-horizontal']//div[2]//div[2]//div[1]//div[1]//button[1]"
live_board_button_xpath = "//div[@class='flex flex-col w-full']//div[@class='flex justify-between']//div[1]//button[1]"
live_board_buttons = browser.find_elements(By.XPATH, live_board_button_xpath)

while len(live_board_buttons) == 0:
    print('['+time.strftime('%H:%M')+'] for new tab')
    time.sleep(1)
    live_board_buttons = browser.find_elements(By.XPATH, live_board_button_xpath)


live_count = len(live_board_buttons)

handles_before = browser.window_handles

#save seller center window
seller_center_window = browser.window_handles[0]

#live_board_menu = browser.find_element(By.XPATH, '//button[text()="ไลฟ์บอร์ด"]') 
for i in range(live_count):
    live_board_buttons[i].click()
    browser.switch_to.window(browser.window_handles[0])
    live_board_button_xpath = "//div[@class='flex flex-col w-full']//div[@class='flex justify-between']//div[1]//button[1]"
    live_board_buttons = browser.find_elements(By.XPATH, live_board_button_xpath)
    #print('['+time.strftime('%H:%M')+'][Product] live board opened')

#print("after windows", browser.window_handles)

#print("waiting for new window")
    
#wait for new window to open
WebDriverWait(browser, 30).until(lambda browser: len(handles_before) != len(browser.window_handles))
#new_window = WebDriverWait(browser, timeout=30).until(ExpectedConditions.new_window_is_opened(browser.window_handles))


lives = []

#Openning a live board tab
for i in range(live_count):
    #switch to new tab
    browser.switch_to.window(browser.window_handles[i+1])
    #print("[Live Windows] Added", browser.window_handles[i+1])
    #print("[Product] switched to window", i+1, "["+browser.window_handles[i+1]+"]")
    #product_tab = WebDriverWait(browser, 5).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//span[@class='text-headingL hover:text-text1 transition-colors text-text3'][contains(text(),'สินค้า')]")))
    #product_tab = WebDriverWait(browser, 30).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//div[@role='tab']/span/span[2]")))
    #product_tab = browser.find_elements(By.XPATH, "//div[@role='tab']/span/span[contains(text(),'สินค้า')]")[0]
    # tab สินค้า
    product_tab = WebDriverWait(browser, 5).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@role='tab'][2]/span/span")))

    product_tab.click()

    live_video = browser.find_elements(By.XPATH, "//div[@class='h-[480px] w-full relative flex-shrink-0']")[0]
    #browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", live_video)
    remove(browser, live_video)
    dashboard = browser.find_elements(By.XPATH, "//div[@class='w-full h-[540px] rounded-lg p-8 relative flex-shrink-0']")[0]
    #browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", dashboard)
    remove(browser, dashboard)
    print('['+time.strftime('%H:%M')+'][LiveBoard] Ready')

    unique_id = browser.find_elements(By.XPATH, "//span[@class='text-headingM']")[3].text
    created_time = browser.find_elements(By.XPATH, "//span[@class='text-headingM']")[0].text
    lives.append({'index':i, 'window_id':browser.window_handles[i+1], 'unique_id':unique_id, 'created_time':created_time, 'product_key_to_pin':'', 'product_count':0, 'products':{}})
    #print("Live Initiated :", lives)

#Notify Before End
for live_index in range(live_count):

    time_now = int(time.time())
    
    create_time = datetime.datetime.strptime(lives[live_index]['created_time'], '%H:%M:%S %Y-%m-%d')
    create_time_epoch = int(create_time.timestamp())

    #check how many seconds have been passed since room created
    time_diff = time_now - create_time_epoch

    #check how many round for each 4hours passes
    round_count = int(time_diff / 14400)

    #find ending time (each 4 hours since created)
    ending_time_epoch = create_time_epoch + 14400*(round_count+1)
    ending_time_str = time.strftime('%H:%M', time.localtime(ending_time_epoch))

    thread = threading.Thread(target=notify_before_end, args={unique_id:unique_id, time_diff:time_diff})
    thread.start()

##############################################################
### Product Initial
##############################################################
#init product button

def product_initial():
    try:
        for live_index in range(live_count):
            browser.switch_to.window(browser.window_handles[i+1])
            #wait for table to show up            
            WebDriverWait(browser, 10).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
            product_elements = browser.find_elements(By.XPATH, "//table/tbody/tr")
            #print("=================================================================\nProduct Elements:",product_elements)
            lives[live_index]['product_count'] = len(product_elements)
            #print("Lives :", lives[live_index])
            for j in range(len(product_elements)):
                title = product_elements[j].find_elements(By.XPATH, "./td/div/span/div/div[2]/div")[0].text
                button = product_elements[j].find_elements(By.XPATH, "./td/div/span/button")[0]
                lives[live_index]['products'][title] = button
        print('['+time.strftime('%H:%M')+'][Product] all pin elements saved')
    except:
        print("[Product] pin elements cannot be found")
        browser.refresh()

def time_to_pin(last_pin_time_epoch):
    now_epoch = int(datetime.datetime.now().timestamp())
    next_pin_epoch = last_pin_time_epoch + 15 + (int(random.random()*100)) % 5 + 1
    if(next_pin_epoch < now_epoch):
        return True
    else:
        return False

def next_product_key_to_pin(live_index):
    #print("[Next Key To Pin]")
    # Check if this is at the beginning
    if lives[live_index]['product_key_to_pin'] == '':
        next_product_key = list(lives[live_index]['products'].keys())[0]
        lives[live_index]['product_key_to_pin'] = next_product_key
        return next_product_key
    # find next product key

    if len(PRODUCTS) == 0:
        keys = list(lives[live_index]['products'].keys())
        #print("->keys", keys)
        current_key_index = keys.index(lives[live_index]['product_key_to_pin'])
        #print("->current_key", current_key_index)
        next_key_index = current_key_index + 1
        next_key_index = next_key_index % lives[live_index]['product_count']
        #print("->next Key index", next_key_index)
        next_product_key = keys[next_key_index]
    else:
        current_key_index = PRODUCTS.index(lives[live_index]['product_key_to_pin'])
        next_key_index = current_key_index + 1
        next_key_index = next_key_index % len(PRODUCTS)
        next_product_key = PRODUCTS[next_key_index]

    #print("->next product key", next_product_key)
    lives[live_index]['product_key_to_pin'] = next_product_key
    return next_product_key

product_initial()
#print("Product Initialized", lives[0]['products'])
################################################################

##############################################################
### Flashsale
##############################################################
if FLASHSALE_ENABLED:    
    # switch back to seller center
    browser.switch_to.window(seller_center_window)

    # going to promotional page
    WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.ID, 'top_nav_seller_center_logo'))).click()
    # เมนู โปรโมชั่น
    WebDriverWait(browser, 30).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//div[@class='theme-m4b-menu-title-txt'][contains(text(),'โปรโมชั่น')]"))).click()
    # เมนูย่อย เครื่องมือโปรโมชั่น
    WebDriverWait(browser, 10).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//a[@id='menu_item_35']//div[1]"))).click()

##############################################################

def flashsale_ended(ending_time_str):
    ending_time_epoch = int(datetime.datetime.strptime(ending_time_str, '%d/%m/%Y %H:%M').timestamp())
    now_epoch = int(datetime.datetime.now().timestamp())
    if(ending_time_epoch < now_epoch):
        return True
    else:
        return False
    
###############################################################

ending_time_str = ""



#################################################################
### Chat
if COMMENT_ENABLED:
    comments = []
    current_window_index = 0

def chat(browser, current_window_index):
    #print("window", window_index)
    browser.switch_to.window(lives[current_window_index]['window_id'])
    temp_comments = browser.find_elements(By.XPATH, "//div[@class='py-2 px-4 rounded-full bg-brand-hover bg-opacity-[.14] break-words mb-4']")
    unique_id = lives[current_window_index]['unique_id']
    for i in range(len(temp_comments)):
        notify(lives[current_window_index]['unique_id'], temp_comments[i].text)
        user = temp_comments[i].text.split(':')[0]
        comment = ' '.join(temp_comments[i].text.split(':')[1:])
        siri(unique_id, user, comment)
        remove(browser, temp_comments[i])

def siri(unique_id, user, comment):
    print('['+time.strftime('%H:%M')+']['+unique_id+'][Comment] ' + user + ' : ' + comment)
    message = user + ' : ' + comment
    if len(comment) > 0 and comment[0] == "@" and len(comment.split()) > 1:
        comment = comment.split()[1:]
        comment = ' '.join(comment) 
    tts = gTTS(comment, lang='th')
    filename = str(int(time.time())) + '_' + comment
    tts.save(os.path.join('comment', filename +'.ogg'))

######################################
# Initiate for Loop
######################################
last_pin_time_epoch = 0
######################################

for live_index in range(live_count):
    print("===============================================")
    print("Live ID :", lives[live_index]['unique_id'])
    print("Product Count :", lives[live_index]['product_count'])
    print("Start Time :", lives[live_index]['created_time'])
print("===============================================")

while True:
    ##################################
    #   Chat action
    ##################################
    try:
        if COMMENT_ENABLED:
            current_window_index = (current_window_index + 1) % live_count
            chat(browser, current_window_index)
    except:
        print('['+time.strftime('%H:%M')+'][Comment] Error')
    ##################################
    #   Flashsale action
    ##################################
    try:
        if FLASHSALE_ENABLED and ending_time_str == "":
            browser.switch_to.window(seller_center_window)
            WebDriverWait(browser, 20).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td/div/span/div")))
            ending_time_str = browser.find_elements(By.XPATH, "//table/tbody/tr/td[4]/div/span/div")[0].text
            print("[Flashsale] ending time :", ending_time_str)

        if FLASHSALE_ENABLED and flashsale_ended(ending_time_str):
            print("[Flashsale] Time to create a flashsale")
            browser.switch_to.window(seller_center_window)
            #"ดูเพิ่ม"
            WebDriverWait(browser, 60).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[6]/div[1]/span[1]/div[1]/div[1]/div[1]/div[1]/button[1]//*[name()='svg']"))).click()
            #ทำซ้ำ
            WebDriverWait(browser, 30).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//div[@data-tid='m4b_dropdown_menu']/div/div[contains(text(),'ทำซ้ำ')]"))).click()
            affect_immediately_button = WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//span[contains(text(),'มีผลทันที')]")))
            location = affect_immediately_button.location_once_scrolled_into_view
            location['y'] = location['y']-100
            browser.execute_script("window.scrollTo(0,"+str(location['y'])+");")
            affect_immediately_button.click()

            duration_input = browser.find_element(By.XPATH, "//input[@id='effectiveDuration_input']")
            duration_input.clear()
            duration_input.send_keys(Keys.CONTROL,"a")
            duration_input.send_keys(Keys.DELETE)
            duration_input.send_keys("20")

            confirm_button = browser.find_elements(By.XPATH, "//button[@class='theme-arco-btn theme-arco-btn-primary theme-arco-btn-size-default theme-arco-btn-shape-square theme-m4b-button ml-16']/span[contains(text(),'ตกลงและบันทึก')]")[1]
            location = confirm_button.location_once_scrolled_into_view
            browser.execute_script("window.scrollTo("+str(location['x'])+", document.body.scrollHeight);")
            confirm_button.click()
            #error_div = browser.find_elements(By.XPATH, "//div[contains(text(),'ไม่สามารถเพิ่มผลิตภัณฑ์ได้ 1 รายการ')]")
            time.sleep(2)
            
            #check if there is an error
            error_confirm_button = browser.find_elements(By.XPATH, "//div[@role='dialog']/div/div/div/div/div/button[@data-tid='m4b_button']/span[contains(text(),'ยกเลิก')]")
            if(len(error_confirm_button)>0):
                print("[Flashsale] Duplicate, flashsale is still going on")
                # ERROR : Probably duplicate
                error_confirm_button[0].click()
                #ปุ่มยกเลิก
                WebDriverWait(browser, 10).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//button[@data-tid='m4b_button']/span[contains(text(),'ยกเลิก')]")))
                cancel_button = browser.find_elements(By.XPATH, "//button[@data-tid='m4b_button']/span[contains(text(),'ยกเลิก')]")[1]
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                cancel_button.click()
                #ปุ่มละทิ้ง (ยืนยันการยกเลิก)
                try:
                    cancel_button = browser.find_elements(By.XPATH, "//button/span[contains(text(),'ละทิ้ง')]")
                    if(len(cancel_button) > 0):
                        cancel_button.click()
                except:
                    print("No delete confirmation button")
                    continue
            ending_time_str = ""
            print("[Flashsale] created")
    except:
        print('['+time.strftime('%H:%M')+'][Flashsale] Error')
    ##################################
    #   Product pin action
    ##################################
    #print("[Product] check time to pin")
    if(PINNING_ENABLED and time_to_pin(last_pin_time_epoch)):
        for live_index in range(live_count):
            product_key = next_product_key_to_pin(live_index)
            #print('Product_key', product_key)
            browser.switch_to.window(browser.window_handles[live_index+1])
            try:
                products_temp = lives[live_index]['products']
                browser.execute_script("arguments[0].scrollIntoView();", lives[live_index]['products'][product_key])
                lives[live_index]['products'][product_key].click()
            except:
                print('['+time.strftime('%H:%M')+']['+str(lives[live_index]['unique_id'])+"]["+str(product_key)+"] Failed to clicked")
                product_initial()
                time.sleep(1)
                continue
            print('['+time.strftime('%H:%M')+']['+str(lives[live_index]['unique_id'])+"]["+str(product_key)+"] has been pinned")
        last_pin_time_epoch = int(datetime.datetime.now().timestamp())
    
    #The End of Loop
    time.sleep(1)