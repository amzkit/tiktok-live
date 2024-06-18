import sys
try:
    uid = sys.argv[1]
    token = sys.argv[2]
except:
    uid = "@byprw_official"
    token = 'CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW'

# TiktokLiveClient
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent

#GTTS Speech
from gtts import gTTS
import time
#Line Notify
import requests

url = 'https://notify-api.line.me/api/notify'
#token = 'CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW'
#token = 'NIcr2QFJ1eJCfuELDLZQzJpYF5E3mdt8x3Baho2qRGu' Test
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

#Tiktok Account

# Create the client
print('['+time.strftime('%H:%M')+']['+uid+'] Connecting')
client: TikTokLiveClient = TikTokLiveClient(unique_id=uid)


# Listen to an event with a decorator!
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print('['+time.strftime('%H:%M')+']['+event.unique_id+'] Connected')
    #print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")

# Or, add it manually via "client.add_listener()"
async def on_comment(event: CommentEvent) -> None:
    print('['+time.strftime('%H:%M')+']['+uid+'] '+event.user.nickname+' : '+event.comment)
    try:
        response = requests.post(url, headers=headers, data = {'message': event.user.nickname + ':' + event.comment})
    except:
        print('['+time.strftime('%H:%M')+']['+uid+'] Line Notify Error')
    
    try:
        response = requests.post("https://line.ininit.com/chat/store", params={'comment': event.comment})
    except:
        print('['+time.strftime('%H:%M')+']['+uid+'] Chat DB Store Error')

    try:
        tts = gTTS(event.comment, lang='th')
    except:
        print('['+time.strftime('%H:%M')+']['+uid+'] siri (gTTS) Error', tts)

    try:
        filename = str(int(time.time())) + '_' + event.comment
        tts.save('comment\\'+filename+'.mp3')
    except:
        print('['+time.strftime('%H:%M')+']['+uid+'] Save File Error')
    #print(response)

client.add_listener(CommentEvent, on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()


