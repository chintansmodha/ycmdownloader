from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))

d = 470

divisioncode=[]
store=[]
supplier=[]
item=[]
pageno=0

CompanyQuantityTotal=0
StoreQuantityTotal=0
SupplierQuantityTotal=0
ItemQuantityTotal=0

CompanyAmountTotal=0
StoreAmountTotal=0
SupplierAmountTotal=0
ItemAmountTotal=0

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


def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(landscape(A4))
        c.showPage()
        header(stdt, etdt, divisioncode)
        fonts(7)
        return d

def dvalueten():
    global d
    d = d - 10
    return d

def dvaluegst():
    global d
    d=d+10
    return d

def header(stdt,etdt,divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(400, 550, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(400, 530, "Supplier Wise Summary MRN Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(780,530,"Page No."+str(p))
    c.line(0, 520, 850, 520)
    c.line(0, 480, 850, 480)
    #Upperline in header

    c.drawString(10, 505, "ITEM")
    c.drawString(350, 505, "UNIT")
    c.drawString(480, 505, "QUANTITY")
    c.drawString(550, 505, "P/O RATE")
    c.drawString(610, 505, "MRN RATE")
    c.drawString(680, 505, "AMOUNT")
    c.drawString(730, 505, "COST RT")
    c.drawString(780, 505, "COST AMT")
    fonts(7)

def data(result,d):
    # Upperline in data
    fonts(7)
    c.drawString(10, d, result['ITEM'][:50])
    c.drawString(350, d, result['UNIT'])
    c.drawAlignedString(510, d, str("%.3f" % float(result['QUANTITY'])))
    c.drawAlignedString(570, d, str("%.4f" % float(result['PORATE'])))
    c.drawAlignedString(640, d, str("%.4f" % float(result['MRNRATE'])))
    c.drawAlignedString(710, d, str(locale.currency(float(result['AMOUNT']), grouping=True))[1:])
    c.drawAlignedString(760, d, '0.00')
    c.drawAlignedString(810, d, '0.00')
    total(result)


def total(result):
    global CompanyQuantityTotal
    global StoreQuantityTotal
    global SupplierQuantityTotal
    global ItemQuantityTotal

    global CompanyAmountTotal
    global StoreAmountTotal
    global SupplierAmountTotal
    global ItemAmountTotal

    CompanyAmountTotal = CompanyAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    ItemAmountTotal = ItemAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    SupplierAmountTotal= SupplierAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    StoreAmountTotal = StoreAmountTotal + float(("%.2f" % float(result['AMOUNT'])))

    CompanyQuantityTotal=CompanyQuantityTotal+float(("%.3f" % float(result['QUANTITY'])))
    ItemQuantityTotal = ItemQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    StoreQuantityTotal = StoreQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    SupplierQuantityTotal = SupplierQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))

def logic(result):
    divisioncode.append(result['DIVCODE'])
    store.append(result['STORE'])
    supplier.append(result['SUPPLIER'])
    item.append(result['ITEM'])

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    d = 470
    return d

def newrequest():
    global divisioncode
    global pageno
    global item
    global supplier
    global store
    global d
    divisioncode = []
    pageno = 0
    item = []
    store = []
    supplier = []
    d = 480

def printcompanytotal():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyQuantityTotal
    c.drawString(10, d, str(divisioncode[-2])[:50] + " TOTAL : ")
    c.drawAlignedString(710, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(CompanyQuantityTotal)))
    CompanyQuantityTotal=0
    CompanyAmountTotal=0
    fonts(7)
    dvalueten()

