import subprocess
import threading
import time

import json
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = json.loads(os.getenv('TOKEN', 'True').replace('\n', '').replace('\\',''))
UIDS = json.loads(os.getenv('LIVE_CHAT_IDS', 'True').replace('\n', '').replace('\\','').replace(' ',''))

#uids = [
#    ["byprw_official","CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW"],
#    ["prw.xx", "PNTRtn2tZDnz6zI3mVRC4o7xthxogTVwDmo21HI2r07"],
#]

def callback(uid, token):
    print("[Execute] python", '4-web-live-chat.py', uid, token)
    process = subprocess.run(['python', '4-web-live-chat.py', uid, token])

threads = []
threads_sleep_time = []

for temp in range(len(UIDS)):
    threads.append([])
    threads_sleep_time.append(5)

while True:
    for i in range(len(UIDS)):
        if threads[i] == []:
            time.sleep(threads_sleep_time[i])
            uid = UIDS[i]
            token = TOKEN[UIDS[i]]
            threads[i] = threading.Thread(target=callback, args=[uid, token])
            threads[i].start()
            #print('[xxx]', type(threads[i]))
            if(threads_sleep_time[i] < 30):
                threads_sleep_time[i] = 30
            else:
                threads_sleep_time[i] = threads_sleep_time[i] * 2
            if(threads_sleep_time[i] > 3600):
                threads_sleep_time[i] = 3600

        elif type(threads[i]) == threading.Thread:
            if not threads[i].is_alive():
                print("[ATTENTION]", uid, "Disconnected")
                threads[i] = []
    time.sleep(2)
    #process = subprocess.run(['python', 'tiktok-client.py', account[0], account[1]])

