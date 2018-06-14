from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

def gg(self):
    self.delete(0, 100)

MailWin = Tk()
MailWin.geometry("250x200")
MailWin.resizable(False, False)
MailWin.title("메일 보내기")


text1 = Label(MailWin, text="아아아아아아", font=12)
text1.pack(anchor="center")

text2 = Label(MailWin, text="기기기기기기", font=12)
text2.pack(anchor="center")


MailInput = Entry(MailWin, width=30)
MailInput.bind("<FocusIn>", gg)
MailInput.insert(0, "보낼 메일의 주소를 입력하세요.")
MailInput.pack(anchor="center")


button = Button(MailWin, text="메일 보내기")
button.pack(anchor="center")


MailWin.mainloop()
