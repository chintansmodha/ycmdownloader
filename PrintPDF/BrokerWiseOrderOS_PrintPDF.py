from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
# from GetDataFromDB import BrokerWiseOrderOS_GetDataFromDB
locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 750
new=0
divisioncode = []
party = []
broker = []
pageno = 0
BrokergrpAmountTotal=0
BrokerAmountTotal=0
CompanyAmountTotal=0

BrokergrpInvAmountTotal=0
BrokerInvAmountTotal=0
CompanyInvAmountTotal=0


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
    d = d + 10
    return d


def header(stdt, etdt, result, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, "Beekaylon Group Of Companies")
    boldfonts(9)
    c.drawCentredString(300, 780, "Broker Wise Outstanding From " + str(stdt) + " To " + str(etdt))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    # Upperline in header

    c.drawString(10, 755, "INVNO")
    c.drawString(80, 755, "INVDATE")
    c.drawString(150, 755, "ISS.DATE")
    c.drawString(210, 755, "DAYS")
    c.drawString(290, 755, "O/D")
    c.drawString(370, 755, "INV.AMT")
    c.drawString(450, 755, "OS AMT")
    c.drawString(530, 755, "CUM. AMT")
    fonts(7)


def data(stdt, etdt, result, d):
    fonts(7)
    # Upperline in data
    c.drawString(10, d, result['INVNO'])
    c.drawString(80, d, str(result['DUEDATE'].strftime('%d-%m-%Y')))
    c.drawString(150, d, str(result['ISSUEDATE'].strftime('%d-%m-%Y')))
    # if result['CHALLANDATE'] != None:
    #     c.drawString(210, d, result['CHALLANDATE'].strftime('%d-%m-%Y'))
    c.drawString(290, d, str(result['OD']))
    c.drawAlignedString(400, d, str(result['INVAMT']))
    c.drawAlignedString(490, d, str(result['OSAMT']))
    c.drawAlignedString(580, d, str(result['CUMAMT']))
    divisiontotal(result)
    brokertotal(result)
    brokergrptotal(result)


def brokergrptotal(result):
    global BrokergrpAmountTotal
    global BrokergrpInvAmountTotal
    BrokergrpAmountTotal = BrokergrpAmountTotal + float(("%.2f" % float(result['OSAMT'])))
    BrokergrpInvAmountTotal = BrokergrpInvAmountTotal + float(("%.2f" % float(result['INVAMT'])))


def brokertotal(result):
    global BrokerAmountTotal
    global BrokerInvAmountTotal
    BrokerAmountTotal = BrokerAmountTotal + float(("%.2f" % float(result['OSAMT'])))
    BrokerInvAmountTotal = BrokerInvAmountTotal + float(("%.2f" % float(result['INVAMT'])))


def divisiontotal(result):
    global CompanyAmountTotal
    global CompanyInvAmountTotal
    CompanyAmountTotal = CompanyAmountTotal + float(("%.2f" % float(result['OSAMT'])))
    CompanyInvAmountTotal = CompanyInvAmountTotal + float(("%.2f" % float(result['INVAMT'])))


def printbrokergrptotal():
    boldfonts(7)
    global BrokergrpAmountTotal
    global BrokergrpInvAmountTotal
    c.drawString(150, d, str("Net Outstanding : "))
    c.drawAlignedString(580, d, str(locale.currency(float(BrokergrpAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokergrpInvAmountTotal), grouping=True))[1:])
    BrokergrpAmountTotal = 0
    BrokergrpInvAmountTotal = 0
    fonts(7)


def printdivisiontotal():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyInvAmountTotal
    c.drawString(150, d, str("Total : "))
    c.drawAlignedString(580, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(CompanyInvAmountTotal), grouping=True))[1:])
    fonts(7)


def printbrokertotal():
    boldfonts(7)
    global BrokerAmountTotal
    global BrokerInvAmountTotal
    c.drawString(150, d, "Total Outstanding: ")
    c.drawAlignedString(580, d, str(locale.currency(float(BrokerAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokerInvAmountTotal), grouping=True))[1:])
    BrokerAmountTotal = 0
    BrokerInvAmountTotal = 0
    fonts(7)


def printbrokergrptotallast():
    boldfonts(7)
    global BrokergrpAmountTotal
    global BrokergrpInvAmountTotal
    c.drawString(150, d, "Net Outstanding : ")
    c.drawAlignedString(580, d, str(locale.currency(float(BrokergrpAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokergrpInvAmountTotal), grouping=True))[1:])
    BrokergrpAmountTotal = 0
    BrokergrpInvAmountTotal = 0
    fonts(7)


def printdivisiontotallast():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyInvAmountTotal
    c.drawString(150, d, "Total : ")
    c.drawAlignedString(580, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(CompanyInvAmountTotal), grouping=True))[1:])
    CompanyAmountTotal = 0
    CompanyInvAmountTotal = 0
    fonts(7)


