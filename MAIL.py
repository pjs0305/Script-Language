import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PASSWORD import password

def MakeHTMLBusInf(ExitList):
    from xml.dom.minidom import getDOMImplementation

    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for ExitNo in ExitList:
        # create bold element
        E = newdoc.createElement('ExitNo')

        # create text node
        Exit = newdoc.createTextNode(ExitNo + "번 출구 : ")
        E.appendChild(Exit)

        for Bus in ExitList[ExitNo]:
            B = newdoc.createElement('BusNo')
            BusNo = newdoc.createTextNode(str(Bus) + "번 ")
            B.appendChild(BusNo)
            E.appendChild(B)

        body.appendChild(E)

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

    # append Body
    top_element.appendChild(body)

    return newdoc.toxml()

D = { "11" : [1,2,3,4,5], "22" : [6,7,8,9,10]}

def SendData(mail, title, MakeHTML, DataList):
    #global value
    host = "smtp.gmail.com" # Gmail STMP 서버 주소.
    port = "587"
    html = ""

    senderAddr = "w3sw3s74@gmail.com"# 보내는 사람 email 주소.
    recipientAddr = mail   	# 받는 사람 email 주소.

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    html = MakeHTML(DataList)
    DataPart = MIMEText(html, 'html', _charset='UTF-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(DataPart)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("w3sw3s74@gmail.com",password)
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
