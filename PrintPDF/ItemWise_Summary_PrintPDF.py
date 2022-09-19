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
itemtype=[]
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
        c.showPage()
        header(stdt, etdt, divisioncode[:-1])
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
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Item Wise Summary MRN Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    #Upperline in header

    c.drawString(10, 750, "ITEM")
    c.drawString(270, 750, "UNIT")
    c.drawString(370, 750, "QUANTITY")
    c.drawString(435, 750, "P/O RATE")
    c.drawString(490, 750, "MRN RATE")
    c.drawString(550, 750, "AMOUNT")
    fonts(7)

def data(result,d):
    # Upperline in data
    fonts(7)
    c.drawString(10, d, result['ITEM'][:50])
    c.drawString(270, d, result['UNIT'][:30])
    c.drawAlignedString(400, d, str("%.3f" % float(result['QUANTITY'])))
    c.drawAlignedString(460, d, str("%.4f" % float(result['PORATE'])))
    c.drawAlignedString(520, d, str("%.4f" % float(result['MRNRATE'])))
    c.drawAlignedString(580, d, str(locale.currency(float(result['AMOUNT']), grouping=True))[1:])
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
    itemtype.append(result['ITEMTYPE'])
    item.append(result['ITEM'])

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
    global itemtype
    global store
    global d
    divisioncode=[]
    pageno=0
    item=[]
    store=[]
    itemtype=[]
    d=730

def printcompanytotal():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyQuantityTotal
    c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(CompanyQuantityTotal)))
    CompanyQuantityTotal=0
    CompanyAmountTotal=0
    fonts(7)

def printstoretotal():
    boldfonts(7)
    global StoreQuantityTotal
    global StoreAmountTotal
    c.drawString(120, d, str(store[-2])[:50] + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(StoreAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(StoreQuantityTotal)))
    StoreAmountTotal=0
    StoreQuantityTotal=0
    fonts(7)
    dvalueten()

def printsuppliertotal():
    boldfonts(7)
    global SupplierQuantityTotal
    global SupplierAmountTotal
    c.drawString(120, d, str(itemtype[-2]) + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(SupplierAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(SupplierQuantityTotal)))
    SupplierQuantityTotal=0
    SupplierAmountTotal=0
    fonts(7)

def printitemtotal():
    boldfonts(7)
    global ItemQuantityTotal
    global ItemAmountTotal
    c.drawString(120, d, str(itemtype[-2]) + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(ItemAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(ItemQuantityTotal)))
    ItemAmountTotal=0
    ItemQuantityTotal=0
    fonts(7)

def printcompanytotallast():
    boldfonts(7)
    global CompanyAmountTotal
    global CompanyQuantityTotal
    c.drawString(10, d, str(divisioncode[-1]) + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(CompanyAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(CompanyQuantityTotal)))
    CompanyQuantityTotal=0
    CompanyAmountTotal=0
    fonts(7)

def printstoretotallast():
    boldfonts(7)
    global StoreQuantityTotal
    global StoreAmountTotal
    c.drawString(120, d, str(store[-1])[:50] + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(StoreAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(StoreQuantityTotal)))
    StoreAmountTotal=0
    StoreQuantityTotal=0
    fonts(7)
    dvalueten()

def printsuppliertotallast():
    boldfonts(7)
    global SupplierQuantityTotal
    global SupplierAmountTotal
    c.drawString(120, d, str(itemtype[-1]) + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(SupplierAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(SupplierQuantityTotal)))
    SupplierQuantityTotal=0
    SupplierAmountTotal=0
    fonts(7)

def printitemtotallast():
    boldfonts(7)
    global ItemQuantityTotal
    global ItemAmountTotal
    c.drawString(120, d, str(itemtype[-1]) + " TOTAL : ")
    c.drawAlignedString(580, d, str(locale.currency(float(ItemAmountTotal), grouping=True))[1:])
    c.drawAlignedString(400, d, str("%.3f" % float(ItemQuantityTotal)))
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
                if len(itemtype) == 1:
                    if len(item) == 1:
                        header(stdt, etdt, divisioncode)
                        boldfonts(7)
                        c.drawString(10, d, store[-1])
                        d = dvalue(stdt, etdt, divisioncode)
                        fonts(7)
                        boldfonts(7)
                        c.drawString(10, d, itemtype[-1])
                        d=dvalue(stdt, etdt, divisioncode)
                        fonts(7)
                        data(result, d)


        elif divisioncode[-1]==divisioncode[-2]:
            if store[-1]==store[-2]:
                if itemtype[-1]==itemtype[-2]:
                    if item[-1] == item[-2]:
                        data(result,d)
                    elif item[-1]!=item[-2]:
                        data(result, d)

                elif itemtype[-1]!=itemtype[-2]:
                    printitemtotal()
                    d=dvalue(stdt, etdt, divisioncode)
                    boldfonts(7)
                    c.drawString(10, d, itemtype[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    fonts(7)
                    data(result, d)

            elif store[-1]!=store[-2]:
                printitemtotal()
                d=dvalue(stdt, etdt, divisioncode)
                printstoretotal()
                d=dvalue(stdt, etdt, divisioncode)
                boldfonts(7)
                c.drawString(10, d, store[-1])
                d=dvalue(stdt, etdt, divisioncode)
                fonts(7)
                boldfonts(7)
                c.drawString(10, d, itemtype[-1])
                d=dvalue(stdt, etdt, divisioncode)
                fonts(7)
                data(result, d)

        elif divisioncode[-1]!=divisioncode[-2]:
            printitemtotal()
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
            boldfonts(7)
            c.drawString(10, d, itemtype[-1])
            d = dvalue(stdt, etdt, divisioncode)
            if store[-1] == store[-2]:
                if itemtype[-1] == itemtype[-2]:
                    if item[-1] == item[-2]:
                        data(result, d)
                    elif item[-1] != item[-2]:
                        data(result, d)

                elif itemtype[-1] != itemtype[-2]:
                    printitemtotal()
                    d = dvalue(stdt, etdt, divisioncode)
                    boldfonts(7)
                    c.drawString(10, d, itemtype[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    fonts(7)
                    data(result, d)

            elif store[-1] != store[-2]:
                printitemtotal()
                d = dvalue(stdt, etdt, divisioncode)
                printstoretotal()
                d = dvalue(stdt, etdt, divisioncode)
                boldfonts(7)
                c.drawString(10, d, store[-1])
                d = dvalue(stdt, etdt, divisioncode)
                fonts(7)
                boldfonts(7)
                c.drawString(10, d, itemtype[-1])
                d = dvalue(stdt, etdt, divisioncode)
                fonts(7)
                data(result, d)