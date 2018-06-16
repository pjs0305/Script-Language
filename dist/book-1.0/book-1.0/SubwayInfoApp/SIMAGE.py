from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import win32api

class ImageWindow:
    def __init__(self, mainWindow, txt):
        self.window = Toplevel(mainWindow)
        self.window.geometry("640x600")
        self.window.resizable(False, False)
        self.window.title("지하철 노선도")

        self.Text = txt

        # 이미지 크기
        self.image_w = 2408
        self.image_h = 1958

        # 이미지 축소 시 간격
        self.image_w_s = self.image_w // 4
        self.image_h_s = self.image_h // 4

        # 이미지 프레임 크기
        self.imageFrame_w = 600
        self.imageFrame_h = 480

        # 노선도 이미지 표시할 프레임
        self.LineWindow = Frame(self.window, width=500, height=400)
        self.LineWindow.place(x = 10, y = 30)

        # # # 크기 조절 스크롤 # # #
        self.ScaleVar = IntVar()

        self.scale = Scale(self.LineWindow, variable=self.ScaleVar, command=self.PhotoResize, orient="horizontal", showvalue=False, from_=0,
                      to=3, length=self.imageFrame_w)

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

        self.Scrolly.set(5)
        # # # # # # # # # # # # # #

        # # # # 이미지 설정 # # # #
        self.SetPhotoList()

        self.ImageFrame = Frame(self.LineWindow, width=self.imageFrame_w, height=self.imageFrame_h)
        self.ImageFrame.pack()

        self.label = Label(self.ImageFrame, image=self.tk_image[0])
        self.label.bind("<MouseWheel>", self.WheelMove)
        self.label.bind("<Button-2>", self.WheelClick)
        self.label.bind("<B2-Motion>", self.WheelClickMove)

        self.SetPosition()
        # # # # # # # # # # # # # #

        values = ['수도권 1호선', '수도권 2호선', '수도권 3호선', '수도권 4호선', '수도권 5호선', '수도권 6호선',
                  '수도권 7호선', '수도권 8호선', '수도권 9호선', '수도권 경강선', '수도권 경의중앙성',
                  '수도권 경춘선', '수도권 공항철도', '수도권 분당선', '수도권 수인선', '수도권 신분당선',
                  '수도권 에버라인', '수도권 우이신설선', '수도권 의정부경전철',
                  '수도권 인천 1호선', '수도권 인천 2호선',
                  '부산 1호선', '부산 2호선', '부산 3호선', '부산 4호선', '부산 동해선', '부산 부산김해경전철',
                  '대구 1호선', '대구 2호선', '대구 3호선',
                  '대전 1호선',
                  '광주 1호선',]

        self.combobox = ttk.Combobox(self.window, values = values, height=10, state='readonly')
        self.combobox.bind("<<ComboboxSelected>>", self.SetPhoto)
        self.combobox.pack()

        self.combobox.set("수도권 1호선")

    def WheelClick(self, event):
        self.startx, self.starty = win32api.GetCursorPos()
        self.startSx = self.Scrollx.get()
        self.startSy = self.Scrolly.get()

    def WheelClickMove(self, event):
        self.deltax = win32api.GetCursorPos()[0] - self.startx
        self.deltay = win32api.GetCursorPos()[1] - self.starty

        SetScrollx = self.deltax // 150
        SetScrolly = self.deltay // 150

        self.Scrollx.set( self.startSx + SetScrollx)
        self.Scrolly.set( self.startSy + SetScrolly)

    def WheelMove(self, event):
        if event.delta < 0:
            SetScaleScroll = self.scale.get() + 1
            if SetScaleScroll > self.scale["to"]:
                SetScaleScroll = self.scale["to"]
        elif event.delta > 0:
            SetScaleScroll = self.scale.get() - 1
            if SetScaleScroll < 0:
                SetScaleScroll = 0

        self.scale.set(SetScaleScroll)

    def SetPhoto(self, event=None):
        self.Text = self.combobox.get()
        self.SetPhotoList()

        value = self.scale.get()

        self.label = Label(self.ImageFrame, image=self.tk_image[value])
        self.label.bind("<MouseWheel>", self.WheelMove)
        self.label.bind("<Button-2>", self.WheelClick)
        self.label.bind("<B2-Motion>", self.WheelClickMove)

        self.SetPosition()

    def SetPhotoList(self):
        ImageURL = 'Image\\' + self.Text + ' 노선도.jpg'

        self.Subway_Image = []
        self.tk_image = []
        self.w = []
        self.h = []

        for i in range(0, 4):
            # 이미지 추가
            self.Subway_Image.append(Image.open(ImageURL).resize(
                (self.image_w - (i * self.image_w_s), self.image_h - (i * self.image_h_s)),
                Image.ANTIALIAS))

            # 이미지 설정
            self.tk_image.append(ImageTk.PhotoImage(self.Subway_Image[i]))

            # 이미지 크기 설정
            self.w.append(self.Subway_Image[i].width)
            self.h.append(self.Subway_Image[i].height)

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

    def PhotoResize(self, event=None):
        value = self.scale.get()

        self.label = Label(self.ImageFrame, image=self.tk_image[value])
        self.label.bind("<MouseWheel>", self.WheelMove)
        self.label.bind("<Button-2>", self.WheelClick)
        self.label.bind("<B2-Motion>", self.WheelClickMove)

        self.SetPosition()

    def PhotoScroll(self, event=None):
        self.SetPosition()