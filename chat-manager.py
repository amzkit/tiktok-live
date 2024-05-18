import subprocess
import threading
import time

uids = [
    ["byprw_official","CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW"],
    ["prw.xx", "PNTRtn2tZDnz6zI3mVRC4o7xthxogTVwDmo21HI2r07"],
]

def callback(uid, token):
    print("[Execute] python", 'chat.py', uid, token)
    process = subprocess.run(['python', 'chat.py', uid, token])

threads = []
threads_sleep_time = []

for temp in range(len(uids)):
    threads.append([])
    threads_sleep_time.append(2)

while True:
    for i in range(len(uids)):
        if threads[i] == []:
            time.sleep(threads_sleep_time[i])
            uid = uids[i][0]
            token = uids[i][1]
            threads[i] = threading.Thread(target=callback, args=[uid, token])
            threads[i].start()
            #print('[xxx]', type(threads[i]))

            threads_sleep_time[i] = threads_sleep_time[i] * 2
            if(threads_sleep_time[i] > 900):
                threads_sleep_time[i] = 900

        elif type(threads[i]) == threading.Thread:
            if not threads[i].is_alive():
                threads[i] = []
    time.sleep(2)
    #process = subprocess.run(['python', 'tiktok-client.py', account[0], account[1]])

