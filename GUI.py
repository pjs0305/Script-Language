from tkinter import *
from tkinter import font
from XML import *


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
    InputStation = Entry(LeftWindow, width=20, borderwidth=3)
    InputStation.place(x=160, y=50)

    # 검색 버튼
    SearchButton = Button(LeftWindow, text="검색", command=SearchStation)
    SearchButton.place(x=330, y=47.5)

    # 검색결과 리스트
    ListFrame = Frame(LeftWindow)

    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")

    global StationListBox
    StationListBox = Listbox(ListFrame, width=43, borderwidth=5, font=Listfont, activestyle="none", yscrollcommand=scrollbar.set)
    StationListBox.pack()
    scrollbar.config(command=StationListBox.yview)
    ListFrame.place(x=15, y=90)

    # 글자
    SearchText = Label(LeftWindow, font=Subfont, text="지하철역 정보")
    SearchText.place(x=145, y=280)

    # 버튼
    global BusButton
    BusButton = Button(LeftWindow, font=Listfont, text="출구별 주변 버스 조회", command=ShowBus, state="disabled")
    BusButton.place(x=115, y=310)

    global BuildingButton
    BuildingButton = Button(LeftWindow, font=Listfont, text="출구별 주변 건물 조회", command=ShowBuilding, state="disabled")
    BuildingButton.place(x=115, y=350)

    global ScheduleButton
    ScheduleButton = Button(LeftWindow, font=Listfont, text="시간표 조회", command=ShowSchedule, state="disabled")
    ScheduleButton.place(x=50, y=420)

    OpenButton = Checkbutton(LeftWindow, text="정보 보기", command=OpenCloseRight)
    OpenButton.place(x=300, y=280)

def SetRight(): # 오른쪽 창 설정
    global RightWindow

    if RightWindow:
        RightWindow.destroy()

    RightWindow = Frame(MainWindow, relief="solid", bd=1)
    RightWindow.pack(side="right", fill="both")

    if Open == 1:
        RightWindow.pack(expand=True)

    MainText = Label(RightWindow, font = Mainfont, text = "지하철역 정보 조회 결과")
    MainText.place(x=80, y=10)

def OpenCloseRight(): # 오른쪽 창 펼치거나 닫기
    global Open, MainWindow, RightWindow
    Open = (Open + 1) % 2
    if Open == 1:
        MainWindow.geometry("800x500")
        RightWindow.pack(expand=True)
    else:
        MainWindow.geometry("400x500")
        RightWindow.pack(expand=False)

def OpenRight():
    global Open, MainWindow, RightWindow
    if Open == 0:
        Open = 1
        OpenButton.select()
        MainWindow.geometry("800x500")
        RightWindow.pack(expand=True)

def SearchStation():
    global stationList, stationListId
    
    StationListBox.delete(0, END) # 검색된 리스트 초기화
    stationList = FindStation(InputStation.get()) # 검색한 문자열로 지하철역 검색
    stationListId = ExtractDictKey(stationList)

    # 검색 결과를 리스트 박스에 추가
    global StationListBox
    i = 0
    for Station in stationList:
        str = stationList[Station] + " " + "[" + FindStationLine(Station) + "]"
        StationListBox.insert(i, str)
        i+=1

    # 검색 결과가 있을 경우 조회 버튼 활성화
    # 없을 경우 비활성화
    if StationListBox.size() > 0:
        StationListBox.selection_set(0)

        BusButton.configure(state = "active")
        BuildingButton.configure(state = "active")
        ScheduleButton.configure(state = "active")
    else:
        BusButton.configure(state = "disabled")
        BuildingButton.configure(state = "disabled")
        ScheduleButton.configure(state = "disabled")


