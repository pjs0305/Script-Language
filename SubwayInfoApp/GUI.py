from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from io import BytesIO
from XML import *
from MAIL import *
import spam

# 윈도우창
MainWindow = Tk()

# 윈도우창 내부 분할 창
LeftWindow = Frame(MainWindow, relief="solid", bd=1)
RightWindow = Frame(MainWindow, relief="solid", bd=1)

# 윈도우창 펼칠지 안펼칠지 판단하는 변수
RightWindowOpen = False

# 글자 폰트들
Titlefont = font.Font(size=20, weight='bold', family='굴림')
Mainfont = font.Font(size=16, weight='bold', family='굴림')
Subfont = font.Font(size=13, family='굴림')
Listfont = font.Font(size=12, family='굴림')
font10 = font.Font(size=10, family='굴림')

# 검색결과 지하철역 저장
stationList = {} # 검색된 지하철역 ( ID : 이름 )
stationListId = [] # 검색된 지하철역 ID 리스트

# 즐겨찾기 지하철역 저장
BookMarkList = {} # 즐겨찾는 지하철역 ( ID : 이름 )
BookMarkListId = [] # 즐겨찾는 지하철역 ID 리스트

# 버스 검색 관련
SearchBus = {} # 검색된 지하철역 주변 버스 ( ExitNo : BusNo )
BusNoList = None

# 건물 검색 관련
SearchBuilding = {} # 검색된 지하철역 주변 건물 ( ExitNo : BuildingName )
BuildingList = None

# 출구 번호 관련
SearchExitNo = [] # 검색된 지하철역 출구 번호 리스트
ExitNoVar = None

# 시간표 검색 관련
ScheduleText = {"평일" : "01", "토요일" : "02", "일요일" : "03", "상행" : "U", "하행" : "D"}
ScheduleDailyTypeText = ["평일", "토요일", "일요일"]
ScheduleUDTypeText = ["상행", "하행"]
UDIndex = {"상행" : 0, "하행" : 1}
# 검색된 지하철역 시간표 ( Hour : 분 )
StationSchedule = { "평일"      : [ {"상행" : None }, { "하행" : None } ], \
                    "토요일"    : [ {"상행" : None }, { "하행" : None } ], \
                    "일요일"    : [ {"상행" : None }, { "하행" : None } ]   }
# 검색된 지하철역 시간
HourList = { "평일"      : [ {"상행" : None }, { "하행" : None } ], \
             "토요일"    : [ {"상행" : None }, { "하행" : None } ], \
             "일요일"    : [ {"상행" : None }, { "하행" : None } ]   }
DailyTypeIntVar = None
UDTypeIntVar = None
MinuteList = None
HourIntVar = None
# 시간 버튼 프레임
ButtonFrame = None
# 결과 텍스트 프레임
TextFrame = None

