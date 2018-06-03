from tkinter import *

root = Tk()

def new_winF(): # new window definition
    newwin = Toplevel(root)
    display = Label(newwin, text="Humm, see a new window !")
    display.pack()

button1 =Button(root, text ="open new window", command =new_winF) #command linked
button1.pack()

root.mainloop()