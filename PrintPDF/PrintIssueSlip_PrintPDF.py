import textwrap
from reportlab.lib.pagesizes import landscape, A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")

d = 665
i = 1

divisioncode = []
CompanyAddress = []
todepartment = []
Number = []
Remark = []
pageno = 0
quantitytotal = 0
boxtotal = 0
copstotal = 0
# DocumentType = []
def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue():
    global d
    d = d - 5
    return d

def dvalueincrease():
    global d
    d = d + 10
    return d

def dlocalvalue():
    global d
    d = d - 70
    return d

def serialNo():
    global i
    i = i + 1
    return i

def header(result, divisioncode, todepartment):
    fonts(9)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(10, 810, str(date.today().strftime("%d/%m/%Y")))
    fonts(12)
    c.drawCentredString(300, 810, "Issue Slip ")
    fonts(15)
    c.drawCentredString(300, 785, divisioncode[-1])
    fonts(9)
    c.drawString(10, 760, "To,  ")
    c.drawString(400, 760, "Issue No: " + Number[-1])
    c.drawString(400, 745, "Issue Dt: " + str(result['ISSUEDT']))
    c.drawString(400, 720, "Req. No.: " + str(result['REQNUMBER']))
    c.drawString(400, 705, "Req. Dt.: " + str(result['REQDATE']))
    fonts(8)
    c.drawString(50, 730, todepartment[-1])
    fonts(9)

    c.line(0, 690, 600, 690)
    c.line(0, 670, 600, 670)
    # Upperline in header
    c.drawString(10,  675, "Sr. ")
    c.drawString(30,  675, "Item Name")
    c.drawString(190, 675, "Base")
    c.drawString(275, 675, "Lot No.")
    c.drawString(370, 675, "Quality")
    c.drawString(440, 675, "Bxs")
    c.drawString(490, 675, "Cops")
    c.drawString(550, 675, "Quantity")


def data(result, d, i):
    fonts(7)
    c.drawString(10, d, str(i))
    str1 = ''
    string = str1.join(result['ITEMNAME'])
    res = sum(not chr.isspace() for chr in string)
    wrap_text = textwrap.wrap(string, width=30)
    # print(len(wrap_text))
    e = 0
    while e < len(wrap_text):
        c.drawString(30, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrease()
        f = f + 1

    c.drawString(190, d, str(result['BASENAME']))
    c.drawString(276, d, str(result['LOTNO']))
    c.drawString(374, d, str(result['QUALITY']))
    c.drawAlignedString(450, d, str(result['BOXES']))
    c.drawAlignedString(508, d, str(result['COPS']))
    c.drawAlignedString(570, d, str(result['QUANTITY']))

    g = 0
    while g < len(wrap_text)-1:
        d = dvalue()
        d = dvalue()
        g = g + 1

    i = serialNo()


def dataheader(result):
    fonts(9)
    c.drawString(455, 730, result['DATE'])
    # c.drawString(455, 700, result['OWNER'])

def logic(result):
    global divisioncode
    global todepartment
    global Number
    divisioncode.append(result['DEPARTMENT'])
    todepartment.append(result['TODEPARTMENT'])
    Number.append(result['ISSUENO'])


def newpage():
    global d
    d = 665
    return d

def newserialNo():
    global i
    i = 1
    return i

def newrequest():
    global divisioncode
    global todepartment
    global Number
    # global pageno
    divisioncode = []
    todepartment = []
    pageno = 0
    Number = []
    i = newserialNo()

def Total(result):
    global quantitytotal
    global boxtotal
    global copstotal
    quantitytotal = quantitytotal + float(result['QUANTITY'])
    boxtotal = boxtotal + float(result['BOXES'])
    copstotal = copstotal + float(result['COPS'])

def TotalClean():
    global quantitytotal
    global boxtotal
    global copstotal
    quantitytotal = 0
    boxtotal = 0
    copstotal = 0

def textsize(c, result, d, i):
    d = dvalue()
    logic(result)

    if len(Number) == 1:
        TotalClean()
        header(result, divisioncode, todepartment)
        # c.drawString(455, 760, Number[-1])
        # dataheader(result)
        data(result, d, i)
        Total(result)


    elif Number[-1] == Number[-2]:
        data(result, d, i)
        Total(result)

    elif Number[-1] != Number[-2]:
        c.line(0, d+5, 600, d+5)
        d = dvalue()
        c.setFont("Helvetica-Bold", 8)
        c.drawString(275, d, "Total : ")
        c.drawAlignedString(450, d, str('{0:1.0f}'.format(boxtotal)))
        c.drawAlignedString(508, d, str('{0:1.0f}'.format(copstotal)))
        c.drawAlignedString(570, d, str('{0:1.3f}'.format(quantitytotal)))
        d = dvalue()
        c.line(0, d, 600, d)
        fonts(7)
        d = dlocalvalue()
        c.drawString(30, d, "Dept.Incharge")
        c.drawString(400, d, "Receiver's Signature")
        TotalClean()
        c.showPage()
        d = newpage()
        i = newserialNo()
        header(result, divisioncode, todepartment)
        fonts(9)
        d = dvalue()
        # c.drawString(455, 760, Number[-1])
        # dataheader(result)
        data(result, d, i)
        Total(result)