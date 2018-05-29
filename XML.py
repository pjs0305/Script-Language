from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
import urllib.parse
import urllib.request

client_key = "serviceKey=QCt6OJN%2BX%2BK%2F1QWhl3xAV6wrYByNl7oLDFyYobuvd%2FXsKryONWzAm0FH9zbTDU0syJHEkFxCHE31CKqoCcUIKg%3D%3D"
keymenu = ["subwayStationName", "subwayStationId", "dailyTypeCode", "upDownTypeCode"]
DayList = { "01" : "평일", "02" : "토요일", "03" : "일요일" }
UpDown = { "U" : "상행", "D" : "하행" }

def LoadXML(search, key, **data):
    s = "http://openapi.tago.go.kr/openapi/service/SubwayInfoService/" + search + "?" + key + "&"

    for d in data.keys():
        s += d + "=" + data[d] + "&"

    s += "numOfRows=1000"
    request = urllib.request.Request(s)
    response = urllib.request.urlopen(request)
    response_body = response.read()
    dom = parseString(response_body)

    return (ElementTree.fromstring(dom.toxml()))

# 역 검색
def FindStation(text):
    encText = urllib.parse.quote(text)

    tree = LoadXML("getKwrdFndSubwaySttnList", client_key, subwayStationName=encText)
    itemElements = tree.getiterator("item") # tree 내의 item만 뽑아오기

    searchList = {} # 검색된 지하철역과 ID를 저장할 사전

    index = 0
    for item in itemElements:
        searchList[item.find("subwayStationId").text] = item.find("subwayStationName").text
        index+=1

    PrintDict(searchList)

    return searchList

def FindStationLine(ID): # 지하철역 ID에 따라 라인 구분
    LineId = ID[3:]

    Line = ""
    # 100 ~ 999
    if len(LineId) == 3:
         # 100 ~ 199
        if LineId[0] == '1':
            # 100 ~ 189
            if LineId[1] != '9':
                Line = LineId[0] + "호선"
            # 190 ~ 199
            else:
                # 190
                if LineId[2] == '0':
                    Line = LineId[0] + "호선"
                # 191 ~ 199
                else:
                    Line = "경의중앙선"
        # 200 ~ 999
        else:
            Line = LineId[0] + "호선"
    # 1000 ~ 9999
    elif len(LineId) == 4:
        # 1000 ~ 1999
        if LineId[0] == '1':
            # 1100 ~ 1199
            if LineId[1] == '1':
                Line = "1호선"
            # 1200 ~ 1399
            elif '2' <= LineId[1] <= '3':
                Line = "경의중앙선"
            # 1400 ~ 1499
            elif LineId[1] == '4':
                Line = "1호선"
            # 1500 ~ 1599
            elif LineId[1] == '5':
                Line = "분당선"
            # 1600 ~ 1699
            elif LineId[1] == '6':
                Line = "경의중앙선"
            # 1700 ~ 1799
            elif LineId[1] == '7':
                Line = "에버라인"
            # 1800 ~ 1899
            elif LineId[1] == '8':
                Line = "경춘선"
            # 1900 ~ 1999
            elif LineId[1] == '9':
                Line = "신분당선"
        # 4000 ~ 4999
        elif LineId[0] == '4':
            # 4000 ~ 4099
            if LineId[1] == '0':
                Line = "공항철도"
            # 4100 ~ 4199
            elif LineId[1] == '1':
                Line = "자기부상철도"
    # 10000 ~ 99999
    elif len(LineId) == 5:
        # 10000 ~ 19999
        if LineId[0] == '1':
            # 11000 ~ 11099
            if LineId[2] == '0':
                Line = "의정부경전철"
            # 11100 ~ 11199
            elif LineId[2] == '1':
                Line = "수인선"
            # 11200 ~ 11299
            elif LineId[2] == '2':
                Line = "경강선"
            # 11300 ~ 11399
            elif LineId[2] == '3':
                Line = "우이신설선"
        # 20000 ~ 29999
        elif LineId[0] == '2':
            # 20100 ~ 20199
            if LineId[2] == '1':
                Line = "인천1호선"
            # 20200 ~ 20299
            elif LineId[2] == '2':
                Line = "인천2호선"
        # 30000 ~ 39999
        elif LineId[0] == '3':
            Line = "대전1호선"
        # 40000 ~ 49999
        elif LineId[0] == '4':
            # 40100 ~ 40199
            if LineId[2] == '1':
                Line = "대구1호선"
            # 40200 ~ 40299
            elif LineId[2] == '2':
                Line = "대구2호선"
            # 40300 ~ 40399
            elif LineId[2] == '3':
                Line = "대구3호선"
        # 50000 ~ 59999
        elif LineId[0] == '5':
            Line = "광주1호선"
        # 70000 ~ 79999
        elif LineId[0] == '7':
            # 70000 ~ 70199
            if '0' <= LineId[2] < '2':
                Line = "부산1호선"
            # 70200 ~ 70299
            elif LineId[2] == '2':
                Line = "부산2호선"
            # 70300 ~ 70399
            elif LineId[2] == '3':
                Line = "부산3호선"
            # 70400 ~ 70499
            elif LineId[2] == '4':
                Line = "부산4호선"
            # 70800 ~ 70899
            elif LineId[2] == '8':
                Line = "부산동해선"
            # 70900 ~ 70999
            elif LineId[2] == '9':
                Line = "부산김해경전철"

    return Line

# 버스 조회
def FindBus(ID):
    encID = urllib.parse.quote(ID)
    tree = LoadXML("getSubwaySttnExitAcctoBusRouteList", client_key, subwayStationId=encID)

    itemElements = tree.getiterator("item")

    searchBus = {}

    for item in itemElements:
        if item.find("exitNo").text not in searchBus:
            searchBus[item.find("exitNo").text] = []
        searchBus[item.find("exitNo").text].append(item.find("busRouteNo").text)

    PrintDict(searchBus)
    return searchBus

# 건물 조회
def FindBuilding(ID):
    encID = urllib.parse.quote(ID)
    tree = LoadXML("getSubwaySttnExitAcctoCfrFcltyList", client_key, subwayStationId=encID)

    itemElements = tree.getiterator("item")

    searchBuilding = {}

    for item in itemElements:
        if item.find("exitNo").text not in searchBuilding:
            searchBuilding[item.find("exitNo").text] = []
        searchBuilding[item.find("exitNo").text].append(item.find("dirDesc").text)

    PrintDict(searchBuilding)
    return searchBuilding

# 시간표 조회
def FindSchedule(ID, DayType, UDType):
    encID = urllib.parse.quote(ID)
    encDay = urllib.parse.quote(DayType)
    encUD = urllib.parse.quote(UDType)

    tree = LoadXML("getSubwaySttnAcctoSchdulList", client_key, subwayStationId=encID, dailyTypeCode=encDay, upDownTypeCode=encUD)
    itemElements = tree.getiterator("arrTime")

    HourList = {}

    for time in itemElements:
        if time.text[:2] not in HourList:
            HourList[time.text[:2]] = []
        HourList[time.text[:2]].append(time.text[2:4])

    PrintDict(HourList)

    return HourList

# 사전 키값 리스트로 뽑아내기
def ExtractDictKey(Dict): # 사전의 키값들만 리스트로 뽑아내는 함수
    KeyList = []

    for i in Dict.keys():
        KeyList.append(i)

    return KeyList

# 사전 출력
def PrintDict(Dict):
    for i in Dict:
        print(i, " : ", Dict[i])