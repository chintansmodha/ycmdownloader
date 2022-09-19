from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 730

divisioncode = []

CompanyCreditTotal = 0
CompanyDebitTotal  = 0
pageno = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue(stdt, etdt):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, divisioncode)
        return d


def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    # c.drawCentredString(300, 780, "Item Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "Vch. Date")
    c.drawString(70, 755, "TXN")
    c.drawString(100, 755, "Vch. No.")
    c.drawString(210, 755, "Chq. No.")
    c.drawString(290, 755, "Doc. No.")
    c.drawString(370, 755, "Debit Amt.")
    c.drawString(450, 755, "Credit Amt.")
    c.drawString(530, 755, "Cum. Amt.")

def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['VCHDATE']))
    c.drawString(70, d, result['TXN'])
    c.drawString(100, d, result['VCHNO'])
    c.drawString(210, d, result['CHQNO'])
    if result['DEBIT'] != '0.00':
        c.drawAlignedString(400, d, str(("%.2f" % float(result['DEBIT']))))
    if result['CREDIT'] != '0.00':
        c.drawAlignedString(490, d, str(("%.2f" % float(result['CREDIT']))))
    c.drawAlignedString(570, d, str(("%.2f" % float(result['CUMAMT']))))
    if result['REMARKS'] != '':
        d=d-10
        c.drawString(10,d,result['REMARKS'])
    total(result)

def total(result):
    global CompanyCreditTotal
    global CompanyDebitTotal
    if result['CREDIT'] != None:
        CompanyCreditTotal = CompanyCreditTotal + (float("%.2f" % float(result['CREDIT'])))
        CompanyDebitTotal = CompanyDebitTotal + (float("%.2f" % float(result['DEBIT'])))
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
    global CompanyCreditTotal
    global CompanyDebitTotal
    CompanyCreditTotal = 0
    CompanyDebitTotal = 0

def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt,etdt)
    logic(result)
    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        data(result, d)


    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
        c.drawAlignedString(490, d, str("%.2f" % float(CompanyCreditTotal)))
        c.drawAlignedString(400, d, str("%.2f" % float(CompanyDebitTotal)))
        companyclean()
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue(stdt,etdt)
        data(result, d)