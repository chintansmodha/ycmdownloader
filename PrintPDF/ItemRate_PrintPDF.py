import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date, datetime
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 470
# d = 0
i = 0
x = 0
pageno = 0
checkItmrep = 0
lastclm = 0
itemlen = 0
boldornot = 0

divisioncode = []
Item = []
pricecurr = []
priceprev = []
Area = []
Column = []

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


def wrap(string, type, width, x, y):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - 10
        e = e + 1
    return s

def header(divisioncode, result,startdate):
    c.setTitle('Item Rate')
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(420, 570, 'Beekaylon Group Of Companies')
    fonts(8)
    string = 'Office 15, 16 & 17 , Maker Chambers - III, Jamnalal Bajaj Road, Nariman Point, ' \
             'Mumbai - 400 021  Tel No. 4353 0400   Email Id.   ho@beekaylon.com'
    wrap(string,c.drawCentredString,200,420, 555)
    now = datetime.now()
    current_time = datetime.today().strftime("%I:%M:%S %p")
    c.drawCentredString(420, 540, 'Indicative Price As On   ' + startdate + '    ' + 'time??' + '   -   ' + result['LOCATION'] )
    #footer
    c.drawString(30, 80, str(result['REMARKS1']))
    c.drawString(30, 70, str(result['REMARKS2']))
    c.drawString(30, 60, str(result['REMARKS3']))
    c.drawString(30, 50, str(result['REMARKS4']))
    c.drawString(30, 40, str(result['REMARKS5']))
    fonts(12)
    c.drawCentredString(420, 15, str(result['REMARKS6']))

    #Horizontal Line
    c.line(30, 510, 810, 510)
    c.line(30, 480, 810, 480)
    c.line(30, 100, 810, 100)

    # verticl line
    c.line(30, 510, 30, 100)
    c.line(215, 510, 215,100)
    c.line(415, 510, 415, 100)
    c.line(615, 510, 615, 100)
    c.line(810, 510, 810, 100)
    #Refrence Box
    boldfonts(10)
    c.drawString(32, 487, 'FDY')
    c.drawAlignedString(213, 487, 'BASIC RATE')
    c.drawString(217, 487, 'DTY')
    c.drawAlignedString(413, 487, 'BASIC RATE')
    c.drawString(417, 487, 'TWISTED YARN')
    c.drawAlignedString(613, 487, 'BASIC RATE')
    c.drawString(617, 487, 'PACKAGE DYED')
    c.drawAlignedString(809, 487, 'BASIC RATE')






def data(result,d, x):
    fonts(7)
    str1 = ''
    string = str1.join(str(result['ITEM']))
    wrap_text = textwrap.wrap(string, width=35, break_long_words=False)
    e = 0
    while e < len(wrap_text):
        c.drawString(x, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # print(f,len(wrap_text))

    if pricecurr[-1] != priceprev[-1]:
        boldfonts(7)
    c.drawAlignedString(x + 170, d, str(pricecurr[-1]))
    fonts(7)
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1

def logic(result):
    global divisioncode, Area, Column, Item, pricecurr, priceprev
    divisioncode.append(result['COMPANY'])
    Area.append(str(result['LOCATION']))
    Column.append(int(result['COLUMN']))
    Item.append(str(result['ITEM']))
    pricecurr.append(str(result['PRICECURR']))
    priceprev.append(str(result['PRICEPREV']))

def newpage():
    global d
    d = 470
    return d

def newrequest():
    global divisioncode, Area, Column, Item
    global pageno, i, pricecurr, priceprev
    divisioncode = []
    Area = []
    Column = []
    Item = []
    pricecurr = []
    priceprev = []
    pageno = 0
    i = 0

def ClearColumn():
    global Column
    Column = []

def ItemAppend(result):
    global Item, price
    # price.append(str(result['PRICE']))
    Item.append(str(result['ITEM']))

def ClearItem():
    global Item, price
    price = []
    Item = []

def textsize(c, result,startdate,x):
    d = dvalue()
    logic(result)
    global i,lastclm,boldornot,itemlen
    #'{0:1.3f}'.format(

    if Column[0] == 1:
        if i == 0:
            header(divisioncode, result,startdate)
        x = 32
        data(result,d,x)
        ClearColumn()
        # ClearItem()
        i = 1

    elif Column[0] == 2:
        if i == 0:
            header(divisioncode, result,startdate)
        if i == 1:
            d = newpage()
            d = dvalue()
        x = 217
        data(result,d,x)
        ClearColumn()

        i = 2

    elif Column[0] == 3:
        if i == 0:
            header(divisioncode, result,startdate)
        if i == 2 or i == 1:
            d = newpage()
            d = dvalue()
        x = 417
        data(result,d,x)
        ClearColumn()
        i = 3

    elif Column[0] == 4:
        if i == 0:
            header(divisioncode, result,startdate)
        if i == 3 or i == 2 or i == 1:
            d = newpage()
            d = dvalue()
        x = 617
        ClearColumn()
        data(result,d,x)
        i = 4
