import subprocess
import threading
import time
accounts = [
    ['@janua_official', 'CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW'],
    ['@prw.xx', 'PNTRtn2tZDnz6zI3mVRC4o7xthxogTVwDmo21HI2r07'],
#    ['@itsskin_byprw','zNaqvEdjUqsiHoRtHNegEh1XLIV6e4NPAtyeGwuwd3a'],
#    ['@perfumexlab', 'QRmlgL6hLf5oBBWxHrEJ9RtndZQMpOcppePlzWF069H']
]


def callback(id, token):
    process = subprocess.run(['python', 'tiktok-client.py', id, token])

threads = []
threads_sleep_time = []

for temp in accounts:
    threads.append([])
    threads_sleep_time.append(1)

while True:
    for i in range(len(accounts)):
        if threads[i] == []:
            print('['+time.strftime('%H:%M')+'][' + accounts[i][0] + '] Attempt to connect | waiting time = ' + str(threads_sleep_time[i]))
            threads[i] = threading.Thread(target=callback, args=accounts[i])
            threads[i].start()
            #print('[xxx]', type(threads[i]))

            time.sleep(threads_sleep_time[i])
            threads_sleep_time[i] = threads_sleep_time[i] * 2
            if(threads_sleep_time[i] > 600):
                threads_sleep_time[i] = 600

        elif type(threads[i]) == threading.Thread:
            if not threads[i].is_alive():
                threads[i] = []
    time.sleep(2)
    #process = subprocess.run(['python', 'tiktok-client.py', account[0], account[1]])

