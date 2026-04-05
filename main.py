# Note to self : .\env\Script\activate to enable the virtual environment
import os 

import sys 
print(sys.executable)

import json as simplejson
from pytubefix import YouTube 

from tkinter import *


try:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    json_file = os.path.join(parent_directory, "videoLink.json")

    with open(json_file, "r") as f:
        config = simplejson.load(json_file)

except:
    print(f"Video Config loading error")

def Download(link):
    #youtubeObject = YouTube(link)
    #youtubeObject = youtubeObject.streams

    try:
        youtubeObject = YouTube(link).streams.get_highest_resolution()
        youtubeObject.download()
    except Exception as e:
        print(f"An error occured : {e}")
    print(f"Download completed")


# Inputting of Link
Link = None

#Download(Link)

print(config["Link"])
