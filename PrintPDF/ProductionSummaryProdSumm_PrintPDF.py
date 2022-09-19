import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 750
i = 1
pageno = 0

divisioncode = []
Itemname = []
ShadeName = []
ShadeCode =  []
LotNo = []
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

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Item Wise/Machine Wise Production Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Machine")
    c.drawString(90, 760, "Item")
    c.drawString(420, 760, "Lot No.")
    c.drawString(555, 760, "NetWt.")


def data(result, d):
    fonts(7)
    c.drawString(11, d, str(result['MACHINECODE']))
    str1 = ''
    string = str1.join(result['PRODUCT'])
    wrap_text = textwrap.wrap(string, width=75)
    e = 0
    while e < len(wrap_text):
        c.drawString(91, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrease()
        f = f + 1
    # c.drawString(111, d, str(result['PRODUCT']))
    c.drawString(421, d, str(result['LOTNO']))
    c.drawAlignedString(570, d, str(result['NETWT']))
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
    d = 750
    return d

def newrequest():
    global divisioncode
    global pageno
    divisioncode = []
    pageno = 0

def CompanyTotal(result):
    global Netwt
    Netwt = Netwt + float(result['NETWT'])

def CompanyClean():
    global Netwt
    Netwt = 0

def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    # str('{0:1.3f}'.format(

    if len(divisioncode) == 1:
        CompanyClean()
        header(stdt, etdt, divisioncode)
        data(result, d)
        CompanyTotal(result)

    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)
        CompanyTotal(result)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.drawString(350, d, "Company Total: ")
        c.drawAlignedString(570, d, str('{0:1.3f}'.format(Netwt)))
        CompanyClean()
        fonts(7)
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        data(result, d)
        CompanyTotal(result)
