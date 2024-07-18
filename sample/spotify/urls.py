from django.urls import path
from spotify.views import AuthSpotify,callback,isAuthanticated,spotify_get_details,PauseCall,PlayCall,PlayCNext,PlayList,DownloadReq
urlpatterns=[
    path('get-url-auth/',AuthSpotify.as_view()),
    path('redirect/',callback),
    path('isAuth/',isAuthanticated.as_view()),
    path('current-song/',spotify_get_details.as_view()),
    path('pause-song/',PauseCall.as_view()),
    path('play-song/',PlayCall.as_view()),
    path('play-next/',PlayCNext.as_view()),
    path('play-list',PlayList.as_view()),
    path('download',DownloadReq.as_view())
]