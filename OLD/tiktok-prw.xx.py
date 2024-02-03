# TiktokLiveClient
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent

#GTTS Speech
from gtts import gTTS
import time
#Line Notify
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'PNTRtn2tZDnz6zI3mVRC4o7xthxogTVwDmo21HI2r07'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

#Tiktok Account
unique_id = "@prw.xx"

client: TikTokLiveClient = TikTokLiveClient(unique_id)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)
    message = unique_id + ' connected'
    r = requests.post(url, headers=headers, data = {'message':message})
    tts = gTTS("สวัสดีค่า", lang='th')
    filename = str(int(time.time()))
    tts.save('comment\\'+filename+'.mp3')

# Notice no decorator?
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} : {event.comment}")
    message = event.user.nickname + ' : ' + event.comment
    r = requests.post(url, headers=headers, data = {'message':message})
    tts = gTTS(event.comment, lang='th')
    filename = str(int(time.time())) + '_' + event.comment
    #filename = ''.join(e for e in filename if e.isalnum())
    tts.save('comment\\'+filename+'.mp3')

# Define handling an event via a "callback"
client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()

