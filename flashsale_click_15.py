import time
import random
import datetime
import threading

#GTTS Speech
from gtts import gTTS

from io import BytesIO
from pygame import mixer
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\\Users\\Kit\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 15") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--remote-debugging-pipe')
browser = webdriver.Chrome(options)

browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')

flashsale_enabled = False
comment_enabled = True
pinning_enabled = True
#login_with_email_btn = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Email_Panel_Button")
#login_with_email_btn.click()
#email_input = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Email_Input")
#email_input.send_keys("khotcham.perfumexlab@gmail.com")
#password_input = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Pwd_Input")
#password_input.send_keys("Euei@1440")
#login_btn = browser.find_element(By.ID,"TikTok_Ads_SSO_Login_Btn")
#login_btn.click()

navbar = WebDriverWait(browser, 120).until(ExpectedConditions.presence_of_element_located((By.ID, "top_nav_menu_compass_v2")))
#navbar = browser.find_element(By.ID, "top_nav_menu_compass_v2")
navbar.click()

link = WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, '//a[contains(@href,"/compass/live-analysis")]')))
#link = browser.find_element(By.XPATH, '//a[contains(@href,"/compass/live-analysis")]')
link.click()

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
#print("before windows", handles_before)

#save seller center window
seller_center_window = browser.window_handles[0]
live_windows = []

#live_board_menu = browser.find_element(By.XPATH, '//button[text()="ไลฟ์บอร์ด"]') 
for i in range(live_count):
    live_board_buttons[i].click()
    browser.switch_to.window(browser.window_handles[0])
    live_board_button_xpath = "//div[@class='flex flex-col w-full']//div[@class='flex justify-between']//div[1]//button[1]"
    live_board_buttons = browser.find_elements(By.XPATH, live_board_button_xpath)
    print("[Product] live board opened")

#print("after windows", browser.window_handles)

#print("waiting for new window")

#live_board_product_button = WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@id='arco-tabs-1-tab-1']//span[@class='arco-tabs-header-title-text']//span[1]")))
#live_board_product_button = browser.find_element(By.XPATH, "//div[@id='arco-tabs-1-tab-1']//span[@class='arco-tabs-header-title-text']//span[1]")
#live_board_product_button.click()
WebDriverWait(browser, 30).until(lambda browser: len(handles_before) != len(browser.window_handles))
#new_window = WebDriverWait(browser, timeout=30).until(ExpectedConditions.new_window_is_opened(browser.window_handles))

#init product button
products = []
product_index = 0
last_pin_time_epoch = 0
for i in range(live_count):
    products.append([])

#open product tab
for i in range(live_count):
    #switch to new tab
    browser.switch_to.window(browser.window_handles[i+1])
    live_windows.append(browser.window_handles[i+1])
    #print("[Live Windows] Added", browser.window_handles[i+1])
    #print("[Product] switched to window", i+1, "["+browser.window_handles[i+1]+"]")
    product_tab = WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//span[@class='text-headingL hover:text-text1 transition-colors text-text3'][contains(text(),'สินค้า')]")))
    product_tab.click()
    print('['+time.strftime('%H:%M')+'][Product] product tab ready')

#save products
try:
    for i in range(live_count):
        browser.switch_to.window(browser.window_handles[i+1])
        for j in range(0, 10):
            products[i].append(WebDriverWait(browser, 30).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//tbody/tr["+ str(j+1) +"]/td[7]/div[1]/span[1]/button[1]/span[1]"))))
    print('['+time.strftime('%H:%M')+'][Product] all pin elements saved')
except:
    print("[Product] pin elements cannot be found")

##############################################################
### Flashsale
##############################################################
    
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

def time_to_pin(last_pin_time_epoch):
    now_epoch = int(datetime.datetime.now().timestamp())
    next_pin_epoch = last_pin_time_epoch + 15 + (int(random.random()*100)) % 5 + 1
    if(next_pin_epoch < now_epoch):
        return True
    else:
        return False
    
################################################################

ending_time_str = ""

#################################################################
### Chat
last_process_comment_index = -1
comments = []
live_comment_saved_index = {}
current_window_index = 0

for window_index in range(live_count):
    live_comment_saved_index[window_index] = 0

def chat(browser, current_window_index):
    #print("window", window_index)
    browser.switch_to.window(live_windows[current_window_index])
    #print("Switch to ", current_window_index)
    temp_users = browser.find_elements(By.XPATH, "//div[@class='py-2 px-4 rounded-full bg-brand-hover bg-opacity-[.14] break-words mb-4']/span/span[1]")
    temp_comments = browser.find_elements(By.XPATH, "//div[@class='py-2 px-4 rounded-full bg-brand-hover bg-opacity-[.14] break-words mb-4']/span[2]")
    for comment_index in range(live_comment_saved_index[current_window_index], len(temp_users)):
        index = len(comments)
        comments.append({'index': index, 'user':temp_users[comment_index].text, 'comment':temp_comments[comment_index].text})
        live_comment_saved_index[current_window_index] = live_comment_saved_index[current_window_index] + 1
    #print(window_index, comments)

def siri(comment_dict):
    user = comment_dict['user']
    comment = comment_dict['comment']
    print('['+time.strftime('%H:%M')+'][Comment][' + user + '] : ' + comment)
    message = user + ' : ' + comment
    #notify(message)
    if len(comment) > 0 and comment[0] == "@" and len(comment.split()) > 1:
        comment = comment.split()[1:]
        comment = ' '.join(comment) 
    #r = requests.post(url, headers=headers, data = {'message':message})
    tts = gTTS(comment, lang='th')
    filename = str(int(time.time())) + '_' + comment
    tts.save(os.path.join('comment', filename +'.ogg'))

while True:
    ##################################
    #   Chat action
    ##################################
    try:
        if(comment_enabled):
            current_window_index = (current_window_index + 1) % live_count
            chat(browser, current_window_index)
        if(comment_enabled and last_process_comment_index < len(comments) - 1):
            last_process_comment_index = last_process_comment_index + 1
            #print("[Comment] Process Comment :", comments[last_process_comment_index])
            siri(comments[last_process_comment_index])
            time.sleep(1)
    except:
        print('['+time.strftime('%H:%M')+'][Comment] Error')
    ##################################
    #   Flashsale action
    ##################################
    try:
        if flashsale_enabled and ending_time_str == "":
            browser.switch_to.window(seller_center_window)
            WebDriverWait(browser, 20).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td/div/span/div")))
            ending_time_str = browser.find_elements(By.XPATH, "//table/tbody/tr/td[4]/div/span/div")[0].text
            print("[Flashsale] ending time :", ending_time_str)

        if flashsale_enabled and flashsale_ended(ending_time_str):
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
    try:
        if(pinning_enabled and time_to_pin(last_pin_time_epoch)):
            product_index = product_index % 10
            print('['+time.strftime('%H:%M')+'][Pinning] Time to pin ['+str(product_index)+"] ", end="")
            for live_index in range(live_count):
                browser.switch_to.window(browser.window_handles[live_index+1])
                try:
                    browser.execute_script("arguments[0].scrollIntoView();", products[live_index][product_index])
                    products[live_index][product_index].click()
                    print("["+str(live_index)+"]", end="")
                    #print("["+str(live_index)+"-"+str(product_index)+"]", end="")
                except:
                    print("["+str(live_index)+"-"+str(product_index)+"] FAILED")
                    time.sleep(1)
                    continue
            print("")

            product_index = product_index + 1
            last_pin_time_epoch = datetime.datetime.now().timestamp()
    except:
        print('['+time.strftime('%H:%M')+'][Pinning] Error')

    time.sleep(1)






