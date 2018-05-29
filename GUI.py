from tkinter import *
from tkinter import font
from XML import *

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

# 지하철역 저장 변수
stationList = {} # 검색된 지하철역 ( ID : 이름 )
stationListId = [] # 검색된 지하철역 ID 리스트

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
    BusButton.place(x=115, y=320)

    global BuildingButton
    BuildingButton = Button(LeftWindow, font=Listfont, text="출구별 주변 건물 조회", command=ShowBuilding, state="disabled")
    BuildingButton.place(x=115, y=380)

    global ScheduleButton
    ScheduleButton = Button(LeftWindow, font=Listfont, text="시간표 조회", command=ShowSchedule, state="disabled")
    ScheduleButton.place(x=150, y=440)

    global OpenButton
    OpenButton = Checkbutton(LeftWindow, text="정보 보기", command=OpenCloseRight)
    OpenButton.place(x=300, y=280)

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
    SetRight()
    OpenRightWindow()

    # 현재 선택된 지하철역으로 춣구별 주변 버스 찾기
    select = StationListBox.curselection()

    global SearchBus, SearchExitNo
    SearchBus = FindBus(stationListId[select[0]])
    SearchExitNo = ExtractDictKey(SearchBus)

    # 선택된 지하철역 글자
    TEXT = stationList[stationListId[select[0]]]
    if TEXT[len(TEXT)-1:len(TEXT)] != "역":
        TEXT += "역"
    StationText = Label(RightWindow, text=TEXT, font=Subfont)
    StationText.place(x = 15 , y=50)

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

    BusNoList = Listbox(ListFrame, width= 20, height=20, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
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

def ShowBusList(): # 버스 리스트박스에 출력
    BusNoList.config(state='normal') # 리스트박스 일반 상태로
    BusNoList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for BusNo in SearchBus[SearchExitNo[ExitNoVar.get()]]:
        BusNoList.insert(i, BusNo)
        i += 1

    BusNoList.config(state='disabled') # 리스트박스 읽기 상태로


def ShowBuilding():
    SetRight()
    OpenRightWindow()

    # 현재 선택된 지하철역
    select = StationListBox.curselection()

    # 지하철역 주변 버스, 출구 파싱
    global SearchBuilding, SearchExitNo
    SearchBuilding = FindBuilding(stationListId[select[0]])
    SearchExitNo = ExtractDictKey(SearchBuilding)

    # 선택된 지하철역 글자
    TEXT = stationList[stationListId[select[0]]]
    if TEXT[len(TEXT)-1:len(TEXT)] != "역":
        TEXT += "역"

    StationText = Label(RightWindow, text=TEXT, font=Subfont)
    StationText.place(x = 15 , y=50)

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

    BuildingList = Listbox(ListFrame, width= 43, height=13, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
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

def ShowBuildingList():
    BuildingList.config(state='normal')
    BuildingList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for Building in SearchBuilding[SearchExitNo[ExitNoVar.get()]]:
        BuildingList.insert(i, Building)
        i += 1

    BuildingList.config(state='disabled')


def ShowSchedule():
    SetRight()
    OpenRightWindow()

    # 시간표 위젯 만들기
    CreateScheduleWidget()
    
    # 모든 시간표 파싱
    global StationSchedule, HourList

    # 현재 선택된 지하철역
    select = StationListBox.curselection()

    for Dtype in ["평일", "토요일", "일요일"]:
        for UDtype in ["상행", "하행"]:
            StationSchedule[Dtype][UDIndex[UDtype]][UDtype] = FindSchedule(stationListId[select[0]], ScheduleText[Dtype], ScheduleText[UDtype])

    for Dtype in ["평일", "토요일", "일요일"]:
        for UDtype in ["상행", "하행"]:
            HourList[Dtype][UDIndex[UDtype]][UDtype] = ExtractDictKey_Int(StationSchedule[Dtype][UDIndex[UDtype]][UDtype])

    #ShowScheduleList()

def ShowScheduleList():
    global BuildingList, ExitNoVar

    BuildingList.config(state='normal')

    BuildingList.delete(0, END)  # 검색된 리스트 초기화

    i = 0
    for Building in SearchBuilding[SearchExitNo[ExitNoVar.get()]]:
        BuildingList.insert(i, Building)
        i += 1

    BuildingList.config(state='disabled')

def CreateScheduleWidget():
    # 현재 선택된 지하철역
    select = StationListBox.curselection()

    # 현재 선택된 지하철역 이름과 라인 구분
    TEXT = stationList[stationListId[select[0]]]
    if TEXT[len(TEXT) - 1:len(TEXT)] != "역":
        TEXT += "역" + " " + "[" + FindStationLine(stationListId[select[0]]) + "]"

    StationText = Label(RightWindow, text=TEXT, font=Subfont)
    StationText.place(x=15, y=50)

    # 그 외 글자들
    Text1 = Label(RightWindow, text="시간", font=Subfont)
    Text1.place(x=15, y=160)

    Text2 = Label(RightWindow, text="분", font=Subfont)
    Text2.place(x=200, y=160)

    # 시간표 검색타입 버튼
    global DailyTypeIntVar, UDTypeIntVar
    DailyTypeIntVar = IntVar()
    UDTypeIntVar = IntVar()

    WeekDay = Radiobutton(RightWindow, text = "평일", value = "01", variable=DailyTypeIntVar)
    WeekDay.place(x=30, y=80)
    Saturday = Radiobutton(RightWindow, text = "토요일", value = "02", variable=DailyTypeIntVar)
    Saturday.place(x=100, y=80)
    Sunday = Radiobutton(RightWindow, text = "일요일", value = "03", variable=DailyTypeIntVar)
    Sunday.place(x=170, y=80)

    Up = Radiobutton(RightWindow, text = "상행", value = "U", variable=UDTypeIntVar)
    Up.place(x=30, y=120)
    Down = Radiobutton(RightWindow, text = "하행", value = "D", variable=UDTypeIntVar)
    Down.place(x=100, y=120)

    # 검색결과 리스트
    global MinuteList
    ListFrame = Frame(RightWindow)

    scrollbar = Scrollbar(ListFrame)
    scrollbar.pack(side="right", fill="y")

    MinuteList = Listbox(ListFrame, width= 20, height=16, borderwidth=5, font = Listfont, yscrollcommand = scrollbar.set)
    MinuteList.pack()

    scrollbar.config(command=MinuteList.yview)
    ListFrame.place(x = 200, y = 200)

    # 시간 버튼들
    global HourIntVar
    HourIntVar = IntVar()

    x = y = 0
    for Hour in HourList[DailyTypeIntVar.get()][UDIndex[UDTypeIntVar.get()]][UDTypeIntVar.get()]:
        radio = Radiobutton(RightWindow, text=Hour, value=y*3 + x, variable=HourIntVar, command=ShowScheduleList)
        radio.place(x = 15 + x*20, y=180 + y*20)
        x+=1
        if x%3 == 0:
            y+=1
            x=0

# 함수 호출
CreateWindow()
SetRight()

MainWindow.mainloop()
