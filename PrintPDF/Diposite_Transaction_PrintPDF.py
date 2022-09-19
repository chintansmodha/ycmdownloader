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
AgentName=[]
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
    try:
        CompanyName.append(result['COMPANYNAME'])
    except:
        print("problem in appending company name")
    try:
        AgentName.append(result['AGENTNAME'])
    except:
        print("problem in appending agent name ")

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


def textsizeYes(c, result,d, stdt, etdt):
    d = dvalue()
    logic(result)
    if d< 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt)

    if len(AgentName)==1:
        header(stdt, etdt)
        data(result, d)
    else:
        data(result,d)


def textsizeNo(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    if d < 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt)
    if len(CompanyName) == 1:
        header(stdt, etdt)
        fonts(12)
        d=dvalue()
        c.drawString(10, d, result['COMPANYNAME'])
        d=dvalue()
        fonts(9)
        data(result, d)
    elif CompanyName[-1] == CompanyName[-2]:
        data(result, d)
    elif CompanyName[-1] != CompanyName[-2]:
        printotalconsolidation()
        d=dvalue()
        fonts(12)
        d=dvalue()
        c.drawString(10,d,result['COMPANYNAME'])
        fonts(9)
        d=dvalue()
        data(result, d)


def header(stdt, etdt):
    now = datetime.datetime.now()
    print("Date: " + now.strftime("%Y-%m-%d"))  # this will print **2018-02-01** that is todays date
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(300, 800, CompanyName[-1])
    c.drawCentredString(300, 800, "Beekaylon Group of Companies")
    fonts(9)
    c.drawCentredString(300, 785,
                        "Agent Wise Consolidated Collection From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    c.drawString(10, 780, str(now.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 777, 600, 777)
    # Upperline in header
    c.drawString(10, 755, "Broker")
    c.drawString(400, 755, "Amount")
    c.drawString(500, 755, "Represented")
    c.line(0, 750, 600, 750)


def data(result, d):
    fonts(9)
    c.drawString(10, d, result['AGENTNAME'])
    # c.drawAlignedString(430, d, result['AMOUNT'])
    c.drawAlignedString(430, d, str(format_currency("%.2f" % float(result['AMOUNT']), '', locale='en_IN')))
    c.drawString(550, d, "--")
    total(result)


def total(result):
    global totalbrokeramount
    global grandtotal
    grandtotal = grandtotal + (float("%.2f" % float(result['AMOUNT'])))
    totalbrokeramount = totalbrokeramount + (float("%.2f" % float(result['AMOUNT'])))

def printotalconsolidation():
    global totalbrokeramount
    global grandtotal
    d=dvalue()
    c.drawAlignedString(430, d, " Consolidated Total : "+str(format_currency("%.2f" % float(totalbrokeramount), '', locale='en_IN')))
    totalbrokeramount=0

def printtotalnoconsolidation():
    global totalbrokeramount
    global grandtotal
    d = dvalue()
    c.drawAlignedString(430, d, " Consolidated Total : " + str(
        format_currency("%.2f" % float(totalbrokeramount), '', locale='en_IN')))
    totalbrokeramount = 0
