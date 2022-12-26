from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 730

divisioncode = []

CompanyAmountTotal = 0
pageno = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue(stdt, etdt, divisioncode,result,LS1,LS2,LS3):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, divisioncode,LS1,LS2,LS3)
        return d

def header(stdt, etdt, divisioncode,LS1,LS2,LS3):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, "Book Bebt As On " + str(stdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "Party")
    if LS1 == '0':
        c.drawString(250, 755, "1-1")
    else:
        c.drawString(250, 755, "1-"+LS1)
    if LS2 == '0':
        pass
        # c.drawString(350, 755, "1-1")
    else:
        c.drawString(320, 755, str(int(LS1)+1)+"-"+LS2)
    if LS3 == '0':
        pass
        # c.drawString(350, 755, "1-1")
    else:
        c.drawString(390, 755, str(int(LS2)+1)+"-"+LS3)
    if int(LS1)<int(LS2)<int(LS3):
        c.drawString(460, 755, "Over "+LS3)
    elif int(LS1)<int(LS2):
        c.drawString(460, 755, "Over "+LS2)
    else:
        c.drawString(460, 755, "Over "+LS1)
    c.drawString(550, 755, "Total")

def data(result, d):
    fonts(7)
    c.drawString(10, d, result['BROKERGRP'])
    c.drawAlignedString(260, d, str(("%.2f" % float(result['BETWEEN1']))))
    c.drawAlignedString(330, d, str(("%.2f" % float(result['BETWEEN2']))))
    c.drawAlignedString(400, d, str(("%.2f" % float(result['BETWEEN3']))))
    c.drawAlignedString(480, d, str(("%.2f" % float(result['OVER4']))))
    c.drawAlignedString(560, d, str(("%.2f" % float(float(result['BETWEEN1'])+float(result['BETWEEN2'])+float(result['BETWEEN3'])+float(result['OVER4'])))))

    total(result)

def total(result):
    global CompanyAmountTotal
    CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(float(result['BETWEEN1'])+float(result['BETWEEN2'])+float(result['BETWEEN3'])+float(result['OVER4']))))

def logic(result):
    divisioncode.append(result['COMPANY'])

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global divisioncode
    global pageno
    divisioncode = []
    pageno = 0

def companyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0

def textsize(c, result, d, stdt, etdt,LS1,LS2,LS3):
    print(type(LS1),LS2,LS3)
    d = dvalue(stdt, etdt, divisioncode,result,LS1,LS2,LS3)
    logic(result)
    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode,LS1,LS2,LS3)
        data(result, d)


    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
        c.drawAlignedString(560, d, str("%.2f" % float(CompanyAmountTotal)))
        companyclean()
        c.showPage()

        header(stdt, etdt, divisioncode,LS1,LS2,LS3)
        d = newpage()
        d = dvalue(stdt, etdt, divisioncode,result,LS1,LS2,LS3)
        data(result, d)