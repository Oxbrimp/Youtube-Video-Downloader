# Note to self : .\env\Script\activate to enable the virtual environment

# Note to Self : creating executable - ( install pyinstaller ) &  pyinstaller --onefile main.py

import os 
import re 

import sys 
print(sys.executable)

from pytubefix import YouTube 
from pytubefix.cli import on_progress
import subprocess

from tkinter import *
import tkinter as tk 
from tkinter import messagebox

import threading 


##  DOWNLOADING LOGIC  ##

download_video = True # Default is MP4

def extract_video_id(link):
    # URL
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", link)
    if match:
        return match.group(1)
    # ID ONLY
    if len(link) == 11:
        return link
    raise ValueError("Invalid YouTube link or video ID")

def Download(video_link, video_bool):

    try:
        video_id = extract_video_id(video_link)
        url = f"https://www.youtube.com/watch?v={video_id}"

        yt = YouTube(url, on_progress_callback=on_progress)

        print(yt.title)

        if video_bool == "mp4":
            ys = yt.streams.get_highest_resolution()
        else:
            ys = yt.streams.filter(only_audio=True).first()
        

        temp_file = ys.download(output_path=os.getcwd())

        # MP3 - MP4 conv.
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", yt.title)

        # Output 
        if video_bool =="mp3":
            output_file = os.path.join(os.getcwd(), f"{safe_title}.mp3")
        else:
            output_file = os.path.join(os.getcwd(), f"{safe_title}.mp4")


        # ffmpeg valid extension.
        fixed_input = temp_file
        if not fixed_input.lower().endswith(".mp4"):
            fixed_input = temp_file + ".mp4"
            if not os.path.exists(fixed_input):
                os.rename(temp_file, fixed_input)

        

        cmd = [
            "ffmpeg",
            "-i", fixed_input,
        ]

        if video_bool == "mp3":
            cmd += [
                "-vn",
                "-c:a", "libmp3lame",
                "-ar", "44100",
                "-ab", "192k",
                "-ac", "2"
            ]
        elif video_bool == "mp4":
            cmd += [
                "-c:v", 
                "copy", 
                "-c:a", 
                "copy",
                "-map_metadata", "1"
            ]


        cmd += [
            "-metadata", f"title={yt.title}",
            "-metadata", f"artist={yt.author}",
            output_file
        ]

        # ffmpeg execution
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("FFmpeg Error, please quote this error to the GitHub Repository" , result.stderr)
            return 

        #subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Removing of original file - replace with new (metadata filled) variant 
        if os.path.exists(fixed_input):
            os.remove(fixed_input)

        messagebox.showinfo("Success", f"Video downloaded in directory {output_file}")

    except Exception as e:
        messagebox.showerror("Error, please quote this to the GitHub Repository", str(e))

## GUI  SECTION   ##

root = tk.Tk()
root.title("Youtube Video Downloader V0.2")
root.geometry("400x331")
root.resizable(False, False)

#frame = ttk.Frame(root, padding=10)
#frame.grid()


#label = Label(frame, text="Link Download").grid(column=0, row=0)
#button = Button(root, text="Close", command=root.destroy).grid(column=2, row=0)

label1 = tk.Label(root, text="Enter Section after Link", bg="lightblue")

#label1.place(x=10, y=20)
label1.place(x=200, y=85, anchor = CENTER)

agreement = tk.StringVar()  # For MP3/MP4 settings

def agreement_val():
    global download_video
    download_video = agreement.get()
    print(download_video)

checkbox = tk.Checkbutton(root, 
                          text="VIDEO", 
                          command=agreement_val, 
                          variable=agreement, 
                          onvalue="mp4", 
                          offvalue="mp3")
checkbox.place(x=270,y=165.5,anchor=CENTER)
checkbox.select()


text = tk.StringVar()
text.set("")
textBox = tk.Entry(root, textvariable=text)
textBox.place(x=200,y=110,anchor=CENTER)



def on_button_click():
    #messagebox.showinfo("Downloading", "Please wait for a download to occur")
    print(f"{textBox.get()} Selected") # Gets the code entered 
    #Download(textBox.get(), agreement.get())
    link = textBox.get()
    fmt = agreement.get()
    threading.Thread(target=Download, args=(link, fmt), daemon=True).start() 

button = tk.Button(
    root, text="Download", command=on_button_click, bg="lightblue", fg="black"
)
button.place(x=200,y=165.5,anchor=CENTER)

root.mainloop()
