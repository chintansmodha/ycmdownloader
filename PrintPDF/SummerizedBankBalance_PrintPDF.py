from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
from . import SummerizedBankBalance_SubQueries as SubQueries
from ProcessSelection import SummerizedBankBalance_ProcessSelection as SBBV
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d =770

divisioncode = []
bankname = []
pageno = 0
OpenBalTotal = 0
ReceiptTotal = 0
PaymentTotal = 0
ClBalTotal = 0

GrandOpenBalTotal = 0
GrandReceiptTotal = 0
GrandPaymentTotal = 0
GrandClBalTotal = 0

ClosingBalance = 0
def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def dvaluegst():
    global d
    d = d - 5
    return d

def dv():
    global d
    d = d - 10
    return d

def company(divisioncode,d):
    boldfonts(7)
    # c.line(0, d, 600, d)
    c.drawString(10, d, divisioncode[-1])
    c.line(0, d-10, 600, d-10)
    fonts(7)

def header(stdt, etdt, divisioncode):
    c.setFillColorRGB(0, 0, 0)
    boldfonts(7)
    c.drawCentredString(300, 820, "Summarized Bank Balance For: " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 820, "Page No." + str(p))
    c.line(0, 800, 600, 800)
    c.line(0, 780, 600, 780)
    # Upperline in header

    c.drawString(10, 790, "Bank")
    c.line(160, 800, 160, 780)
    c.drawString(170, 790, "OP Balance")
    c.line(210, 800, 210, 780)
    c.drawString(280, 790, "               ")
    c.line(330, 800, 330, 780)
    c.drawString(360, 790, "Receipt")
    c.line(390, 800, 390, 780)
    c.drawString(430, 790, "               ")
    c.line(470, 800, 470, 780)
    c.drawString(500, 790, "Payment")
    c.line(535,800,535,780)
    c.drawString(550, 790, "CL Balance")

def data(stdt, etdt, result, d):
    fonts(7)
    # Upperline in data
    c.line(160, d+10, 160, d-20)
    c.line(210, d + 10, 210, d - 20)
    c.line(330, d + 10, 330, d - 20)

    c.line(390, d + 10, 390, d - 20)
    c.line(470, d + 10, 470, d - 20)
    c.drawString(395, d, result['PAIDTO'][:16])
    c.drawString(215, d, result['RECIEVEDFROM'][:36])
    if float(result['RECEIPTS']) != 0:
        printnonzeroreceipt(result)
    if float(result['PAYMENTS']) != 0:
        printnonzeropayment(result)
    c.line(535, d + 10, 535, d - 20)
    # total(result)

def printnonzeroreceipt(result):
    c.drawAlignedString(375, d,
                        str(format_currency(("%.2f" % float(result['RECEIPTS'])), 'INR', locale='en_IN')).replace('₹',
                                                                                                                  ''))

def printnonzeropayment(result):
    c.drawAlignedString(520, d,
                        str(format_currency(("%.2f" % float(result['PAYMENTS'])), 'INR', locale='en_IN')).replace('₹',
                                                                                                                  ''))

