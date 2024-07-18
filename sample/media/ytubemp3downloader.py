#!/bin/env python
# Requires: youtube_dl module
# Requires: ffmpeg

# pip install youtube-search
# pip install xlrd
# pip install youtube-dl

import yt_dlp as youtube_dl
import xlrd
from youtube_search import YoutubeSearch

import sys,os

class YouTubeMp3:
    def __init__(self,path = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'):
        self.path = path

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': self.path + '/%(title)s.%(ext)s',
    
        }




    def find_video_link_by_name(self,name):
        video = YoutubeSearch(name, max_results=1).to_dict()[0]
        id = video["id"]
        ylink = "https://www.youtube.com/watch?v={}".format(id)

        return [video,ylink]


    def downloadmp3_by_name(self,name):
        "name : Ex: Modern Talking - Cheri Cheri Lady"
        ylink = self.find_video_link_by_name(name)[1]


        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            filenames = [ylink]
            ydl.download(filenames)

    def downloadmp3_by_ytlink(self,link):
        ylink = link

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            filenames = [ylink]
            ydl.download(filenames)


    def changePath(self,newpath):
        self.path = newpath