def printbrokertotallast():
    boldfonts(7)
    global BrokerAmountTotal
    global BrokerInvAmountTotal
    c.drawString(150, d, "Total Outstanding : ")
    c.drawAlignedString(580, d, str(locale.currency(float(BrokerAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokerInvAmountTotal), grouping=True))[1:])
    BrokerAmountTotal = 0
    BrokerInvAmountTotal = 0
    fonts(7)

def date(result):
    c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))

def LowerLineData(result, d):
    # Lowerline in data
    fonts(7)
    c.drawString(65, d, result['ITEM'][0:30])
    c.drawAlignedString(310, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawString(350, d, result['UNIT'])



def logic(result):
    divisioncode.append(result['COMPANY'])
    party.append(result['PARTY'])
    broker.append(result['BROKER'])


def dvalue(stdt, etdt, result, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, result, divisioncode)
        return d


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 740
    return d


def newrequest():
    global divisioncode
    global pageno
    global broker
    global brokergrp
    global party
    global new
    new = 0
    party=[]
    divisioncode = []
    pageno = 0
    broker = []
    brokergrp = []


def companyclean():
    global CompanyBillAmtTotal
    global CompanyQuantityTotal
    CompanyBillAmtTotal = 0
    CompanyQuantityTotal = 0


def cleanstore():
    global store
    store = []


def storeclean():
    global StoreBillAmtTotal
    global StoreQuantityTotal
    StoreBillAmtTotal = 0
    StoreQuantityTotal = 0


def textsize(c, result, d, stdt, etdt):
    global new
    global CompanyAmountTotal
    print(result)
    d = dvalue(stdt, etdt, result, divisioncode)
    logic(result)
    if len(broker) == 1:
        if len(divisioncode) == 1:
            if len(party) == 1:
                new = new + round(float(result['INVAMT']), 2)
                result['CUMAMT'] = round(new, 2)
                header(stdt, etdt, result, divisioncode)
                boldfonts(8)
                c.drawCentredString(300, d, broker[-1])
                d = dvalue(stdt, etdt, result, divisioncode)
                boldfonts(8)
                c.drawString(10, d, divisioncode[-1])
                d = dvalue(stdt, etdt, result, divisioncode)
                c.drawString(10, d, party[-1])
                fonts(7)
                d = dvalue(stdt, etdt, result, divisioncode)
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))

    elif broker[-1] == broker[-2]:
        if divisioncode[-1] == divisioncode[-2]:
            if party[-1] == party[-2]:
                new = new + round(float(result['INVAMT']), 2)
                result['CUMAMT'] = round(new, 2)
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))
            elif party[-1] != party[-2]:
                printdivisiontotal()
                # # BrokerWiseOrderOS_GetDataFromDB.netout = 0
                # # printtotal()
                d = dvalue(stdt, etdt,result,divisioncode)
                printbrokergrptotal()
                d = dvalue(stdt, etdt, result, divisioncode)
                boldfonts(8)
                c.drawString(10, d, party[-1])
                fonts(7)
                d = dvalue(stdt, etdt, result, divisioncode)

                new = new + round(float(result['INVAMT']), 2)
                result['CUMAMT'] = round(new, 2)
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))

        elif divisioncode[-1] != divisioncode[-2]:
            # BrokerWiseOrderOS_GetDataFromDB.cumamt - float(netoutlist[-2])
            # printtotal()
            # d = dvalue(stdt, etdt,result,divisioncode)
            # # printnetout()
            # d = dvalue(stdt, etdt,result,divisioncode)
            # printtotalout()
            printdivisiontotal()
            # # BrokerWiseOrderOS_GetDataFromDB.netout = 0
            # # printtotal()
            d = dvalue(stdt, etdt, result, divisioncode)
            printbrokergrptotal()
            d = dvalue(stdt, etdt, result, divisioncode)
            boldfonts(8)
            c.drawString(10, d, divisioncode[-1])
            d = dvalue(stdt, etdt, result, divisioncode)
            c.drawString(10, d, party[-1])
            d = dvalue(stdt, etdt, result, divisioncode)
            data(stdt, etdt, result, d)

    elif broker[-1] != broker[-2]:
        boldfonts(8)
        printdivisiontotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        printbrokergrptotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        printbrokertotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        CompanyAmountTotal=0
        c.showPage()
        header(stdt, etdt, result, divisioncode)
        d = newpage()
        boldfonts(8)
        c.drawCentredString(300, d, broker[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        boldfonts(8)
        c.drawString(10, d, divisioncode[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        c.drawString(10, d, party[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        fonts(7)
        new = 0
        new = new + round(float(result['INVAMT']), 2)
        result['CUMAMT'] = round(new, 2)
        data(stdt, etdt, result, d)
        # c.drawAlignedString(560, d, str(round(float(result['CUMAMTT']) - float(netoutlist[-2]), 3)))
