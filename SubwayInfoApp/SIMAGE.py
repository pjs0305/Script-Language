from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class ImageWindow:
    # 이미지 크기별 리스트
    Subway_Image = {}

    # 이미지 크기별 위젯 리스트
    tk_image = {}

    # 현재 이미지 크기
    w = []
    h = []

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
        self.image_w_s = self.image_w // 10
        self.image_h_s = self.image_h // 10

        # 이미지 프레임 크기
        self.imageFrame_w = 600
        self.imageFrame_h = 500


        # 노선도 이미지 표시할 프레임
        self.LineWindow = Frame(self.window, width=500, height=400)
        self.LineWindow.place(x = 10, y = 30)

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

        self.Scrolly.set(5)
        # # # # # # # # # # # # # #

        # # # # 이미지 설정 # # # #
        self.SetPhotoList()

        self.ImageFrame = Frame(self.LineWindow, width=self.imageFrame_w, height=self.imageFrame_h)
        self.ImageFrame.pack()

        self.label = Label(self.ImageFrame, image=ImageWindow.tk_image[self.Text][0])

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

    def SetPhoto(self, self1=1):
        print(1)
        self.Text = self.combobox.get()
        self.SetPhotoList()

        value = self.scale.get()

        self.label = Label(self.ImageFrame, image=ImageWindow.tk_image[self.Text][value])
        self.SetPosition()

    def SetPhotoList(self):
        ImageURL = 'Image\\' + self.Text + ' 노선도.jpg'

        if not ImageWindow.Subway_Image.get(self.Text):
            ImageWindow.Subway_Image[self.Text] = []
            ImageWindow.tk_image[self.Text] = []

            for i in range(0, 8):
                # 이미지 추가
                ImageWindow.Subway_Image[self.Text].append(Image.open(ImageURL).resize(
                    (self.image_w - (i * self.image_w_s), self.image_h - (i * self.image_h_s)),
                    Image.ANTIALIAS))

                # 이미지 설정
                ImageWindow.tk_image[self.Text].append(ImageTk.PhotoImage(ImageWindow.Subway_Image[self.Text][i]))

                # 이미지 크기 설정
                ImageWindow.w.append(ImageWindow.Subway_Image[self.Text][i].width)
                ImageWindow.h.append(ImageWindow.Subway_Image[self.Text][i].height)

    def SetPosition(self):
        value = self.scale.get()

        # 이미지 크기와 윈도우 창 크기로 이미지 위치 계산
        IPx = (ImageWindow.w[value] // 2) - (self.imageFrame_w // 2)
        IPy = (ImageWindow.h[value] // 2) - (self.imageFrame_h // 2)

        # 이미지 크기와 스크롤바 중간 값으로 스크롤바를 움직일 때 얼만큼 이동할지 계산
        sx = IPx // 5
        sy = IPy // 5

        # 이미지 위치를 스크롤바 값으로 계산 ~~~
        IPx -= ((5 - self.Scrollx.get()) * sx)
        IPy -= ((5 - self.Scrolly.get()) * sy)

        self.label.place(x=-IPx, y=-IPy)

    def PhotoResize(self, self2):
        value = self.scale.get()

        self.label = Label(self.ImageFrame, image=ImageWindow.tk_image[self.Text][value])

        self.SetPosition()

    def PhotoScroll(self, self2):
        self.SetPosition()