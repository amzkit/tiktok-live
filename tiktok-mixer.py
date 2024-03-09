import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
clips = os.listdir('loop')

import pygame
import random

#Line Notify
import requests


url = 'https://notify-api.line.me/api/notify'
token = 'AQaMH3QBpt26fMtJajb0FAusthjXwAhZ7eMcDGZuriT'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
#main_volume = 0.05

reply_path = 'reply'
comment_path = 'comment'
comment_error_path = 'error'

loop_path = 'loop'

sound_ext = '.ogg'


#play blackground music
import subprocess
import threading

def callback():
    process = subprocess.run(['python', 'play-background-music.py'])

thread = threading.Thread(target=callback)
thread.start()

#main loop
pygame.mixer.init()
#pygame.mixer.music.load(os.path.join(music_path, 'kpop'+sound_ext))
#pygame.mixer.music.set_volume(0.03)
#pygame.mixer.music.play(loops=-1)

search_array = [
#   [['keyword1','keyword2', 'keyword3'], ['filename_1', 'filename_2']],
#   keyword1 and keyword2 and keyword 3 => reply with filename_1 or filename_2 randomly
    [['ผช','แถม','กลิ่น'], ['can_be_mixed_1','can_be_mixed_2']],

    [['คละ','กลิ่น'], ['can_be_mixed_1','can_be_mixed_2']],

    [['แถม', 'สี'], ['แถมสี_สีสติ๊กเกอร์']],
    [['เทส', 'สี'], ['แถมสี_สีสติ๊กเกอร์']],

    [['แถม', 'ของ'], ['แถม_1แถม1ตะกร้าที่1เท่านั้น']],
    [['1', 'แถม'], ['แถม_1แถม1ตะกร้าที่1เท่านั้น']],

    [['sexy'], ['ซซ_รีวิวเซกซี่']],
    [['เซ็กซี่'], ['ซซ_รีวิวเซกซี่']],
    [['ซซ'],['ซซ_รีวิวเซกซี่']],

    [['ขายดี'],['ขายดี_บลูมมิ่ง_เซกซี่']],
    [['กลิ่นไหน','หอม'],['ขายดี_บลูมมิ่ง_เซกซี่']],

    [['บอนนี่'], ['บอนนี่_รีวิวบอนนี่']],
    [['bonnie'], ['บอนนี่_รีวิวบอนนี่']],

    [['sweetie'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['picnic'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['สวีตตี้'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['สวีทตี้'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['ปิก'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['ปิค'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['นิค'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],
    [['นิก'], ['ปิคนิค_ปิคนิคดีที่สุด','ปิคนิค_ปิคนิค1']],

    [['blooming'], ['บลุมมื่ง_บลุมมื่ง']],
    [['boom'], ['บลุมมื่ง_บลุมมื่ง']],
    [['บูม'], ['บลุมมื่ง_บลุมมื่ง']],
    [['บลูมมิ่ง'], ['บลุมมื่ง_บลุมมื่ง']],

    [['wood'], ['วูดแซน_วูดแซน']],
    [['วูด'], ['วูดแซน_วูดแซน']], 

    [['กลิ่นใหม่'], ['หนังสือ_รีวิวหนังสือ']],
    [['หนังสือ'], ['หนังสือ_รีวิวหนังสือ']],
    [['ใช้','นาน'], ['ใช้นาน_ใช้ได้นาน','ใช้นาน_ใช้ได้นาน2']],

    [['onyx'], ['onyx_สำหรับonyx_1','onyx_สำหรับonyx_2']],
    [['โอนิค'], ['onyx_สำหรับonyx_1','onyx_สำหรับonyx_2']],
    [['โอนิก'], ['onyx_สำหรับonyx_1','onyx_สำหรับonyx_2']],
    [['ออนิก'], ['onyx_สำหรับonyx_1','onyx_สำหรับonyx_2']],
    [['ออนิค'], ['onyx_สำหรับonyx_1','onyx_สำหรับonyx_2']],

    [['tender'], ['tender_สำหรับtender_1', 'tender_สำหรับtender_2']],
    [['เทนเดอ'], ['tender_สำหรับtender_1', 'tender_สำหรับtender_2']],

    [['exceed'], ['exceed_สำหรับกลิ่นexceed_1','exceed_สำหรับกลิ่นexceed_2']],
    [['เอ๊กซ'], ['exceed_สำหรับกลิ่นexceed_1','exceed_สำหรับกลิ่นexceed_2']],
    [['เอกซ'], ['exceed_สำหรับกลิ่นexceed_1','exceed_สำหรับกลิ่นexceed_2']],
    [['เอก'], ['exceed_สำหรับกลิ่นexceed_1','exceed_สำหรับกลิ่นexceed_2']],

    [['ml'], ['ml_ขนาด_30_กับ_2']],
    [['คละ','กลิ่น'], ['can_be_mixed_1','can_be_mixed_2']],

    [['สั่ง','แล้ว'],['สั่งแล้ว_สั่งแล้ว1','สั่งแล้ว_สั่งแล้ว2']],
    [['สั่ง','ละ'],['สั่งแล้ว_สั่งแล้ว1','สั่งแล้ว_สั่งแล้ว2']],
    [['สั่ง','ไป'],['สั่งแล้ว_สั่งแล้ว1','สั่งแล้ว_สั่งแล้ว2']],

    [['ดูฟ'], ['ดุฟ_ดุฟรวมทั้งหมด']],
    [['ดูป'], ['ดุฟ_ดุฟรวมทั้งหมด']],
    [['กลิ่น', 'คล้าย'], ['ดุฟ_ดุฟรวมทั้งหมด']],
    [['กลิ่น', 'เทียบ'], ['ดุฟ_ดุฟรวมทั้งหมด']],


    [['ส่ง','จาก'], ['ส่งจาก_ส่งจากเชียงใหม่']],

    [['จัดส่ง'],['กี่วัน_จัดส่ง_ครบ_เคลม']],
    [['กี่','วัน'],['กี่วัน_จัดส่ง_ครบ_เคลม']],
    [['ส่ง','วัน'],['กี่วัน_จัดส่ง_ครบ_เคลม']],
    [['ส่ง','ของ'],['กี่วัน_จัดส่ง_ครบ_เคลม']],

    [['ติด','ทน'],['ติดทน_ติดทนนานไม']],
    [['ติด','นาน'],['ติดทน_ติดทนนานไม']],

    [['unisex'], ['unisex_ใช้ได้ทั้งผญ_ผช']],
    [['ผช','ผญ'], ['unisex_ใช้ได้ทั้งผญ_ผช']],
    [['ชาย','หญิง'], ['unisex_ใช้ได้ทั้งผญ_ผช']],
    [['ผช','หญิง'], ['unisex_ใช้ได้ทั้งผญ_ผช']],
    [['ชาย','ผญ'], ['unisex_ใช้ได้ทั้งผญ_ผช']],

    [['ผช'], ['รีวิวผช_ผช_รีวิวครบ_กลิ่นเทียบ']],
    [['ผู้ชาย'], ['รีวิวผช_ผช_รีวิวครบ_กลิ่นเทียบ']],

    [['ผญ'], ['ผญ_รีวิว_ผู้หญิง']],
    [['ผู้หญิง'], ['ผญ_รีวิว_ผู้หญิง']],


    [['ชาร์ม'], ['ชาร์มมิ่ง_ชาร์มมิ่ง','ชาร์มมิ่ง_ชาร์มมิ่ง2']],
    [['charm'], ['ชาร์มมิ่ง_ชาร์มมิ่ง','ชาร์มมิ่ง_ชาร์มมิ่ง2']],
    [['ขวด', 'ส้ม'], ['ชาร์มมิ่ง_ชาร์มมิ่ง','ชาร์มมิ่ง_ชาร์มมิ่ง2']],


    [['มาติ'], ['มาตินี่_เซกซี่มาตินี่']],
    [['ม่วง'], ['มาตินี่_เซกซี่มาตินี่']],
    [['martini'], ['มาตินี่_เซกซี่มาตินี่']],
    [['martiny'], ['มาตินี่_เซกซี่มาตินี่']],

    [['เติม'], ['เติม_เติมตะกร้า']],

    [['ฉุน'],['ฉุน_ไม่ฉุน_เวียน','ฉุน_กลิ่นไม่ฉุนไม่เวียนหัว']],
    [['เวียนหัว'],['ฉุน_ไม่ฉุน_เวียน','ฉุน_กลิ่นไม่ฉุนไม่เวียนหัว']],

    [['หนาว'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['memory'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['เมมโม'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['โมรี่'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['cuddle'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['คัด','เดิ้ล'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['คัท','เดิ้ล'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['คัท','เดิ้น'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['คัด','เดิ้น'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['warm'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['วอร์ม'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],
    [['วอม'],['หนาว_คอลหน้าหนาว','หนาว_คอลหน้าหนาว2']],


    [['ไม่','ระบุ'],['ลืมแจ้ง_ไม่ได้ระบุกลิ่น']],
    [['ลืม','ระบุ'],['ลืมแจ้ง_ไม่ได้ระบุกลิ่น']],
    [['ไม่','แจ้ง'],['ลืมแจ้ง_ไม่ได้ระบุกลิ่น']],
    [['ลืม','แจ้ง'],['ลืมแจ้ง_ไม่ได้ระบุกลิ่น']],

    [['ขนส่ง'],['ขนส่ง_ขนส่ง']],
    [['แท้'], ['แท้_✅Geniune 3']],

    [['กะล่อน'], ['กะล่อน_กลิ่นฟลุ้คกะล่อน']],



    [['ไม่หวาน'], ['ไม่หวาน_แนะนำวูดแซน']],
    [['สดชื่น'], ['ไม่หวาน_แนะนำวูดแซน']],
    [['กลิ่น','หวาน'], ['หวาน_แนะนำปิคนิค']],
    [['แป้ง'], ['แป้ง_แนะนำบอนนี่']],
    [['กลิ่น','อ่อน'],['แป้ง_แนะนำบอนนี่']],
    [['ไป','เรียน'],['แป้ง_แนะนำบอนนี่']],
    [['ไป','ทำงาน'],['แป้ง_แนะนำบอนนี่']],
    [['คุณหนู'],['แป้ง_แนะนำบอนนี่']],
    [['มหาลัย'],['แป้ง_แนะนำบอนนี่']],
    [['ออฟฟิต'],['แป้ง_แนะนำบอนนี่']],
    [['เที่ยว','กลางคืน'],['เที่ยวกลางคืน_แนะนำเซกซี่']],
    [['เที่ยว','ผับ'],['เที่ยวกลางคืน_แนะนำเซกซี่']],
    [['หัน','มอง'],['เที่ยวกลางคืน_แนะนำเซกซี่']],

    [['แถม'], ['แถม_1แถม1ตะกร้าที่1เท่านั้น']],

    [['ตะกร้า', '10'],['ตะกร้าที่_10']],
    [['ตะกร้า', '1'],['ตะกร้าที่_1']],
    [['ตะกร้า', '2'],['ตะกร้าที่_2']],
    [['ตะกร้า', '3'],['ตะกร้าที่_3']],

    [['ตะกร้า', '4'],['ตะกร้าที่_4']],
    [['ตะกร้า', '5'],['ตะกร้าที่_5']],
    [['ตะกร้า', '6'],['ตะกร้าที่_6']],
    [['ตะกร้า', '7'],['ตะกร้าที่_7']],
    [['ตะกร้า', '8'],['ตะกร้าที่_8']],
    [['ตะกร้า', '9'],['ตะกร้าที่_9']],

    [['01'], ['01_แอดมินตอบ']],

]

i = 0
while(True):
    #main loop
    main = pygame.mixer.Sound(os.path.join(loop_path, clips[i]))
    print('['+time.strftime('%H:%M')+'][Main] : playing ' + clips[i] + ' | Duration :', int(main.get_length()), 'secs')
    pygame.mixer.Channel(0).queue(main)
    #main.set_volume(main_volume)
    #main.play()
    pygame.mixer.Channel(0).play(main)

    while pygame.mixer.get_busy():
        # Comment Found
        speech_queue = os.listdir(comment_path)
        if len(speech_queue) > 0:
            time.sleep(0.5)
            # if there is speech, pause main loop
            for speech in speech_queue:
                speech_filename = speech
                try:
                    pygame.mixer.Channel(0).pause()
                    reply_file = ''

                    q = pygame.mixer.Sound(os.path.join(comment_path, speech_filename))

                    print('['+time.strftime('%H:%M')+'][Speech] : play ' + speech_filename + ' | Duration :', int(q.get_length()), 'secs')
                    pygame.mixer.Channel(1).play(q)
                    #q = pygame.mixer.Sound('comment\\'+speech)
                    #pygame.mixer.pause()
                    #pygame.time.wait(int(q.get_length()*1000))
                    #q.play()
                    speech = speech.split("_")[1:]
                    speech = '_'.join(speech)

                    while pygame.mixer.Channel(1).get_busy():
                        time.sleep(1)
                    
                    #print("[TRY] playing comment done")
                    for search in search_array:
                        found_all = True
                        for keyword in search[0]:
                            if not (keyword in speech.lower()):
                                found_all = False
                                break
                        if found_all:
                            reply_file = search[1][int(random.random()*100) % len(search[1])]
                            break
                    #print("[TRY] searching for done", reply_file)

                    if(reply_file != ''):
                        r = requests.post(url, headers=headers, data = {'message': 'ตอบกลับ ' + reply_file})
                        reply_file = reply_file + sound_ext
                        #print("[TRY] reply with ", reply_file)

                        if not os.path.exists(os.path.join(reply_path, reply_file)):
                            print("[ERROR] Missing reply file", reply_file)
                            os.remove(os.path.join(comment_path, speech_filename))
                            print('['+time.strftime('%H:%M')+'][Main] : resume ' + clips[i])
                            pygame.mixer.Channel(0).unpause()
                            continue

                        reply = pygame.mixer.Sound(os.path.join(reply_path, reply_file))

                        print('['+time.strftime('%H:%M')+'][Reply] : play ' + reply_file + ' | Duration :', int(reply.get_length()), 'secs')
                        #reply.set_volume(main_volume)
                        pygame.mixer.Channel(1).play(reply)
                        
                        while pygame.mixer.Channel(1).get_busy():
                            time.sleep(1)
                        reply_file = ''
                        
                    print('['+time.strftime('%H:%M')+'][Main] : resume ' + clips[i])
                    pygame.mixer.Channel(0).unpause()

                    time.sleep(1)
                    os.remove(os.path.join(comment_path, speech_filename))
                except FileNotFoundError:
                    time.sleep(1)

                    try:
                        print("[ERROR] FileNotFoundError:", os.path.join(reply_path, reply_file))
                        r = requests.post(url, headers=headers, data = {'message': 'Error: ตรวจสอบว่ามีไฟล์คำตอบจริงไหม ' + reply_file})

                        if os.path.exists(os.path.join(comment_path, speech_filename)):
                            os.remove(os.path.join(comment_path, speech_filename))
                            print("[ERROR] The comment file has been removed", speech_filename)

                            #os.rename(os.path.join(comment_path, speech), os.path.join(comment_error_path, speech))
                            #print("[ERR] The file has been moved to error directory")
                    except:
                        time.sleep(1)
                        #r = requests.post(url, headers=headers, data = {'message': 'Error: ' + reply_file})
                    finally:
                        pygame.mixer.Channel(0).unpause()

        time.sleep(2)

    # play next clip
    i = (i + 1) % len(clips)
