# Note to self : .\env\Script\activate to enable the virtual environment

import os 
import re 

import sys 
print(sys.executable)

import json as simplejson
from pytubefix import YouTube 
from pytubefix.cli import on_progress

from tkinter import *
import tkinter as tk 
from tkinter import messagebox

"""
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
#Link = None
#Download(Link)
#print(config["Link"])
"""

##  DOWNLOADING LOGIC  ##

def extract_video_id(link):
    # URL
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", link)
    if match:
        return match.group(1)
    # ID ONLY
    if len(link) == 11:
        return link
    raise ValueError("Invalid YouTube link or video ID")

def Download(video_link):
    video_id = extract_video_id(video_link)
    url = f"https://www.youtube.com/watch?v={video_id}"

    yt = YouTube(url, on_progress_callback=on_progress)

    print(yt.title)
    ys = yt.streams.filter(only_audio=True).first()

    out_file = os.path.join(os.getcwd(), f"{yt.title}.mp3")
    ys.download(output_path=os.getcwd(), filename=f"{yt.title}.mp3")

    messagebox.showinfo("Success", f"Video downloaded in directory {out_file}")



## GUI  SECTION   ##

root = tk.Tk()
root.title("Youtube Video Downloader V0.1")
root.geometry("400x331")

#frame = ttk.Frame(root, padding=10)
#frame.grid()


#label = Label(frame, text="Link Download").grid(column=0, row=0)
#button = Button(root, text="Close", command=root.destroy).grid(column=2, row=0)

label1 = tk.Label(root, text="Enter Section after Link", bg="lightblue")
#label1.place(x=10, y=20)
label1.pack(padx=10, pady=40)


text = tk.StringVar()
text.set("")
textBox = tk.Entry(root, textvariable=text)
textBox.pack(padx=15,pady=40)

def on_button_click():
    #messagebox.showinfo("Downloading", "Please wait for a download to occur")
    print(textBox.get()) # Gets the code entered 
    Download(textBox.get())

button = tk.Button(
    root, text="Download", command=on_button_click, bg="lightblue", fg="black"
)
button.pack(pady=50)

root.mainloop()
