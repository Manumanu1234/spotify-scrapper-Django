#!/usr/bin/env python
# Requires: youtube_dl module
# Requires: ffmpeg

# pip install youtube-search
# pip install xlrd
# pip install yt-dlp

import csv
import yt_dlp as youtube_dl
from youtube_search import YoutubeSearch
from win10toast import ToastNotifier
from os import startfile, getcwd, path as os_path

class YouTubeMp3:
    def __init__(self, path=os_path.join(getcwd(), 'Downloads')):
        self.path = path
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os_path.join(self.path, '%(title)s.%(ext)s'),
        }

    def find_video_link_by_name(self, name):
        video = YoutubeSearch(name, max_results=1).to_dict()[0]
        video_id = video["id"]
        ylink = f"https://www.youtube.com/watch?v={video_id}"
        return [video, ylink]

    def downloadmp3_by_name(self, name):
        ylink = self.find_video_link_by_name(name)[1]
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([ylink])

    def downloadmp3_by_ytlink(self, link):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([link])

    def changePath(self, newpath):
        self.path = newpath

def getCSV(file: str) -> list:
    songs = []
    with open(file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for x in csv_reader:
            songs.append(x[0] + " " + x[1] + " " + x[2])
    print(f"{len(songs)} Songs Detected in the File.\n")
    return songs

def getLinks(file: str, songs: list) -> list:
    global youtube
    global path

    file = file.replace("\\", "/")
    path = f"./{file.split('.')[0].split('/')[-1]}_Musics"
    youtube = YouTubeMp3(path=path)
    links = []

    for song in songs:
        try:
            result = youtube.find_video_link_by_name(song)
            link = result[1]
            title = result[0]['title']
            links.append(link)
            print(f"Song Found: '{title}'")
        except:
            pass

    print(f"\n{len(links)} Songs Found.\n")
    return links

def download(links):
    count = 0
    for link in links:
        try:
            youtube.downloadmp3_by_ytlink(link)
        except:
            pass
        else:
            count += 1
            print(f"{count}/{len(links)}")
    
    print("\nSongs Downloaded.")
    ToastNotifier().show_toast("CSV Playlist Download", "Songs Downloaded.", "icon.ico", 5)
    startfile(path)
    quit()

def run(file):
    songs = getCSV(file)
    links = getLinks(file, songs)
    download(links)

if __name__ == "__main__":
    file = input("File Path (.csv):").replace('"', '').replace("'", "")
    run(file)
