from tkinter import *
from PIL import Image, ImageTk

window=Tk()
window.geometry("700x700")

# 이미지 크기
image_w = 2408
image_h = 1958

# 이미지 축소 시 간격
image_w_s = image_w // 10
image_h_s = image_h // 10

# 현재 이미지 크기
w = []
h = []

Subway_Image = []
tk_image = []

def SetPhotoSizeList():
    global Subway_Image

    for i in range(0, 8):
        Subway_Image.append( Image.open('F:\스크립트 언어\Script Language\SubwayInfoApp\Image\대구 지하철 노선도.jpg').resize( (image_w - (i*image_w_s), image_h - (i*image_h_s)),
                                                                                                      Image.ANTIALIAS) )
        tk_image.append(ImageTk.PhotoImage(Subway_Image[i]))

        w.append(image_w - (i*image_w_s))
        h.append(image_h - (i*image_h_s))

def SetPosition():
    value= scale.get()

    # 이미지 크기와 윈도우 창 크기로 이미지 위치 계산
    IPx = (w[value] // 2) - (500 // 2)
    IPy = (h[value] // 2) - (300 // 2)

    # 이미지 크기와 스크롤바 중간 값으로 스크롤바를 움직일 때 얼만큼 이동할지 계산
    sx = IPx // 5
    sy = IPy // 5

    # 이미지 위치를 스크롤바 값으로 계산 ~~~
    IPx -= ( ( 5 - Scrollx.get() ) * sx)
    IPy -= ( ( 5 - Scrolly.get() ) * sy)

    canvas.place(x=  -IPx , y= -IPy)

def PhotoResize(self):
    global Subway_Image, tk_image, canvas

    value= scale.get()

    SetPosition()

    canvas.config(image = tk_image[value])


def PhotoScroll(self):
    SetPosition()

LineWindow = Frame(window, width = 500, height = 400)
LineWindow.pack()

ScaleVar=IntVar()

scale=Scale(LineWindow, variable=ScaleVar, command=PhotoResize, orient="horizontal", showvalue=False, from_=0, to=7, length=500)
scale.pack(side="bottom")

SetPhotoSizeList()

# # # # 가로 스크롤 # # # #

ScrollxVar = IntVar()

Scrollx=Scale(LineWindow, variable=ScrollxVar, command=PhotoScroll, orient="horizontal", showvalue=False, from_=0, to=10, length=500)
Scrollx.pack(side="bottom")

Scrollx.set(5)
# # # # # # # # # # # # # #


# # # # 세로 스크롤 # # # #
ScrollyVar = IntVar()

Scrolly=Scale(LineWindow, variable=ScrollyVar, command=PhotoScroll, orient="vertical", showvalue=False, from_=0, to=10, length=300)
Scrolly.pack(side="right")
# # # # # # # # # # # # # #

ImageFrame = Frame(LineWindow, width = 500, height = 300)
ImageFrame.pack()

Scrolly.set(5)

canvas = Canvas(ImageFrame, image=tk_image[0])
SetPosition()

window.mainloop()