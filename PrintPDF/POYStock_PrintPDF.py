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
item = []
mrndivisioncode=[]
mrnstore=[]
issuedivisioncode=[]
issuestore=[]
pageno = 0
CompanyRecQtyTotal = 0
StoreBillAmtTotal = 0
CompanyIssQtyTotal = 0
StoreQuantityTotal = 0
CompanyOpQtyTotal=0
CompanyClQtyTotal=0
CompanyRecWtTotal=0
CompanyBoxesTotal=0
CompanyCopTotal=0
CompanyBoxeTotal=0
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

def mrnheader(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, str(divisioncode))
    boldfonts(9)
    c.drawCentredString(300, 780, "Yarn Receipt Note From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "GRN. No.")
    c.drawString(80, 755, "Supplier")
    c.drawString(270, 755, "Chal No.")
    c.drawString(340, 755, "Chal Dt.")
    c.drawString(410, 755, "LR No.")
    c.drawString(480, 755, "LR Dt.")
    c.drawString(550, 755, "Place")

    #Lowerline in Header
    c.drawString(80, 745, "Item Name")
    c.drawString(270, 745, "Lot No.")
    c.drawString(480, 745, "Recd wt")
    c.drawString(550, 745, "Boxes")

    # Lowerline in Header
    c.drawString(80, 735, "GRN Type")

    fonts(7)


def header(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, str(divisioncode))
    boldfonts(9)
    c.drawCentredString(300, 780, "POY Stock In Hand Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "Item")
    c.drawString(160,755, "Qlt.")
    c.drawString(200, 755, "Base")
    c.drawString(200, 745, "Lotcode")
    c.drawString(550, 745, "Mtd. Pur.")
    c.drawString(390, 755, "OpQty")
    c.drawString(450, 755, "Rec Qty")
    c.drawString(500, 755, "Iss QTY")
    c.drawString(550, 755, "Bal Qty")
    fonts(7)

def YarnIssueHeader(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, str(divisioncode))
    boldfonts(9)
    
    c.drawCentredString(300, 780, "Yarn Issued From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    # Upperline in header

    c.drawString(10, 755, "Dept.(Issued To)")
    c.drawString(110, 745, "Item Name")
    c.drawString(400, 755, "Lot No.")
    c.drawString(480, 755, "Quantity")
    c.drawString(550, 755, "Boxes")

    # Lowerline in Header
    c.drawString(10, 745, "Issue No.")
    c.drawString(400, 745, "Base Name")
    c.drawString(480, 745, "Iss. Dt")
    c.drawString(550, 745, "Cops")
    fonts(7)

def mrndata(stdt, etdt, result, d):
    c.drawString(10, d, str(result['MRNNO'])[:40])
    c.drawString(80, d, result['SUPPLIER'][:25])
    c.drawString(270, d, str(result['CHALLANNO']) if result['CHALLANNO'] != None else '')
    c.drawString(340, d, str(result['CHALLANDATE']) if result['CHALLANDATE'] != None else '')
    c.drawString(410, d, str(result['LRNO']) if result['LRNO'] != None else '')
    c.drawString(480, d, str(result['LRDATE']) if result['LRDATE'] != None else '')
    c.drawString(550, d, str(result['PLACE']) if result['PLACE'] != None else '')

    d = mrndvalue(stdt,etdt,mrndivisioncode)

    c.drawString(80, d, result['ITEMNAME'][:25])
    c.drawString(270, d, str(result['LOTCODE']) if result['LOTCODE'] != None else '')
    c.drawAlignedString(500, d, result['RECDWT'])
    c.drawAlignedString(570, d, str(result['BOXES']))

    d = mrndvalue(stdt, etdt, mrndivisioncode)
    mrntotal(result)

def data(stdt, etdt, result, d):
    global clbal
    clbal = clbal + float(result['BALQTY'])
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(result['PRODUCTNAME'])[:30])
    c.drawString(160,d,result['QUALITY'])
    c.drawString(200, d, result['BASE'])
    c.drawAlignedString(410, d, result['OPBAL'])
    c.drawAlignedString(470, d, result['RECQTY'])
    c.drawAlignedString(520, d, result['ISSQTY'])
    c.drawAlignedString(570, d, result['BALQTY'])
    d = dvalue(stdt, etdt, divisioncode)
    c.drawString(200, d, result['LOTCODE'])
    if result['MTDPUR'] != None:
        c.drawAlignedString(570, d, result['MTDPUR'])
    total(result)


def issuedata(stdt, etdt, result, d):
    c.drawString(10, d, result['TODEPARTMENT'])
    c.drawString(400, d, str(result['LOTNO']))
    c.drawString(480, d, result['QUANTITY'])
    c.drawString(550, d, str(result['BOXES']))
    d = issuedvalue(stdt,etdt,mrndivisioncode)
    c.drawString(10, d, result['ISSUENO'])
    c.drawString(400, d, result['BASENAME'])
    c.drawString(480, d, result['ISSUEDT'])
    c.drawString(550, d, str(result['COPS']))
    c.drawString(110, d, result['ITEMNAME'])
    d = issuedvalue(stdt, etdt, mrndivisioncode)

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

def mrntotal(result):
    global CompanyRecWtTotal
    global CompanyBoxesTotal
    CompanyRecWtTotal = CompanyRecWtTotal + float(("%.2f" % float(result['RECDWT'])))
    CompanyBoxesTotal = CompanyBoxesTotal + float(("%.3f" % float(result['BOXES'])))


def issuetotal(result):
    global CompanyCopTotal
    global CompanyBoxeTotal
    CompanyCopTotal = CompanyRecWtTotal + float(("%.2f" % float(result['RECDWT'])))
    CompanyBoxeTotal = CompanyBoxesTotal + float(("%.3f" % float(result['BOXES'])))

def mrnlogic(result):
    mrndivisioncode.append(result['DIVCODE'])
    mrnstore.append(result['ITEMNAME'])

def logic(result):
    divisioncode.append(result['DIVCODE'])
    store.append(result['PRODUCTNAME'])
    # mrnno.append(result['MRNNO'])

def issuelogic(result):
    issuedivisioncode.append(result['DIVCODE'])
    issuestore.append(result['ITEMNAME'])

def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, str(divisioncode[-2]))
        return d

def mrndvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        mrnheader(stdt, etdt, str(mrndivisioncode[-2]))
        return d

def issuedvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        YarnIssueHeader(stdt, etdt, str(issuedivisioncode[-2]))
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

def mrnnewrequest():
    global mrndivisioncode
    global pageno
    global mrnno
    global mrnstore
    mrndivisioncode = []
    pageno = 0
    mrnno = []
    mrnstore = []

def issuenewrequest():
    global issuedivisioncode
    global pageno
    global mrnno
    global issuestore
    issuedivisioncode = []
    pageno = 0
    mrnno = []
    issuestore = []

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

def printtotallast():
    boldfonts(7)
    global d
    global CompanyRecQtyTotal
    global CompanyIssQtyTotal
    global CompanyOpQtyTotal
    global CompanyClQtyTotal
    c.drawString(40, d, str(divisioncode[-1]) + " TOTAL : ")
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

def printmrntotal():
    boldfonts(7)
    global d
    global CompanyRecWtTotal
    global CompanyBoxesTotal
    c.drawString(40, d, str(mrndivisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(round(CompanyRecWtTotal, 2)))
    c.drawAlignedString(570, d, str(round(CompanyBoxesTotal, 2)))
    CompanyRecWtTotal = 0
    CompanyBoxesTotal = 0
    
def printmrntotallast():
    boldfonts(7)
    global d
    global CompanyRecWtTotal
    global CompanyBoxesTotal
    c.drawString(40, d, str(mrndivisioncode[-1]) + " TOTAL : ")
    c.drawAlignedString(500, d, str(round(CompanyRecWtTotal, 2)))
    c.drawAlignedString(570, d, str(round(CompanyBoxesTotal, 2)))
    CompanyRecWtTotal = 0
    CompanyBoxesTotal = 0

def printissuetotal():
    boldfonts(7)
    global d
    global CompanyBoxeTotal
    global CompanyCopTotal
    c.drawString(40, d, str(issuedivisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(550, d, str(round(CompanyBoxeTotal, 2)))
    d = d - 10
    c.drawAlignedString(550, d, str(round(CompanyCopTotal, 2)))
    fonts(7)

    CompanyBoxeTotal = 0
    CompanyCopTotal = 0

def printissuetotallast():
    boldfonts(7)
    global d
    global CompanyBoxeTotal
    global CompanyCopTotal
    c.drawString(40, d, str(issuedivisioncode[-1]) + " TOTAL : ")
    c.drawAlignedString(550, d, str(round(CompanyBoxeTotal, 2)))
    d = d - 10
    c.drawAlignedString(550, d, str(round(CompanyCopTotal, 2)))
    fonts(7)

    CompanyBoxeTotal = 0
    CompanyCopTotal = 0

def printmrnstoretotal(stdt, etdt, mrndivisioncode):
    boldfonts(7)
    global StoreBillAmtTotal
    global StoreQuantityTotal
    c.drawString(40, d, str(mrnstore[-2]) + " TOTAL : ")
    c.drawAlignedString(560, d, str(locale.currency(float(StoreBillAmtTotal), grouping=True))[1:])
    c.drawAlignedString(310, d, str("%.3f" % float(StoreQuantityTotal)))
    fonts(7)
    dvalue(stdt, etdt, mrndivisioncode)


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

def mrntextsize(c, result, d, stdt, etdt):
    global clbal
    d = mrndvalue(stdt, etdt, mrndivisioncode)
    mrnlogic(result)
    mrndata(stdt, etdt, result, d)
    # if len(mrndivisioncode) == 1:
    #     if len(mrnstore) == 1:
    #         mrnheader(stdt, etdt, mrndivisioncode)
    #         fonts(7)
            

    # elif mrndivisioncode[-1] == mrndivisioncode[-2]:
    #     if mrnstore[-1] == mrnstore[-2]:
    #         mrndata(stdt, etdt, result, d)
    #     elif mrnstore[-1] != mrnstore[-2]:
    #         mrndata(stdt, etdt, result, d)

    # elif mrndivisioncode[-1] != mrndivisioncode[-2]:
    #     fonts(7)
    #     printmrntotal()
    #     clbal = 0
    #     c.showPage()
    #     mrnheader(stdt, etdt, mrndivisioncode)
    #     d = newpage()
    #     mrndata(stdt, etdt, result, d)

def textsize(c, result, d, stdt, etdt):
    global clbal
    d = dvalue(stdt, etdt, divisioncode)
    logic(result)
    # if len(divisioncode) == 1:
    #     if len(store) == 1:
    #         header(stdt, etdt, divisioncode)
    #         fonts(7)
    #         data(stdt, etdt, result, d)
    data(stdt, etdt, result, d)
#     elif divisioncode[-1] == divisioncode[-2]:
#         if store[-1] == store[-2]:
#             data(stdt,etdt,result,d)

#         elif store[-1] != store[-2]:
#             data(stdt, etdt, result, d)

#     elif divisioncode[-1] != divisioncode[-2]:
#         fonts(7)
#         # printtotal()
#         clbal = 0
#         # c.showPage()
#         header(stdt, etdt, divisioncode)
#         d = newpage()
#         data(stdt,etdt,result,d)

def YarnIssuetextsize(c, result, d, stdt, etdt):
    global clbal
    d = issuedvalue(stdt, etdt, issuedivisioncode)
    issuelogic(result)
    issuedata(stdt, etdt, result, d)
    # if len(issuedivisioncode) == 1:
    #     if len(issuestore) == 1:
    #         YarnIssueHeader(stdt, etdt, issuedivisioncode)
    #         fonts(7)
    #         issuedata(stdt, etdt, result, d)

    # elif issuedivisioncode[-1] == issuedivisioncode[-2]:
    #     if issuestore[-1] == issuestore[-2]:
    #         issuedata(stdt,etdt,result,d)

    #     elif issuestore[-1] != issuestore[-2]:
    #         issuedata(stdt, etdt, result, d)

    # elif issuedivisioncode[-1] != issuedivisioncode[-2]:
    #     fonts(7)
    #     printtotal()
    #     clbal = 0
    #     c.showPage()
    #     YarnIssueHeader(stdt, etdt, issuedivisioncode)
    #     d = newpage()
    #     issuedata(stdt,etdt,result,d)