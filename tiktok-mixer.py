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
main_volume = 0.05

reply_path = 'reply'
comment_path = 'comment'
comment_error_path = 'error'
music_path = 'music'
loop_path = 'loop'

sound_ext = '.ogg'
#play blackground music
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(music_path, 'kpop'+sound_ext))
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(loops=-1)

search_array = [
#   [['keyword1','keyword2', 'keyword3'], ['filename_1', 'filename_2']],
#   keyword1 and keyword2 and keyword 3 => reply with filename_1 or filename_2 randomly
    [['ผช','แถม','กลิ่น'], ['can_be_mixed_1','can_be_mixed_2']],

    [['คละ','กลิ่น'], ['can_be_mixed_1','can_be_mixed_2']],

    [['แถม', 'สี'], ['what_scent_of_free_gift_1']],
    [['เทส', 'สี'], ['what_scent_of_free_gift_1']],

    [['แถม', 'ของ'], ['reply_bogof_1']],
    [['1', 'แถม'], ['reply_bogof_1']],

    [['sexy'], ['desc_sexy']],
    [['เซ็กซี่'], ['desc_sexy']],
    [['เที่ยว','กลางคืน'],['desc_sexy']],
    [['เที่ยว','ผับ'],['desc_sexy']],
    [['ซซ'],['desc_sexy']],
    [['ขายดี'],['best_seller_sexy_1','best_seller_sexy_2']],
    [['กลิ่นไหน','หอม'],['best_scent_sexy_1']],

    [['ไป','เรียน'],['bonnie_scenario_1']],
    [['ไป','ทำงาน'],['bonnie_scenario_1']],
    [['มหาลัย'],['bonnie_scenario_1']],
    [['ออฟฟิต'],['bonnie_scenario_1']],
    [['บอนนี่'], ['desc_bonnie']],
    [['bonnie'], ['desc_bonnie']],
    [['แป้ง'], ['desc_bonnie']],

    [['sweetie'], ['desc_sweetie']],
    [['picnic'], ['desc_sweetie']],
    [['สวีตตี้'], ['desc_sweetie']],
    [['สวีทตี้'], ['desc_sweetie']],
    [['ปิก'], ['desc_sweetie']],
    [['ปิค'], ['desc_sweetie']],
    [['นิค'], ['desc_sweetie']],
    [['นิก'], ['desc_sweetie']],
    [['หวาน'], ['desc_sweetie']],

    [['blooming'], ['desc_blooming']],
    [['boom'], ['desc_blooming']],
    [['บูม'], ['desc_blooming']],
    [['บลูมมิ่ง'], ['desc_blooming']],

    [['wood'], ['desc_wood']],
    [['วูด'], ['desc_wood']], 
    [['สดชื่น'], ['desc_wood']],
    [['ไม่หวาน'], ['desc_wood']],

    [['กลิ่นใหม่'], ['desc_charming_sexy_martiny']],
    [['ใช้ได้','นาน'], ['how_long_can_be_use_1','how_long_can_be_use_2','how_long_can_be_use_3']],


    [['ml'], ['how_many_ml_1','how_many_ml_2','how_many_ml_3']],
    [['คละ','กลิ่น'], ['can_be_mixed_1','can_be_mixed_2']],

    [['สั่ง','แล้ว'],['ordered_1','ordered_1','ordered_2']],
    [['สั่ง','ละ'],['ordered_1','ordered_1','ordered_2']],
    [['สั่ง','ไป'],['ordered_1','ordered_1','ordered_2']],

    [['กี่','วัน'],['how_many_days_1','how_many_days_2']],
    [['ส่ง','วัน'],['how_many_days_1','how_many_days_2']],
    [['ส่ง','ของ'],['how_many_days_1','how_many_days_2']],

    [['ติด','ทน'],['how_long_it_stays_1','how_long_it_stays_2','how_long_it_stays_3']],
    [['ติด','นาน'],['how_long_it_stays_1','how_long_it_stays_2','how_long_it_stays_3']],

    [['unisex'], ['unisex_1','unisex_1','unisex_2']],
    [['ผช','ผญ'], ['unisex_1','unisex_1','unisex_2']],
    [['ชาย','หญิง'], ['unisex_1','unisex_1','unisex_2']],
    [['ผช','หญิง'], ['unisex_1','unisex_1','unisex_2']],
    [['ชาย','ผญ'], ['unisex_1','unisex_1','unisex_2']],

    [['ผช'], ['desc_men']],
    [['ผู้ชาย'], ['desc_men']],

    [['ไม่ฉุน'],['non_stink_1']],
    [['กลิ่น','อ่อน'],['gentle_smell_bonnie_sweetie_1','gentle_smell_bonnie_sweetie_2']],
    [['ตะกร้า'],['basket_123_1']],

    [['ไม่','ระบุ'],['forget_to_select_1','forget_to_select_2']],
    [['ลืม','ระบุ'],['forget_to_select_1','forget_to_select_2']],
    [['ไม่','แจ้ง'],['forget_to_select_1','forget_to_select_2']],
    [['ลืม','แจ้ง'],['forget_to_select_1','forget_to_select_2']],

    [['ขนส่ง'],['shipping_1']],
    [['แถม'], ['reply_bogof_1']],
    [['แท้'], ['partner_genuine_1']],
]

