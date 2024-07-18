# __author__ = "Enes Uğur"


import csv
from ytubemp3downloader import YouTubeMp3
from win10toast import ToastNotifier
from os import startfile


def getCSV(file:str) -> list:
	songs = []
	with open(file,"r",encoding="utf-8") as csv_file:
		csv_reader = csv.reader(csv_file)

		next(csv_reader)

		for x in csv_reader:
			songs.append(x[0] + " " + x[1] + " " + x[2])

	print(f"{len(songs)} Songs Detected in the File.\n")
	return songs


def getLinks(file:str,songs:list) -> list:
	global youtube
	global path

	file = file.replace("\\","/")
	path = f"./{file.split('.')[0].split('/')[-1]}_Musics"

	youtube = YouTubeMp3(path=path)

	links = []
	
	for song in songs:
		try:
			result = youtube.find_video_link_by_name(song)
			link = result[1]
			title = result[0]['title']
			links.append(link)
		except:
			pass
		else:
			print(f"Song Found: '{title}'")

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
			print(count + "/" + len(links))

	print("\nSongs Downloaded.")
	ToastNotifier().show_toast("CSV Playlist Download","Songs Downloaded.","icon.ico",5)
	startfile(path)
	quit()

def run(file):
	songs = getCSV(file)
	links = getLinks(file,songs)
	download(links)



file = input("File Path (.csv):").replace('"','').replace("'","")

run(file)