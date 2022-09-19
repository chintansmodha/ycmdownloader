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
department = []
boxcount = 0

# total ref

deptNtwt = 0

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

def dvalue(c, result, stdt):
    global d
    if d<30:
        c.showPage()
        d = newpage()
        d = dvalue(c, result, stdt)
        header(stdt, divisioncode)
        boldfonts(7)
    else:
        d = d - 5
    return d

def dvalueincrese():
    global d
    if d > 30 and d < 745:
        d = d + 10
    else:
        pass
    return d

def wrap(string, type, width, x, y, result, stdt):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = dvalue(c, result, stdt)
        y = dvalue(c, result, stdt)
        e = e + 1
    d = dvalueincrese()
    # y = dvalueincrese()

def header(stdt, divisioncode):
    fonts(15)
    c.setTitle('FinishedStockInHand DeptBoxWise')
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Stock In Hand (DeptWise Boxes in Hand)  As On " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    # c.drawString()
    # c.setDash(3,3)# Dash Linne
    # c.line(0, 730, 600, 730)
    # c.setDash([], 0)  # continuous
    c.drawString(10, 760, 'Box No.')
    c.drawString(90, 760, 'Date')
    c.drawString(160, 760, 'LotNo.')
    c.drawString(240, 760, 'Item')
    c.drawString(557, 760, 'Net Wt.')


def data(result, d, stdt):
    fonts(7)
    global boxcount
    c.drawString(10, d, str(result['BOXNO']))
    c.drawString(90, d, str(result['BOXDT'].strftime(' %d-%m-%Y')))
    c.drawString(160, d, str(result['LOTNO']))
    # c.drawString(240, 760, 'Item')
    c.drawAlignedString(570, d, str(result['NETWT']))
    wrap(str(result['PRODUCT']), c.drawString, 60, 241, d, result, stdt)
    # d = dvalueincrese()
    boxcount += 1
    Total(result)


def logic(result):
    global divisioncode
    global department
    divisioncode.append(result['PLANT'])
    department.append(result['DEPARTMENT'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global department
    global pageno
    divisioncode = []
    department = []
    pageno = 0

def Total(result):
    global deptNtwt
    deptNtwt += float(result['NETWT'])

def PrintDeptTotal():
    boldfonts(7)
    global deptNtwt, boxcount
    c.drawString(50, d, 'Department Total: ')
    c.drawAlignedString(230, d, str(boxcount))
    c.drawAlignedString(570, d, str('{0:1.3f}'.format(deptNtwt)))
    deptNtwt = 0
    boxcount = 0
    fonts(7)


def textsize(c, result, d, stdt):
    d = dvalue(c, result, stdt)
    logic(result)
    global boxcount
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, department[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        data(result, d, stdt)

    elif divisioncode[-1] == divisioncode[-2]:
        if department[-1] == department[-2]:
            data(result, d, stdt)

        elif department[-1] != department[-2]:
            PrintDeptTotal()
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            boldfonts(7)
            c.drawCentredString(300, d, department[-1])
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            data(result, d, stdt)

    elif divisioncode[-1] != divisioncode[-2]:
        PrintDeptTotal()
        c.showPage()
        d = newpage()
        d = dvalue(c, result, stdt)
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, department[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        data(result, d, stdt)
