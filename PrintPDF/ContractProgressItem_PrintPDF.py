import textwrap
from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))
d = 735
i = 1
y = 0
s = 1
k = 0
pageno = 0

divisioncode = []
Party = []
Broker  = []
Item = []
ItemTyp = []
ContNo = []
Shade = []
OrdNo = []
OrdQty = []

ConOrdQty = 0
ConChalQty = 0

BroOrdQty = 0
BroChalQty = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def dvalueset():
    global d
    d = 490
    return d

def SetDvalue():
    global d
    d = 0
    return d

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

def dvalues(stdt,etdt, divisioncode):
    global d
    if d > 20:
        d = d - 5
        return d
    else:
        c.setPageSize(landscape(A3))
        c.showPage()
        d = newpage()
        header(stdt,etdt, divisioncode)
        return d


def dvalueincrese():
    global d
    d = d + 10
    return d

def header(stdt,etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(600, 800, divisioncode[-1])
    fonts(9)
    # c.drawString(10, 550, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(600, 785, "Contract Progress Report (Item Wise) From  " + str(stdt.strftime(' %d  %B  %Y')) +
                        "  To  " + str(etdt.strftime(' %d  %B  %Y')))
    p = page()
    c.drawString(1000, 785, "Page No." + str(p))
    c.line(0, 775, 1200, 775)
    c.line(0, 745, 1200, 745)
    fonts(9)
    # Upperline in header
    c.drawString(10, 755, "Cont No.")
    c.drawString(80, 755, "Cont.Dt.")
    c.drawString(150, 755, "Broker")
    c.drawString(300, 755, "CntQty")
    c.drawString(370, 755, "CntRate")
    c.drawString(440, 755, "ContPndQty")
    c.drawString(500, 755, "CntSta")
    c.drawString(550, 755, "OrdNo.")
    c.drawString(600, 755, "OrdDt")
    c.drawString(675, 755, "Shade")
    c.drawString(775, 755, "Lot No.")
    c.drawString(830, 755, "Ord Stat")
    c.drawString(870, 755, "OrdQty")
    c.drawString(930, 755, "OrdPndQty")
    c.drawString(990, 755, "Chal. No.")
    c.drawString(1040, 755, "Chal Dt")
    c.drawString(1100, 755, "Ch. Lot")
    c.drawString(1150, 755, "Ch. Qty")

def data(result, d, stdt,etdt, divisioncode):
    fonts(7)
    if result['CONTNO'] != None:
        c.drawString(10, d, result['CONTNO'])
    if result['CONTDT'] != None:
        c.drawString(75, d, str(result['CONTDT'].strftime('%d-%m-%Y')))
    if result['BROKER'] != None:
        c.drawString(145, d, str(result['BROKER']))
    if result['CONTQTY'] != None:
        c.drawAlignedString(315, d, str(result['CONTQTY']))
    if result['CONTRACTRATE'] != None:
        c.drawAlignedString(385, d, str(result['CONTRACTRATE']))
    if result['CONTPENDQTY'] != None:
        c.drawAlignedString(460, d, str(result['CONTPENDQTY']))
    if result['CONTSTATUS'] != None:
        c.drawString(500, d, str(result['CONTSTATUS']))
    if result['ORDNO'] != None:
        c.drawString(550, d, str(result['ORDNO']))
    if result['ORDDT'] != None:
        c.drawString(600, d, str(result['ORDDT'].strftime('%d-%m-%Y')))
    if result['ORDSTATUS'] != None:
        c.drawString(830, d, str(result['ORDSTATUS']))
    if result['ORDQTY'] != None:
        c.drawAlignedString(885, d, str(result['ORDQTY']))
    if result['ORDPNDQTY'] != None:
        c.drawAlignedString(945, d, str(result['ORDPNDQTY']))
    if result['CHALNO'] != None:
        c.drawString(990, d, str(result['CHALNO']))
    if result['CHALDT'] != None:
        c.drawString(1040, d, str(result['CHALDT'].strftime('%d-%m-%Y')))
    if result['CHALLOT'] != None:
        c.drawString(1100, d, str(result['CHALLOT']))
    if result['CHALQTY'] != None:
        c.drawAlignedString(1165, d, str(result['CHALQTY']))
    if result['SHADE'] != None:
        if len(str(result['SHADE'])) > 25:
            lines = textwrap.wrap(str(result['SHADE']), 25, break_long_words=False)
            for i in lines:
                c.drawString(672, d, str(i))
                d = dvalues(stdt,etdt, divisioncode)
                d = dvalues(stdt, etdt, divisioncode)
        else:
            c.drawString(672, d, str(result['SHADE']))
    despatchTotal(result,d)


def logic(result):
    global divisioncode, Party, Broker, Item, ItemTyp
    global ContNo, Shade, OrdNo, OrdQty
    divisioncode.append(result['COMPANY'])
    Broker.append(str(result['BROKER']))
    Item.append(str(result['ITEM']))
    # ContNo.append(str(result['CONTNO']))
    # Shade.append(str(result['SHADE']))
    # OrdNo.append(str(result['ORDNO']))
    # OrdQty.append(str(result['ORDQTY']))

def newpage():
    global d
    d = 735
    return d

def newrequest():
    global divisioncode, Party, Broker, Item, ItemTyp
    global ContNo, Shade, y, OrdNo, OrdQty
    global pageno
    divisioncode = []
    Party = []
    Broker  = []
    Item = []
    ItemTyp = []
    ContNo = []
    Shade = []
    y = 0
    OrdNo = []
    OrdQty = []
    pageno = 0

def despatchTotal(result,d):
    global ConChalQty
    if result['CHALQTY'] != None:
        ConChalQty = ConChalQty + float(result['CHALQTY'])

def PrintTotalDespatch(c, result, d, stdt,etdt):
    global ConChalQty
    boldfonts(7)
    if int(ConChalQty) != 0:
        c.drawString(1040, d, 'Total Despatch : ')
        c.drawAlignedString(1165, d, str('{0:1.3f}'.format(ConChalQty)))
    ConChalQty = 0
    fonts(7)

def textsize(c, result, d, stdt,etdt):
    d = dvalues(stdt,etdt, divisioncode)
    logic(result)
    global y, s, k
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt,etdt, divisioncode)
        boldfonts(8)
        c.drawString(10, d, Item[-1])
        d = dvalues(stdt,etdt, divisioncode)
        d = dvalues(stdt,etdt, divisioncode)
        d = dvalues(stdt,etdt, divisioncode)
        data(result, d, stdt,etdt, divisioncode)

    elif divisioncode[-1] == divisioncode[-2]:
        if Item[-1] == Item[-2]:
            data(result, d, stdt,etdt, divisioncode)

        elif Item[-1] != Item[-2] :
            PrintTotalDespatch(c, result, d, stdt, etdt)
            d = dvalues(stdt,etdt, divisioncode)
            d = dvalues(stdt,etdt, divisioncode)
            boldfonts(8)
            c.drawString(10, d, Item[-1])
            d = dvalues(stdt, etdt, divisioncode)
            d = dvalues(stdt, etdt, divisioncode)
            d = dvalues(stdt, etdt, divisioncode)
            data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] != divisioncode[-2]:
        PrintTotalDespatch(c,result,d,stdt,etdt)
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode)
        d = dvalues(stdt, etdt, divisioncode)
        boldfonts(8)
        c.drawString(10, d, Item[-1])
        d = dvalues(stdt, etdt, divisioncode)
        d = dvalues(stdt, etdt, divisioncode)
        d = dvalues(stdt, etdt, divisioncode)
        data(result, d, stdt, etdt, divisioncode)