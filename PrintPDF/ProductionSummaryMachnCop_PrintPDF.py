import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 740
i = 1
pageno = 0

divisioncode = []
Department = []
ShadeName = []
ShadeCode =  []
LotNo = []
Boxes = 0
Cops = 0
NetWt = 0
avgNEtwtCtn = 0
avgNEtwtTube = 0
COPS = []
BOX = []
QUANTITY = []

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

def dvalueincrese():
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

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Machine/Cops Wise Production Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header
    c.drawString(10, 760, "Tubes Item")
    c.drawString(350, 760, "No. Of Ctns")
    c.drawString(420, 760, "Net Qty")
    c.drawString(480, 760, "Avg. Wt")
    c.drawString(480, 750, "Per Ctn.")
    c.drawString(540, 760, "Avg. Wt")
    c.drawString(540, 750, "Per Tube")


def data(result, d):
    fonts(7)
    global avgNEtwtCtn, avgNEtwtTube
    global COPS, BOX, QUANTITY
    str1 = ''
    string = str1.join(result['PRODUCT'])
    res = sum(not chr.isspace() for chr in string)
    wrap_text = textwrap.wrap(string, width=75)
    # print(len(wrap_text))
    e = 0
    while e < len(wrap_text):
        c.drawString(11, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(11, d, str(result['PRODUCT']))
    c.drawAlignedString(370, d, str(result['BOXES']))
    c.drawAlignedString(440, d, str(result['NETWT']))
    avgwtperctn = 0
    if int(result['BOXES']) != 0:
        avgwtperctn = ((float(result['NETWT']))/(int(result['BOXES'])))
        c.drawAlignedString(500, d, str('{0:1.3f}'.format(avgwtperctn)))
        avgNEtwtCtn = avgNEtwtCtn + avgwtperctn
    else:
        c.drawAlignedString(500, d, '0.000')
    if int(result['COPS']) != 0:
        avgwtpertube = ((avgwtperctn)/(int(result['COPS'])))
        c.drawAlignedString(560, d, str('{0:1.3f}'.format(avgwtpertube)))
        avgNEtwtTube = avgNEtwtTube + avgwtpertube
    else:
        c.drawAlignedString(560, d, '0.000')
    ItemTotal(result)
    COPS.append(result['COPS'])
    BOX.append(result['BOXES'])
    QUANTITY.append(result['NETWT'])
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1


def logic(result):
    global divisioncode
    global Department
    divisioncode.append(result['COMPNAME'])
    Department.append(result['DEPARTMENT'])

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode
    global Department
    global pageno
    divisioncode = []
    Department = []
    pageno = 0

def ItemTotal(result):
    global Boxes, NetWt, Cops
    Boxes = Boxes + int(result['BOXES'])
    NetWt = NetWt + float(result['NETWT'])
    Cops = Cops + int(result['COPS'])

def Clean():
    global avgNEtwtCtn, avgNEtwtTube
    global Boxes, NetWt, Cops
    global COPS, BOX, QUANTITY
    avgNEtwtTube = avgNEtwtCtn = 0
    Boxes = NetWt = Cops = 0
    BOX = []
    COPS = []
    QUANTITY = []


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    global COPS, BOX, QUANTITY
    # str('{0:1.3f}'.format())

    if len(divisioncode) == 1:
        Clean()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(10, d, Department[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            data(result, d)
        else:
            boldfonts(7)
            c.drawAlignedString(370, d, str(Boxes))
            c.drawAlignedString(440, d, str('{0:1.3f}'.format(NetWt)))
            c.drawAlignedString(500, d, str('{0:1.3f}'.format(avgNEtwtCtn)))
            c.drawAlignedString(560, d, str('{0:1.3f}'.format(avgNEtwtTube)))
            d = dvalue()
            d = dvalue()
            c.line(50, d, 400, d)
            d = dvalue()
            d = dvalue()
            c.drawString(60, d, "Cops")
            c.drawString(150, d, "Boxes")
            c.drawString(300, d, "Quantity")
            d = dvalue()
            c.line(50, d, 400, d)
            d = dvalue()
            d = dvalue()
            i = 0
            while i < len(COPS):
                fonts(7)
                c.drawAlignedString(75, d, str(COPS[i]))
                c.drawAlignedString(170, d, str(BOX[i]))
                c.drawAlignedString(320, d, str(QUANTITY[i]))
                d = dvalue()
                d = dvalue()
                i = i + 1
            boldfonts(7)
            c.line(50, d, 400, d)
            d = dvalue()
            d = dvalue()
            c.drawAlignedString(75, d, str(Cops))
            c.drawAlignedString(170, d, str(Boxes))
            c.drawAlignedString(320, d, str('{0:1.3f}'.format(NetWt)))
            d = dvalue()
            c.line(50, d, 400, d)
            Clean()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, Department[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.drawAlignedString(370, d, str(Boxes))
        c.drawAlignedString(440, d, str('{0:1.3f}'.format(NetWt)))
        c.drawAlignedString(500, d, str('{0:1.3f}'.format(avgNEtwtCtn)))
        c.drawAlignedString(560, d, str('{0:1.3f}'.format(avgNEtwtTube)))
        d = dvalue()
        d = dvalue()
        c.line(50, d, 400, d)
        d = dvalue()
        d = dvalue()
        c.drawString(60, d, "Cops")
        c.drawString(150, d, "Boxes")
        c.drawString(300, d, "Quantity")
        d = dvalue()
        c.line(50, d, 400, d)
        d = dvalue()
        d = dvalue()
        i = 0
        while i < len(COPS):
            fonts(7)
            c.drawAlignedString(75, d, str(COPS[i]))
            c.drawAlignedString(170, d, str(BOX[i]))
            c.drawAlignedString(320, d, str(QUANTITY[i]))
            d = dvalue()
            d = dvalue()
            i = i + 1
        boldfonts(7)
        c.line(50, d, 400, d)
        d = dvalue()
        d = dvalue()
        c.drawAlignedString(75, d, str(Cops))
        c.drawAlignedString(170, d, str(Boxes))
        c.drawAlignedString(320, d, str('{0:1.3f}'.format(NetWt)))
        d = dvalue()
        c.line(50, d, 400, d)
        fonts(7)
        Clean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(10, d, Department[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

