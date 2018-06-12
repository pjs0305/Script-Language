from XML import *
import time
import telepot

MAX_MSG_LENGTH = 300

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '알 수 없는 명령입니다.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('검색') and len(args)>1:
        replyStationData(args[1], chat_id)
    elif text.startswith('버스') and len(args)>1:
        replyBusData(args[1], chat_id)
    elif text.startswith('건물') and len(args)>1:
        replyBuildData(args[1], chat_id)
    elif text.startswith('시간표') and len(args)>3:
        replySchedData(args[1], chat_id, args[2], args[3])
    else:
        sendMessage(chat_id, """모르는 명령어 입니다.\n검색 [이름]\n버스 [지하철역 ID]\n건물 [지하철역 ID]\n시간표 [지하철역 ID] [요일(평일, 토요일, 일요일)] [상하행(상행, 하행)]\n지하철역 ID는 검색을 통해 알 수 있습니다.""")

def replyStationData(date_param, user):
    StationList = FindStation(date_param)
    msg = ''
    for Station in StationList:
        text = StationList[Station] + " [" + FindStationLine(Station)+ "]" + " : " + Station

        if len(text+msg)+1>MAX_MSG_LENGTH:
            sendMessage( user, msg )
            msg = text + '\n'
        else:
            msg += text +'\n'

    if msg:
        sendMessage( user, msg )
    else:
        sendMessage( user, '해당 글자가 들어간 지하철역이 없습니다.')

def replyBusData(date_param, user):
    BusList = FindBus(date_param)
    ExitList = ExtractDictKey(BusList)

    msg = ''
    for ExitNo in ExitList:
        msg = ExitNo + "번 출구 : "
        for Bus in BusList[ExitNo]:
            Bustext = Bus + "번, "

            if len(Bustext+msg)+1>MAX_MSG_LENGTH:
                sendMessage( user, msg )
                msg = Bustext
            else:
                msg += Bustext
        msg = msg[:len(msg)-2]
        sendMessage( user, msg )

    if len(msg) == 0:
        sendMessage( user, '해당 지하철역 주변에 버스가 없습니다.')

def replyBuildData(date_param, user):
    BuildList = FindBuilding(date_param)
    ExitList = ExtractDictKey(BuildList)

    msg = ''
    for ExitNo in ExitList:
        msg = ExitNo + "번 출구 : "
        for Build in BuildList[ExitNo]:
            Btext = Build+ ", "

            if len(Btext+msg)+1>MAX_MSG_LENGTH:
                sendMessage( user, msg )
                msg = Btext
            else:
                msg += Btext
        msg = msg[:len(msg)-2]
        sendMessage( user, msg )

    if len(msg) == 0:
        sendMessage( user, '해당 지하철역 주변에 건물이 없거나 지하철역 ID가 잘못되었습니다.')

def replySchedData(date_param, user, day, UD):
    if day not in DayList or UD not in UpDown:
        sendMessage( user, '입력이 잘못되었습니다.')
        return

    SchduleList = FindSchedule(date_param, DayList[day], UpDown[UD])
    HourList = ExtractDictKey(SchduleList)

    msg = ''
    for Hour in HourList:
        msg = Hour + "시 : "
        for Minute in SchduleList[Hour]:
            Mtext = Minute+ "분, "

            if len(Mtext+msg)+1>MAX_MSG_LENGTH:
                sendMessage( user, msg )
                msg = Mtext
            else:
                msg += Mtext

        msg = msg[:len(msg)-2]
        sendMessage( user, msg )

    if len(msg) == 0:
        sendMessage( user, '지하철역 ID가 잘못되었습니다.')

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

bot = telepot.Bot('556167059:AAGwkquuOsnelB4DHYyrgg8_8N-DdHo64J0')
bot.getMe()
bot.message_loop(handle)
print('Listening...')
while 1:
  time.sleep(10)