def printbank(result):
    fonts(7)
    c.drawString(10, d, result['BANKNAME'])
    c.drawAlignedString(200, d,
                        str(format_currency(("%.2f" % float(result['OPBAL'])), 'INR', locale='en_IN')).replace('₹', ''))
    c.drawAlignedString(580, d,
                        str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹', ''))
    total(result)

def printname(result):
    c.drawString(395, d, result['PAIDTO'][:16])
    c.drawString(215, d, result['RECIEVEDFROM'][:36])


def total(result):
    global OpenBalTotal
    global ReceiptTotal
    global PaymentTotal
    global ClBalTotal
    global GrandOpenBalTotal
    global GrandReceiptTotal
    global GrandPaymentTotal
    global GrandClBalTotal
    OpenBalTotal = OpenBalTotal + float(("%.2f" % float(result['OPBAL'])))
    ReceiptTotal = ReceiptTotal + float(("%.2f" % float(result['RECEIPTS'])))
    PaymentTotal = PaymentTotal + float(("%.2f" % float(result['PAYMENTS'])))
    ClBalTotal = ClBalTotal + float(("%.2f" % float(result['OPBAL'])))

    GrandOpenBalTotal = GrandOpenBalTotal + float(("%.2f" % float(result['OPBAL'])))
    GrandReceiptTotal = GrandReceiptTotal + float(("%.2f" % float(result['RECEIPTS'])))
    GrandPaymentTotal = GrandPaymentTotal + float(("%.2f" % float(result['PAYMENTS'])))
    GrandClBalTotal = GrandClBalTotal + float(("%.2f" % float(result['OPBAL'])))

def logic(result):
    divisioncode.append(result['BUSINESSUNITNAME'])
    bankname.append(result['BANKNAME'])

def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, divisioncode[:-1])
        return d

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 770
    return d

def newrequest():
    global divisioncode
    global pageno
    global  bankname
    global GrandOpenBalTotal
    global GrandReceiptTotal
    global GrandPaymentTotal
    global GrandClBalTotal
    global ClosingBalance
    divisioncode = []
    bankname=[]
    pageno = 0
    ClosingBalance = 0
    GrandOpenBalTotal = 0
    GrandReceiptTotal = 0
    GrandPaymentTotal = 0
    GrandClBalTotal = 0

