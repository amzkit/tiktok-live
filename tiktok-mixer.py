import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
clips = os.listdir('loop')

import pygame
import random
from pathlib import Path

#Line Notify
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'AQaMH3QBpt26fMtJajb0FAusthjXwAhZ7eMcDGZuriT'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
main_volume = 0.05

reply_path = Path('reply/')
comment_path = Path('comment/')
music_path = Path('music/')
loop_path = Path('loop/')

#play blackground music
pygame.mixer.init()
pygame.mixer.music.load(music_path / 'kpop.mp3')
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(loops=-1)

i = 0
while(True):


    #main loop
    main = pygame.mixer.Sound(loop_path / clips[i])
    print('['+time.strftime('%H:%M')+'][Main] : playing ' + clips[i] + ' | Duration : ', main.get_length())
    pygame.mixer.Channel(0).queue(main)
    main.set_volume(main_volume)
    #main.play()
    pygame.mixer.Channel(0).play(main)

    while pygame.mixer.get_busy():
        # Comment Found
        speech_queue = os.listdir('comment')
        if len(speech_queue) > 0:
            time.sleep(0.5)
            # if there is speech, pause main loop
            for speech in speech_queue:
                try:
                    pygame.mixer.Channel(0).pause()
                    reply_file = ''

                    q = pygame.mixer.Sound(comment_path / speech)
                    
                    print('['+time.strftime('%H:%M')+'][Speech] : play ' + speech + ' | Duration : ', q.get_length())
                    pygame.mixer.Channel(1).play(q)
                    #q = pygame.mixer.Sound('comment\\'+speech)
                    #pygame.mixer.pause()
                    #pygame.time.wait(int(q.get_length()*1000))
                    #q.play()
                    while pygame.mixer.Channel(1).get_busy():
                        time.sleep(1)
                        #time.sleep(0.5)
                    
                    # Reply
                    #print(speech)
                    search_array = [
    #   [['keyword1','keyword2', 'keyword3'], ['filename_1', 'filename_2']],
    #   keyword1 and keyword2 and keyword 3 => reply with filename_1 or filename_2 randomly
                        [['ผช','แถม','กลิ่น'], ['can_be_mixed_1.mp3','can_be_mixed_2.mp3']],

                        [['คละ','กลิ่น'], ['can_be_mixed_1.mp3','can_be_mixed_2.mp3']],

                        [['แถม', 'สี'], ['what_scent_of_free_gift_1.mp3']],
                        [['เทส', 'สี'], ['what_scent_of_free_gift_1.mp3']],

                        [['แถม', 'ของ'], ['reply_bogof_1.mp3']],
                        [['1', 'แถม'], ['reply_bogof_1.mp3']],
                        [['แถม'], ['reply_bogof_1.mp3']],
                        [['แท้'], ['partner_genuine_1.mp3']],



                        [['sexy'], ['desc_sexy.mp3']],
                        [['เซ็กซี่'], ['desc_sexy.mp3']],
                        [['กลิ่นไหน','หอม'],['best_scent_sexy_1.mp3']],
                        [['ขายดี'],['best_seller_sexy_1.mp3','best_seller_sexy_2.mp3']],
                        [['ไป','เรียน'],['bonnie_scenario_1.mp3']],
                        [['ไป','ทำงาน'],['bonnie_scenario_1.mp3']],
                        [['ไป','มหาลัย'],['bonnie_scenario_1.mp3']],
                        [['ไป','ออฟฟิต'],['bonnie_scenario_1.mp3']],
                        [['บอนนี่'], ['desc_bonnie.mp3']],
                        [['bonnie'], ['desc_bonnie.mp3']],
                        [['แป้ง'], ['desc_bonnie.mp3']],


                        [['sweetie'], ['desc_sweetie.mp3']],
                        [['picnic'], ['desc_sweetie.mp3']],
                        [['สวีตตี้'], ['desc_sweetie.mp3']],
                        [['ปิก'], ['desc_sweetie.mp3']],
                        [['ปิค'], ['desc_sweetie.mp3']],
                        [['นิค'], ['desc_sweetie.mp3']],
                        [['นิก'], ['desc_sweetie.mp3']],

                        [['blooming'], ['desc_blooming.mp3']],
                        [['boom'], ['desc_blooming.mp3']],
                        [['บูม'], ['desc_blooming.mp3']],
                        [['บลูมมิ่ง'], ['desc_blooming.mp3']],

                        [['wood'], ['desc_wood.mp3']],
                        [['วูด'], ['desc_wood.mp3']], 

                        [['กลิ่นใหม่'], ['desc_charming_sexy_martiny.mp3']],
                        [['ใช้ได้','นาน'], ['how_long_can_be_use_1.mp3','how_long_can_be_use_2.mp3','how_long_can_be_use_3.mp3']],


                        [['ml'], ['how_many_ml_1.mp3','how_many_ml_2.mp3','how_many_ml_3.mp3']],
                        [['คละ','กลิ่น'], ['can_be_mixed_1.mp3','can_be_mixed_2.mp3']],

                        [['สั่ง','แล้ว'],['ordered_1.mp3','ordered_1.mp3','ordered_2.mp3']],
                        [['สั่ง','ละ'],['ordered_1.mp3','ordered_1.mp3','ordered_2.mp3']],
                        [['สั่ง','ไป'],['ordered_1.mp3','ordered_1.mp3','ordered_2.mp3']],

                        [['ส่ง','วัน'],['how_many_days_1.mp3','how_many_days_2.mp3']],
                        [['ส่ง','ของ'],['how_many_days_1.mp3','how_many_days_2.mp3']],

                        [['ติด','ทน'],['how_long_it_stays_1.mp3','how_long_it_stays_2.mp3','how_long_it_stays_3.mp3']],
                        [['ติด','นาน'],['how_long_it_stays_1.mp3','how_long_it_stays_2.mp3','how_long_it_stays_3.mp3']],

                        [['unisex'], ['unisex_1.mp3','unisex_1.mp3','unisex_2.mp3']],
                        [['ผช','ผญ'], ['unisex_1.mp3','unisex_1.mp3','unisex_2.mp3']],
                        [['ชาย','หญิง'], ['unisex_1.mp3','unisex_1.mp3','unisex_2.mp3']],
                        [['ผช','หญิง'], ['unisex_1.mp3','unisex_1.mp3','unisex_2.mp3']],
                        [['ชาย','ผญ'], ['unisex_1.mp3','unisex_1.mp3','unisex_2.mp3']],

                        [['ผช'], ['desc_men.mp3']],
                        [['ผู้ชาย'], ['desc_men.mp3']],

                        [['ไม่ฉุน'],['non_stink.mp3']],
                        [['กลิ่น','อ่อน'],['gentle_smell_bonnie_sweetie_1.mp3','gentle_smell_bonnie_sweetie_2.mp3']],
                        [['ตะกร้า'],['basket_123_1.mp3']],

                        [['ไม่','ระบุ'],['forget_to_select_1.mp3','forget_to_select_2.mp3']],
                        [['ลืม','ระบุ'],['forget_to_select_1.mp3','forget_to_select_2.mp3']],
                        [['ไม่','แจ้ง'],['forget_to_select_1.mp3','forget_to_select_2.mp3']],
                        [['ลืม','แจ้ง'],['forget_to_select_1.mp3','forget_to_select_2.mp3']],

                        [['ขนส่ง'],['shipping_1.mp3']],
                    ]

                    for search in search_array:
                        found_all = True
                        for keyword in search[0]:
                            if not (keyword in speech.lower()):
                                found_all = False
                                break
                        if found_all:
                            reply_file = search[1][int(random.random()*100) % len(search[1])]
                            break

                    if(reply_file != ''):
                        reply = pygame.mixer.Sound(reply_path / reply_file)
                        reply.set_volume(main_volume)
                        print('['+time.strftime('%H:%M')+'][Reply] : play ' + reply_file + ' | Duration : ', reply.get_length())
                        r = requests.post(url, headers=headers, data = {'message':'ตอบกลับ ' + reply_file})
                        pygame.mixer.Channel(1).play(reply)
                        
                        while pygame.mixer.Channel(1).get_busy():
                            time.sleep(1)
                        reply_file = ''
                        
                    print('['+time.strftime('%H:%M')+'][Main] : continue ' + clips[i])
                    pygame.mixer.Channel(0).unpause()

                    os.remove('comment\\'+speech)
                except FileNotFoundError:
                    print(FileNotFoundError)
        time.sleep(2)

    # play next clip
    i = (i + 1) % len(clips)


#mixer.music.load("speech.mp3")
#mixer.music.play()




#while mixer.music.get_busy():  # wait for music to finish playing
#    time.sleep(0.5)