from reportlab.lib.pagesizes import portrait,A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import textwrap
# from GetDataFromDB import BrokerGroupCompanyWiseOS_GetDataFromDB as BGC_Views
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(portrait(A5)))
c.setPageSize(portrait(A5))
d = 730
no=0
new=0
brokergrp=[]
broker=[]
divisioncode=[]
invno=[]
pageno=0
count=0

BrokergrpAmountTotal=0
BrokerAmountTotal=0
CompanyAmountTotal=0

BrokergrpInvAmountTotal=0
BrokerInvAmountTotal=0
CompanyInvAmountTotal=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt, etdt,result,divisioncode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,result,divisioncode)
        return d

def header(stdt,etdt,result,divisioncode):
    d=670
    global pan
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, "Beekaylon Group Of Companies")
    fonts(12)
    c.drawCentredString(300, 780, str("Broker Group-Company Wise Outstanding Details From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y'))))
    # p = page()
    # c.drawString(700, 760, "Page No." + str(p))
    fonts(9)
    c.drawString(10, 780, str(etdt.strftime('%d-%m-%Y')))
    c.line(0, 760, 1190, 760)
    c.line(0, 740, 1190, 740)
    c.drawString(10,750,str("NO."))
    c.drawString(40, 750, str("INV NO."))
    c.drawString(90, 750, str("ISSUE DATE."))
    c.drawString(160, 750, str("DAYS"))
    c.drawString(220, 750, str("PARTY"))
    c.drawString(350, 750, str("O/D"))
    c.drawString(380, 750, str("INV. AMOUNT"))
    c.drawString(450, 750, str("OS. AMOUNT"))
    c.drawString(520, 750, str("CUMM. AMOUNT"))


def data(stdt,etdt,result,d):
    global no
    no=no+1
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(no))
    c.drawString(40, d, str(result['INVNO']))
    c.drawString(90, d, str(result['ISSUEDATE']))
    c.drawString(160, d, str(result['DAYS']))
    c.drawAlignedString(365, d, str(result['OD']))
    c.drawAlignedString(420, d, str(result['INVAMT']))
    c.drawAlignedString(500, d, str(result['OSAMT']))
    c.drawAlignedString(580, d, str("%.2f" )% float(result['CUMAMT']))
    # c.drawString(220, d, str(result['PARTY']))
    if len(str(result['PARTY']))>50:
        lines = textwrap.wrap(str(result['PARTY']), 50, break_long_words=False)
        for i in lines:
            c.drawString(200, d, str(i))
            d = dvalue(stdt, etdt, result, divisioncode)
    else:
        c.drawString(200, d, str(result['PARTY']))
        d = dvalue(stdt, etdt, result, divisioncode)
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
    c.drawString(220, d, str(brokergrp[-2]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(locale.currency(float(BrokergrpAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokergrpInvAmountTotal), grouping=True))[1:])
    BrokergrpAmountTotal = 0
    BrokergrpInvAmountTotal = 0
    fonts(7)

def printdivisiontotal():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyInvAmountTotal
    c.drawString(220, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(CompanyInvAmountTotal), grouping=True))[1:])
    CompanyAmountTotal = 0
    CompanyInvAmountTotal = 0
    fonts(7)

