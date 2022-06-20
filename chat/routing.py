# from core import consumers
from chat.consumers import ChatConsumer
from django.urls import re_path, include
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws$', ChatConsumer.as_asgi()),
    # url(r'^ws$', consumers.IndexConsumer),

]