def CreateWindow(): # 윈도우 설정
    global MainWindow
    MainWindow.geometry("400x500")
    MainWindow.resizable(False, False)
    MainWindow.title("지하철역 정보 조회 애플리케이션")

    global LeftWindow
    LeftWindow.pack(side="left", fill="both", expand=True)

    # 상단 글자
    MainText = Label(LeftWindow, font=Titlefont, text="지하철역 정보 조회 App")
    MainText.place(x=50)
    StationText = Label(LeftWindow, font=Subfont, text="지하철역 입력")
    StationText.place(x=30, y=47)

    # 검색 박스
    global InputStation
    InputStation = Entry(LeftWindow, width=20, borderwidth=3, exportselection=True)
    InputStation.place(x=160, y=50)

    # 검색 버튼
    SearchButton = Button(LeftWindow, text="검색", command=SearchStation)
    SearchButton.place(x=330, y=47.5)



    # 리스트박스
    global ListBook
    ListBook = ttk.Notebook(LeftWindow)
    ListBook.pack(fill = 'both', expand = 1)

    # 검색결과 리스트박스
    ListFrame = Frame(ListBook)

    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")

    global StationListBox
    StationListBox = Listbox(ListFrame, width=43, height= 10, borderwidth=5, font=Listfont, activestyle="none", yscrollcommand=scrollbar.set, exportselection=True)
    StationListBox.pack()
    scrollbar.config(command=StationListBox.yview)

    global AddBookButton
    AddBookButton = Button(ListFrame, font=font10, text = "즐겨찾기에 추가하기", command=AddBookMark, width=44)
    AddBookButton.pack(side="bottom", anchor="w")

    # 즐겨찾기 리스트박스
    BookMarkFrame = Frame(ListBook)

    rscrollbar = Scrollbar(BookMarkFrame)
    rscrollbar.pack(side="right", fill="y")

    global BookMarkListBox
    BookMarkListBox = Listbox(BookMarkFrame, width=43, height= 10, borderwidth=5, font=Listfont, activestyle="none", yscrollcommand=rscrollbar.set, exportselection=True)
    BookMarkListBox.pack()
    rscrollbar.config(command=BookMarkListBox.yview)

    global SubBookButton

    SubBookButton = Button(BookMarkFrame, font=font10, text = "즐겨찾기에서 삭제하기", command=SubBookMark, width=44)
    SubBookButton.pack(side="bottom", anchor="w")

    ListBook.add(ListFrame, text = "검색결과")
    ListBook.add(BookMarkFrame, text = "즐겨찾기")
    ListBook.place(x=10, y=80)

    # 글자
    SearchText = Label(LeftWindow, font=Subfont, text="지하철역 정보")
    SearchText.place(x=145, y=320)

    # 버튼
    global BusButton
    BusButton = Button(LeftWindow, font=Listfont, text="출구별 주변 버스 조회", command=ShowBus)
    BusButton.place(x=115, y=360)

    global BuildingButton
    BuildingButton = Button(LeftWindow, font=Listfont, text="출구별 주변 건물 조회", command=ShowBuilding)
    BuildingButton.place(x=115, y=405)

    global ScheduleButton
    ScheduleButton = Button(LeftWindow, font=Listfont, text="시간표 조회", command=ShowSchedule)
    ScheduleButton.place(x=150, y=455)

    global OpenButton
    OpenButton = Checkbutton(LeftWindow, text="정보 보기", command=OpenCloseRight)
    OpenButton.place(x=300, y=320)

def AddBookMark():
    global StationListBox
    global BookMarkListBox
    global stationList, stationListId
    global BookMarkList, BookMarkListId

    select = StationListBox.curselection()

    # 선택된 지하철역 ID와 이름
    StationId = stationListId[select[0]]
    StationName = stationList[StationId]
    
    prevSize = len(BookMarkList)
    BookMarkList[StationId] = StationName
    NowSize = len(BookMarkList)

    if prevSize != NowSize: # 즐겨찾기 추가에 성공했을 때
        BookMarkListId.append(stationListId[select[0]])

        str = StationName + " " + "[" + FindStationLine(StationId) + "]"
        BookMarkListBox.insert(prevSize, str)

    print(BookMarkList)

def SubBookMark():
    global BookMarkListBox
    global BookMarkList, BookMarkListId

    select = BookMarkListBox.curselection()

    removeStationId = BookMarkListId[select[0]]

    BookMarkList.pop(removeStationId)
    BookMarkListId.remove(removeStationId)

    BookMarkListBox.delete(select[0])

    print(BookMarkList)

def SetRight(): # 오른쪽 창 설정
    global RightWindow

    if RightWindow:
        RightWindow.destroy()

    RightWindow = Frame(MainWindow, relief="solid", bd=1)
    RightWindow.pack(side="right", fill="both")

    if RightWindowOpen == True  :
        RightWindow.pack(expand=True)

    RightWindowMainText = Label(RightWindow, font = Mainfont, text = "지하철역 정보 조회 결과")
    RightWindowMainText.place(x=80, y=10)

