import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
clips = os.listdir('loop')

import pygame
import random

main_volume = 0.05

pygame.mixer.init()
i = 0
while(True):


    main = pygame.mixer.Sound('loop\\'+clips[i])
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

                    q = pygame.mixer.Sound('comment\\'+speech)
                    
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
                        ['แถม', 'reply_bogof_1.mp3'],
                        ['แท้', 'partner_genuine_1.mp3'],
                        ['ผช', 'pro_men_best_seller.mp3'],
                        ['ผู้ชาย', 'pro_men_best_seller.mp3'],
                    ]    
                    
                    if("แถม" in speech):
                        reply_file = 'reply\\reply_bogof_1.mp3'
                    elif("แท้" in speech):
                        reply_file = 'reply\\partner_genuine_1.mp3'
                    elif("ผช" in speech or "ผู้ชาย" in speech):
                        reply_file = 'reply\\pro_men_best_seller.mp3'

                    for search in search_array:
                        if search[0] in speech:
                            reply_file = 'reply\\' + search[1]
                            break
                    

                    if(reply_file != ''):
                        reply = pygame.mixer.Sound(reply_file)
                        reply.set_volume(main_volume)
                        print('['+time.strftime('%H:%M')+'][Reply] : play ' + reply_file + ' | Duration : ', reply.get_length())
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