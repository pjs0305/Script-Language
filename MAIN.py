import GUI

# 윈도우창
MainWindow = Tk()

# 윈도우창 내부 분할 창
LeftWindow = Frame(MainWindow, relief="solid", bd=1)
RightWindow = Frame(MainWindow, relief="solid", bd=1)

# 윈도우창 펼칠지 안펼칠지 판단하는 변수
Open = False

# 글자 폰트들
Titlefont = font.Font(size=20, weight='bold', family='굴림')
Mainfont = font.Font(size=16, weight='bold', family='굴림')
Subfont = font.Font(size=13, family='굴림')
Listfont = font.Font(size=12, family='굴림')

stationList = {} # 검색된 지하철역 ( ID : 이름 )
stationListId = [] # 검색된 지하철역 ID 리스트

SearchBus = {} # 검색된 지하철역 주변 버스 ( ExitNo : BusNo )
SearchBuilding = {} # 검색된 지하철역 주변 건물 ( ExitNo : BuildingName )
SearchExitNo = [] # 검색된 지하철역 출구 번호 리스트

# 함수 호출
CreateWindow()
SetRight()

MainWindow.mainloop()