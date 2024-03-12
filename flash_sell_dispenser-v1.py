import time
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

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\\Users\\Kit\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 19") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--remote-debugging-pipe')
options.add_argument("--start-maximized")
browser = webdriver.Chrome(options)

browser.get('https://seller-th.tiktok.com/account/login?shop_region=TH')

#browser.switch_to.window(browser.window_handles[0])
#ปุ่มโฮม
#WebDriverWait(browser, 5).until(ExpectedConditions.presence_of_element_located((By.ID, 'top_nav_seller_center_logo'))).click()
#เมนู โปรโมชั่น
WebDriverWait(browser, 30).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//div[@class='theme-m4b-menu-title-txt'][contains(text(),'โปรโมชั่น')]"))).click()
#เมนูย่อย เครื่องมือโปรโมชั่น
WebDriverWait(browser, 10).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//a[@id='menu_item_35']//div[1]"))).click()



while True:
    # Check if flash sell still going on

    # Check ending time
    WebDriverWait(browser, 20).until(ExpectedConditions.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td/div/span/div")))
    ending_time_str = browser.find_elements(By.XPATH, "//table/tbody/tr/td[4]/div/span/div")[0].text
    ending_time_epoch = int(datetime.datetime.strptime(ending_time_str, '%d/%m/%Y %H:%M').timestamp())
    now_epoch = int(datetime.datetime.now().timestamp())

    waiting_seconds = 0
    if((now_epoch) > (ending_time_epoch)):
        #no flash deal is going on
        print("Create new flash deal")
    elif((now_epoch) <= (ending_time_epoch)):
        waiting_seconds = ending_time_epoch - now_epoch
        print("Flashdeal is going on, will end in", waiting_seconds, "seconds")

    #    if browser.find_elements(By.XPATH, "//table/tbody/tr/td[2]/div/span/span/div/span/div/div[contains(text(), 'กำลังจะจัดขึ้น')]") or \
    #       browser.find_elements(By.XPATH, "//table/tbody/tr/td[2]/div/span/span/div/span/div/div[contains(text(), 'ดำเนินการอยู่')]"):
    #        waiting_seconds = waiting_seconds + 1200

    print("Waiting Time :", waiting_seconds, "seconds")

    time.sleep(waiting_seconds)

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

    print("End Loop")
