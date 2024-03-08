# TiktokLiveClient
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent

from io import BytesIO
from pygame import mixer

#GTTS Speech
from gtts import gTTS
import time
#Line Notify
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'PNTRtn2tZDnz6zI3mVRC4o7xthxogTVwDmo21HI2r07'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

#Tiktok Account
unique_id = "@janua_official"

client: TikTokLiveClient = TikTokLiveClient(unique_id)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)
    

# Notice no decorator?
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} : {event.comment}")
    #filename = ''.join(e for e in filename if e.isalnum())
    mp3_fp = BytesIO()
    tts = gTTS(event.comment, lang='th')
    tts.write_to_fp(mp3_fp)
    
    mp3_fp.seek(0)
    mixer.music.load(mp3_fp, "mp3")
    mixer.music.play()
    while True:
        if mixer.get_busy():
            time.sleep(1)
        else:
            break
    
# Define handling an event via a "callback"
client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    mixer.init()
    client.run()

