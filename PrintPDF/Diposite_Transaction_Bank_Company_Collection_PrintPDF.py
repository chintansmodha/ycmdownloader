from babel.numbers import format_currency
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
d = 750
BUSINESSUNITNAME = []
BankName=[]
pageno = 0
totalbankamount = 0
totalbankchecque=0
totalCompantBankAmount=0
totalCompanyCheque=0

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

def logic(result):
    BUSINESSUNITNAME.append(result['BUSINESSUNITNAME'])
    BankName.append(result['BANKNAME'])

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global BUSINESSUNITNAME
    global pageno
    global totalbankamount
    global totalchecque
    BUSINESSUNITNAME = []
    pageno = 0
    totalbankamount=0
    totalchecque=0




def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if d < 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt, BUSINESSUNITNAME)

    if len(BUSINESSUNITNAME) == 1:
        header(stdt, etdt, BUSINESSUNITNAME)
        fonts(12)
        d=dvalue()
        c.drawString(10, d, result['BUSINESSUNITNAME'])
        d=dvalue()
        fonts(9)
        c.drawString(10, d, result['BANKNAME'])
        data(result, d)
    elif BUSINESSUNITNAME[-1] == BUSINESSUNITNAME[-2]:
        if len(BankName) == 1:
            c.drawString(10, d, result['BANKNAME'])
        elif BankName[-1] != BankName[-2]:
            # d = dvalue()
            # c.drawString(300, d, "Bank Total : ")
            printbanktotal()
            d=dvalue()
            d=dvalue()
            c.drawString(10, d, result['BANKNAME'])
        data(result, d)
    elif BUSINESSUNITNAME[-1] != BUSINESSUNITNAME[-2]:
        c.drawString(300, d, "Bank Total : ")
        printbanktotal()
        d = dvalue()
        d = dvalue()
        d=dvalue()
        fonts(12)
        d=dvalue()
        c.drawString(10,d,result['BUSINESSUNITNAME'])
        fonts(9)
        d=dvalue()
        # if len(BankName) == 1:
        c.drawString(10, d, result['BANKNAME'])
        data(result, d)


def header(stdt, etdt, BUSINESSUNITNAME):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(300, 800, BUSINESSUNITNAME[-1])
    c.drawCentredString(300, 800, "Beekaylon Group of Companies")
    fonts(9)
    c.drawCentredString(300, 785,
                        "Company/Bank/Voucher Wise Consolidated Collection From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 777, 600, 777)
    # Upperline in header
    c.drawString(10, 755, "Bank")
    # c.drawString(200, 755, "Account No.")
    c.drawString(320, 755, "Vch No. ")
    c.drawString(415, 755, "Vch Date ")
    c.drawString(470, 755, "Cheques ")
    c.drawString(550, 755, "Amount ")
    c.line(0, 750, 600, 750)


def data(result, d):
    fonts(9)
    c.drawString(300, d, str(result['VOUCHERNUMBER']))
    c.drawString(415, d, str(result['VOUCHERDATE']))
    c.drawAlignedString(490, d, str(result['CHEQUE']))
    c.drawAlignedString(570, d, str(format_currency("%.2f" % float(result['AMOUNT']), '', locale='en_IN')))
    # c.drawString(550, d, "--")
    total(result)


def total(result):
    global totalbankamount
    global totalbankchecque
    global totalCompanyCheque
    global totalCompantBankAmount
    totalbankchecque = totalbankchecque + (float("%.2f" % float(result['CHEQUE'])))
    totalbankamount = totalbankamount + (float("%.2f" % float(result['AMOUNT'])))
    totalCompanyCheque = totalCompanyCheque + (float("%.2f" % float(result['CHEQUE'])))
    totalCompantBankAmount = totalCompantBankAmount + (float("%.2f" % float(result['AMOUNT'])))

def printbanktotal():
    global totalbankamount
    global totalbankchecque
    c.drawString(300, d, "Bank Total : ")
    c.drawAlignedString(490, d, ""+str(("%.0f" % float(totalbankchecque))))
    c.drawAlignedString(570, d, ""+str(format_currency("%.2f" % float(totalbankamount), '', locale='en_IN')))
    totalbankamount=0
    totalbankchecque=0

def prinCompanytotal():
    d=dvalue()
    global totalCompantBankAmount
    global totalCompanyCheque
    c.drawString(300, d, "Company Total : ")
    c.drawAlignedString(490, d, ""+str(("%.0f" % float(totalCompanyCheque))))
    c.drawAlignedString(570, d, ""+str(format_currency("%.2f" % float(totalCompantBankAmount), '', locale='en_IN')))
    totalCompanyCheque=0
    totalCompantBankAmount=0