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
box = 0
cops = 0
gross = 0
tarewt = 0
netwt = 0

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
    c.drawCentredString(300, 780, "Department Wise Production From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Department")
    c.drawString(250, 760, "Boxes")
    c.drawString(305, 760, "Cops")
    c.drawString(380, 760, "Gross Wt")
    c.drawString(460, 760, "Tare Wt")
    c.drawString(555, 760, "Net Wt")



def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['DEPARTMENT']))
    c.drawAlignedString(270, d, str(result['BOXES']))
    c.drawAlignedString(325, d, str(result['COPS']))
    c.drawAlignedString(405, d, str(result['GROSSWT']))
    c.drawAlignedString(480, d, str(result['TAREWT']))
    c.drawAlignedString(570, d, str(result['NETWT']))
    CompanyTotal(result)


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
    global box, cops, gross, tarewt, netwt
    box = box + int(result['BOXES'])
    cops = cops + int(result['COPS'])
    gross = gross + float(result['GROSSWT'])
    tarewt = tarewt + float(result['TAREWT'])
    netwt = netwt + float(result['NETWT'])

def CompanyClean():
    global box, cops, gross, tarewt, netwt
    box = cops = gross = tarewt = netwt = 0

def CompanyTotalPrint(d):
    boldfonts(7)
    c.drawString(150, d, "Company Total: ")
    c.drawAlignedString(270, d, str(box))
    c.drawAlignedString(325, d, str(cops))
    c.drawAlignedString(405, d, str('{0:1.3f}'.format(gross)))
    c.drawAlignedString(480, d, str('{0:1.3f}'.format(tarewt)))
    c.drawAlignedString(570, d, str('{0:1.3f}'.format(netwt)))
    CompanyClean()
    fonts(7)


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        fonts(7)
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        CompanyTotalPrint(d)
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        fonts(7)
        data(result, d)