def ShowBus(): # 버스 조회 GUI
    OpenRight()
    SetRight()

    # 현재 선택된 지하철역으로 춣구별 주변 버스 찾기
    select = StationListBox.curselection()

    global SearchBus, SearchExitNo
    SearchBus = FindBus(stationListId[select[0]])
    SearchExitNo = ExtractDictKey(SearchBus)

    TEXT = stationList[stationListId[select[0]]]
    if TEXT[len(TEXT)-1:len(TEXT)] != "역":
        TEXT += "역"

    StationText = Label(RightWindow, text=TEXT, font=Subfont)
    StationText.place(x = 15 , y=50)

    Text1 = Label(RightWindow, text="버스번호 리스트", font=Subfont)
    Text1.place(x=180, y=90)

    # 검색결과 리스트
    global BusNoList

    ListFrame = Frame(RightWindow)

    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")

    BusNoList = Listbox(ListFrame, width= 20, height=20, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
    BusNoList.pack()

    scrollbar.config(command=BusNoList.yview)

    Text2 = Label(RightWindow, text="출구번호", font=Subfont)
    Text2.place(x=15, y=90)

    ListFrame.place(x = 180, y = 120)

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

    ShowBusList()

def ShowBusList():
    global BusNoList

    BusNoList.config(state='normal')

    BusNoList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for BusNo in SearchBus[SearchExitNo[ExitNoVar.get()]]:
        BusNoList.insert(i, BusNo)
        i += 1

    BusNoList.config(state='disabled')


def ShowBuilding():
    OpenRight()
    SetRight()

    # 현재 선택된 지하철역으로 춣구별 주변 건물 찾기
    select = StationListBox.curselection()

    global SearchBuilding, SearchExitNo
    SearchBuilding = FindBuilding(stationListId[select[0]])
    SearchExitNo = ExtractDictKey(SearchBuilding)

    TEXT = stationList[stationListId[select[0]]]
    if TEXT[len(TEXT)-1:len(TEXT)] != "역":
        TEXT += "역"

    global RightWindow

    StationText = Label(RightWindow, text=TEXT, font=Subfont)
    StationText.place(x = 15 , y=50)

    Text1 = Label(RightWindow, text="건물이름 리스트", font=Subfont)
    Text1.place(x=15, y=220)

    # 검색결과 리스트
    global BuildingList

    ListFrame = Frame(RightWindow)

    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")

    BuildingList = Listbox(ListFrame, width= 43, height=13, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
    BuildingList.pack()

    scrollbar.config(command=BuildingList.yview)

    Text2 = Label(RightWindow, text="출구번호", font=Subfont)
    Text2.place(x=15, y=90)

    ListFrame.place(x = 15, y = 250)

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

    ShowBuildingList()

def ShowBuildingList():
    global BuildingList

    BuildingList.config(state='normal')

    BuildingList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for Building in SearchBuilding[SearchExitNo[ExitNoVar.get()]]:
        BuildingList.insert(i, Building)
        i += 1

    BuildingList.config(state='disabled')


def ShowSchedule():
    OpenRight()
    SetRight()

    # 현재 선택된 지하철역으로 춣구별 주변 건물 찾기
    select = StationListBox.curselection()

    global SearchBuilding, SearchExitNo
    SearchBuilding = FindBuilding(stationListId[select[0]])
    SearchExitNo = ExtractDictKey(SearchBuilding)

    CreateScheduleWidget(rightwin)

    ShowScheduleList()

def ShowScheduleList():
    global BuildingList, ExitNoVar

    BuildingList.config(state='normal')

    BuildingList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for Building in SearchBuilding[SearchExitNo[ExitNoVar.get()]]:
        BuildingList.insert(i, Building)
        i += 1

    BuildingList.config(state='disabled')

def CreateScheduleWidget(window):
    # 시간표 검색타입
    global DailyTypeIntVar, UDTypeIntVar
    DailyTypeIntVar = IntVar()
    UDTypeIntVar = IntVar()

    WeekDay = Radiobutton(window, text = "평일", value = "01", variable=DailyTypeIntVar)
    WeekDay.place(x=180, y=390)
    Saturday = Radiobutton(window, text = "토요일", value = "02", variable=DailyTypeIntVar)
    Saturday.place(x=180, y=420)
    Sunday = Radiobutton(window, text = "일요일", value = "03", variable=DailyTypeIntVar)
    Sunday.place(x=180, y=450)

    Up = Radiobutton(window, text = "상행", value = "U", variable=UDTypeIntVar)
    Up.place(x=270, y=400)
    Down = Radiobutton(window, text = "하행", value = "D", variable=UDTypeIntVar)
    Down.place(x=270, y=440)

    # 글자들
    TEXT = stationList[stationListId[select[0]]]
    if TEXT[len(TEXT)-1:len(TEXT)] != "역":
        TEXT += "역"
        
    StationText = Label(window, text=TEXT, font=Subfont)
    StationText.place(x = 15 , y=50)
    Text1 = Label(window, text="건물이름 리스트", font=Subfont)
    Text1.place(x=15, y=220)
    Text2 = Label(window, text="출구번호", font=Subfont)
    Text2.place(x=15, y=90)

    # 검색결과 리스트
    global BuildingList
    ListFrame = Frame(window)
    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")
    BuildingList = Listbox(ListFrame, width= 43, height=13, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
    BuildingList.pack()
    scrollbar.config(command=BuildingList.yview)
    ListFrame.place(x = 15, y = 250)

