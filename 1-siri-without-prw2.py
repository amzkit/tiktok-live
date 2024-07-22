import time
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
clips = os.listdir('loop')

from gtts import gTTS

import pygame
import random

#Line Notify
import requests

#PRW2 Token
url = 'https://notify-api.line.me/api/notify'
token = 'AQaMH3QBpt26fMtJajb0FAusthjXwAhZ7eMcDGZuriT'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
#main_volume = 0.05

reply_path = 'reply'
comment_path = 'comment'
comment_error_path = 'error'

loop_path = 'loop'

sound_ext = '.ogg'

play_background_music = False

# Remove stale_comments
stale_comments = os.listdir(comment_path)
for file in stale_comments:
    try:
        os.remove(os.path.join(comment_path, file))
    except:
        print('['+time.strftime('%H:%M')+'][FATAL ERROR] ลบไฟล์เก่าไม่ได้ ' + file)
        try:
            r = requests.post(url, headers=headers, data = {'message': 'มีไฟล์ที่ลบไม่ได้ '+file})
        except:
            print('['+time.strftime('%H:%M')+'][FATAL ERROR] Line Notify Error: (Remove Stale)')

        time.sleep(10)

#play blackground music
import subprocess
import threading

def callback():
    process = subprocess.run(['python', 'play-background-music.py'])

if play_background_music:
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

    #[['ปลายทาง'], []],


]

while(True):
    #main loop

    # Comment Found
    speech_queue = os.listdir(comment_path)
    #chats = requests.get("https://line.ininit.com/chats")
    #if(chats):
    #    chats = chats.json()["chats"]
    #    if(len(chats)):
    #        for chat in chats:
    #            tts = gTTS(chat['text'], lang='th')
    #
    #            filename = str(int(time.time())) + '_' + chat['text']
    #            #filename = ''.join(e for e in filename if e.isalnum())
    #            tts.save(os.path.join(comment_path, filename +'.ogg'))
    #
    if len(speech_queue) > 0:
        time.sleep(0.5)
        # if there is speech, pause main loop
        for speech in speech_queue:
            speech_filename = speech

            #Playing Chat
            try:
                q = pygame.mixer.Sound(os.path.join(comment_path, speech_filename))
                print('['+time.strftime('%H:%M')+'][Chat] ' + speech_filename + ' [' + str(int(q.get_length())) + 's]')
                pygame.mixer.Channel(1).play(q)
                while pygame.mixer.Channel(1).get_busy():
                    time.sleep(1)
            except:
                print('['+time.strftime('%H:%M')+'][ERROR] Playing chat error', speech_filename)
                #!!!! DANGEROUS IF ERROR AND CANNOT REMOVE FILE

            #Removing Chat
            try:
                os.remove(os.path.join(comment_path, speech_filename))
            except:
                print('['+time.strftime('%H:%M')+'][ERROR] Remove chat error', speech_filename)
                continue

    time.sleep(1)



