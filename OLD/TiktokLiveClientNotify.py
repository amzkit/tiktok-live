from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent


class TiktokLiveClientNotify(object):
    def __init__(self,unique_id,token):
        self.unique_id = unique_id
        self.token = token
        
        # Instantiate the client with the user's username
        client: TikTokLiveClient = TikTokLiveClient(unique_id, token)


        # Define how you want to handle specific events via decorator