def printstoretotal():
    boldfonts(7)
    global StoreQuantityTotal
    global StoreAmountTotal
    c.drawString(120, d, "Grand Total : ")
    c.drawAlignedString(710, d, str(locale.currency(float(StoreAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(StoreQuantityTotal)))
    StoreAmountTotal=0
    StoreQuantityTotal=0
    fonts(7)
    dvalueten()

def printsuppliertotal():
    boldfonts(7)
    global SupplierQuantityTotal
    global SupplierAmountTotal
    c.drawString(120, d,"Supplier Wise Total : ")
    c.drawAlignedString(710, d, str(locale.currency(float(SupplierAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(SupplierQuantityTotal)))
    SupplierQuantityTotal=0
    SupplierAmountTotal=0
    fonts(7)
    dvalueten()

def printitemtotal():
    boldfonts(7)
    global ItemQuantityTotal
    global ItemAmountTotal
    c.drawString(120, d, str(item[-2])[:50] + " TOTAL : ")
    c.drawAlignedString(710, d, str(locale.currency(float(ItemAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(ItemQuantityTotal)))
    ItemAmountTotal=0
    ItemQuantityTotal=0
    fonts(7)

def printcompanytotallast():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyQuantityTotal
    c.drawString(10, d, str(divisioncode[-1])[:50] + " TOTAL : ")
    c.drawAlignedString(710, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(CompanyQuantityTotal)))
    CompanyQuantityTotal=0
    CompanyAmountTotal=0
    fonts(7)
    dvalueten()

def printstoretotallast():
    boldfonts(7)
    global StoreQuantityTotal
    global StoreAmountTotal
    c.drawString(120, d, "Grand Total : ")
    c.drawAlignedString(710, d, str(locale.currency(float(StoreAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(StoreQuantityTotal)))
    StoreAmountTotal=0
    StoreQuantityTotal=0
    fonts(7)
    dvalueten()

def printsuppliertotallast():
    boldfonts(7)
    global SupplierQuantityTotal
    global SupplierAmountTotal
    c.drawString(120, d,"Supplier Wise Total : ")
    c.drawAlignedString(710, d, str(locale.currency(float(SupplierAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(SupplierQuantityTotal)))
    SupplierQuantityTotal=0
    SupplierAmountTotal=0
    fonts(7)
    dvalueten()

def printitemtotallast():
    boldfonts(7)
    global ItemQuantityTotal
    global ItemAmountTotal
    c.drawString(120, d, str(item[-1])[:50] + " TOTAL : ")
    c.drawAlignedString(710, d, str(locale.currency(float(ItemAmountTotal), grouping=True))[1:])
    c.drawAlignedString(510, d, str("%.3f" % float(ItemQuantityTotal)))
    ItemAmountTotal=0
    ItemQuantityTotal=0
    fonts(7)


def cleanstore():
    global store
    store=store[-2:]
    print(store)

def textsize(c, result, d, stdt, etdt):
    d=dvalue(stdt, etdt, divisioncode)
    logic(result)
    if d>20:
        if len(divisioncode)==1:
            if len(store)==1:
                if len(supplier)==1:
                    if len(item)==1:
                        header(stdt, etdt, divisioncode)
                        boldfonts(7)
                        c.drawString(10, d, store[-1])
                        d = dvalue(stdt, etdt, divisioncode)
                        fonts(7)
                        boldfonts(7)
                        c.drawString(10, d, supplier[-1])
                        d=dvalue(stdt, etdt, divisioncode)
                        fonts(7)
                        data(result, d)


        elif divisioncode[-1]==divisioncode[-2]:
            if store[-1]==store[-2]:
                if supplier[-1]==supplier[-2]:
                    data(result,d)

                elif supplier[-1]!=supplier[-2]:
                    printsuppliertotal()

                    d=dvalue(stdt, etdt, divisioncode)
                    boldfonts(7)
                    c.drawString(10, d, supplier[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    fonts(7)
                    data(result, d)

            elif store[-1]!=store[-2]:
                printsuppliertotal()
                printstoretotal()
                d=dvalue(stdt, etdt, divisioncode)
                boldfonts(7)
                c.drawString(10, d, store[-1])
                d=dvalue(stdt, etdt, divisioncode)
                fonts(7)
                boldfonts(7)
                c.drawString(10, d, supplier[-1])
                d=dvalue(stdt, etdt, divisioncode)
                fonts(7)
                data(result, d)

        elif divisioncode[-1]!=divisioncode[-2]:
            printsuppliertotal()
            d = dvalue(stdt, etdt, divisioncode[-3:-2])
            printstoretotal()
            d = dvalue(stdt, etdt, divisioncode[-3:-2])
            printcompanytotal()
            d = newpage()
            d = dvalue(stdt, etdt, divisioncode[-3:-2])
            c.setPageSize(landscape(A4))
            c.showPage()
            c.setPageSize(landscape(A4))
            cleanstore()
            logic(result)
            header(stdt,etdt,divisioncode)
            boldfonts(7)
            c.drawString(10, d, store[-1])
            d = dvalue(stdt, etdt, divisioncode)
            fonts(7)
            boldfonts(7)
            c.drawString(10, d, supplier[-1])
            d = dvalue(stdt, etdt, divisioncode)
            fonts(7)
            if store[-1] == store[-2]:
                if supplier[-1] == supplier[-2]:
                    data(result, d)

                elif supplier[-1] != supplier[-2]:
                    printsuppliertotal()

                    d = dvalue(stdt, etdt, divisioncode)
                    boldfonts(7)
                    c.drawString(10, d, supplier[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    fonts(7)
                    data(result, d)

            elif store[-1] != store[-2]:
                printsuppliertotal()
                printstoretotal()
                d = dvalue(stdt, etdt, divisioncode)
                boldfonts(7)
                c.drawString(10, d, store[-1])
                d = dvalue(stdt, etdt, divisioncode)
                fonts(7)
                boldfonts(7)
                c.drawString(10, d, supplier[-1])
                d = dvalue(stdt, etdt, divisioncode)
                fonts(7)
                data(result, d)
