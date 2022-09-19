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


def dvalue():
    global d
    d = d - 10
    return d

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, "Purchase/Tax Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "CHARGE NAME")
    c.drawString(540, 755, "AMOUNT")

def data(result, d):
    fonts(7)
    c.drawString(10, d, result['CHARGENAME'])
    c.drawAlignedString(570, d, str(("%.2f" % float(result['CHARGEAMOUNT']))))
    total(result)

def total(result):
    global CompanyAmountTotal
    CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['CHARGEAMOUNT'])))

def logic(result):
    divisioncode.append(result['DIVCODE'])

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

def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        data(result, d)


    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
        c.drawAlignedString(570, d, str("%.2f" % float(CompanyAmountTotal)))
        companyclean()
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue()
        data(result, d)