from tkinter import *

root = Tk()

playPhoto = PhotoImage(file='play.png')
playBtn = ttk.Button(root, image=playPhoto)
playBtn.grid(row=0,column=1)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = ttk.Button(root, image=stopPhoto)
stopBtn.grid(row=0,column=2)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = ttk.Button(root, image=pausePhoto)
pauseBtn.grid(row=0,column=3)

root.mainloop()
