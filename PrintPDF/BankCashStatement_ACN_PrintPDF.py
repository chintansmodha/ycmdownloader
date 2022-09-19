from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
from babel.numbers import format_currency

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 730

divisioncode = []
bankname = []
OpeningBalance=0
pageno = 0
date=[]
CompanyName = []
paymentTotal = 0
receiptTotal = 0
def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 7
    return d

def header(stdt, etdt, CompanyName):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, CompanyName[-1])
    # c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780,"Consolidated AdHoc Cash/Bank book from " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')) )

    # fonts(9)
    # c.drawCentredString(300, 770, divisioncode[-1])
    fonts(9)
    p = page()
    c.drawString(540, 770, "Page No." + str(p))
    c.line(0, 765, 600, 765)
    c.line(0, 735, 600, 735)
    # Upperline in header
    fonts(9)
    c.drawString(10, 750, "VchDate")
    c.drawString(50, 750, "TXN")
    c.drawString(70, 750, " ChqNo")#100
    c.drawString(120, 750, "VchNo")
    c.drawString(175, 750, "Party")#200
    c.drawString(375, 750, "Payment")
    c.drawString(460, 750, "Receipt")
    c.drawString(545, 750, "Balance")

def data(result, d):
    if str(result['VCHDATE']) != '1980-01-01':
        fonts(8)
        c.drawString(10, d, result['VCHDATE'].strftime('%d-%m-%Y'))
        c.drawString(55, d, result['TXNTYPE'])
        if result['CHEQUENUMBER']!=None:
            c.drawString(75, d, result['CHEQUENUMBER'])
        c.drawString(120, d, result['VCHNO'])
        c.drawString(175, d, result['PARTYNAME'])
        if float(result['PAYMENTAMT']) != 0:
            c.drawAlignedString(400, d, str(locale.currency(float(result['PAYMENTAMT']), grouping=True))[1:])
        if float(result['RECEIPTAMT']) != 0:
            c.drawAlignedString(480, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
        if OpeningBalance > 0:
            c.drawAlignedString(570, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
        else:
            c.drawAlignedString(570, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
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
    Company = ("Beekaylon Group Of Companies ")
    CompanyName.append(Company)

def dlocvalue(d):
    d = d - 10
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global divisioncode
    global pageno
    global bankname
    global CompanyName
    divisioncode = []
    pageno = 0
    bankname=[]
    CompanyName = []
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

def openingbalance(result):
    global OpeningBalance
    OpeningBalance = float(result['OPBAL'])

def textsize(c, result, d, stdt, etdt):
    # date.append(result['VCHDATE'].strftime('%d-%m-%Y'))
    # if str(result['VCHDATE']) != '1980-01-01':
    global OpeningBalance
    global paymentTotal
    global receiptTotal
    # d = newpage()
    d = dvalue()
    logic(result)

    if len(CompanyName)  == 1:
    # if len(divisioncode) == 1:
    #     if len(bankname) ==1:
        # total(result)
        header(stdt, etdt, CompanyName)
        openingbalance(result)
        CompanyAmtClean()
        # d = dvalue()
        fonts(8)
        # if str(result['VCHDATE']) != '1980-01-01':
        #     c.drawString(240, 760, bankname[-1] )

        if float(OpeningBalance) != 0:
            c.drawString(10, d, "Opening Balance" )
            # c.drawAlignedString(510, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
            # c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), 'INR', locale='en_IN'))[1:])
            if OpeningBalance > 0:
                c.drawAlignedString(570, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
            else:
                c.drawAlignedString(570, d, str(format_currency(float(OpeningBalance), ' ', locale='en_IN')))
        # d=dvalue()
        total(result)
        # data(result, d)
        CompanyAmountTotal(result)
        data(result, d)
        # d = dvalue()
    elif CompanyName[-1] == CompanyName[-2]:
    # elif divisioncode[-1] == divisioncode[-2]:
    #     if bankname[-1] == bankname[-2]:
        total(result)
        data(result,d)
        CompanyAmountTotal(result)
        # d = dvalue()

        # elif bankname[-1]!=bankname[-2]:
        #     # fonts(7)
        #     # c.drawString(10, d, str(bankname[-2]) + " TOTAL : ")
        #     # c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
        #     # fonts(7)
        #     # d = dvalue()
        #     # d = dvalue()
        #     c.showPage()
        #     # d = dvalue()
        #     header(stdt, etdt, divisioncode)
        #     d = newpage()
        #     d = dvalue()
        #     openingbalance(result)
        #     fonts(7)
        #     # c.drawString(240, 760, bankname[-1])
        #     d = dvalue()
        #     if float(OpeningBalance) != 0:
        #         c.drawString(10, d, "Opening Balance")
        #         # c.drawAlignedString(510, d, str(locale.currency(float(result['RECEIPTAMT']), grouping=True))[1:])
        #         # c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), 'INR', locale='en_IN'))[1:])
        #         if OpeningBalance > 0:
        #             c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
        #         else:
        #             c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), '- ', locale='en_IN')))
        #     total(result)
        #     # d = dvalue()
        #     CompanyAmountTotal(result)
        #     data(result,d)
            # d = dvalue()


        # if float(result['OPBAL']) > 0:
        #     c.drawString(10, d, "Opening Balance")
        #     c.drawAlignedString(510, d, str(locale.currency(float(result['RECEIPTAMT']), grouping=True))[1:])
        #     c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])

    # elif divisioncode[-1] != divisioncode[-2]:
    # elif CompanyName[-1] != CompanyName[-2]:
    #     # fonts(7)
    #     # if str(result['VCHDATE']) != '1980-01-01':
    #     #     c.drawString(10, d, str(bankname[-2]) + " TOTAL : ")
    #     #     c.drawAlignedString(575, d, str(locale.currency(float(OpeningBalance), grouping=True))[1:])
    #     # companyclean()
    #     c.showPage()
    #
    #     header(stdt, etdt, divisioncode)
    #     d = newpage()
    #     d = dvalue()
    #     #total(result)
    #     openingbalance(result)
    #     fonts(7)
    #     if str(result['VCHDATE']) != '1980-01-01':
    #         c.drawString(240, 760, bankname[-1])
    #
    #     if float (OpeningBalance) != 0:
    #         # (result['OPBAL']) != 0:
    #         c.drawString(10, d, "Opening Balance")
    #         # c.drawAlignedString(510, d, str(locale.currency (float(result['RECEIPTAMT']), grouping=True))[1:])
    #         # c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), 'INR', locale='en_IN'))[1:])
    #         if OpeningBalance > 0:
    #             c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), '', locale='en_IN')))
    #         else:
    #             c.drawAlignedString(575, d, str(format_currency(float(OpeningBalance), '- ', locale='en_IN')))
    #     total(result)
    #     # data(result, d)
    #
    #     data(result, d)
    #     CompanyAmountTotal(result)


    # data(result, d)

    #c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))