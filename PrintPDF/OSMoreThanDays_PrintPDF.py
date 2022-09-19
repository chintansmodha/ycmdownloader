from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
from GetDataFromDB import OSMoreThanDays_GetDataFromDB
locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 750
divisioncode = []
brokergrp = []
broker = []
store = []
mrnno = []
pageno = 0
CompanyBillAmtTotal = 0
StoreBillAmtTotal = 0
CompanyQuantityTotal = 0
StoreQuantityTotal = 0
cumamtlist=[]
new = 0
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


def header(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Broker Wise More Than " + str(OSMoreThanDays_GetDataFromDB.day[-1]) + " Days")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    # Upperline in header

    c.drawString(10, 755, "INVNO")
    c.drawString(60, 755, "ISS.DATE")
    c.drawString(110, 755, "DAYS")
    c.drawString(150, 755, "O/D")
    c.drawString(180, 755, "PARTY")
    c.drawString(370, 755, "INV.AMT")
    c.drawString(450, 755, "OS AMT")
    c.drawString(530, 755, "CUM. AMT")
    fonts(7)


def data(stdt, etdt, result, d):
    fonts(7)
    # Upperline in data
    fonts(7)
    # Upperline in data
    c.drawString(10, d, result['INVNO'])
    c.drawString(60, d, str(result['ISSUEDATE'].strftime('%d-%m-%Y')))
    c.drawAlignedString(165, d, str(result['OD']))
    c.drawString(180, d, str(result['PARTY']))
    c.drawAlignedString(390, d, str("%.2f" )% float(result['INVAMT']))
    c.drawAlignedString(470, d, str("%.2f" )% float(result['OSAMT']))
    c.drawAlignedString(560, d, str("%.2f" )% float(result['CUMAMT']))
    total(result)

def date(result):
    c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))


def LowerLineData(result, d):
    # Lowerline in data
    fonts(7)
    c.drawString(65, d, result['ITEM'][0:30])
    c.drawAlignedString(310, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawString(350, d, result['UNIT'])
    total(result)


def total(result):
    global CompanyBillAmtTotal
    global StoreBillAmtTotal
    global CompanyQuantityTotal
    global StoreQuantityTotal
    CompanyBillAmtTotal = CompanyBillAmtTotal + float(("%.2f" % float(result['INVAMT'])))


def logic(result):
    global cumamtlist
    cumamtlist.append(result['CUMAMTT'])
    divisioncode.append(result['COMPANY'])
    brokergrp.append(result['BROKERGRP'])
    broker.append(result['BROKER'])


def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
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
    d = 740
    return d


def newrequest():
    global divisioncode
    global pageno
    global mrnno
    global store
    global cumamtlist
    global broker
    global brokergrp
    divisioncode = []
    pageno = 0
    mrnno = []
    store = []
    broker =[]
    brokergrp = []

def printtotal(result):
    global CompanyBillAmtTotal
    boldfonts(7)
    c.drawString(160, d," TOTAL : ")
    c.drawAlignedString(560, d, str(round(CompanyBillAmtTotal,2)))
    c.line(0, d-10, 600, d-10)
    c.drawString(160, d-20, " NET OUTSTANDING : ")
    c.drawAlignedString(560, d-20, str(round(CompanyBillAmtTotal,2)))
    c.line(0, d-30, 600, d-30)
    fonts(7)
    CompanyBillAmtTotal = 0

def printtotallast(result):
    global totallist
    boldfonts(7)
    c.drawString(160, d, " TOTAL : ")
    c.drawAlignedString(560, d, str(result[-1]))
    c.line(0, d - 10, 600, d - 10)
    c.drawString(160, d - 20, " NET OUTSTANDING : ")
    c.drawAlignedString(560, d - 20, str(result[-1]))
    c.line(0, d - 30, 600, d - 30)
    fonts(7)


def printstoretotal(stdt, etdt, divisioncode):
    boldfonts(7)
    global StoreBillAmtTotal
    global StoreQuantityTotal
    c.drawString(40, d, str(store[-2]) + " TOTAL : ")
    c.drawAlignedString(560, d, str(locale.currency(float(StoreBillAmtTotal), grouping=True))[1:])
    c.drawAlignedString(310, d, str("%.3f" % float(StoreQuantityTotal)))
    fonts(7)
    dvalue(stdt, etdt, divisioncode)


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
    d = dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(brokergrp) == 1:
            if len(broker) == 1:
                new = 0
                new = new + round(float(result['INVAMT']), 2)
                result['CUMAMT'] = round(new, 2)
                header(stdt, etdt, divisioncode)
                boldfonts(10)
                c.drawCentredString(300, d, brokergrp[-1])
                d = dvalue(stdt, etdt, divisioncode)
                fonts(7)
                d = dvalue(stdt, etdt, divisioncode)
                data(stdt, etdt, result, d)
                # c.drawAlignedString(560, d, str(result['CUMAMTT']))

    elif divisioncode[-1] == divisioncode[-2]:
        if brokergrp[-1] == brokergrp[-2]:
            new = new + round(float(result['INVAMT']), 2)
            result['CUMAMT'] = round(new, 2)
            data(stdt, etdt, result, d)
            # c.drawAlignedString(560, d, str(result['CUMAMTT']))

        elif brokergrp[-1] != brokergrp[-2]:
            OSMoreThanDays_GetDataFromDB.cumamt - float(cumamtlist[-2])
            printtotal(result)
            d = dvalue(stdt, etdt, divisioncode)
            # printnetout()
            d = dvalue(stdt, etdt, divisioncode)
            # printtotalout()
            d = dvalue(stdt, etdt, divisioncode)
            c.showPage()
            header(stdt, etdt, divisioncode)
            d = newpage()
            boldfonts(10)
            c.drawCentredString(300, d, brokergrp[-1])
            d = dvalue(stdt, etdt, divisioncode)
            boldfonts(8)
            d = dvalue(stdt, etdt, divisioncode)
            new=0
            new = new + round(float(result['INVAMT']), 2)
            result['CUMAMT'] = round(new, 2)
            data(stdt, etdt, result, d)
            # c.drawAlignedString(560, d, str(round(float(result['CUMAMTT']) - float(cumamtlist[-2]),3)))

    elif divisioncode[-1] != divisioncode[-2]:
        printtotal(result)
        c.showPage()
        header(stdt, etdt, divisioncode)
        d = newpage()
        boldfonts(10)
        c.drawCentredString(300, d, brokergrp[-1])
        boldfonts(8)
        d = dvalue(stdt, etdt, divisioncode)
        new = 0
        new = new + round(float(result['INVAMT']), 2)
        result['CUMAMT'] = round(new, 2)
        data(stdt, etdt, result, d)
        # c.drawAlignedString(560, d, str(round(float(result['CUMAMTT']) - float(cumamtlist[-2]),3)))