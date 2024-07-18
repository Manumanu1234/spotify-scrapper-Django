from django.contrib import admin
from django.urls import path
from projectApp.views import RoomView,createRoomByUser,GetRoom,JoinRoom,Roomexist,Leaving,UpdateRoom
app_name='projectApp'
urlpatterns = [
  path('home/',RoomView.as_view(),name=''),
  path('createroom/',createRoomByUser.as_view()),
  path('getroom/',GetRoom.as_view()),
  path('joinroom/',JoinRoom.as_view()),
  path('roomexist/',Roomexist.as_view()),
  path('leavingroom/',Leaving.as_view()),
  path('updateroom/',UpdateRoom.as_view())
  
]
