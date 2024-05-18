import sys
#id = sys.argv[1]


# TiktokLiveClient
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent

#GTTS Speech
from gtts import gTTS
import time
#Line Notify
import requests

url = 'https://notify-api.line.me/api/notify'
token = 'CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW'
#token = 'NIcr2QFJ1eJCfuELDLZQzJpYF5E3mdt8x3Baho2qRGu' Test
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

#Tiktok Account

# Create the client
client: TikTokLiveClient = TikTokLiveClient(unique_id="@byprw_official")


# Listen to an event with a decorator!
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id}")


# Or, add it manually via "client.add_listener()"
async def on_comment(event: CommentEvent) -> None:
    print(f"{event.user.nickname} -> {event.comment}")
    response = requests.post("https://line.ininit.com/chat/store", params={'comment': event.comment})
    tts = gTTS(event.comment, lang='th')

    filename = str(int(time.time())) + '_' + event.comment
    tts.save('comment\\'+filename+'.mp3')
    #print(response)

client.add_listener(CommentEvent, on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()


