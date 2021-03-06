import os
import threading
import time
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from tkinter import ttk  # themed tkinter used for styling button
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("radiance")  # Sets an available theme

# Fonts: Arial, Courier New (courier), Comic Sans MS, Fixedsys, MS Sans Serif, MS Serif, Symbol, System,
# Times New Roman(Times), and Verdana
#
# Styles: normal, bold, italic, roman, underline, and overstrike

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN)
statusbar.pack(side=BOTTOM, fill=X)

mixer.init()  # initializing the mixer
menubar = Menu(root)  # create the menubar
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)  # create the submenu & tearoff: Width of the trashed line

playlist = []


# playlist: It contains the full path + filename
# playlistbox: Contain just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)  # add file option in menu
subMenu.add_command(label='Open', command=browse_file)  # add open option in submenu
subMenu.add_command(label='Exit', command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build in Python Language using tkinter by Ankush Agarwal')


def contact_no():
    tkinter.messagebox.showinfo('Contact No',
                                'If you have any issue related to this music player you can freely call this number: +91 7248030408')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label='Contact No', command=contact_no)
subMenu.add_command(label='About Us', command=about_us)

root.title('Melody')
root.iconbitmap(r'hnet.com-image.ico')

# Root window - StatusBar, LeftFrame, RightFrame
# Left Frame -  List Box
# Right Frame - TopFrame, MiddleFrame, BottomFrame


leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="-Del", command=del_song)
delBtn.pack(side=RIGHT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text="Total Lenght: --:--")
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text="Current Time: --:--", relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == ".mp3":
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)  # div: total_length/60, mod: total_length % 60
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy():- Return FALSE when we pressed the stop button (music stop playing)
    # continue: Ignores all the statements below it. We check if music is paused or not
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("File not found", "Melody could not found the file. Please check again")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewind"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer take value from 0 t0 1  [i.e volume is divided by 100]


muted = FALSE


def mute_music():
    global muted
    if muted:  # unmuted the music
        mixer.music.set_volume(0.35)
        volumeBtn.configure(image=volumePhoto)
        scale.set(35)
        muted = FALSE

    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(padx=30, pady=30)

playPhoto = PhotoImage(file='play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# bottom frame for speaker, rewind, mute etc

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file='rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='speaker.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(35)
mixer.music.set_volume(0.35)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    tkinter.messagebox.showinfo("EXIT",'Are you sure?')
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



# Code by Ankush Agarwal