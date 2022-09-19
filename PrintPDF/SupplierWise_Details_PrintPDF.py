from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 720


divisioncode=[]
store=[]
supplier=[]
item=[]
mrnno=[]
pageno=0
count=0

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
        c.showPage()
        header(stdt, etdt, divisioncode)
        return d

def dvalueten():
    global d
    d = d - 10
    return d

def dvaluegst():
    global d
    d=d+10
    return d

def nodaterpt(result):
    fonts(7)
    c.drawString(10, d, result['MRNNO'])
    c.drawString(65, d, result['MRNDATE'].strftime('%d-%m-%Y'))


def header(stdt,etdt,divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Supplier Wise Detail MRN Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    #Upperline in header

    c.drawString(10, 750, "MRN NO")
    c.drawString(65, 750, "MRN DATE")
    c.drawString(120, 750, "ITEM")
    c.drawString(350, 750, "QUANTITY")
    c.drawString(430, 750, "P/O RATE")
    c.drawString(480, 750, "MRN RATE")
    c.drawString(540, 750, "AMOUNT")
    fonts(7)

def data(result,d):
    # Upperline in data
    fonts(7)
    # c.drawString(10, d, result['MRNNO'])
    # c.drawString(65, d, result['MRNDATE'].strftime('%d-%m-%Y'))
    c.drawString(120, d, result['ITEM'][:50])
    c.drawAlignedString(380, d, str("%.3f" % float(result['QUANTITY'])))
    c.drawAlignedString(450, d, str("%.4f" % float(result['PORATE'])))
    c.drawAlignedString(510, d, str("%.4f" % float(result['MRNRATE'])))
    c.drawAlignedString(570, d, str(locale.currency(float(result['AMOUNT']), grouping=True))[1:])
    total(result)
    itemtotal(result)


def total(result):
    global CompanyQuantityTotal
    global StoreQuantityTotal
    global SupplierQuantityTotal
    #global ItemQuantityTotal

    global CompanyAmountTotal
    global StoreAmountTotal
    global SupplierAmountTotal
    #global ItemAmountTotal

    CompanyAmountTotal = CompanyAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    #ItemAmountTotal = ItemAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    SupplierAmountTotal= SupplierAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    StoreAmountTotal = StoreAmountTotal + float(("%.2f" % float(result['AMOUNT'])))

    CompanyQuantityTotal=CompanyQuantityTotal+float(("%.3f" % float(result['QUANTITY'])))
    #ItemQuantityTotal = ItemQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    StoreQuantityTotal = StoreQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    SupplierQuantityTotal = SupplierQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))

def logic(result):
    divisioncode.append(result['DIVCODE'])
    store.append(result['STORE'])
    supplier.append(result['SUPPLIER'])
    item.append(result['ITEM'])
    mrnno.append(result['MRNNO'])

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    d = 720
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
    d = 730

def itemtotal(result):
    global ItemQuantityTotal
    global ItemAmountTotal
    ItemAmountTotal = ItemAmountTotal + float(("%.2f" % float(result['AMOUNT'])))
    ItemQuantityTotal = ItemQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))

def cleanitem():
    global ItemQuantityTotal
    global ItemAmountTotal
    ItemQuantityTotal=0
    ItemAmountTotal=0

def printcompanytotal():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyQuantityTotal
    c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(570, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(CompanyQuantityTotal)))
    CompanyQuantityTotal=0
    CompanyAmountTotal=0
    fonts(7)

