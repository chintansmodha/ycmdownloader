import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 770
i = 1
pageno = 0

divisioncode = []
Itemname = []
ShadeName = []
ShadeCode =  []
LotNo = []
Boxes = 0
Cops = 0
Gross = 0
Tare = 0
Netwt = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

def dvalue():
    global d
    d = d - 5
    return d

def dvalueincrease():
    global d
    d = d + 10
    return d

def SerialNo():
    global i
    i = i + 1
    return i

def SetSerialNo():
    global i
    i = 1
    return i

def header(stdt, etdt):
    # fonts(15)
    # c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 820, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 800, "Item Wise Production Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 800, "Page No." + str(p))
    c.line(0, 795, 600, 795)
    c.line(0, 775, 600, 775)
    # Upperline in header
    c.drawString(10, 780, "Item")
    c.drawString(250, 780, "Boxes")
    c.drawString(320, 780, "Cops")
    c.drawString(400, 780, "Gross Wt")
    c.drawString(480, 780, "Tare Wt")
    c.drawString(550, 780, "Net Wt")


def data(result, d):
    fonts(7)
    str1 = ''
    string = str1.join(result['PRODUCT'])
    res = sum(not chr.isspace() for chr in string)
    wrap_text = textwrap.wrap(string, width=50)
    # print(len(wrap_text))
    e = 0
    while e < len(wrap_text):
        c.drawString(11, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrease()
        f = f + 1
    # c.drawString(11, d, str(result['PRODUCT']))
    c.drawAlignedString(270, d, str(result['BOXES']))
    c.drawAlignedString(340, d, str(result['COPS']))
    c.drawAlignedString(420, d, str(result['GROSSWT']))
    c.drawAlignedString(500, d, str(result['TAREWT']))
    c.drawAlignedString(570, d, str(result['NETWT']))
    Total(result)
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1

def logic(result):
    global divisioncode
    divisioncode.append(result['COMPNAME'])

def newpage():
    global d
    d = 770
    return d

def newrequest():
    global divisioncode
    global pageno
    divisioncode = []
    pageno = 0

def Total(result):
    global Boxes, Cops, Gross
    global Tare, Netwt
    Boxes = Boxes + int(result['BOXES'])
    Cops = Cops + int(result['COPS'])
    Gross = Gross + float(result['GROSSWT'])
    Tare = Tare + float(result['TAREWT'])
    Netwt = Netwt + float(result['NETWT'])

def TotalClean():
    global Boxes, Cops, Gross
    global Tare, Netwt
    Boxes = 0
    Cops = 0
    Gross = 0
    Tare = 0
    Netwt = 0


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    # str('{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, etdt)
        data(result, d)

    else:
        data(result, d)

