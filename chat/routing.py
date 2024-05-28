# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat_interfon4/(?P<room_name>\w+)/(?P<user_name>\w+)/$", consumers.ChatInterfonConsumer_async4.as_asgi()),
    
    #re_path(r"ws/chat_interfon3/", consumers.ChatInterfonConsumer_async3.as_asgi()),
    #re_path(r"ws/chat_interfon3/", consumers.ChatConsumer001.as_asgi()),
    #re_path(r"ws/chat_interfon2/", consumers.ChatConsumer000.as_asgi()),
    
    re_path(r"ws/chat_interfon/(?P<room_name>\w+)/(?P<name>\w+)/$", consumers.ChatInterfonConsumer_async.as_asgi()),
    
    re_path(r"ws/chat/testws/$", consumers.TestWsConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]