def OpenCloseRight(): # 오른쪽 창 펼치거나 닫기
    global RightWindowOpen

    if RightWindowOpen:
        RightWindowOpen = False
    else:
        RightWindowOpen = True

    if RightWindowOpen == True:
        MainWindow.geometry("800x500")
        RightWindow.pack(expand=True)
    else:
        MainWindow.geometry("400x500")
        RightWindow.pack(expand=False)

def OpenRightWindow():
    global RightWindowOpen, OpenButton

    if RightWindowOpen == False:
        RightWindowOpen = True
        OpenButton.select()
        MainWindow.geometry("800x500")
        RightWindow.pack(expand=True)

def SearchStation():
    SetRight()

    global ListBook
    ListBook.select(0)

    StationListBox.delete(0, END) # 검색된 리스트박스 초기화

    global stationList, stationListId
    stationList = FindStation(InputStation.get()) # 검색한 문자열로 지하철역 검색
    stationListId = ExtractDictKey(stationList) # 검색된 지하철역 ID만 저장

    # 검색 결과를 리스트 박스에 추가
    i = 0
    for Station in stationList:
        str = stationList[Station] + " " + "[" + FindStationLine(Station) + "]"
        StationListBox.insert(i, str)
        i+=1


def ShowBus(): # 버스 조회 GUI
    SetRight()
    OpenRightWindow()

    # 현재 선택된 지하철역으로 출구별 주변 버스 찾기

    global SearchBus, SearchExitNo

    global StationName, StationId
    StationName, StationId = SelectStation()

    SearchBus = FindBus(StationId)
    SearchExitNo = ExtractDictKey(SearchBus)

    if len(SearchBus) != 0:
        # 그 외 글자들
        Text1 = Label(RightWindow, text="버스번호 리스트", font=Subfont)
        Text1.place(x=180, y=90)

        Text2 = Label(RightWindow, text="출구번호", font=Subfont)
        Text2.place(x=15, y=90)

        # 검색결과 리스트
        global BusNoList

        ListFrame = Frame(RightWindow)

        scrollbar = Scrollbar(ListFrame)
        scrollbar.pack(side="right", fill="y")

        BusNoList = Listbox(ListFrame, width= 20, height=16, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
        BusNoList.pack()

        scrollbar.config(command=BusNoList.yview)
        ListFrame.place(x = 180, y = 120)

        # 출구 번호 버튼들
        global ExitNoVar
        ExitNoVar = IntVar()

        x = y = 0
        for Exit in SearchExitNo:
            radio1 = Radiobutton(RightWindow, text=Exit, value=y*2 + x, variable=ExitNoVar, command=ShowBusList)
            radio1.place(x= 15 + x*60, y=120 + y*30)
            x+=1
            if x%2 == 0:
                y+=1
                x=0

        # 보여주기
        ShowBusList()

        EmailButton = Button(RightWindow, text= "조회 결과 메일로 보내기", font = Listfont, command = MailBusInf)
        EmailButton.place(x=80, y=445)
    else:
        Text1 = Label(RightWindow, text="조회 결과가 없음", font=Subfont)
        Text1.place(x=130, y=150)

def ShowBusList(): # 버스 리스트박스에 출력
    BusNoList.config(state='normal') # 리스트박스 일반 상태로
    BusNoList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for BusNo in SearchBus[SearchExitNo[ExitNoVar.get()]]:
        BusNoList.insert(i, BusNo)
        i += 1

    BusNoList.config(state='disabled') # 리스트박스 읽기 상태로

    global TextFrame
    # 결과 텍스트
    if TextFrame:
        TextFrame.destroy()

    TextFrame = Frame(RightWindow)
    TextFrame.place(x=15, y=50)

    TEXT = StationName
    if TEXT[len(TEXT) - 1:len(TEXT)] != "역":
        TEXT += "역"

    TEXT += " " + str(SearchExitNo[ExitNoVar.get()]) + "번 출구"

    ResultText = Label(TextFrame, text=TEXT, font=font10)
    ResultText.pack()

def MailBusInf():
    CreateSendMailWindow(SendBusInf, "출구별 주변 버스 정보")

def SendBusInf():
    # 메일 주소 받아옴
    text = StationName + " 출구별 주변 버스 목록"
    SendData(MailInput.get(), text, MakeBodyBus, SearchBus)
    messagebox.showinfo("알림", "메일을 전송하였습니다.")


def ShowBuilding():
    SetRight()
    OpenRightWindow()

    global SearchBuilding, SearchExitNo

    global StationName, StationId
    StationName, StationId = SelectStation()

    SearchBuilding = FindBuilding(StationId)
    SearchExitNo = ExtractDictKey(SearchBuilding)

    if len(SearchBuilding) != 0:
        # 그 외 글자
        Text1 = Label(RightWindow, text="건물이름 리스트", font=Subfont)
        Text1.place(x=15, y=220)

        Text2 = Label(RightWindow, text="출구번호", font=Subfont)
        Text2.place(x=15, y=90)

        # 검색결과 리스트
        global BuildingList

        ListFrame = Frame(RightWindow)

        scrollbar = Scrollbar(ListFrame)
        scrollbar.pack(side="right", fill="y")

        BuildingList = Listbox(ListFrame, width= 43, height=10, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
        BuildingList.pack()

        scrollbar.config(command=BuildingList.yview)
        ListFrame.place(x = 15, y = 250)

        # 출구 번호 버튼들
        global ExitNoVar
        ExitNoVar = IntVar()

        x = y = 0
        for Exit in SearchExitNo:
            radio1 = Radiobutton(RightWindow, text=Exit, value=y*7 + x, variable=ExitNoVar, command=ShowBuildingList)
            radio1.place(x= 15 + x*50, y=120 + y*30)
            x+=1
            if x%7 == 0:
                y+=1
                x=0

        # 보여주기
        ShowBuildingList()

        EmailButton = Button(RightWindow, text= "조회 결과 메일로 보내기", font = Listfont, command = MailBuilInf)
        EmailButton.place(x = 100, y = 445)
    else:
        Text1 = Label(RightWindow, text="조회 결과가 없음", font=Subfont)
        Text1.place(x=130, y=150)

def ShowBuildingList():
    BuildingList.config(state='normal')
    BuildingList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for Building in SearchBuilding[SearchExitNo[ExitNoVar.get()]]:
        BuildingList.insert(i, Building)
        i += 1

    BuildingList.config(state='disabled')

    global TextFrame
    # 결과 텍스트
    if TextFrame:
        TextFrame.destroy()

    TextFrame = Frame(RightWindow)
    TextFrame.place(x=15, y=50)

    TEXT = StationName
    if TEXT[len(TEXT) - 1:len(TEXT)] != "역":
        TEXT += "역"

    TEXT += " " + str(SearchExitNo[ExitNoVar.get()]) + "번 출구"

    ResultText = Label(TextFrame, text=TEXT, font=font10)
    ResultText.pack()

def MailBuilInf():
    CreateSendMailWindow(SendBuilInf, "출구별 주변 건물 정보")

def SendBuilInf():
    # 메일 주소 받아옴
    text = StationName + " 출구별 주변 건물 목록"
    SendData(MailInput.get(), text, MakeBodyBuild, SearchBuilding)
    messagebox.showinfo("알림", "메일을 전송하였습니다.")


def ShowSchedule():
    SetRight()
    OpenRightWindow()

    global StationSchedule

    global StationName, StationId
    StationName, StationId = SelectStation()

    for Dtype in ["평일", "토요일", "일요일"]:
        for UDtype in ["상행", "하행"]:
            StationSchedule[Dtype][UDIndex[UDtype]][UDtype] = FindSchedule(StationId, ScheduleText[Dtype], ScheduleText[UDtype])

    for Dtype in ["평일", "토요일", "일요일"]:
        for UDtype in ["상행", "하행"]:
            HourList[Dtype][UDIndex[UDtype]][UDtype] = ExtractDictKey(StationSchedule[Dtype][UDIndex[UDtype]][UDtype])

    # 시간표 위젯 만들기
    CreateScheduleWidget()

def ShowHourList():
    global ButtonFrame

    # 시간 버튼들
    if ButtonFrame:
        ButtonFrame.destroy()

    ButtonFrame = Frame(RightWindow, width=200, height=200)
    ButtonFrame.place(x=15, y=200)

    global HourIntVar
    HourIntVar = IntVar()

    x = y = 0

    for Hour in StationSchedule[ScheduleDailyTypeText[DailyTypeIntVar.get()]]   [UDTypeIntVar.get()]    [ScheduleUDTypeText[UDTypeIntVar.get()]]:
        # 평일 or 토요일 일요일
        # 0 or 1
        # 상행 or 하행
        radio = Radiobutton(ButtonFrame, text=Hour, value=y*4 + x, variable=HourIntVar, command=ShowScheduleList)
        radio.place(x = x*50, y = y*40)
        x += 1
        if x % 4 == 0:
            y += 1
            x=0
    
    ShowScheduleList()

def ShowScheduleList():
    global MinuteList

    MinuteList.config(state='normal')

    MinuteList.delete(0, END)  # 검색된 리스트 초기화

    # DailyTypeIntVar, UDTypeIntVar, HourIntVar

    i = 0
    if len(HourList[ScheduleDailyTypeText[DailyTypeIntVar.get()]][UDTypeIntVar.get()][ScheduleUDTypeText[UDTypeIntVar.get()]]) != 0:
        for Minute in StationSchedule[ScheduleDailyTypeText[DailyTypeIntVar.get()]]  [UDTypeIntVar.get()]    [ScheduleUDTypeText[UDTypeIntVar.get()]]  [HourList[ScheduleDailyTypeText[DailyTypeIntVar.get()]]      [UDTypeIntVar.get()]    [ScheduleUDTypeText[UDTypeIntVar.get()]]  [HourIntVar.get()]]:
            MinuteList.insert(i, Minute)
            i += 1

    MinuteList.config(state='disabled')

    global TextFrame
    # 결과 텍스트
    if TextFrame:
        TextFrame.destroy()

    TextFrame = Frame(RightWindow)
    TextFrame.place(x=15, y=50)

    TEXT = StationName
    if TEXT[len(TEXT) - 1:len(TEXT)] != "역":
        TEXT += "역"
    TEXT += " " + "[" + FindStationLine(StationId) + "]"


    TEXT += "-" + ScheduleDailyTypeText[DailyTypeIntVar.get()] + "-" + ScheduleUDTypeText[UDTypeIntVar.get()]

    if len(HourList[ScheduleDailyTypeText[DailyTypeIntVar.get()]]      [UDTypeIntVar.get()]    [ScheduleUDTypeText[UDTypeIntVar.get()]] ) != 0:
        TEXT += "-" + HourList[ScheduleDailyTypeText[DailyTypeIntVar.get()]]      [UDTypeIntVar.get()]    [ScheduleUDTypeText[UDTypeIntVar.get()]]  [HourIntVar.get()] + "시"
    else:
        TEXT += "-" + "시간 없음"

    ResultText = Label(TextFrame, text=TEXT, font=font10)
    ResultText.pack()

def CreateScheduleWidget():

    # 그 외 글자들
    Text1 = Label(RightWindow, text="시간", font=Subfont)
    Text1.place(x=15, y=170)

    Text2 = Label(RightWindow, text="분", font=Subfont)
    Text2.place(x=250, y=170)

    # 시간표 검색타입 버튼
    global DailyTypeIntVar, UDTypeIntVar
    DailyTypeIntVar = IntVar()
    UDTypeIntVar = IntVar()

    WeekDay = Radiobutton(RightWindow, text = "평일", value = 0, variable=DailyTypeIntVar, command=ShowHourList)
    WeekDay.place(x=30, y=90)
    WeekDay.select()
    Saturday = Radiobutton(RightWindow, text = "토요일", value = 1, variable=DailyTypeIntVar, command=ShowHourList)
    Saturday.place(x=100, y=90)
    Sunday = Radiobutton(RightWindow, text = "일요일", value = 2, variable=DailyTypeIntVar, command=ShowHourList)
    Sunday.place(x=170, y=90)

    Up = Radiobutton(RightWindow, text = "상행", value = 0, variable=UDTypeIntVar, command=ShowHourList)
    Up.place(x=30, y=130)
    Up.select()
    Down = Radiobutton(RightWindow, text = "하행", value = 1, variable=UDTypeIntVar, command=ShowHourList)
    Down.place(x=100, y=130)

    # 검색결과 리스트
    global MinuteList
    ListFrame = Frame(RightWindow)
    ListFrame.place(x = 250, y = 200)

    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")

    MinuteList = Listbox(ListFrame, width= 10, height=12, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
    MinuteList.pack()

    scrollbar.config(command=MinuteList.yview)

    ShowHourList()

    EmailButton = Button(RightWindow, text= "조회 결과 메일로 보내기", font = Listfont, command = MailSchedInf)
    EmailButton.place(x=100, y=445)

def MailSchedInf():
    CreateSendMailWindow(SendSchedInf, "시간표 정보")

def SendSchedInf():
    # 메일 주소 받아옴
    text = StationName + " " + FindStationLine(StationId) + " 시간표"
    SendData(MailInput.get(), text, MakeBodySched, StationSchedule)
    messagebox.showinfo("알림", "메일을 전송하였습니다.")


def SelectStation():
    global ListBook
    global StationListBox, BookMarkListBox

    if ListBook.index(ListBook.select()) == 0: # 검색결과창
        select = StationListBox.curselection()
        StationId = stationListId[select[0]]
        StationName = stationList[StationId]
    else:
        select = BookMarkListBox.curselection()
        StationId = BookMarkListId[select[0]]
        StationName = BookMarkList[StationId]

    return StationName, StationId

def CreateSendMailWindow(SendFunc, title):
    global StationName, StationId

    MailWin = Toplevel(MainWindow, width=350, height=200)
    MailWin.resizable(False, False)
    MailWin.title("메일 보내기")

    text1 = Label(MailWin, font=Listfont, text=title)
    text1.pack(side="top", anchor="center")
    #text1.place(y= 10)

    station = StationName + " " + FindStationLine(StationId)

    text2 = Label(MailWin, font=Listfont, text=station)
    text2.pack(side="top", anchor="center")
    #text2.place(y=50)

    global MailInput
    MailInput = Entry(MailWin)
    MailInput.pack(anchor="center")
    #input.place(x=100, y = 120)

    text3 = Label(MailWin, text="보낼 메일 주소")
    text3.pack(anchor="center")
    #text3.place(x= 10, y= 118)

    button = Button(MailWin, text="메일 보내기", command=SendFunc)
    button.pack(anchor="center")

def ShowSubwayLine():

    LineWin = Toplevel(MainWindow, width=400, height=350)
    LineWin.resizable(False, False)
    LineWin.title("지하철 노선도")

    ImageFrame = Frame(LineWin)
    ImageFrame.place(x=50, y=10)

    url = "http://tong.visitkorea.or.kr/cms/resource/74/2396274_image2_1.JPG"
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    label = Label(root, image=image, height=400, width=400)
    label.pack()
    label.place(x=0, y=0)
    root.mainloop()


# 함수 호출
CreateWindow()
SetRight()

MainWindow.mainloop()
