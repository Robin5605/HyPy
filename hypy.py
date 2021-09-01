from typing import List
import requests
import json
from exceptions import APIError
from datetime import date, datetime

class Endpoints:
    KEY     = 'https://api.hypixel.net/key'
    DATA    = 'https://api.hypixel.net/player'
    FRIENDS = 'https://api.hypixel.net/friends'

class FriendRequest:
    def __init__(self, **kwargs) -> None:
        self.id : str = kwargs['_id']
        self.sender : str = kwargs['uuidSender']
        self.receiver : str = kwargs['uuidReceiver']
        self.started : datetime = datetime.fromtimestamp(kwargs['started'] / 1000)

class Hypixel8:
    def __init__(self, *, api_key : str):
        self.api_key= api_key
        self.owner = self.get_owner()

    def _request(self, url : str, **kwargs):
        """Custom request handler to make requests and raise errors"""
        with requests.get(url, **kwargs) as r:
            json = r.json()
            if not r.ok:
                raise APIError(json['cause'])
            return json

    def get_data(self, uuid : str = None) -> dict:
        uuid = uuid or self.owner
        r = self._request(Endpoints.DATA, headers={'API-Key': self.api_key}, params = {'uuid': uuid})
        return r

    def get_friends(self, uuid : str = None) -> List[FriendRequest]:
        uuid = uuid or self.owner
        friends = []
        r = self._request(Endpoints.FRIENDS, headers={'API-Key': self.api_key}, params = {'uuid': uuid})
        for friend_data in r['records']:
            friend = FriendRequest(**friend_data)
            friends.append(friend)
        return friends

    def get_owner(self) -> str:
        r = self._request(Endpoints.KEY, headers={'API-Key': self.api_key})
        owner_uuid = r['record']['owner']
            
        return owner_uuid