i = 0
while(True):
    #main loop
    main = pygame.mixer.Sound(os.path.join(loop_path, clips[i]))
    print('['+time.strftime('%H:%M')+'][Main] : playing ' + clips[i] + ' | Duration :', int(main.get_length()), 'secs')
    pygame.mixer.Channel(0).queue(main)
    main.set_volume(main_volume)
    #main.play()
    pygame.mixer.Channel(0).play(main)

    while pygame.mixer.get_busy():
        # Comment Found
        speech_queue = os.listdir(comment_path)
        if len(speech_queue) > 0:
            time.sleep(0.5)
            # if there is speech, pause main loop
            for speech in speech_queue:
                try:
                    pygame.mixer.Channel(0).pause()
                    reply_file = ''

                    q = pygame.mixer.Sound(os.path.join(comment_path, speech))
                    
                    print('['+time.strftime('%H:%M')+'][Speech] : play ' + speech + ' | Duration :', int(q.get_length()), 'secs')
                    pygame.mixer.Channel(1).play(q)
                    #q = pygame.mixer.Sound('comment\\'+speech)
                    #pygame.mixer.pause()
                    #pygame.time.wait(int(q.get_length()*1000))
                    #q.play()
                    while pygame.mixer.Channel(1).get_busy():
                        time.sleep(1)
                        
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
                        r = requests.post(url, headers=headers, data = {'message': 'ตอบกลับ ' + reply_file})
                        reply_file = reply_file + sound_ext
                        reply = pygame.mixer.Sound(os.path.join(reply_path, reply_file))
                        print('['+time.strftime('%H:%M')+'][Reply] : play ' + reply_file + ' | Duration :', int(reply.get_length()), 'secs')
                        reply.set_volume(main_volume)
                        pygame.mixer.Channel(1).play(reply)
                        
                        while pygame.mixer.Channel(1).get_busy():
                            time.sleep(1)
                        reply_file = ''
                        
                    print('['+time.strftime('%H:%M')+'][Main] : continue ' + clips[i])
                    pygame.mixer.Channel(0).unpause()

                    os.remove(os.path.join(comment_path, speech))
                except FileNotFoundError:
                    time.sleep(1)
                    try:
                        print("FileNotFoundError:", os.path.join(comment_path, speech))
                        if os.path.exists(os.path.join(comment_path, speech)):
                            os.rename(os.path.join(comment_path, speech), os.path.join(comment_error_path, speech))
                    except:
                        time.sleep(1)
                        print("Error: cannot move a file", os.path.join(comment_path, speech))
                        r = requests.post(url, headers=headers, data = {'message': 'Error: ' + reply_file})

        time.sleep(2)

    # play next clip
    i = (i + 1) % len(clips)
