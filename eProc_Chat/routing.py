# chat/routing.py
from django.urls import path

from eProc_Chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer),
]

# websocket_urlpatterns = [
#     url(r'^ws/chat/(?P<str:room_name>[^/]+)/$', ChatConsumer),
# ]