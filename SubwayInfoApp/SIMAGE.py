from tkinter import *
from PIL import Image, ImageTk

class ImageWindow:
    def __init__(self, mainWindow):
        self.window = Toplevel(mainWindow)
        self.window.geometry("700x700")
        self.window.resizable(False, False)
        self.window.title("지하철 노선도")

        # 이미지 크기
        self.image_w = 2408
        self.image_h = 1958

        #이미지 축소 시 간격
        self.image_w_s = self.image_w // 10
        self.image_h_s = self.image_h // 10

        self.imageFrame_w = 600
        self.imageFrame_h = 500

        # 현재 이미지 크기
        self.w = []
        self.h = []

        # 이미지 크기별 리스트
        self.Subway_Image = []
        
        # 이미지 크기별 위젯 리스트
        self.tk_image = []

        # 노선도 이미지 표시할 프레임
        self.LineWindow = Frame(self.window, width=500, height=400)
        self.LineWindow.place(x = 40, y = 130)

        # # # 크기 조절 스크롤 # # #
        self.ScaleVar = IntVar()

        self.scale = Scale(self.LineWindow, variable=self.ScaleVar, command=self.PhotoResize, orient="horizontal", showvalue=False, from_=0,
                      to=7, length=self.imageFrame_w)
        self.scale.pack(side="top")
        # # # # # # # # # # # # # #

        # # # # 가로 스크롤 # # # #
        self.ScrollxVar = IntVar()

        self.Scrollx = Scale(self.LineWindow, variable=self.ScrollxVar, command=self.PhotoScroll, orient="horizontal", showvalue=False,
                        from_=0, to=10, length=self.imageFrame_w)
        self.Scrollx.pack(side="bottom")

        self.Scrollx.set(5)
        # # # # # # # # # # # # # #

        # # # # 세로 스크롤 # # # #
        self.ScrollyVar = IntVar()

        self.Scrolly = Scale(self.LineWindow, variable=self.ScrollyVar, command=self.PhotoScroll, orient="vertical", showvalue=False,
                        from_=0, to=10, length=self.imageFrame_h)
        self.Scrolly.pack(side="right")
        # # # # # # # # # # # # # #

        # # # # 이미지 설정 # # # #
        self.SetPhotoList()

        self.ImageFrame = Frame(self.LineWindow, width=self.imageFrame_w, height=self.imageFrame_h)
        self.ImageFrame.pack()

        self.Scrolly.set(5)

        self.label = Label(self.ImageFrame, image=self.tk_image[0])
        self.SetPosition()
        # # # # # # # # # # # # # #

    def SetPhotoList(self):
        for i in range(0, 8):
            self.Subway_Image.append(Image.open('F:\스크립트 언어\Script Language\SubwayInfoApp\Image\대구 지하철 노선도.jpg').resize(
                (self.image_w - (i * self.image_w_s), self.image_h - (i * self.image_h_s)),
                Image.ANTIALIAS))
            self.tk_image.append(ImageTk.PhotoImage(self.Subway_Image[i]))

            self.w.append(self.image_w - (i * self.image_w_s))
            self.h.append(self.image_h - (i * self.image_h_s))

    def SetPosition(self):
        value = self.scale.get()

        # 이미지 크기와 윈도우 창 크기로 이미지 위치 계산
        IPx = (self.w[value] // 2) - (self.imageFrame_w // 2)
        IPy = (self.h[value] // 2) - (self.imageFrame_h // 2)

        # 이미지 크기와 스크롤바 중간 값으로 스크롤바를 움직일 때 얼만큼 이동할지 계산
        sx = IPx // 5
        sy = IPy // 5

        # 이미지 위치를 스크롤바 값으로 계산 ~~~
        IPx -= ((5 - self.Scrollx.get()) * sx)
        IPy -= ((5 - self.Scrolly.get()) * sy)

        self.label.place(x=-IPx, y=-IPy)

    def PhotoResize(self, self2):
        value = self.scale.get()

        self.label = Label(self.ImageFrame, image=self.tk_image[value])

        self.SetPosition()

    def PhotoScroll(self, self2):
        self.SetPosition()