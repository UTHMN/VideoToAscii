import os
import time
import climage
import shutil
import cv2
import pytube
import re
import subprocess

global vidurl
vidurl = ""

def getyt(link):
    youtubeObject = pytube.YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    video = pytube.YouTube(f"{link}")
    vtitle = re.sub(r'[^\w]', ' ', video.title) # Removes symbols

    stream = video.streams.filter(only_video=True).first()
    stream.download(filename=f"getyt_export.mp4")
    stream = video.streams.filter(only_audio=True).first()
    stream.download(filename=f"audio.mp3")

def split(pathtovid):
    capture = cv2.VideoCapture(f"{pathtovid}")
    frameNr = 0
    os.makedirs(f"./export")

    while True:
        success, frame = capture.read()
        if success:
            cv2.imwrite(f'./export/{frameNr}.jpg', frame)
        else:
            break
        frameNr = frameNr+1
 
    capture.release()

if os.path.exists("./export"):
    if str(input("we detected a export, play it? [y/n]: ")).lower() == "y":
        vidurl = input("path to original video (ignore to manually input): ")
    else:
        shutil.rmtree("./export")
        if os.path.exists("./audio.mp3"):
            os.remove("./audio.mp3")
        vidurl = input("link to video or path to video: ")
        if not os.path.exists(vidurl):
            getyt(str(vidurl))
            vidurl = "./getyt_export.mp4"
            split("./getyt_export.mp4")
        else:
            split(vidurl)
else:
    if os.path.exists("./getyt_export.mp4"):
        os.remove("./getyt_export.mp4")
    if os.path.exists("./audio.mp3"):
        os.remove("./audio.mp3")
    vidurl = input("link to video or path to video: ")
    if not os.path.exists(vidurl):
        getyt(str(vidurl))
        vidurl = "./getyt_export.mp4"
        split("./getyt_export.mp4")
    else:
        split(vidurl)

files = os.listdir("./export")

cam = cv2.VideoCapture(str(vidurl))
fps = round(cam.get(cv2.CAP_PROP_FPS))

if fps == 0:
    fps = input("fps: ")

subprocess.call(['gnome-terminal', '-x', 'python3', '/home/kingvcheese/code/VideoToAscii/soundplayer.py'])
time.sleep(1)

for i in range(len(files)):
    output = climage.convert(f'./export/{i}.jpg', is_256color=True)
    os.system("clear")
    print(output)
    time.sleep(1 / int(fps))