import csv
import os
import re
from googleapiclient.discovery import build
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from win10toast import ToastNotifier

# Function to retrieve data from CSV
def getCSV(file:str) -> list:
    tracks = []
    try:
        with open(file, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                tracks.append({
                    'track_name': row['Track name'],
                    'artist_name': row['Artist name'],
                })

        print(f"{len(tracks)} Tracks Detected in the File.\n")
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"Error opening '{file}': {e}")

    return tracks if tracks else None

# Function to clean track and artist names for YouTube search
def clean_name(name):
    # Remove special characters and excess whitespace
    cleaned_name = re.sub(r'[^\w\s]', '', name.strip())
    return cleaned_name

# Function to search YouTube for the video
def search_youtube(query):
    api_key = 'AIzaSyCJkix_wJWwAFjMQBgMAPGZqmbYj-x7V08'  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    return response['items'][0]['id']['videoId'] if response['items'] else None

# Function to download songs
def download(tracks, path):
    if not os.path.exists(path):
        os.makedirs(path)

    count = 0
    for track in tracks:
        try:
            clean_track_name = clean_name(track['track_name'])
            clean_artist_name = clean_name(track['artist_name'])
            query = f"{clean_track_name} {clean_artist_name} official audio"
            video_id = search_youtube(query)
            if video_id:
                youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                yt = YouTube(youtube_url)
                stream = yt.streams.filter(only_audio=True).first()
                if stream:
                    filename = f"{clean_artist_name} - {clean_track_name}.mp3"
                    filepath = os.path.join(path, filename)
                    stream.download(output_path=path, filename='temp_audio')
                    os.rename(os.path.join(path, 'temp_audio'), filepath)
                    count += 1
                    print(f"{count}/{len(tracks)} - Downloaded: {filename}")
                else:
                    print(f"No audio stream available for {track['track_name']} by {track['artist_name']}")
            else:
                print(f"Video not found for {track['track_name']} by {track['artist_name']}")
        except RegexMatchError:
            print(f"Invalid YouTube URL format for {track['track_name']} by {track['artist_name']}")
        except Exception as e:
            print(f"Error downloading {track['track_name']} by {track['artist_name']}: {e}")

    if count > 0:
        print("\nSongs Downloaded.")
        ToastNotifier().show_toast("CSV Playlist Download", "Songs Downloaded.", "icon.ico", 5)
        os.startfile(path)
    else:
        print("\nNo songs downloaded.")

# Main function to run the script
def run(file):
    tracks = getCSV(file)
    if tracks:
        download(tracks, os.path.dirname(os.path.abspath(file)))

if __name__ == "__main__":
    file = input("File Path (.csv):").replace('"', '').replace("'", "")
    run(file)

