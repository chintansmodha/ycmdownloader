import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 525
Yordno = 760
i = 0
sr = 1
pageno = 0

divisioncode = []
invoiceno = []
orderno = []
lotno = []
itemname = []
itemtype = []
hsncode = []
payment = []
Remark = []
countryofOrigin = []
grosswt = 0
netwt = 0
packages = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def serialNo():
    global sr
    sr = sr + 1
    return sr

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

def updatedvalue():
    global d
    d = 190
    return d

def yordnovalue():
    global Yordno
    Yordno = Yordno - 8
    return Yordno

def wrap(string, type, width, x, y,h):
    global i
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - h
        e = e + 1
        i = i + 1
    return s

def header(divisioncode, result,Yordno):
    c.setTitle('Certificate Of Origin')
    fonts(8)
    c.drawString(25, 800, divisioncode[-1])
    if result['CORP_ADDRESS'] != None:
        wrap(str(result['CORP_ADDRESS']),c.drawString,65,25, 785,10)
    c.drawString(500, 800, str(result['IMCNO']))
    #Buyer
    c.drawString(25, 725, str(result['BUYER']))
    wrap(str(result['BUYERADDRESS']),c.drawString,65,25,710, 10)
    #PORT
    fonts(7)
    if result['PORTOFLOADING'] != None:
        c.drawString(25, 650, str(result['PORTOFLOADING']))
    if result['PORTOFDISCHARGE'] != None:
        c.drawString(25, 640, str(result['PORTOFDISCHARGE']))
    #contNo,Seal,Eseal
    c.drawString(35, 620, 'Cont No.: ')
    c.drawString(40, 610, str(result['CONTNO']))
    c.drawString(150, 620, str(result['BOXES']))#OXES............
    c.drawString(35, 600, 'Seal No.:')
    c.drawString(40, 590, str(result['SEALNO']))
    c.drawString(35, 580, 'ESeal No.: ')
    c.drawString(40, 570, str(result['ESEALNO']))
    #load in Country
    c.drawString(400, 600, str(result['COUNTRYOFORIGIN']).upper())
    #grosswt, NtWt
    c.drawString(460, 605, str(result['GRWT']))
    c.drawString(450, 595, 'GR. WT  ' + str(result['UNIT']))
    c.drawString(460, 585, str(result['NETWT']))
    c.drawString(450, 575, 'NT. WT  ' + str(result['UNIT']))
    #Bottom
    c.drawString(510, 120, str(result['COUNTRYOFORIGIN']).upper())
    if result['COUNTRYOFDESTN'] != None:
        c.drawString(500, 90, str(result['COUNTRYOFDESTN']))
    c.drawString(490, 60, str(result['INVDT'].strftime('%d-%m-%Y')))




def data(result, d):
    fonts(7)
    global sr
    c.drawString(35, d, str(sr))
    str1 = ''
    string = str1.join(result['ITEM'])
    wrap_text = textwrap.wrap(string, width=75)
    e = 0
    while e < len(wrap_text):
        c.drawString(85, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(155, d, str(result['ITEM']))
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1
    sr = serialNo()


def logic(result):
    global divisioncode, lotno
    global invoiceno, Remark, itemtype, orderno
    global itemname, hsncode, payment, countryofOrigin
    divisioncode.append(str(result['COMPANY']))
    invoiceno.append(result['INVOICENO'])
    itemtype.append(str(result['ITMTYP']))
    lotno.append(str(result['LOTNO']))
    hsncode.append(str(result['HSNCODE']))

def newpage():
    global d
    d = 525
    return d

def newrequest():
    global divisioncode, lotno
    global invoiceno, Remark, itemtype
    global itemname, hsncode, payment, countryofOrigin
    global pageno, Yordno
    divisioncode = []
    pageno = 0
    Yordno = 760
    invoiceno = []
    itemname = []
    hsncode = []
    payment = []
    Remark = []
    itemtype = []
    countryofOrigin = []
    lotno = []

def TotalWT(result):
    global grosswt, netwt, packages

def TotalClean():
    global grosswt
    global netwt
    global packages
    grosswt = 0
    netwt = 0
    packages = 0

def textsize(c, result):
    d = dvalue()
    logic(result)
    global i, Yordno
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(divisioncode, result,Yordno)
        boldfonts(7)
        c.drawString(155, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1] == invoiceno[-2]:
            if itemtype[-1] == itemtype[-2]:
                if lotno[-1] == lotno[-2]:
                    data(result,d)

                else:
                    c.drawString(95, d,'Lot No. : ' + lotno[-2])
                    d = dvalue()
                    d = dvalue()
                    data(result, d)
            else:
                c.drawString(95, d,'Lot No. : ' + lotno[-2])
                d = dvalue()
                d = dvalue()
                c.drawString(95, d, 'HSNCODE : ' + hsncode[-2])
                d = dvalue()
                d = dvalue()
                boldfonts(7)
                c.drawString(155, d, itemtype[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)
        else:
            c.drawString(95, d,'Lot No. : ' + lotno[-2])
            d = dvalue()
            d = dvalue()
            c.drawString(95, d, 'HSNCODE : ' + hsncode[-2])
            c.showPage()
            d = newpage()
            header(divisioncode, result, Yordno)
            boldfonts(7)
            c.drawString(155, d, itemtype[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        c.drawString(95, d,'Lot No. : ' + lotno[-2])
        d = dvalue()
        d = dvalue()
        c.drawString(95, d, 'HSNCODE : ' + hsncode[-2])
        c.showPage()
        d = newpage()
        header(divisioncode, result, Yordno)
        boldfonts(7)
        c.drawString(155, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)


