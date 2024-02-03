from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent

from threading import Thread
import time

import requests
url = 'https://notify-api.line.me/api/notify'
token = 'CPF3M1CLAuEGUxHP2S5WnmjdeeDiZtcwyLxhb5stCsW'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def thread_callback(unique_id):
    print("Start Thread : ", unique_id)
    client: TikTokLiveClient = TikTokLiveClient(unique_id)
    @client.on("connect")
    
    async def on_connect(_: ConnectEvent):
        print("Connected to Room ID:", client.room_id)

    # Notice no decorator?
    async def on_comment(event: CommentEvent):
        print(f"{event.user.nickname} -> {event.comment}")
        r = requests.post(url, headers=headers, data = {'message':msg})



    # Define handling an event via a "callback"
    client.add_listener("comment", on_comment)

    print("Thread done setup : ", unique_id)

    print("Run TiktokLiveClient : ", unique_id)

    client.run()

ids = [
    ["@janua_official", ""],
    ["@prw.xx", ""]
]


client1 = Thread(target=thread_callback, args=[ids[0][0]])
#client1.daemon = True
client1.start()
#client2 = Thread(target=thread_callback, args=[ids[1][0]])
#client2.daemon = True
#client2.start()
#clients = []
#if __name__ == '__main__':
#    client = Thread(target=thread_callback, args=[ids[0][0]])

    # Run the client and block the main thread
    # await client.start() to run non-blocking
    #for id in ids:
