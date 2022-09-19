import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, portrait, A4, A1, A2, A0, A5, A3, A6, A7
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number, format_currency, format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialItalic', 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBoldItalic', 'arialbi.ttf'))

c = canvas.Canvas("1.pdf")
c.setPageSize(portrait(A4))

d = 755
i = 1
pageno = 0
pageSize = 0
Xaxis = 0
Yaxis = 0

divisioncode = []
Itemname = []
LotNo = []

gainTotal = 0
lossTotal = 0
grandgainTotal = 0
grandlossTotal = 0


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


def dvalue(stdt, etdt, result, divisioncode):
    global d
    if d > 20:
        d = d - 5
        return d
    else:
        d = newpage()
        # c.setPageSize(landscape(A4))
        c.showPage()
        header(stdt, etdt, divisioncode)
        return d


def dvalueincrese():
    global d
    if d > 30 and d < 745:
        d = d + 10
    else:
        pass
    return d


def wrap(string, type, width, x, y, result, stdt, etdt):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        e = e + 1
        if e < len(wrap_text):
            y = dvalue(stdt, etdt, result, divisioncode)
            y = dvalue(stdt, etdt, result, divisioncode)


def header(stdt, etdt, divisioncode):
    c.setTitle('DGGainLossItemWise')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    # c.drawString(10, Yaxis, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 785, "D. G. Gain/Loss Report (Itemwise Summary) From  " + str(stdt.strftime(' %d  %B  %Y'))
                        + ' To ' + str(etdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 785, "Page No." + str(p))
    # c.setDash(2,3)
    c.line(0, 780, 600, 780)
    c.line(0, 760, 600, 760)
    # Upperline in header
    # fonts(8)
    c.drawString(30, 765, 'Item ')
    c.drawString(390, 765, 'Gain ')
    c.drawString(520, 765, 'Loss ')


def data(result, d, stdt, etdt, divisioncode):
    fonts(7)
    c.drawString(31, d, str(result['ITEM']))
    c.drawAlignedString(400, d, str(result['GAIN']))
    c.drawAlignedString(530, d, str(result['LOSS']))
    Total(result)
    GrandTotal(result)


def logic(result):
    global divisioncode
    global Itemname
    global LotNo
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['ITEM'])


def newpage():
    global d
    d = 755
    return d


def newrequest():
    global divisioncode
    global Itemname
    global LotNo
    global pageSize
    global pageno
    divisioncode = []
    pageno = 0
    Itemname = []
    LotNo = []
    pageSize = 0


def Total(result):
    global gainTotal
    global lossTotal
    gainTotal += float(result['GAIN'])
    lossTotal += float(result['LOSS'])


def GrandTotal(result):
    global grandgainTotal
    global grandlossTotal
    grandgainTotal += float(result['GAIN'])
    grandlossTotal += float(result['LOSS'])


def PrintTotal():
    boldfonts(7)
    global gainTotal
    global lossTotal
    c.drawString(131, d, 'Total: ')
    c.drawAlignedString(400, d, str('{0:1.3f}'.format(gainTotal)))
    c.drawAlignedString(530, d, str('{0:1.3f}'.format(lossTotal)))
    gainTotal = 0
    lossTotal = 0
    fonts(7)


def PrintGrandTotal():
    boldfonts(7)
    global grandgainTotal
    global grandlossTotal
    c.drawString(131, d, 'Grand Total: ')
    c.drawAlignedString(400, d, str('{0:1.3f}'.format(grandgainTotal)))
    c.drawAlignedString(530, d, str('{0:1.3f}'.format(grandlossTotal)))
    grandgainTotal = 0
    grandlossTotal = 0
    fonts(7)


def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt, etdt, result, divisioncode)
    logic(result)
    # print('rohit  ', A4)
    # '{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] != divisioncode[-2]:
        PrintGrandTotal()
        c.showPage()
        d = newpage()
        d = dvalue(stdt, etdt, result, divisioncode)
        header(stdt, etdt, divisioncode)
        data(result, d, stdt, etdt, divisioncode)



