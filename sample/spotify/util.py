from spotify.models import SpotifyToken 
from django.utils import timezone
from datetime import timedelta
from .credinals import CLIENT_ID,CLIENT_SECRET
from requests import post,put,get
import spotipy
import csv
from django.conf import settings
import os
from fuzzywuzzy import process
from django.http import HttpResponse,FileResponse
from spotify.script import run
BASE_URL='https://api.spotify.com/v1/me/'
def get_user_auth(session_id):
    details=SpotifyToken.objects.filter(user=session_id)
    if details.exists():
        return details[0]
    else:
        return None

def update_or_create_users(session_id,access_token,token_type,refresh_token,expires_in):
    tokens=get_user_auth(session_id)
    if tokens!=None:
        expires_in=timezone.now()+timedelta(seconds=expires_in)
        tokens.access_token=access_token
        tokens.token_type=token_type
        tokens.refresh_token=refresh_token
        tokens.expires_in=expires_in
        tokens.save(update_fields=['access_token','token_type','refresh_token','expires_in'])
        return 
    else:
        print(expires_in)
        expires_in=timezone.now()+timedelta(seconds=expires_in)
        print(session_id)
        print(access_token)
        print(token_type)
        print(refresh_token)
        print(expires_in)
        
        newtokens=SpotifyToken(user=session_id,access_token=access_token,token_type=token_type,refresh_token=refresh_token,expires_in=expires_in)
        print("saving the data")
        print(newtokens)
        newtokens.save()

def Refresh_tokens(session_id):
    tokens=get_user_auth(session_id)
    refresh_token=tokens.refresh_token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    response = post('https://accounts.spotify.com/api/token', headers=headers, data=data, auth=auth).json()

    
    access_token=response.get('access_token')
    token_type=response.get('token_type')
    refresh_token=refresh_token
    expires_in=response.get('expires_in')
    print('updating tokeen............')
    print(response)
    
    print(access_token)
    print(token_type)
    print(refresh_token)
    print(expires_in)
    update_or_create_users(session_id,access_token,token_type,refresh_token,expires_in)
       
def isAutheticate(session_id):
    tokens=get_user_auth(session_id)
    print(tokens)
    if tokens!=None:
        expiry=tokens.expires_in
        if expiry<=timezone.now():
            Refresh_tokens(session_id)
            return True
        else:
            return True
    else:
        return False        
    

       

def spotify_get_playlist(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_auth(session_id)
    if tokens:
        access_token = tokens.access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+ access_token
        }

        if post_:
            response = post(BASE_URL + endpoint, headers=headers)
        elif put_:
            response = put(BASE_URL + endpoint, headers=headers)
        else:
            response = get(BASE_URL + endpoint,{}, headers=headers)

        try:
            return response.json()
        except ValueError:
            return {'Error': f"Request failed with status code {response.status_code}"}
    else:
        return {'Error': 'No tokens available'}
               


def pausebutton(session_id):
    data=spotify_get_playlist(session_id,"player/pause",put_=True)
    return data      

def playbutton(session_id):

    data=spotify_get_playlist(session_id,"player/play",put_=True)
    return data            

def nextbutton(session_id):
    data=spotify_get_playlist(session_id,"player/next",post_=True)
    return data

def getplaylist(session_id):
    tokens=get_user_auth(session_id)
    if tokens:
        access_token=tokens.access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+ access_token
        }
        response = get(BASE_URL + "playlists", headers=headers).json()
        playlist_id = response['items'][0]['id']
        
        
        headers1 = {
            'Authorization': f'Bearer {access_token}'
        }
        BASE_URL1 = 'https://api.spotify.com/v1/'
        endpoint = f'playlists/{playlist_id}/tracks'
        response = get(BASE_URL1 + endpoint, headers=headers1)
        if response.status_code == 200:
           playlist_data = response.json()
           tracks = []

        # Extract track names and Spotify URLs
        for item in playlist_data['items']:
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']  # Assuming only one artist for simplicity
            album_name = track['album']['name']
            playlist_name = "Car"  # Replace with actual playlist name if needed
            track_type = "Playlist"  # Replace with actual type if needed
            isrc = ""  # Replace with actual ISRC if needed
            spotify_id = track['id']

            tracks.append([track_name, artist_name, album_name, playlist_name, track_type, isrc, spotify_id])

        # Path to save the CSV file
        media_folder = settings.MEDIA_ROOT  # Ensure settings.MEDIA_ROOT is defined
        csv_file = os.path.join(media_folder, 'spotify_playlist_tracks.csv')

        # Writing CSV file
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Track name', 'Artist name', 'Album', 'Playlist name', 'Type', 'ISRC', 'Spotify - id'])  # Write header row
            
            for track in tracks:
                writer.writerow(track)

        print(f"CSV file '{csv_file}' has been created with the track details in the '{media_folder}' folder.")
        
        #run(csv_file)
        return response
    else:
        print(f"Failed to retrieve playlist tracks: {response.status_code} - {response.reason}")




def searchanddownload(song_name, threshold=50):
    matching_files = []
    filenames = os.listdir('spotify_playlist_tracks_Musics')
    folder_path = 'spotify_playlist_tracks_Musics'

    
    for filename in filenames:
      
        score = process.extractOne(song_name, [filename])[1]
        print(score)
        if score >= threshold:
            full_path = os.path.join(folder_path, filename)
            matching_files.append(full_path)

    if not matching_files:
        return HttpResponse("No matching files found.", status=404)
    
  
    file_path = matching_files[0]
    newone = os.path.basename(file_path)  
    print(newone,file_path)
    if os.path.exists(file_path):
        response = HttpResponse(open(file_path, 'rb').read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{newone}"'
        return response
    else:
        return HttpResponse("File not found.", status=404)