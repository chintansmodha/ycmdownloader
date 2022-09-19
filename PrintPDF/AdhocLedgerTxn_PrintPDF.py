import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 745

divisioncode = []
account = []
subaccount = []
AccountSubAcc = []
pageno = 0
date=[]
openingbalance = 0
CRAmountTotal = 0
DRAmountTotal = 0
OpeningCRAmountTotal = 0
OpeningDRAmountTotal = 0
closingbalance = 0
# string1 = ''
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

def dincrease():
    global d
    d = d + 10

def header(stdt, etdt, divisioncode, LMMergeCompany):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    if LMMergeCompany == ['true']:
        c.drawCentredString(300, 780,"TxnWise Summary Merge Company From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    else:
        c.drawCentredString(300, 780, "TxnWise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
            etdt.strftime('%d-%m-%Y')))

    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 750, 600, 750)
    # Upperline in header
    c.drawString(10, 760, "Particular")
    c.drawString(370, 760, "Debit Amount")
    c.drawString(510, 760, "Credit Amount")


def data(result, d ,LCNarration, LCAddress):
    fonts(7)
    if float(result['OPBAL']) != 0:
        c.drawString(35, d, "Opening Balance : ")
        if float(result['OPBAL']) < 0:
            c.drawAlignedString(555, d, str('{0:1.2f}'.format(-float(result['OPBAL']))))
        else:
            c.drawAlignedString(415, d, result['OPBAL'])
        d = dvalue()
        d = dvalue()
    if (float(result['DRAMOUNT']) + float(result['CRAMOUNT'])) != 0:
        # d = dvalue()
        # d = dvalue()
        c.drawString(10, d, result['DOCUMENTTYPE'])
        if float(result['DRAMOUNT']) != 0:
            c.drawAlignedString(415, d, result['DRAMOUNT'])
        if float(result['CRAMOUNT']) != 0:
            c.drawAlignedString(555, d, result['CRAMOUNT'])
    else:
        d = dincrease()

def ClosingBalance(result):
    logic(result)
    global closingbalance
    global CRAmountTotal
    global DRAmountTotal
    global OpeningCRAmountTotal
    global OpeningDRAmountTotal
    closingbalance = closingbalance + float(result['OPBAL']) + float(result['DRAMOUNT']) - float(result['CRAMOUNT'])
    DRAmountTotal = DRAmountTotal + float(result['DRAMOUNT'])
    CRAmountTotal = CRAmountTotal + float(result['CRAMOUNT'])

def OpeningBalance(result):
    global openingbalance
    global CRAmountTotal
    global DRAmountTotal
    openingbalance = float(result['OPBAL'])
    if float(result['OPBAL']) < 0:
        CRAmountTotal = -float(result['OPBAL'])
    else:
        DRAmountTotal = float(result['OPBAL'])

def ClearClosingBalance():
    global closingbalance
    global CRAmountTotal
    global DRAmountTotal
    closingbalance = 0
    CRAmountTotal = 0
    DRAmountTotal = 0

def logic(result):
    global divisioncode
    global account
    # global subaccount
    # global AccountSubAcc
    divisioncode.append(result['BUSINESSUNIT'])
    account.append(result['GLACCOUNT'])
    # subaccount.append(result['SUBACCOUNT'])

def newpage():
    global d
    d = 745
    return d

def newrequest():
    global divisioncode
    global pageno
    global account
    divisioncode = []
    pageno = 0
    account = []


def textsize(c, result, d, stdt, etdt, LCEject, LCNarration, LCAddress, LMMergeCompany ):
    d = dvalue()
    logic(result)
    # CompanyAmtClean()

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode, LMMergeCompany)
        ClearClosingBalance()
        c.setFont('Helvetica-Bold', 7)
        c.drawString(10, d, account[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        OpeningBalance(result)
        data(result, d ,LCNarration, LCAddress)
        ClosingBalance(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if account[-1] == account[-2]:
            data(result, d, LCNarration, LCAddress)
            ClosingBalance(result)

        else:
            fonts(7)
            c.drawString(35, d, "Closing Balance : ")
            if closingbalance != 0:
                if closingbalance < 0:
                    c.drawAlignedString(415, d, str('{0:1.2f}'.format(-closingbalance)))
                else:
                    c.drawAlignedString(555, d, str('{0:1.2f}'.format(closingbalance)))
            elif closingbalance == 0:
                c.drawAlignedString(415, d, str('{0:1.2f}'.format(closingbalance)))
            d = dvalue()
            c.line(340, d, 590, d)
            d = dvalue()
            d = dvalue()
            c.drawString(200, d, "Total : ")
            if closingbalance <= 0 :
                c.drawAlignedString(415, d, str('{0:1.2f}'.format(DRAmountTotal - closingbalance)))
            else:
                c.drawAlignedString(415, d, str('{0:1.2f}'.format(DRAmountTotal)))
            if closingbalance > 0:
                c.drawAlignedString(555, d, str('{0:1.2f}'.format(CRAmountTotal + closingbalance)))
            else:
                c.drawAlignedString(555, d, str('{0:1.2f}'.format(CRAmountTotal)))
            d = dvalue()
            # d = dvalue()
            c.line(340, d, 590, d)
            d = dvalue()
            d = dvalue()
            d = dvalue()
            ClearClosingBalance()
            c.setFont('Helvetica-Bold', 7)
            c.drawString(10, d, account[-1])
            d = dvalue()
            d = dvalue()
            fonts(7)
            OpeningBalance(result)
            data(result, d, LCNarration, LCAddress)
            ClosingBalance(result)

    elif divisioncode[-1] != divisioncode[-2]:
        # d = dvalue()
        fonts(7)
        c.drawString(35, d, "Closing Balance : ")
        if closingbalance != 0:
            if closingbalance < 0:
                c.drawAlignedString(415, d, str('{0:1.2f}'.format(-closingbalance)))
            else:
                c.drawAlignedString(555, d, str('{0:1.2f}'.format(closingbalance)))
        elif closingbalance == 0:
            c.drawAlignedString(415, d, str('{0:1.2f}'.format(closingbalance)))
        d = dvalue()
        c.line(340, d, 590, d)
        d = dvalue()
        d = dvalue()

        c.drawString(200, d, "Total : ")
        if closingbalance <= 0:
            c.drawAlignedString(415, d, str('{0:1.2f}'.format(DRAmountTotal - closingbalance)))
        else:
            c.drawAlignedString(415, d, str('{0:1.2f}'.format(DRAmountTotal)))
        if closingbalance > 0:
            c.drawAlignedString(555, d, str('{0:1.2f}'.format(CRAmountTotal + closingbalance)))
        else:
            c.drawAlignedString(555, d, str('{0:1.2f}'.format(CRAmountTotal)))
        d = dvalue()
        # d = dvalue()
        c.line(340, d, 590, d)
        ClearClosingBalance()
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode, LMMergeCompany)
        d = dvalue()
        c.setFont('Helvetica-Bold', 7)
        c.drawString(10, d, account[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        OpeningBalance(result)
        data(result, d, LCNarration, LCAddress)
        ClosingBalance(result)