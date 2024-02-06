from django.urls import path
from eProc_Chat import views

app_name = 'eProc_Chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:action>/<str:chat_type>/<str:room_name>/<str:client>', views.room, name='room'),
    # re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
