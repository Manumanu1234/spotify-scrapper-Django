from django.shortcuts import render,redirect
from .credinals import CLIENT_SECRET,CLIENT_ID,REDIRECT_URI
from rest_framework.views import APIView
from rest_framework.response import Response
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from requests import post,Request
from django.http import HttpResponse
from projectApp.models import Room
from .util import update_or_create_users,isAutheticate,spotify_get_playlist,pausebutton,playbutton,nextbutton,getplaylist,searchanddownload
# Create your views here.

class AuthSpotify(APIView):
    def get(self,request):
        scope='user-read-playback-state user-modify-playback-state user-read-currently-playing'
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,scope=scope)
        print("\n\nSP_OAuth Object:" ,sp_oauth, "\n\n")
        url = sp_oauth.get_authorize_url()
        print(url)
        return Response({"url":url})
    
def callback(request):
    code=request.GET.get('code')
    error=request.GET.get('error')
    response=post('https://accounts.spotify.com/api/token',data={
        "grant_type":"authorization_code",
        "code": code,
        "redirect_uri":REDIRECT_URI,
        "client_secret":CLIENT_SECRET,
        "client_id":CLIENT_ID,
    }).json()
    print(response)
    access_token=response.get('access_token')
    token_type=response.get('token_type')
    refresh_token=response.get('refresh_token')
    expires_in=response.get('expires_in')
    if not request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_users(request.session.session_key,access_token,token_type,refresh_token,expires_in)
    return redirect('http://localhost:3000')

class isAuthanticated(APIView):
    def get(self,request):
        print('manu')
        print(self.request.session.session_key)
        is_auth=isAutheticate(self.request.session.session_key)
        return Response({'isauth':is_auth})

class spotify_get_details(APIView):
    def get(self,request):
        room_code=self.request.session.get('room-code')
       
        if room_code!=None:
            room=Room.objects.filter(code=room_code)
            if room.exists():
                room=room[0]
                host=room
                endpoint="player/currently-playing"
                response=spotify_get_playlist(host,endpoint)
                
                if 'error' in response or 'item' not in response:
                    return Response({'somthing error occured'})
                item=response.get('item')
                duration=item.get('duration_ms')
                progress=response.get('progress_ms')
                album_cover=item.get('album').get('images')[0].get('url')
                is_playing=response.get('is_playing')
                song_id=item.get('id')
                preview_url=item.get('preview_url')
                artist_string=" "
                for i,artist in enumerate(item.get('artists')):
                    if i > 0: 
                        artist_string+=","
                    name = artist.get('name', 'Unknown Artist')
                    artist_string =artist_string+name
                  
                    
                    
                song={
                    'title':item.get('name'),
                    'artist':artist_string,
                    'duration':duration,
                    'time':progress,
                    'image_url':album_cover,
                    'is_playing':is_playing,
                    'song_id':song_id,
                    'preview_url':preview_url,
                    'votes':0                        
                    }
                    
                return Response({'data':song})
            else:
                return Response('not room find')
        else:
            return Response('not room find')


class PauseCall(APIView):
    def get(self,request):
        room_code=self.request.session.get('room-code')
        room=Room.objects.filter(code=room_code)
        room=room[0]
        host=room.host
        if self.request.session.session_key==host or room.gust_can_pause:
            data=pausebutton(self.request.session.session_key)
            print(data)
            return Response({'sucess':data})
        return Response({'not':'not ok'})
        

class PlayCall(APIView):
    def get(self,request):
        room_code=self.request.session.get('room-code')
        room=Room.objects.filter(code=room_code)
        room=room[0]
        host=room.host
        if self.request.session.session_key==host or room.gust_can_pause:
            data=playbutton(self.request.session.session_key)
            return Response({'sucess':data})
        return Response({'not':'not ok'})


class PlayCNext(APIView):
    def get(self,request):
        room_code=self.request.session.get('room-code')
        room=Room.objects.filter(code=room_code)
        room=room[0]
        host=room.host
        if self.request.session.session_key==host:
            data=nextbutton(self.request.session.session_key)
            print(data)
            return Response({'sucess':data})
        return Response({'not':'not ok'})
    

class PlayList(APIView):
    def get(self, request):
        room_code = self.request.session.get('room-code')
        room = Room.objects.filter(code=room_code).first()  
        if not room:
            return Response({'error': 'Room not found'}, status=404)
        
        host = room.host
        if self.request.session.session_key == host or room:
            
            data = getplaylist(host)
            if data.status_code != 200:
                return Response({'error': 'Failed to fetch playlist data'}, status=500)

            data = data.json()
            tracks_list = []

            for item in data['items']:
                track = item['track']
                images = track['album']['images']
                if images:
                    largest_image = max(images, key=lambda img: img['width'])  
                    album_image_url = largest_image['url']
                else:
                    album_image_url = None
                album_url = track['album']['external_urls']['spotify']
                album_id = album_url.split('/')[-1]    
                track_info = {
                    'track_name': track['name'],
                    'track_url': track['external_urls']['spotify'],
                    'track_duration_seconds': track['duration_ms'] / 1000, 
                    'album_name': track['album']['name'],
                    'album_url': track['album']['external_urls']['spotify'],
                    'album_release_date': track['album']['release_date'],
                    'album_image_url': album_image_url,
                    'album_id': album_id,
                }
                

                tracks_list.append(track_info)
                print(tracks_list)
                
            return Response({'success': tracks_list})
        return Response({'error': 'Unauthorized access'})
    
    
class DownloadReq(APIView):
    def post(self,request):
        room_code=self.request.session
        room_code = self.request.session.get('room-code')
        room = Room.objects.filter(code=room_code)
        if room!=None:
            name=request.data.get('name')
            print(name)
            return searchanddownload(name)
 