def printtotal(stdt, etdt, divisioncode,d):
    boldfonts(7)
    c.line(0, d, 600, d)
    d=dvalue(stdt,etdt,divisioncode)
    fonts(7)
    global OpenBalTotal
    global ReceiptTotal
    global PaymentTotal
    global ClBalTotal

    boldfonts(7)
    c.drawString(10, d, "Company TOTAL : ")
    c.drawAlignedString(200, d, str(format_currency(OpenBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
    c.drawAlignedString(375, d, str(format_currency(ReceiptTotal, 'INR', locale='en_IN')).replace('₹', ''))
    c.drawAlignedString(520, d, str(format_currency(PaymentTotal, 'INR', locale='en_IN')).replace('₹', ''))
    ClBalTotal=(OpenBalTotal+ReceiptTotal)-PaymentTotal

    c.drawAlignedString(580, d, str(format_currency(ClBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
    c.line(160, d + 10, 160, d - 10)
    c.line(210, d + 10, 210, d - 10)
    c.line(330, d + 10, 330, d - 10)
    c.line(390, d + 10, 390, d - 10)
    c.line(470, d + 10, 470, d - 10)
    c.line(535, d + 10, 535, d - 10)

    d = dvalue(stdt, etdt, divisioncode)
    fonts(7)
    c.line(0, d, 600, d)


def printgrandtotal(stdt, etdt, divisioncode,d):
    boldfonts(7)
    c.line(0, d, 600, d)
    d=dvalue(stdt,etdt,divisioncode)
    fonts(7)
    global GrandOpenBalTotal
    global GrandReceiptTotal
    global GrandPaymentTotal
    global GrandClBalTotal
    boldfonts(7)
    c.drawString(10, d, "Grand TOTAL : ")
    c.drawAlignedString(200, d, str(format_currency(GrandOpenBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
    c.drawAlignedString(375, d, str(format_currency(GrandReceiptTotal, 'INR', locale='en_IN')).replace('₹', ''))
    c.drawAlignedString(520, d, str(format_currency(GrandPaymentTotal, 'INR', locale='en_IN')).replace('₹', ''))
    GrandClBalTotal= (GrandOpenBalTotal+GrandReceiptTotal)-GrandPaymentTotal
    c.drawAlignedString(580, d, str(format_currency(GrandClBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
    d = dvalue(stdt, etdt, divisioncode)
    fonts(7)
    c.line(0, d, 600, d)
    c.line(0, d-3, 600, d-3)

def companyclean():
    global OpenBalTotal
    global PaymentTotal
    global ReceiptTotal
    global ClBalTotal
    OpenBalTotal = 0
    PaymentTotal = 0
    ReceiptTotal = 0
    ClBalTotal = 0

def ClBal(result):
    global ClosingBalance
    ClosingBalance = ClosingBalance + float(result['OPBAL']) + float(result['RECEIPTS']) - float(result['PAYMENTS'])
    return ClosingBalance

def cleanClBal():
    global ClosingBalance
    ClosingBalance = 0

def textsize(c, result, d, stdt, etdt):
    logic(result)
    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        company(divisioncode,d)
        d = dvalue(stdt, etdt, divisioncode)
        boldfonts(7)
        fonts(7)
        d = dvalue(stdt, etdt, divisioncode)
        printbank(result)
        if float(result['RECEIPTS']) == 0:
            printnonzeroreceipt(result)
        if float(result['PAYMENTS']) == 0:
            printnonzeropayment(result)
        #c.drawAlignedString(580, d,str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹',''))
        #d = dvalue(stdt, etdt, divisioncode)
        recive=SubQueries.RecievedFrom(SBBV.LDStartDate,SBBV.LDEndDate,str(result['CODE']),str(result['BANKCODE']),c,d)
        paid=SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c, d)
        if len(recive) > len(paid):
            jsm = len(recive)
        else:
            jsm = len(paid)
        for i in range(jsm):
            if i < len(recive):
                data(stdt, etdt, recive[i], d)
            if i < len(paid):
                data(stdt, etdt, paid[i], d)
            d = dvalue(stdt, etdt, divisioncode)


    elif divisioncode[-1] == divisioncode[-2]:
        if bankname[-1]==bankname[-2]:
            fonts(7)
            # c.drawAlignedString(580, d,
            #                      str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace(
            #                          '₹', ''))

            recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
                                             str(result['BANKCODE']), c, d)
            paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
                                     d)
            if len(recive) > len(paid):
                jsm = len(recive)
            else:
                jsm = len(paid)
            for i in range(jsm):
                if i < len(recive):
                    data(stdt, etdt, recive[i], d)
                if i < len(paid):
                    data(stdt, etdt, paid[i], d)
                d = dvalue(stdt, etdt, divisioncode)


        elif bankname[-1]!=bankname[-2]:
            cleanClBal()
            c.line(0,d+5,600,d+5)
            d = dvaluegst()
            printbank(result)
            if float(result['RECEIPTS']) == 0:
                printnonzeroreceipt(result)
            if float(result['PAYMENTS']) == 0:
                printnonzeropayment(result)
            fonts(7)
            # c.drawAlignedString(580, d,str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹', ''))
            data(stdt, etdt, result, d)
            d = dvalue(stdt, etdt, divisioncode)
            recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
                                             str(result['BANKCODE']), c, d)
            paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
                                     d)

            if len(recive) > len(paid):
                jsm = len(recive)
            else:
                jsm = len(paid)
            for i in range(jsm):
                if i < len(recive):
                    data(stdt, etdt, recive[i], d)

                if i < len(paid):
                    data(stdt, etdt, paid[i], d)

                d = dvalue(stdt, etdt, divisioncode)
    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        c.line(0, d, 600, d)
        printtotal(stdt,etdt,divisioncode,d)
        companyclean()
        d = dvalue(stdt, etdt, divisioncode)
        company(divisioncode,d)
        d=dvalue(stdt, etdt, divisioncode)
        if bankname[-1] == bankname[-2]:
            fonts(7)
            # c.drawAlignedString(580, d,
            #                      str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace(
            #                          '₹', ''))

            recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
                                             str(result['BANKCODE']), c, d)
            paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
                                     d)
            if len(recive) > len(paid):
                jsm = len(recive)
            else:
                jsm = len(paid)
            for i in range(jsm):
                if i < len(recive):
                    data(stdt, etdt, recive[i], d)
                if i < len(paid):
                    data(stdt, etdt, paid[i], d)
                d = dvalue(stdt, etdt, divisioncode)


        elif bankname[-1] != bankname[-2]:
            cleanClBal()
            c.line(0, d + 5, 600, d + 5)
            d = dvalue(stdt, etdt, divisioncode)
            printbank(result)
            if float(result['RECEIPTS']) == 0:
                printnonzeroreceipt(result)
            if float(result['PAYMENTS']) == 0:
                printnonzeropayment(result)
            fonts(7)
            # c.drawAlignedString(580, d,str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹', ''))
            data(stdt, etdt, result, d)
            d = dvalue(stdt, etdt, divisioncode)
            recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
                                             str(result['BANKCODE']), c, d)
            paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
                                     d)

            if len(recive) > len(paid):
                jsm = len(recive)
            else:
                jsm = len(paid)
            for i in range(jsm):
                if i < len(recive):
                    data(stdt, etdt, recive[i], d)

                if i < len(paid):
                    data(stdt, etdt, paid[i], d)

                d = dvalue(stdt, etdt, divisioncode)

# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas
# from babel.numbers import format_currency
# from . import SummerizedBankBalance_SubQueries as SubQueries
# from ProcessSelection import SummerizedBankBalance_ProcessSelection as SBBV
# pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
# pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
#
# c = canvas.Canvas("1.pdf")
# d =770
#
# divisioncode = []
# bankname = []
# pageno = 0
# OpenBalTotal = 0
# ReceiptTotal = 0
# PaymentTotal = 0
# ClBalTotal = 0
#
# GrandOpenBalTotal = 0
# GrandReceiptTotal = 0
# GrandPaymentTotal = 0
# GrandClBalTotal = 0
#
# ClosingBalance = 0
# def boldfonts(size):
#     global c
#     c.setFont("MyOwnArialBold", size)
#
#
# def fonts(size):
#     global c
#     c.setFont("MyOwnArial", size)
#
# def page():
#     global pageno
#     pageno = pageno + 1
#     return pageno
#
# def dvaluegst():
#     global d
#     d = d - 5
#     return d
#
# def dv():
#     global d
#     d = d - 10
#     return d
#
# def company(divisioncode,d):
#     boldfonts(7)
#     # c.line(0, d, 600, d)
#     c.drawString(10, d, divisioncode[-1])
#     c.line(0, d-10, 600, d-10)
#     fonts(7)
#
# def header(stdt, etdt, divisioncode):
#     c.setFillColorRGB(0, 0, 0)
#     boldfonts(7)
#     c.drawCentredString(300, 820, "Summarized Bank Balance For: " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
#         etdt.strftime('%d-%m-%Y')))
#     p = page()
#     c.drawString(540, 820, "Page No." + str(p))
#     c.line(0, 800, 600, 800)
#     c.line(0, 780, 600, 780)
#     # Upperline in header
#
#     c.drawString(10, 790, "Bank")
#     c.line(160, 800, 160, 780)
#     c.drawString(170, 790, "OP Balance")
#     c.line(210, 800, 210, 780)
#     c.drawString(280, 790, "               ")
#     c.line(330, 800, 330, 780)
#     c.drawString(360, 790, "Receipt")
#     c.line(390, 800, 390, 780)
#     c.drawString(430, 790, "               ")
#     c.line(470, 800, 470, 780)
#     c.drawString(500, 790, "Payment")
#     c.line(535,800,535,780)
#     c.drawString(550, 790, "CL Balance")
#
# def data(stdt, etdt, result, d):
#     fonts(7)
#     # Upperline in data
#     c.line(160, d+10, 160, d-20)
#     c.line(210, d + 10, 210, d - 20)
#     c.line(330, d + 10, 330, d - 20)
#
#     c.line(390, d + 10, 390, d - 20)
#     c.line(470, d + 10, 470, d - 20)
#     c.drawString(395, d, result['PAIDTO'][:16])
#     c.drawString(215, d, result['RECIEVEDFROM'][:36])
#     if float(result['RECEIPTS']) != 0:
#         printnonzeroreceipt(result)
#     if float(result['PAYMENTS']) != 0:
#         printnonzeropayment(result)
#     c.line(535, d + 10, 535, d - 20)
#     total(result)
#
# def printnonzeroreceipt(result):
#     c.drawAlignedString(375, d,
#                         str(format_currency(("%.2f" % float(result['RECEIPTS'])), 'INR', locale='en_IN')).replace('₹',
#                                                                                                                   ''))
#
# def printnonzeropayment(result):
#     c.drawAlignedString(520, d,
#                         str(format_currency(("%.2f" % float(result['PAYMENTS'])), 'INR', locale='en_IN')).replace('₹',
#                                                                                                                   ''))
#
# def printbank(result):
#     fonts(7)
#     c.drawString(10, d, result['BANKNAME'])
#     c.drawAlignedString(200, d,
#                         str(format_currency(("%.2f" % float(result['OPBAL'])), 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(580, d,
#                         str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹', ''))
#
#
# def printname(result):
#     c.drawString(395, d, result['PAIDTO'][:16])
#     c.drawString(215, d, result['RECIEVEDFROM'][:36])
#
#
# def total(result):
#     global OpenBalTotal
#     global ReceiptTotal
#     global PaymentTotal
#     global ClBalTotal
#     global GrandOpenBalTotal
#     global GrandReceiptTotal
#     global GrandPaymentTotal
#     global GrandClBalTotal
#     OpenBalTotal = OpenBalTotal + float(("%.2f" % float(result['OPBAL'])))
#     ReceiptTotal = ReceiptTotal + float(("%.2f" % float(result['RECEIPTS'])))
#     PaymentTotal = PaymentTotal + float(("%.2f" % float(result['PAYMENTS'])))
#     ClBalTotal = ClBalTotal + float(("%.2f" % float(result['OPBAL'])))
#
#     GrandOpenBalTotal = GrandOpenBalTotal + float(("%.2f" % float(result['OPBAL'])))
#     GrandReceiptTotal = GrandReceiptTotal + float(("%.2f" % float(result['RECEIPTS'])))
#     GrandPaymentTotal = GrandPaymentTotal + float(("%.2f" % float(result['PAYMENTS'])))
#     GrandClBalTotal = GrandClBalTotal + float(("%.2f" % float(result['OPBAL'])))
#
# def logic(result):
#     divisioncode.append(result['BUSINESSUNITNAME'])
#     bankname.append(result['BANKNAME'])
#
# def dvalue(stdt, etdt, divisioncode):
#     global d
#     if d > 20:
#         d = d - 10
#         return d
#     else:
#         d = newpage()
#         c.showPage()
#         header(stdt, etdt, divisioncode[:-1])
#         return d
#
# def dlocvalue(d):
#     d = d - 20
#     return d
#
# def newpage():
#     global d
#     d = 770
#     return d
#
# def newrequest():
#     global divisioncode
#     global pageno
#     global  bankname
#     global GrandOpenBalTotal
#     global GrandReceiptTotal
#     global GrandPaymentTotal
#     global GrandClBalTotal
#     global ClosingBalance
#     divisioncode = []
#     bankname=[]
#     pageno = 0
#     ClosingBalance = 0
#     GrandOpenBalTotal = 0
#     GrandReceiptTotal = 0
#     GrandPaymentTotal = 0
#     GrandClBalTotal = 0
#
# def printtotal(stdt, etdt, divisioncode,d):
#     boldfonts(7)
#     c.line(0, d, 600, d)
#     d=dvalue(stdt,etdt,divisioncode)
#     fonts(7)
#     global OpenBalTotal
#     global ReceiptTotal
#     global PaymentTotal
#     global ClBalTotal
#     boldfonts(7)
#     c.drawString(10, d, "Company TOTAL : ")
#     c.drawAlignedString(200, d, str(format_currency(OpenBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(375, d, str(format_currency(ReceiptTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(520, d, str(format_currency(PaymentTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(580, d, str(format_currency(ClBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.line(160, d + 10, 160, d - 10)
#     c.line(210, d + 10, 210, d - 10)
#     c.line(330, d + 10, 330, d - 10)
#     c.line(390, d + 10, 390, d - 10)
#     c.line(470, d + 10, 470, d - 10)
#     c.line(535, d + 10, 535, d - 10)
#
#     d = dvalue(stdt, etdt, divisioncode)
#     fonts(7)
#     c.line(0, d, 600, d)
#
#
# def printgrandtotal(stdt, etdt, divisioncode,d):
#     boldfonts(7)
#     c.line(0, d, 600, d)
#     d=dvalue(stdt,etdt,divisioncode)
#     fonts(7)
#     global GrandOpenBalTotal
#     global GrandReceiptTotal
#     global GrandPaymentTotal
#     global GrandClBalTotal
#     boldfonts(7)
#     c.drawString(10, d, "Grand TOTAL : ")
#     c.drawAlignedString(200, d, str(format_currency(GrandOpenBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(375, d, str(format_currency(GrandReceiptTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(520, d, str(format_currency(GrandPaymentTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     c.drawAlignedString(580, d, str(format_currency(GrandClBalTotal, 'INR', locale='en_IN')).replace('₹', ''))
#     d = dvalue(stdt, etdt, divisioncode)
#     fonts(7)
#     c.line(0, d, 600, d)
#     c.line(0, d-3, 600, d-3)
#
# def companyclean():
#     global OpenBalTotal
#     global PaymentTotal
#     global ReceiptTotal
#     global ClBalTotal
#     OpenBalTotal = 0
#     PaymentTotal = 0
#     ReceiptTotal = 0
#     ClBalTotal = 0
#
# def ClBal(result):
#     global ClosingBalance
#     ClosingBalance = ClosingBalance + float(result['OPBAL']) + float(result['RECEIPTS']) - float(result['PAYMENTS'])
#     return ClosingBalance
#
# def cleanClBal():
#     global ClosingBalance
#     ClosingBalance = 0
#
# def textsize(c, result, d, stdt, etdt):
#     logic(result)
#     if len(divisioncode) == 1:
#         header(stdt, etdt, divisioncode)
#         company(divisioncode,d)
#         d = dvalue(stdt, etdt, divisioncode)
#         boldfonts(7)
#         fonts(7)
#         d = dvalue(stdt, etdt, divisioncode)
#         printbank(result)
#         if float(result['RECEIPTS']) == 0:
#             printnonzeroreceipt(result)
#         if float(result['PAYMENTS']) == 0:
#             printnonzeropayment(result)
#         #c.drawAlignedString(580, d,str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹',''))
#         #d = dvalue(stdt, etdt, divisioncode)
#         recive=SubQueries.RecievedFrom(SBBV.LDStartDate,SBBV.LDEndDate,str(result['CODE']),str(result['BANKCODE']),c,d)
#         paid=SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c, d)
#         if len(recive) > len(paid):
#             jsm = len(recive)
#         else:
#             jsm = len(paid)
#         for i in range(jsm):
#             if i < len(recive):
#                 data(stdt, etdt, recive[i], d)
#             if i < len(paid):
#                 data(stdt, etdt, paid[i], d)
#             d = dvalue(stdt, etdt, divisioncode)
#
#
#     elif divisioncode[-1] == divisioncode[-2]:
#         if bankname[-1]==bankname[-2]:
#             fonts(7)
#             # c.drawAlignedString(580, d,
#             #                      str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace(
#             #                          '₹', ''))
#
#             recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
#                                              str(result['BANKCODE']), c, d)
#             paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
#                                      d)
#             if len(recive) > len(paid):
#                 jsm = len(recive)
#             else:
#                 jsm = len(paid)
#             for i in range(jsm):
#                 if i < len(recive):
#                     data(stdt, etdt, recive[i], d)
#                 if i < len(paid):
#                     data(stdt, etdt, paid[i], d)
#                 d = dvalue(stdt, etdt, divisioncode)
#
#
#         elif bankname[-1]!=bankname[-2]:
#             cleanClBal()
#             c.line(0,d+5,600,d+5)
#             d = dvaluegst()
#             printbank(result)
#             if float(result['RECEIPTS']) == 0:
#                 printnonzeroreceipt(result)
#             if float(result['PAYMENTS']) == 0:
#                 printnonzeropayment(result)
#             fonts(7)
#             # c.drawAlignedString(580, d,str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹', ''))
#             data(stdt, etdt, result, d)
#             d = dvalue(stdt, etdt, divisioncode)
#             recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
#                                              str(result['BANKCODE']), c, d)
#             paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
#                                      d)
#
#             if len(recive) > len(paid):
#                 jsm = len(recive)
#             else:
#                 jsm = len(paid)
#             for i in range(jsm):
#                 if i < len(recive):
#                     data(stdt, etdt, recive[i], d)
#
#                 if i < len(paid):
#                     data(stdt, etdt, paid[i], d)
#
#                 d = dvalue(stdt, etdt, divisioncode)
#     elif divisioncode[-1] != divisioncode[-2]:
#         fonts(7)
#         c.line(0, d, 600, d)
#         printtotal(stdt,etdt,divisioncode,d)
#         companyclean()
#         d = dvalue(stdt, etdt, divisioncode)
#         company(divisioncode,d)
#         d=dvalue(stdt, etdt, divisioncode)
#         if bankname[-1] == bankname[-2]:
#             fonts(7)
#             # c.drawAlignedString(580, d,
#             #                      str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace(
#             #                          '₹', ''))
#
#             recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
#                                              str(result['BANKCODE']), c, d)
#             paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
#                                      d)
#             if len(recive) > len(paid):
#                 jsm = len(recive)
#             else:
#                 jsm = len(paid)
#             for i in range(jsm):
#                 if i < len(recive):
#                     data(stdt, etdt, recive[i], d)
#                 if i < len(paid):
#                     data(stdt, etdt, paid[i], d)
#                 d = dvalue(stdt, etdt, divisioncode)
#
#
#         elif bankname[-1] != bankname[-2]:
#             cleanClBal()
#             c.line(0, d + 5, 600, d + 5)
#             d = dvalue(stdt, etdt, divisioncode)
#             printbank(result)
#             if float(result['RECEIPTS']) == 0:
#                 printnonzeroreceipt(result)
#             if float(result['PAYMENTS']) == 0:
#                 printnonzeropayment(result)
#             fonts(7)
#             # c.drawAlignedString(580, d,str(format_currency(("%.2f" % float(ClBal(result))), 'INR', locale='en_IN')).replace('₹', ''))
#             data(stdt, etdt, result, d)
#             d = dvalue(stdt, etdt, divisioncode)
#             recive = SubQueries.RecievedFrom(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']),
#                                              str(result['BANKCODE']), c, d)
#             paid = SubQueries.PaidTo(SBBV.LDStartDate, SBBV.LDEndDate, str(result['CODE']), str(result['BANKCODE']), c,
#                                      d)
#
#             if len(recive) > len(paid):
#                 jsm = len(recive)
#             else:
#                 jsm = len(paid)
#             for i in range(jsm):
#                 if i < len(recive):
#                     data(stdt, etdt, recive[i], d)
#
#                 if i < len(paid):
#                     data(stdt, etdt, paid[i], d)
#
#                 d = dvalue(stdt, etdt, divisioncode)