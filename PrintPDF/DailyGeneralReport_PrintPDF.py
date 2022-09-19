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
CompanyOpQtyTotal=0
CompanyClQtyTotal=0
productiondivisioncode=[]
machine=[]
machinetodaytotal=0
machineuptodatetotal=0
grandtodaytotal=0
granduptodatetotal=0
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

def productionheader(stdt, etdt, productiondivisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, productiondivisioncode)
    boldfonts(9)
    print(stdt,etdt)
    c.drawCentredString(300, 780, "Daily General Report From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "M/C.")
    c.drawString(60, 755, "Lot No.")
    c.drawString(120, 755, "Item Description")
    c.drawString(350, 755, "Shade")
    c.drawString(430, 755, "Previous Lots")
    c.drawString(510, 755, "Today")
    c.drawString(550, 755, "Upto Dt.")
    fonts(7)



def productiondata(result):
    c.drawString(60, d, result['LOTCODE'][:25])
    c.drawString(120, d, result['ITEM'])
    c.drawString(350, d, result['SHADENAME'])
    c.drawString(430, d, result['PREVIOUSLOTS'])
    c.drawAlignedString(530, d, result['TODAY'])
    c.drawAlignedString(570, d, result['UPTODATE'])
    productiontotal(result)

def productiontotal(result):
    global machinetodaytotal
    global machineuptodatetotal
    global grandtodaytotal
    global granduptodatetotal
    machinetodaytotal = machinetodaytotal + float(("%.2f" % float(result['TODAY'])))
    machineuptodatetotal = machineuptodatetotal + float(("%.2f" % float(result['UPTODATE'])))
    grandtodaytotal = grandtodaytotal + float(("%.2f" % float(result['TODAY'])))
    granduptodatetotal = granduptodatetotal + float(("%.2f" % float(result['UPTODATE'])))

def productionprinttotal():
    global granduptodatetotal
    global grandtodaytotal
    boldfonts(7)
    c.drawString(350, d, "Grand Total:")
    c.drawAlignedString(570, d, str(round(granduptodatetotal,3)))
    c.drawAlignedString(530, d, str(round(grandtodaytotal,3)))
    grandtodaytotal=0
    granduptodatetotal=0
    fonts(7)

def machinetotal():
    global machinetodaytotal
    global machineuptodatetotal
    boldfonts(7)
    c.drawString(350,d,"Machine Total:")
    c.drawAlignedString(530, d, str(round(machinetodaytotal,3)))
    c.drawAlignedString(570, d, str(round(machineuptodatetotal,3)))
    machinetodaytotal = 0
    machineuptodatetotal =0
    fonts(7)
def productionlogic(result):
    global productiondivisioncode
    global machine
    machine.append(result['MC'])
    productiondivisioncode.append(result['PLANT'])

def productiontextsize(c, result, d, stdt, etdt):
    d = proddvalue(stdt, etdt, productiondivisioncode)
    productionlogic(result)
    if len(machine)==1:
        c.drawString(10, d, str(result['MC']))
        productiondata(result)
    elif machine[-1] == machine[-2]:
        productiondata(result)
    elif machine[-1] != machine[-2]:
        machinetotal()
        d = proddvalue(stdt, etdt, productiondivisioncode)
        c.drawString(10, d, str(result['MC']))
        productiondata(result)

def header(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode)
    boldfonts(9)
    print(stdt,etdt)
    c.drawCentredString(300, 780, "Product Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "Item")
    c.drawString(200, 755, "Base")
    c.drawString(330, 755, "Lotcode")
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

def productionnewrequest():
    global machine
    machine=[]

def data(stdt, etdt, result, d):
    global clbal
    clbal = clbal + float(result['BALQTY'])
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(result['PRODUCTNAME'])[:40])
    c.drawString(200, d, result['BASE'][:25])
    c.drawString(330, d, result['LOTCODE'])
    c.drawAlignedString(410, d, result['OPBAL'])
    c.drawAlignedString(470, d, result['RECQTY'])
    c.drawAlignedString(520, d, result['ISSQTY'])
    c.drawAlignedString(570, d, result['BALQTY'])
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
    global CompanyRecQtyTotal
    global CompanyIssQtyTotal
    global CompanyClQtyTotal
    global CompanyOpQtyTotal
    CompanyRecQtyTotal = CompanyRecQtyTotal + float(("%.2f" % float(result['RECQTY'])))
    CompanyIssQtyTotal = CompanyIssQtyTotal + float(("%.3f" % float(result['ISSQTY'])))
    CompanyOpQtyTotal = CompanyOpQtyTotal + float(("%.2f" % float(result['OPBAL'])))
    CompanyClQtyTotal = CompanyClQtyTotal + float(("%.2f" % float(result['BALQTY'])))
def logic(result):
    divisioncode.append(result['DIVCODE'])
    store.append(result['PRODUCTNAME'])
    # mrnno.append(result['MRNNO'])


def dvalue(stdt, etdt, result):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, result['DIVCODE'])
        return d


