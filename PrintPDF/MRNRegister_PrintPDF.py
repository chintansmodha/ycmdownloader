from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale

locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 720

divisioncode = []
store = []
mrnno = []
pageno = 0
CompanyBillAmtTotal = 0
StoreBillAmtTotal = 0
CompanyQuantityTotal = 0
StoreQuantityTotal = 0


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
    c.drawCentredString(300, 780, "MRN Details From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "MRN NO")
    c.drawString(65, 755, "SUPPLIER")
    c.drawString(280, 755, "CHAL NO")
    c.drawString(350, 755, "CHAL DT")
    c.drawString(410, 755, "BILL NO")
    c.drawString(470, 755, "BILL DT")
    c.drawString(530, 755, "BILL AMT")

    # LowerLine in header
    c.drawString(10, 740, "MRN DT")
    c.drawString(65, 740, "ITEM NAME")
    c.drawString(280, 740, "QUANTITY")
    c.drawString(350, 740, "UNIT")
    fonts(7)


def data(stdt, etdt, result, d):
    fonts(7)
    # Upperline in data
    c.drawString(10, d, result['MRNNO'])
    c.drawString(65, d, result['SUPPLIER'])
    if result['CHALLANNO'] != None:
        c.drawString(290, d, result['CHALLANNO'])
    if result['CHALLANDATE'] != None:
        c.drawString(350, d, result['CHALLANDATE'].strftime('%d-%m-%Y'))


def date(result):
    c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))


def LowerLineData(result, d):
    # Lowerline in data
    fonts(7)
    c.drawString(65, d, result['ITEM'][0:30])
    c.drawAlignedString(310, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawString(350, d, result['UNIT'])
    if result['BILLNO'] != None:
        c.drawString(410, d, result['BILLNO'])
        c.drawString(470, d, str(result['BILLDATE'].strftime('%d-%m-%Y')))
    c.drawAlignedString(560, d, str(locale.currency(float(result['BILLAMOUNT']), grouping=True))[1:])
    total(result)


def total(result):
    global CompanyBillAmtTotal
    global StoreBillAmtTotal
    global CompanyQuantityTotal
    global StoreQuantityTotal
    CompanyBillAmtTotal = CompanyBillAmtTotal + float(("%.2f" % float(result['BILLAMOUNT'])))
    StoreBillAmtTotal = StoreBillAmtTotal + float(("%.2f" % float(result['BILLAMOUNT'])))
    CompanyQuantityTotal = CompanyQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    StoreQuantityTotal = StoreQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))


def logic(result):
    divisioncode.append(result['DIVCODE'])
    store.append(result['STORE'])
    mrnno.append(result['MRNNO'])


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
    d = 710
    return d


def newrequest():
    global divisioncode
    global pageno
    global mrnno
    global store
    divisioncode = []
    pageno = 0

    mrnno = []
    store = []


def printtotal():
    boldfonts(7)
    global CompanyBillAmtTotal
    global CompanyQuantityTotal
    c.drawString(40, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(560, d, str(locale.currency(float(CompanyBillAmtTotal), grouping=True))[1:])
    c.drawAlignedString(310, d, str("%.3f" % float(CompanyQuantityTotal)))
    fonts(7)

def printtotallast():
    boldfonts(7)
    global CompanyBillAmtTotal
    global CompanyQuantityTotal
    c.drawString(40, d, str(divisioncode[-1]) + " TOTAL : ")
    c.drawAlignedString(560, d, str(locale.currency(float(CompanyBillAmtTotal), grouping=True))[1:])
    c.drawAlignedString(310, d, str("%.3f" % float(CompanyQuantityTotal)))
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

def printstoretotallast(stdt, etdt, divisioncode):
    boldfonts(7)
    global StoreBillAmtTotal
    global StoreQuantityTotal
    c.drawString(40, d, str(store[-1]) + " TOTAL : ")
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
    d = dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(store) == 1:
            if len(mrnno) == 1:
                header(stdt, etdt, divisioncode)
                boldfonts(7)
                c.drawString(10, d, store[-1])
                fonts(7)
                d = dvalue(stdt, etdt, divisioncode)
                data(stdt, etdt, result, d)
                d = dvalue(stdt, etdt, divisioncode)
                date(result)
                LowerLineData(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if store[-1] == store[-2]:
            if mrnno[-1] == mrnno[-2]:
                d = dvaluegst()
                LowerLineData(result, d)
            elif mrnno[-1] != mrnno[-2]:
                data(stdt, etdt, result, d)
                d = dvalue(stdt, etdt, divisioncode)
                date(result)
                LowerLineData(result, d)

        elif store[-1] != store[-2]:
            fonts(7)
            printstoretotal(stdt, etdt, divisioncode)
            storeclean()
            d = dvalue(stdt, etdt, divisioncode)
            boldfonts(7)
            c.drawString(10, d, store[-1])
            d = dvalue(stdt, etdt, divisioncode)
            fonts(7)
            if mrnno[-1] == mrnno[-2]:
                LowerLineData(result, d)
            elif mrnno[-1] != mrnno[-2]:
                data(stdt, etdt, result, d)
                d = dvalue(stdt, etdt, divisioncode)
                date(result)
                LowerLineData(result, d)


    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        printstoretotal(stdt, etdt, divisioncode)
        storeclean()
        d = dvalue(stdt, etdt, divisioncode)
        printtotal()
        companyclean()
        # c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
        c.showPage()
        header(stdt, etdt, divisioncode)
        d = newpage()
        # d=dvalue(stdt, etdt, divisioncode)
        if store[-1] == store[-2]:
            if mrnno[-1] == mrnno[-2]:
                d = dvaluegst()
                LowerLineData(result, d)
            elif mrnno[-1] != mrnno[-2]:
                data(stdt, etdt, result, d)
                d = dvalue(stdt, etdt, divisioncode)
                date(result)
                LowerLineData(result, d)

        elif store[-1] != store[-2]:
            fonts(7)
            # printstoretotal(stdt, etdt, divisioncode)
            storeclean()
            # d = dvalue(stdt, etdt, divisioncode)
            boldfonts(7)
            c.drawString(10, d, store[-1])
            d = dvalue(stdt, etdt, divisioncode)
            fonts(7)
            if mrnno[-1] == mrnno[-2]:
                LowerLineData(result, d)
            elif mrnno[-1] != mrnno[-2]:
                data(stdt, etdt, result, d)
                d = dvalue(stdt, etdt, divisioncode)
                date(result)
                LowerLineData(result, d)