def printbrokertotal():
    boldfonts(7)
    global BrokerAmountTotal
    global  BrokerInvAmountTotal
    c.drawString(220, d, str(broker[-2]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(locale.currency(float(BrokerAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokerInvAmountTotal), grouping=True))[1:])
    BrokerAmountTotal = 0
    BrokerInvAmountTotal = 0
    fonts(7)

def printbrokergrptotallast():
    boldfonts(7)
    global BrokergrpAmountTotal
    global BrokergrpInvAmountTotal
    c.drawString(220, d, str(brokergrp[-1]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(locale.currency(float(BrokergrpAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(BrokergrpInvAmountTotal), grouping=True))[1:])
    BrokergrpAmountTotal = 0
    BrokergrpInvAmountTotal = 0
    fonts(7)

def printdivisiontotallast():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyInvAmountTotal
    c.drawString(220, d, str(divisioncode[-1]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    # c.drawAlignedString(340, d, str(locale.currency(float(CompanyInvAmountTotal), grouping=True))[1:])
    CompanyAmountTotal = 0
    CompanyInvAmountTotal = 0
    fonts(7)

def printbrokertotallast():
    boldfonts(7)
    global BrokerAmountTotal
    global  BrokerInvAmountTotal
    c.drawString(220, d, str(broker[-1]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(locale.currency(float(BrokerAmountTotal), grouping=True))[1:])
    c.drawAlignedString(340, d, str(locale.currency(float(BrokerInvAmountTotal), grouping=True))[1:])
    BrokerAmountTotal = 0
    BrokerInvAmountTotal = 0
    fonts(7)

def logic(result):
    brokergrp.append(result['BROKERGROUP'])
    broker.append(result['BROKER'])
    divisioncode.append(result['COMPANY'])
    invno.append(result['INVNO'])

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global brokergrp
    global broker
    global divisioncode
    global invno
    global pageno
    global no
    global new
    brokergrp = []
    broker = []
    divisioncode=[]
    invno=[]
    pageno=0
    no = 0
    new = 0
def textsize(c, result, d, stdt, etdt):
    global new
    print(result)
    d = dvalue(stdt, etdt,result,divisioncode)
    logic(result)
    if len(brokergrp) == 1:
        if len(broker) == 1:
            if len(divisioncode) == 1:
                new = new +float(result['INVAMT'])
                result['CUMAMT'] = new
                header(stdt,etdt,result,divisioncode)
                boldfonts(10)
                c.drawCentredString(300, d, brokergrp[-1])
                d = dvalue(stdt, etdt,result,divisioncode)
                boldfonts(8)
                c.drawString(10, d, broker[-1])
                d = dvalue(stdt, etdt,result,divisioncode)
                c.drawString(10, d, divisioncode[-1])
                fonts(7)
                d = dvalue(stdt, etdt,result,divisioncode)
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))

    elif brokergrp[-1] == brokergrp[-2]:
        if broker[-1] == broker[-2]:
            if divisioncode[-1] == divisioncode[-2]:
                new = new + float(result['INVAMT'])
                result['CUMAMT'] = new
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))
            elif divisioncode[-1] != divisioncode[-2]:
                printdivisiontotal()
                # # BrokerWiseOrderOS_GetDataFromDB.netout = 0
                # # printtotal()
                # d = dvalue(stdt, etdt,result,divisioncode)
                # # printnetout()
                d = dvalue(stdt, etdt,result,divisioncode)
                boldfonts(8)
                c.drawString(10, d, divisioncode[-1])
                fonts(7)
                d = dvalue(stdt, etdt,result,divisioncode)
                new = 0
                new = new + float(result['INVAMT'])
                result['CUMAMT'] = new
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))

        elif broker[-1] != broker[-2]:
            # BrokerWiseOrderOS_GetDataFromDB.cumamt - float(netoutlist[-2])
            # printtotal()
            # d = dvalue(stdt, etdt,result,divisioncode)
            # # printnetout()
            # d = dvalue(stdt, etdt,result,divisioncode)
            # printtotalout()
            printdivisiontotal()
            d = dvalue(stdt, etdt,result,divisioncode)
            printbrokertotal()
            boldfonts(8)
            c.drawString(10, d, broker[-1])
            d = dvalue(stdt, etdt, result, divisioncode)
            c.drawString(10, d, divisioncode[-1])
            d = dvalue(stdt, etdt,result,divisioncode)
            if divisioncode[-1] == divisioncode[-2]:
                new = 0
                new = new + float(result['INVAMT'])
                result['CUMAMT'] = new
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))
            elif divisioncode[-1] != divisioncode[-2]:
                printdivisiontotal()
                # # BrokerWiseOrderOS_GetDataFromDB.netout = 0
                # # printtotal()
                # d = dvalue(stdt, etdt,result,divisioncode)
                # # printnetout()
                new = 0
                new = new + float(result['INVAMT'])
                result['CUMAMT'] = new
                d = dvalue(stdt, etdt, result, divisioncode)
                boldfonts(8)
                c.drawString(10, d, divisioncode[-1])
                fonts(7)
                d = dvalue(stdt, etdt, result, divisioncode)
                data(stdt, etdt, result, d)

    elif brokergrp[-1] != brokergrp[-2]:
        boldfonts(8)
        printdivisiontotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        printbrokertotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        printbrokergrptotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        boldfonts(8)
        c.drawCentredString(300, d, brokergrp[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        boldfonts(8)
        c.drawString(10, d, broker[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        c.drawString(10, d, divisioncode[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        fonts(7)
        new = 0
        new = new + float(result['INVAMT'])
        result['CUMAMT'] = new
        data(stdt, etdt, result, d)
        # c.drawAlignedString(560, d, str(round(float(result['CUMAMTT']) - float(netoutlist[-2]), 3)))
