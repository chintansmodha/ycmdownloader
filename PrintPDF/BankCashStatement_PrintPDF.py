from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
from babel.numbers import format_currency

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 720

divisioncode = []
bankname = []
OpeningBalance=0
# CompanyAmountTotal = 0
paymentTotal = 0
receiptTotal = 0
pageno = 0
date=[]
def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 8
    return d

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 760, "For The Period of " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 760, "Page No." + str(p))
    c.line(0, 755, 600, 755)
    c.line(0, 725, 600, 725)
    # Upperline in header
    c.drawString(10, 740, "VchDate")
    c.drawString(50, 740, "TXN")
    c.drawString(75, 740, " ChqNo")
    c.drawString(130, 740, "VchNo")
    c.drawString(185, 740, "Party")
    c.drawString(390, 740, "Payment")
    c.drawString(465, 740, "Receipt")
    c.drawString(540, 740, "Balance")

def data(result, d):
    if str(result['VCHDATE']) != '1980-01-01':
        fonts(8)
        c.drawString(10, d, result['VCHDATE'].strftime('%d-%m-%Y'))
        c.drawString(55, d, result['TXNTYPE'])
        if result['CHEQUENUMBER']!=None:
            c.drawString(95, d, result['CHEQUENUMBER'])
        c.drawString(130, d, result['VCHNO'])
        c.drawString(185, d, result['PARTYNAME'])
        if float(result['PAYMENTAMT']) != 0:
            c.drawAlignedString(415, d, str(locale.currency(float(result['PAYMENTAMT']), grouping=True))[1:])
        if float(result['RECEIPTAMT']) != 0:
            c.drawAlignedString(485, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
        if OpeningBalance > 0:
            c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
        else:
            c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
        # ClosingBalance = ClosingBalance - float(float("%.3f" % float(result['PAYMENTAMT'])))\
        #                  + float(float("%.3f" % float(result['RECEIPTAMT'])))
        # Print (ClosingBalance)
        #c.drawAlignedString(575, d, str(("%.3f" % float(result['OPBAL']))))
    #total(result)

def total(result):
    global OpeningBalance
    if str(result['VCHDATE']) != '1980-01-01':
        OpeningBalance = OpeningBalance -float(float("%.3f" % float(result['PAYMENTAMT']))) + float(float("%.3f" % float(result['RECEIPTAMT'])))
        # OpeningBalance = float(float("%.3f" % float(result['OPBal'])))
    # ClosingBalance = float(float("%.3f" % float(result['OPBal'])))
    # print(OpeningBalance)

def logic(result):
    divisioncode.append(result['BUSINESSUNITNAME'])
    bankname.append(result['BANKNAME'])

def dlocvalue(d):
    d = d - 10
    return d

def newpage():
    global d
    d = 720
    return d

def newrequest():
    global divisioncode
    global pageno
    global bankname
    divisioncode = []
    pageno = 0
    bankname=[]

def CompanyAmtClean():
    global paymentTotal
    global receiptTotal
    paymentTotal = 0
    receiptTotal = 0

def CompanyAmountTotal(result):
    global paymentTotal
    global receiptTotal
    paymentTotal = paymentTotal + float(result['PAYMENTAMT'])
    receiptTotal = receiptTotal + float(result['RECEIPTAMT'])

# def companyclean():
#     global CompanyAmountTotal
#     CompanyAmountTotal = 0

def openingbalance(result):
    global OpeningBalance
    OpeningBalance = float(result['OPBAL'])

def textsize(c, result, d, stdt, etdt):
    # date.append(result['VCHDATE'].strftime('%d-%m-%Y'))
    # if str(result['VCHDATE']) != '1980-01-01':
    global OpeningBalance
    global paymentTotal
    global receiptTotal
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        if len(bankname) ==1:
            # total(result)
            header(stdt, etdt, divisioncode)
            fonts(9)
            c.drawCentredString(300, 780, "AdHoc Cash/Bank book for " +bankname[-1] )
            openingbalance(result)
            CompanyAmtClean()
            # fonts(7)
            # if str(result['VCHDATE']) != '1980-01-01':
            # c.setFont('Helvetica-Bold', 7)
            # c.drawString(10, 715, bankname[-1] )
            fonts(8)

            if float(OpeningBalance) != 0:
                c.drawString(10, d, "Opening Balance" )
                # c.drawAlignedString(510, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
                # c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
                if OpeningBalance > 0:
                    c.drawAlignedString(485, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
                    c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
                else:
                    c.drawAlignedString(415, d, str(format_currency(float(-OpeningBalance), ' ', locale='en_IN')))
                    c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
            # d=dvalue()
            total(result)

            # data(result, d)

            data(result, d)
            CompanyAmountTotal(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if bankname[-1] == bankname[-2]:
            total(result)
            data(result,d)
            CompanyAmountTotal(result)

        elif bankname[-1]!=bankname[-2]:
            # fonts(7)
            c.setFont('Helvetica-Bold', 8)
            c.drawString(200, d, "Transaction Totals : ")
            # if paymentTotal != 0:
            c.drawAlignedString(415, d, str(format_currency(float(paymentTotal), '', locale='en_IN')))
            # if receiptTotal != 0:
            c.drawAlignedString(485, d, str(format_currency(float(receiptTotal), '', locale='en_IN')))
            d = d -15
            c.drawString(200, d, " Closing Balance : ")
            # c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
            # companyclean()
            # d = dvalue()
            if OpeningBalance > 0:
                c.drawAlignedString(485, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
            else:
                c.drawAlignedString(415, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
            # d = dvalue()
            c.showPage()
            header(stdt, etdt, divisioncode)
            fonts(9)
            c.drawCentredString(300, 780, "AdHoc Cash/Bank book for " + bankname[-1] )
            d = newpage()
            openingbalance(result)
            CompanyAmtClean()
            # fonts(7)
            # c.setFont('Helvetica-Bold', 7)
            # c.drawString(10, d, bankname[-1])
            fonts(8)
            d = dvalue()

            if float(OpeningBalance) != 0:
                c.drawString(10, d, "Opening Balance")
                # c.drawAlignedString(510, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
                # c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
                if OpeningBalance > 0:
                    c.drawAlignedString(485, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
                    c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
                else:
                    c.drawAlignedString(415, d, str(format_currency(float(-OpeningBalance), ' ', locale='en_IN')))
                    c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
            total(result)
            data(result,d)
            CompanyAmountTotal(result)


        # if float(result['OPBAL']) > 0:
        #     c.drawString(10, d, "Opening Balance")
        #     c.drawAlignedString(510, d, str(locale.currency(float(result['RECEIPTAMT']), grouping=True))[1:])
        #     c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])

    elif divisioncode[-1] != divisioncode[-2]:
        # fonts(7)
        # if str(result['VCHDATE']) != '1980-01-01':
        c.setFont('Helvetica-Bold', 8)
        c.drawString(200, d, "Transaction Totals : ")
        # if paymentTotal != 0:
        c.drawAlignedString(415, d, str(format_currency(float(paymentTotal), '', locale='en_IN')))
        # if receiptTotal != 0:
        c.drawAlignedString(485, d, str(format_currency(float(receiptTotal), '', locale='en_IN')))
        d = d -15
        c.drawString(200, d, " Closing Balance : ")
            # c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
        if OpeningBalance > 0:
            c.drawAlignedString(485, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
        else:
            c.drawAlignedString(415, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
        c.showPage()

        header(stdt, etdt, divisioncode)
        fonts(9)
        c.drawCentredString(300, 780, "AdHoc Cash/Bank book for " + bankname[-1] )
        d = newpage()
        d = dvalue()
        #total(result)
        openingbalance(result)
        CompanyAmtClean()

        # c.setFont('Helvetica-Bold', 7)
        # # if str(result['VCHDATE']) != '1980-01-01':
        # c.drawString(10, 715, bankname[-1])
        fonts(8)

        if float(result['OPBAL']) != 0:
            c.drawString(10, d, "Opening Balance")
            # c.drawAlignedString(510, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
            # c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
            if OpeningBalance > 0:
                c.drawAlignedString(485, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
                c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
            else:
                c.drawAlignedString(415, d, str(format_currency(float(-OpeningBalance), ' ', locale='en_IN')))
                c.drawAlignedString(565, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
        total(result)
        # data(result, d)

        data(result, d)
        CompanyAmountTotal(result)

    # data(result, d)

    #c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))