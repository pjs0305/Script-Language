import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PASSWORD import password

def MakeBodyBus(ExitList, newdoc):
    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for ExitNo in ExitList:
        # create bold element
        E = newdoc.createElement('ExitNo')

        # create text node
        Exit = newdoc.createTextNode(ExitNo + "번 출구 :")
        E.appendChild(Exit)

        Text = ""

        for Bus in ExitList[ExitNo]:
            Text += str(Bus) + "번, "

        Text = Text[:len(Text)-2]

        BusNo = newdoc.createTextNode(Text)
        B = newdoc.createElement('BusNoList')
        B.appendChild(BusNo)
        E.appendChild(B)

        body.appendChild(E)

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')
        body.appendChild(br)

        br = newdoc.createElement('br')
        body.appendChild(br)

    return body

def MakeBodyBuild(ExitList, newdoc):
    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for ExitNo in ExitList:
        # create bold element
        E = newdoc.createElement('ExitNo')

        # create text node
        Exit = newdoc.createTextNode(ExitNo + "번 출구 : ")
        E.appendChild(Exit)

        Text = ""

        for Build in ExitList[ExitNo]:
            Text += Build + ", "

        Text = Text[:len(Text)-2]

        Building = newdoc.createTextNode(Text)
        B = newdoc.createElement('BuildingList')
        B.appendChild(Building)
        E.appendChild(B)

        body.appendChild(E)

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')
        body.appendChild(br)

        br = newdoc.createElement('br')
        body.appendChild(br)

    return body

def MakeBodySched(ScheduleInf, newdoc):
    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    # 평일 : [ 상행 : [ 시간 : [], 시간 : [] ], 하행 : [ 시간 : [], 시간 : [] ] ], 토요일 : [ ...
    for Daily in ScheduleInf: # for i in a:
        DayElement = newdoc.createElement('Day')

        # create text node
        Text = newdoc.createTextNode(Daily) # 평일
        DayElement.appendChild(Text)

        br = newdoc.createElement('br')
        DayElement.appendChild(br)
        # 평일 : [ 상행 : [ 시간 : [], 시간 : [] ], 하행 : [ 시간 : [], 시간 : [] ] ]
        for Day in ScheduleInf[Daily]: # for j in a[i]:
            # [ 상행 : [ 시간 : [], 시간 : [] ], 하행 : [ 시간 : [], 시간 : [] ] ]
            for UD in Day: # for k in j:
                UpDownElement = newdoc.createElement('UpDown')

                # create text node
                Text = newdoc.createTextNode(UD) # 상행
                UpDownElement.appendChild(Text)

                DayElement.appendChild(UpDownElement)

                br = newdoc.createElement('br')
                DayElement.appendChild(br)

                # [ 시간 : [분, 분, 분], 시간 : [분, 분, 분] ]
                for Hour in Day[UD]:   # for l in j[k]
                    TimeElement = newdoc.createElement('Times')

                    # create text node
                    Text = Hour + "시 :"
                    for Minuit in Day[UD][Hour]: # for m in j[k][l]
                        Text += " " + Minuit + "분"

                    TimeNode = newdoc.createTextNode(Text)  # 상행
                    TimeElement.appendChild(TimeNode)

                    DayElement.appendChild(TimeElement)

                    br = newdoc.createElement('br')
                    TimeElement.appendChild(br)

                br = newdoc.createElement('br')
                DayElement.appendChild(br)

        body.appendChild(DayElement)

        br = newdoc.createElement('br')
        body.appendChild(br)
        br = newdoc.createElement('br')
        body.appendChild(br)

    return body

def MakeHTML(MakeBody, List):
    from xml.dom.minidom import getDOMImplementation

    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # append Body
    top_element.appendChild(MakeBody(List, newdoc))

    return newdoc.toxml()

def SendData(mail, title, MakeBody, DataList):
    #global value
    host = "smtp.gmail.com" # Gmail STMP 서버 주소.
    port = "587"

    senderAddr = "w3sw3s74@gmail.com"# 보내는 사람 email 주소.
    recipientAddr = mail   	# 받는 사람 email 주소.

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    html = MakeHTML(MakeBody, DataList)
    DataPart = MIMEText(html, 'html', _charset='UTF-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(DataPart)

    # 메일을 발송한다.
    s = smtplib.SMTP(host,port)
    #s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("w3sw3s74@gmail.com",password)
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()

