from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale

locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 720
clbal=0
divisioncode = []
store = []
mrnno = []
pageno = 0
CompanyRecQtyTotal = 0
StoreBillAmtTotal = 0
CompanyIssQtyTotal = 0
StoreQuantityTotal = 0
ItemRecQtyTotal =0
ItemIssQtyTotal =0

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
    c.drawCentredString(300, 780, "Product Detail From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "Date")
    c.drawString(50, 755, "Type")
    c.drawString(80, 755, "Number")
    c.drawString(250, 755, "Department")
    c.drawString(390, 755, "OpQty")
    c.drawString(450, 755, "Rec Qty")
    c.drawString(500, 755, "Iss QTY")
    c.drawString(550, 755, "Bal Qty")

    # LowerLine in header
    # c.drawString(10, 740, "MRN DT")
    # c.drawString(65, 740, "ITEM NAME")
    # c.drawString(280, 740, "QUANTITY")
    # c.drawString(350, 740, "UNIT")
    fonts(7)


def data(stdt, etdt, result, d):
    fonts(7)
    global clbal
    clbal = clbal - float(result['ISSQTY']) + float(result['RECQTY'])
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(result['TXNDATE']))
    c.drawString(60, d, result['TXNTYPE'])
    c.drawString(80, d, result['TXNNO'])
    c.drawAlignedString(470, d, result['RECQTY'])
    c.drawAlignedString(520, d, result['ISSQTY'])
    c.drawAlignedString(570, d, str(round(clbal, 3)))
    total(result)



def date(result):
    c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))


def LowerLineData(result, d):
    # Lowerline in data
    fonts(7)
    global clbal
    clbal = clbal + float(result['BALQTY'])
    fonts(7)
    # Upperline in data
    c.drawAlignedString(470, d, result['RECQTY'])
    c.drawAlignedString(520, d, result['ISSQTY'])
    c.drawAlignedString(570, d, str(round(clbal, 2)))
    total(result)


def total(result):
    global CompanyRecQtyTotal
    global CompanyIssQtyTotal
    global ItemRecQtyTotal
    global ItemIssQtyTotal
    CompanyRecQtyTotal = CompanyRecQtyTotal + float(("%.2f" % float(result['RECQTY'])))
    CompanyIssQtyTotal = CompanyIssQtyTotal + float(("%.3f" % float(result['ISSQTY'])))
    ItemRecQtyTotal = ItemRecQtyTotal + float(("%.2f" % float(result['RECQTY'])))
    ItemIssQtyTotal = ItemIssQtyTotal + float(("%.3f" % float(result['ISSQTY'])))


def logic(result):
    divisioncode.append(result['DIVCODE'])
    store.append(result['PRODUCTNAME'])
    # mrnno.append(result['MRNNO'])


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
    global CompanyRecQtyTotal
    global CompanyIssQtyTotal
    c.drawString(40, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(470, d, str(CompanyRecQtyTotal))
    c.drawAlignedString(520, d, str(CompanyIssQtyTotal))
    fonts(7)
    CompanyRecQtyTotal = 0
    CompanyIssQtyTotal = 0

def printstoretotal(stdt, etdt, divisioncode):
    boldfonts(7)
    global ItemIssQtyTotal
    global ItemRecQtyTotal
    c.drawString(40, d, str(store[-2]) + " TOTAL : ")
    c.drawAlignedString(520, d, str(locale.currency(float(ItemIssQtyTotal), grouping=True))[1:])
    c.drawAlignedString(470, d, str("%.3f" % float(ItemRecQtyTotal)))
    fonts(7)
    dvalue(stdt, etdt, divisioncode)
    ItemIssQtyTotal = 0
    ItemRecQtyTotal = 0

def companyclean():
    global CompanyBillAmtTotal
    global CompanyQuantityTotal


def cleanstore():
    global store
    store = []


def storeclean():
    global StoreBillAmtTotal
    global StoreQuantityTotal
    StoreBillAmtTotal = 0
    StoreQuantityTotal = 0


def textsize(c, result, d, stdt, etdt):
    global clbal
    d = dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(store) == 1:
            clbal = float(result['OPBAL'])
            header(stdt, etdt, divisioncode)
            fonts(7)
            d = dvalue(stdt, etdt, divisioncode)
            boldfonts(7)
            c.drawString(50, d, result['PRODUCTNAME'])
            d = dvalue(stdt, etdt, divisioncode)
            c.drawAlignedString(410, d, result['OPBAL'])
            data(stdt, etdt, result, d)
            # date(result)


    elif divisioncode[-1] == divisioncode[-2]:
        if store[-1] == store[-2]:
            data(stdt, etdt, result, d)

        elif store[-1] != store[-2]:
            printstoretotal(stdt,etdt,divisioncode)
            d = dvalue(stdt, etdt, divisioncode)
            clbal = float(result['OPBAL'])
            boldfonts(7)
            c.drawString(50, d, result['PRODUCTNAME'])
            d = dvalue(stdt, etdt, divisioncode)
            fonts(7)
            c.drawAlignedString(410, d, result['OPBAL'])
            data(stdt, etdt, result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        printtotal()
        clbal = 0
        c.showPage()
        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(50, d, result['PRODUCTNAME'])
        fonts(7)
        d=dvalue(stdt, etdt, divisioncode)
        data(stdt,etdt,result,d)