def printstoretotal():
    boldfonts(7)
    global StoreQuantityTotal
    global StoreAmountTotal
    c.drawString(120, d,"Grand Total : ")
    c.drawAlignedString(570, d, str(locale.currency(float(StoreAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(StoreQuantityTotal)))
    StoreAmountTotal=0
    StoreQuantityTotal=0
    fonts(7)


def printsuppliertotal():
    boldfonts(7)
    global SupplierQuantityTotal
    global SupplierAmountTotal
    c.drawString(120, d,"Party Wise Total : ")
    c.drawAlignedString(570, d, str(locale.currency(float(SupplierAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(SupplierQuantityTotal)))
    SupplierQuantityTotal=0
    SupplierAmountTotal=0
    fonts(7)

def printitemtotal():
    boldfonts(7)
    global ItemQuantityTotal
    global ItemAmountTotal
    c.drawString(120, d,"Item Wise Total : ")
    c.drawAlignedString(570, d, str(locale.currency(float(ItemAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(ItemQuantityTotal)))
    ItemAmountTotal=0
    ItemQuantityTotal=0
    fonts(7)

def printcompanytotallast():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyQuantityTotal
    c.drawString(10, d, str(divisioncode[-1]) + " TOTAL : ")
    c.drawAlignedString(570, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(CompanyQuantityTotal)))
    CompanyQuantityTotal=0
    CompanyAmountTotal=0
    fonts(7)

def printstoretotallast():
    boldfonts(7)
    global StoreQuantityTotal
    global StoreAmountTotal
    c.drawString(120, d,"Grand Total : ")
    c.drawAlignedString(570, d, str(locale.currency(float(StoreAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(StoreQuantityTotal)))
    StoreAmountTotal=0
    StoreQuantityTotal=0
    fonts(7)


def printsuppliertotallast():
    boldfonts(7)
    global SupplierQuantityTotal
    global SupplierAmountTotal
    c.drawString(120, d,"Party Wise Total : ")
    c.drawAlignedString(570, d, str(locale.currency(float(SupplierAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(SupplierQuantityTotal)))
    SupplierQuantityTotal=0
    SupplierAmountTotal=0
    fonts(7)

def printitemtotallast():
    boldfonts(7)
    global ItemQuantityTotal
    global ItemAmountTotal
    c.drawString(120, d,"Item Wise Total : ")
    c.drawAlignedString(570, d, str(locale.currency(float(ItemAmountTotal), grouping=True))[1:])
    c.drawAlignedString(380, d, str("%.3f" % float(ItemQuantityTotal)))
    ItemAmountTotal=0
    ItemQuantityTotal=0
    fonts(7)

def cleanstore():
    global store
    store=store[-2:]


def textsize(c, result, d, stdt, etdt):
    d=dvalue(stdt, etdt, divisioncode)
    logic(result)
    global count
    if d>20:
        if len(divisioncode)==1:
            if len(store)==1:
                if len(supplier)==1:
                    if len(item)==1:
                        header(stdt, etdt, divisioncode)
                        boldfonts(7)
                        c.drawString(10, d, store[-1])
                        fonts(7)
                        d = dvalue(stdt, etdt, divisioncode)
                        boldfonts(7)
                        c.drawString(10, d, supplier[-1])
                        d=dvalue(stdt, etdt, divisioncode)
                        fonts(7)
                        data(result, d)
                        nodaterpt(result)

        elif divisioncode[-1]==divisioncode[-2]:
            if store[-1]==store[-2]:
                if supplier[-1]==supplier[-2]:
                    if item[-1]==item[-2]:
                        if mrnno[-1] == mrnno[-2]:
                            count = count + 1
                            data(result, d)
                        elif mrnno[-1] != mrnno[-2]:
                            count = count+1
                            data(result, d)
                            nodaterpt(result)

                    elif item[-1]!=item[-2]:
                        if count > 0:
                            printitemtotal()
                            d = dvalue(stdt, etdt, divisioncode)
                        count = 0
                        cleanitem()
                        if mrnno[-1] == mrnno[-2]:
                            data(result, d)

                        elif mrnno[-1] != mrnno[-2]:
                            data(result, d)
                            nodaterpt(result)

                elif supplier[-1]!=supplier[-2]:
                    if count > 0:
                        printitemtotal()
                        d = dvalue(stdt, etdt, divisioncode)
                    count = 0
                    cleanitem()
                    printsuppliertotal()
                    d=dvalue(stdt, etdt, divisioncode)
                    boldfonts(7)
                    d = dvalue(stdt, etdt, divisioncode)
                    c.drawString(10, d, supplier[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    fonts(7)
                    data(result, d)
                    nodaterpt(result)

            elif store[-1]!=store[-2]:
                if count > 0:
                    printitemtotal()
                    d = dvalue(stdt, etdt, divisioncode)
                count = 0
                cleanitem()
                printsuppliertotal()
                d=dvalue(stdt, etdt, divisioncode)
                printstoretotal()
                d = dvalue(stdt, etdt, divisioncode)
                d = dvalue(stdt, etdt, divisioncode)
                boldfonts(7)
                c.drawString(10, d, store[-1])
                d=dvalue(stdt, etdt, divisioncode)
                fonts(7)
                boldfonts(7)
                c.drawString(10, d, supplier[-1])
                d=dvalue(stdt, etdt, divisioncode)
                fonts(7)
                data(result, d)
                nodaterpt(result)

        elif divisioncode[-1]!=divisioncode[-2]:
            if count > 0:
                printitemtotal()
            count = 0
            d = dvalue(stdt, etdt, divisioncode)
            printsuppliertotal()
            d = dvalue(stdt, etdt, divisioncode)
            printstoretotal()
            d = dvalue(stdt, etdt, divisioncode)
            printcompanytotal()
            d = newpage()
            d = dvalue(stdt, etdt, divisioncode)
            c.showPage()
            cleanstore()
            logic(result)
            header(stdt,etdt,divisioncode)
            boldfonts(7)
            c.drawString(10, d, store[-1])
            d = dvalue(stdt, etdt, divisioncode)
            fonts(7)
            c.drawString(10, d, supplier[-1])
            d = dvalue(stdt, etdt, divisioncode)
            if store[-1] == store[-2]:
                if supplier[-1] == supplier[-2]:
                    if item[-1] == item[-2]:
                        if mrnno[-1] == mrnno[-2]:
                            count = count + 1
                            data(result, d)
                        elif mrnno[-1] != mrnno[-2]:
                            count = count + 1
                            data(result, d)
                            nodaterpt(result)

                    elif item[-1] != item[-2]:
                        cleanitem()
                        if mrnno[-1] == mrnno[-2]:
                            data(result, d)

                        elif mrnno[-1] != mrnno[-2]:
                            data(result, d)
                            nodaterpt(result)

                elif supplier[-1] != supplier[-2]:
                    if count > 0:
                        printitemtotal()
                        d = dvalue(stdt, etdt, divisioncode)
                    count = 0
                    cleanitem()
                    printsuppliertotal()
                    d = dvalue(stdt, etdt, divisioncode)
                    boldfonts(7)
                    d = dvalue(stdt, etdt, divisioncode)
                    c.drawString(10, d, supplier[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    fonts(7)
                    data(result, d)
                    nodaterpt(result)

            elif store[-1] != store[-2]:
                if count > 0:
                    printitemtotal()
                    d = dvalue(stdt, etdt, divisioncode)
                count = 0
                cleanitem()
                printsuppliertotal()
                d = dvalue(stdt, etdt, divisioncode)
                printstoretotal()
                d = dvalue(stdt, etdt, divisioncode)
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
                nodaterpt(result)