def proddvalue(stdt, etdt, productiondivisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        productionheader(stdt, etdt, productiondivisioncode)
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
    global d
    global CompanyRecQtyTotal
    global CompanyIssQtyTotal
    global CompanyOpQtyTotal
    global CompanyClQtyTotal
    c.drawString(40, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(410, d, str(round(CompanyOpQtyTotal, 2)))
    c.drawAlignedString(520, d, str(round(CompanyIssQtyTotal, 2)))
    d = d - 10
    c.drawAlignedString(470, d, str(round(CompanyRecQtyTotal, 2)))
    c.drawAlignedString(570, d, str(round(CompanyClQtyTotal, 2)))
    fonts(7)

    CompanyRecQtyTotal = 0
    CompanyIssQtyTotal = 0
    CompanyOpQtyTotal = 0
    CompanyClQtyTotal = 0

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
    d = dvalue(stdt, etdt, result)
    logic(result)
    data(stdt, etdt, result, d)
    # if len(divisioncode) == 1:
    #     if len(store) == 1:
    #         header(stdt, etdt, divisioncode)
    #         fonts(7)
    #         # d = dvalue(stdt, etdt, divisioncode)
    #         data(stdt, etdt, result, d)
    #         # date(result)
    #         #LowerLineData(result, d)
    #
    # elif divisioncode[-1] == divisioncode[-2]:
    #     if store[-1] == store[-2]:
    #         data(stdt,etdt,result,d)
    #
    #     elif store[-1] != store[-2]:
    #         data(stdt, etdt, result, d)
    #         # fonts(7)
    #         # printstoretotal(stdt, etdt, divisioncode)
    #         # storeclean()
    #         # d = dvalue(stdt, etdt, divisioncode)
    #         # boldfonts(7)
    #         # c.drawString(10, d, store[-1])
    #         # d = dvalue(stdt, etdt, divisioncode)
    #         # fonts(7)
    #         # if mrnno[-1] == mrnno[-2]:
    #         #     LowerLineData(result, d)
    #         # elif mrnno[-1] != mrnno[-2]:
    #         #     data(stdt, etdt, result, d)
    #         #     d = dvalue(stdt, etdt, divisioncode)
    #         #     date(result)
    #         #     LowerLineData(result, d)
    #
    #
    # elif divisioncode[-1] != divisioncode[-2]:
    #     # fonts(7)
    #     # printtotal()
    #     clbal = 0
    #     # printstoretotal(stdt, etdt, divisioncode)
    #     # storeclean()
    # #     d = dvalue(stdt, etdt, divisioncode)
    # #     printtotal()
    # #     companyclean()
    # #     # c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
    # #     c.showPage()
    # #     header(stdt, etdt, divisioncode)
    # #     d = newpage()
    #     # d=dvalue(stdt, etdt, divisioncode)
    #     data(stdt,etdt,result,d)
    # #     if store[-1] == store[-2]:
    # #         if mrnno[-1] == mrnno[-2]:
    # #             d = dvaluegst()
    # #             LowerLineData(result, d)
    # #         elif mrnno[-1] != mrnno[-2]:
    # #             data(stdt, etdt, result, d)
    # #             d = dvalue(stdt, etdt, divisioncode)
    # #             date(result)
    # #             LowerLineData(result, d)
    # #
    # #     elif store[-1] != store[-2]:
    # #         fonts(7)
    # #         # printstoretotal(stdt, etdt, divisioncode)
    # #         storeclean()
    # #         # d = dvalue(stdt, etdt, divisioncode)
    # #         boldfonts(7)
    # #         c.drawString(10, d, store[-1])
    # #         d = dvalue(stdt, etdt, divisioncode)
    # #         fonts(7)
    # #         if mrnno[-1] == mrnno[-2]:
    # #             LowerLineData(result, d)
    # #         elif mrnno[-1] != mrnno[-2]:
    # #             data(stdt, etdt, result, d)
    # #             d = dvalue(stdt, etdt, divisioncode)
    # #             date(result)
    # #             LowerLineData(result, d)