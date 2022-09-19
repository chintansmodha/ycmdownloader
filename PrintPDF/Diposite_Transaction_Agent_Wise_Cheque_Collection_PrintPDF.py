import datetime

from babel.numbers import format_currency
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
d = 750
CompanyName = []
BrokerGroupName=[]
AgentName=[]

serialno=0
pageno = 0
totalbrokeramount = 0
grandtotal=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue():
    global d
    d = d - 10
    return d

def logic(result):
    CompanyName.append(result['COMPANYNAME'])
    BrokerGroupName.append(result['BROKERGROUPNAME'])
    AgentName.append(result['AGENTNAME'])

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global CompanyName
    global pageno
    global totalbrokeramount
    global grandtotal
    CompanyName = []
    pageno = 0
    totalbrokeramount=0
    grandtotal=0


def textsizeBoth(c, result,d, stdt, etdt):
    # print("from text size")
    global serialno
    d = dvalue()
    logic(result)
    if d< 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt, CompanyName)
        # printbroker(result,d)
        # printagentname(result,d)
    # printbroker(result,d)
    # d=dvalue()
    # printagentname(result,d)
    # d=dvalue()
    # printcompanyname(result,d)
    # d=dvalue()
    # data(result,d)

    # if len(CompanyName)==1:
    if len(BrokerGroupName)==1:
        header(stdt, etdt, CompanyName)
        printbroker(result,d)
        d=dvalue()
        printagentname(result,d)
        d=dvalue()
        printcompanyname(result,d)
        d=dvalue()
        data(result,d)
    elif BrokerGroupName[-2]==BrokerGroupName[-1]:
        # printbroker(result,d)
        data(result,d)
    elif BrokerGroupName[-2]!=BrokerGroupName[-1]:
        printbroker(result, d)
        d = dvalue()
        printagentname(result, d)
        d = dvalue()
        printcompanyname(result, d)
        d = dvalue()
        serialno=0
        data(result, d)
        # printbroker(result,d)
        # printagentname(result, d)
        # data(result, d)
    # else:
    #     data(result,d)

def textsizeAdjusted(c, result,d, stdt, etdt):
    pass

def textsizeUnAdjusted(c, result,d, stdt, etdt):
    pass


def textsizeNo(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    if d < 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt, CompanyName)

    if len(CompanyName) == 1:
        header(stdt, etdt, CompanyName)
        fonts(12)
        d=dvalue()
        c.drawString(10, d, result['COMPANYNAME'])
        d=dvalue()
        fonts(9)
        data(result, d)
    elif CompanyName[-1] == CompanyName[-2]:
        data(result, d)
    elif CompanyName[-1] != CompanyName[-2]:
        printotal()
        d=dvalue()
        fonts(12)
        d=dvalue()
        c.drawString(10,d,result['COMPANYNAME'])
        fonts(9)
        d=dvalue()
        data(result, d)


def header(stdt, etdt, CompanyName):
    now = datetime.datetime.now()
    print("Date: " + now.strftime("%Y-%m-%d"))  # this will print **2018-02-01** that is todays date
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(300, 800, CompanyName[-1])
    c.drawCentredString(300, 800, "Beekaylon Group of Companies")
    fonts(9)
    c.drawCentredString(300, 785,
                        "Agent Wise Consolidated Adjusted / UnAdjusted Cheque Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    c.drawString(10, 780, str(now.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 777, 600, 777)
    # Upperline in header
    c.drawString(10, 765, "Sr No.")
    c.drawString(40, 765, "Chq No.")
    c.drawString(90, 765, "Chq Dt.")
    c.drawString(140, 765, "Vch Dt")
    c.drawString(190, 765, "Drawee Name")
    c.drawString(280, 765, "Paty Bank")
    c.drawString(480, 765, "Receipt")
    c.drawString(540, 765, "Payment")
    c.line(0, 750, 600, 750)


def data(result, d):
    global serialno
    fonts(9)
    serialno=serialno+1
    # d=dvalue()
    # c.drawString(10, d, result['AGENTNAME'])
    # c.drawAlignedString(430, d, result['AMOUNT'])
    c.drawAlignedString(30, d, str(serialno))
    c.drawString(40, d, "cheque no.")
    c.drawString(90, d, "cheque dt")
    c.drawString(140, d, result['VOUCHERDATE'])
    c.drawString(190, d, "Drawee Name")
    c.drawString(280, d, "Paty Bank")
    c.drawAlignedString(500, d, str(format_currency("%.2f" % float(result['AMOUNT']), '', locale='en_IN')))
    c.drawString(550, d, "--") #Payment
    total(result)

def printcompanyname(result,d):
    c.drawString(10, d, result['COMPANYNAME'])
    # d=dvalue()

def printagentname(result,d):
    c.drawString(10, d, result['AGENTNAME'])
    # d=dvalue()

def printbroker(result,d):
    c.drawCentredString(300,d,result['BROKERGROUPNAME'])
    # d=dvalue()

def total(result):
    global totalbrokeramount
    global grandtotal
    grandtotal = grandtotal + (float("%.2f" % float(result['AMOUNT'])))
    totalbrokeramount = totalbrokeramount + (float("%.2f" % float(result['AMOUNT'])))

def printotal():
    global totalbrokeramount
    global grandtotal
    d=dvalue()
    # c.drawAlignedString(430,d,"Total : "+str(totalbrokeramount))
    # c.drawAlignedString(430,d-10,"Grand Total : "+str(grandtotal))
    c.drawAlignedString(430, d, "Total : "+str(format_currency("%.2f" % float(totalbrokeramount), '', locale='en_IN')))
    c.drawAlignedString(430, d-10, "Grand Total : "+str(format_currency("%.2f" % float(grandtotal), '', locale='en_IN')))
    totalbrokeramount=0