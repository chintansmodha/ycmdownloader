from glob import glob
from tkinter import font
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
c = canvas.Canvas("1.pdf")
d = 730

divisioncode = []
item = []
sumdivisioncode = []
sumitem = []
CompanyAmountTotal = 0
pageno = 0

ItemQuantityTotal = 0
ItemAmountTotal = 0
GrandQuantityTotal = 0
GrandAmountTotal = 0

SumGrpOpnTotal = 0
SumGrpRecTotal = 0
SumGrpIssTotal = 0
SumGrpIssRetTotal = 0
SumGrpChlRetTotal = 0
SumGrandOpnTotal = 0
SumGrandRecTotal = 0
SumGrandIssTotal = 0
SumGrandIssRetTotal = 0
SumGrandChlRetTotal = 0
ServiceType=[]
Service=[]
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


def header(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Purchase ItemWise From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "Date")
    c.drawString(60, 755, "Type")
    c.drawString(110, 755, "Number")
    c.drawString(200, 755, "Supplier/Department")

    c.drawString(460, 755, "Recd. Qty")
    c.drawString(510, 755, "Iss. Qty")
    c.drawString(560, 755, "Balance")
    fonts(7)


def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['TXNDATE']))
    c.drawString(60, d, str(result['TXNTYPE']))
    c.drawString(110, d, str(result['TXNNO']))
    if result['DEPT'] != None:
        c.drawString(200, d, result['DEPT'])
    c.drawAlignedString(480, d, str(("%.3f" % float(result['RECQTY']))))
    c.drawAlignedString(530, d, str(("%.2f" % float(result['ISSQTY']))))
    c.drawAlignedString(580, d, str(("%.2f" % float(result['BALQTY']))))
    total(result)


def total(result):
    global ItemAmountTotal
    global ItemQuantityTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['RECQTY'])))
    ItemQuantityTotal = ItemQuantityTotal + (float("%.2f" % float(result['ISSQTY'])))
    GrandAmountTotal = GrandAmountTotal + (float("%.2f" % float(result['RECQTY'])))
    GrandQuantityTotal = GrandQuantityTotal + (float("%.2f" % float(result['ISSQTY'])))


def logic(result):
    global divisioncode
    global item
    global Service
    divisioncode.append(result['COMPANY'])
    item.append(result['ITEM'])
    Service.append(result['SERVICETYPE'])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 730
    return d


def newrequest():
    global divisioncode
    global pageno
    global item
    global Service
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    divisioncode = []
    pageno = 0
    item = []
    Service=[]
    ItemQuantityTotal = 0
    ItemAmountTotal = 0
    GrandQuantityTotal = 0
    GrandAmountTotal = 0


def textsize(c, result, d, stdt, etdt):
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    d = dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(item) == 1:
            header(stdt, etdt, divisioncode)
            boldfonts(9)
            c.drawString(10,d,result['SERVICETYPE'])
            d = dvalue(stdt, etdt, divisioncode)
            if result['DEPT'] != None:
                c.drawString(10,d,result['DEPT'])
                d = dvalue(stdt, etdt, divisioncode)
            c.drawCentredString(300, d, result['ITEM'])
            fonts(7)
            d = dvalue(stdt, etdt, divisioncode)
            data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Service[-1]==Service[-2]:
            if item[-1] == item[-2]:
                data(result, d)
            elif item[-1] != item[-2]:
                boldfonts(9)
                c.drawString(200, d, "Item Total : ")
                c.drawAlignedString(530, d, str("%.2f" % float(ItemQuantityTotal)))
                c.drawAlignedString(480, d, str("%.2f" % float(ItemAmountTotal)))
                ItemAmountTotal = 0
                ItemQuantityTotal = 0
                d = dvalue(stdt, etdt, divisioncode)
                d = dvalue(stdt, etdt, divisioncode)
                boldfonts(9)
                c.drawCentredString(300, d, result['ITEM'])
                fonts(7)
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
        elif Service[-1]!=Service[-2]:
            if item[-1] == item[-2]:
                c.drawString(10,d,result['SERVICETYPE'])
                d = dvalue(stdt, etdt, divisioncode)
                if result['DEPT'] != None:
                    c.drawString(10,d,result['DEPT'])
                    d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
            elif item[-1] != item[-2]:
                boldfonts(9)
                c.drawString(200, d, "Item Total : ")
                c.drawAlignedString(530, d, str("%.2f" % float(ItemQuantityTotal)))
                c.drawAlignedString(480, d, str("%.2f" % float(ItemAmountTotal)))
                ItemAmountTotal = 0
                ItemQuantityTotal = 0
                d = dvalue(stdt, etdt, divisioncode)
                d = dvalue(stdt, etdt, divisioncode)
                boldfonts(9)
                c.drawString(10,d,result['SERVICETYPE'])
                d = dvalue(stdt, etdt, divisioncode)
                if result['DEPT'] != None:
                    c.drawString(10,d,result['DEPT'])
                d = dvalue(stdt, etdt, divisioncode)
                c.drawCentredString(300, d, result['ITEM'])
                fonts(7)
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Item Total : ")
        c.drawAlignedString(530, d, str("%.2f" % float(ItemQuantityTotal)))
        c.drawAlignedString(480, d, str("%.2f" % float(ItemAmountTotal)))
        ItemAmountTotal = 0
        ItemQuantityTotal = 0
        d = dvalue(stdt, etdt, divisioncode)
        c.drawString(200, d, "Grand Total : ")
        c.drawAlignedString(530, d, str("%.2f" % float(GrandQuantityTotal)))
        c.drawAlignedString(480, d, str("%.2f" % float(GrandAmountTotal)))
        GrandQuantityTotal = 0
        GrandAmountTotal = 0
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        boldfonts(9)
        c.drawString(10,d,result['SERVICETYPE'])
        d = dvalue(stdt, etdt, divisioncode)
        if result['DEPT'] != None:
            c.drawString(10,d,result['DEPT'])
            d = dvalue(stdt, etdt, divisioncode)
        c.drawCentredString(300, d, result['ITEM'])
        d = dvalue(stdt, etdt, divisioncode)
        fonts(7)
        data(result, d)


#############################################################################################################################

def sumdvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        sumheader(stdt, etdt, divisioncode)
        return d


def sumheader(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Purchase ItemWise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "Item")
    c.drawString(260, 755, "Location")
    c.drawString(410, 755, "Opening")
    c.drawString(460, 755, "Receipt")
    c.drawString(510, 755, "Issue")
    c.drawString(560, 755, "Chl Ret")
    fonts(7)


def sumdata(result, d):
    fonts(7)
    c.drawString(10, d, result['ITEM'])
    # c.drawString(260, d, str(result['DEPT']))
    c.drawAlignedString(430, d, str(result['OPBAL']))
    c.drawAlignedString(480, d, str(("%.3f" % float(result['RECQTY']))))
    c.drawAlignedString(530, d, str(("%.2f" % float(result['ISSQTY']))))
    c.drawAlignedString(580, d, str(("%.2f" % float(result['CHALANRET']))))
    
    sumtotal(result)


def sumtotal(result):
    global SumGrpOpnTotal
    global SumGrpRecTotal
    global SumGrpIssTotal
    # global SumGrpIssRetTotal
    global SumGrpChlRetTotal

    global SumGrandOpnTotal
    global SumGrandRecTotal
    global SumGrandIssTotal
    # global SumGrandIssRetTotal
    global SumGrandChlRetTotal

    SumGrpOpnTotal = SumGrpOpnTotal + (float("%.2f" % float(result['OPBAL'])))
    SumGrpRecTotal = SumGrpRecTotal + (float("%.2f" % float(result['RECQTY'])))
    SumGrpIssTotal = SumGrpIssTotal + (float("%.2f" % float(result['ISSQTY'])))
    # SumGrpIssRetTotal = SumGrpIssRetTotal + (float("%.2f" % float(result['ISSQTY'])))
    SumGrpChlRetTotal = SumGrpChlRetTotal + (float("%.2f" % float(result['CHALANRET'])))

    SumGrandOpnTotal = SumGrandOpnTotal + (float("%.2f" % float(result['OPBAL'])))
    SumGrandRecTotal = SumGrandRecTotal + (float("%.2f" % float(result['RECQTY'])))
    SumGrandIssTotal = SumGrandIssTotal + (float("%.2f" % float(result['ISSQTY'])))
    # SumGrandIssRetTotal = SumGrandIssRetTotal + (float("%.2f" % float(result['ISSQTY'])))
    SumGrandChlRetTotal = SumGrandChlRetTotal + (float("%.2f" % float(result['CHALANRET'])))


def sumlogic(result):
    global sumdivisioncode
    global sumitem
    global ServiceType
    ServiceType.append(result['SERVICETYPE'])
    sumdivisioncode.append(result['DIVCODE'])
    sumitem.append(result['ITEMGROUP'])


def sumdlocvalue(d):
    d = d - 20
    return d


def sumnewpage():
    global d
    d = 730
    return d


def sumnewrequest():
    global divisioncode
    global pageno
    global item
    global ServiceType
    global SumGrpOpnTotal
    global SumGrpRecTotal
    global SumGrpIssTotal
    # global SumGrpIssRetTotal
    global SumGrpChlRetTotal

    global SumGrandOpnTotal
    global SumGrandRecTotal
    global SumGrandIssTotal
    # global SumGrandIssRetTotal
    global SumGrandChlRetTotal

    divisioncode = []
    pageno = 0
    item = []
    ServiceType=[]
    SumGrpOpnTotal = 0
    SumGrpRecTotal = 0
    SumGrpIssTotal = 0
    SumGrpIssRetTotal = 0
    SumGrpChlRetTotal = 0
    SumGrandOpnTotal = 0
    SumGrandRecTotal = 0
    SumGrandIssTotal = 0
    SumGrandIssRetTotal = 0
    SumGrandChlRetTotal = 0


def sumcompanyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0


def sumtextsize(c, result, d, stdt, etdt):
    global SumGrpOpnTotal
    global SumGrpRecTotal
    global SumGrpIssTotal
    # global SumGrpIssRetTotal
    global SumGrpChlRetTotal

    global SumGrandOpnTotal
    global SumGrandRecTotal
    global SumGrandIssTotal
    # global SumGrandIssRetTotal
    global SumGrandChlRetTotal

    d = sumdvalue(stdt, etdt, sumdivisioncode)
    sumlogic(result)
    if len(sumdivisioncode) == 1:
        if len(sumitem) == 1:
            sumheader(stdt, etdt, sumdivisioncode)
            boldfonts(9)
            c.drawString(10,d,result['SERVICETYPE'])
            d = sumdvalue(stdt, etdt, sumdivisioncode)
            c.drawCentredString(300, d, result['ITEMGROUP'])
            fonts(7)
            d = sumdvalue(stdt, etdt, sumdivisioncode)
            sumdata(result, d)

    elif sumdivisioncode[-1] == sumdivisioncode[-2]:
        if ServiceType[-1]==ServiceType[-2]:
            if sumitem[-1] == sumitem[-2]:
                sumdata(result, d)
            elif sumitem[-1] != sumitem[-2]:
                boldfonts(8)
                c.drawString(200, d, "Group Total : ")
                c.drawAlignedString(430, d, str("%.2f" % float(SumGrpOpnTotal)))
                c.drawAlignedString(480, d, str("%.2f" % float(SumGrpRecTotal)))
                c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssTotal)))
                # c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssRetTotal)))
                c.drawAlignedString(580, d, str("%.2f" % float(SumGrpChlRetTotal)))
                SumGrpOpnTotal = 0
                SumGrpRecTotal = 0
                SumGrpIssTotal = 0
                SumGrpChlRetTotal = 0
        
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                boldfonts(9)
                c.drawCentredString(300, d, result['ITEMGROUP'])
                fonts(7)
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                sumdata(result, d)
        elif ServiceType[-1]!=ServiceType[-2]:
            if sumitem[-1] == sumitem[-2]:
                boldfonts(8)
                c.drawString(10,d,result['SERVICETYPE'])
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                sumdata(result, d)
            elif sumitem[-1] != sumitem[-2]:
                boldfonts(8)
                c.drawString(200, d, "Group Total : ")
                c.drawAlignedString(430, d, str("%.2f" % float(SumGrpOpnTotal)))
                c.drawAlignedString(480, d, str("%.2f" % float(SumGrpRecTotal)))
                c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssTotal)))
                # c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssRetTotal)))
                c.drawAlignedString(580, d, str("%.2f" % float(SumGrpChlRetTotal)))
                SumGrpOpnTotal = 0
                SumGrpRecTotal = 0
                SumGrpIssTotal = 0
                SumGrpChlRetTotal = 0
        
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                boldfonts(9)
                c.drawString(10,d,result['SERVICETYPE'])
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                c.drawCentredString(300, d, result['ITEMGROUP'])
                fonts(7)
                d = sumdvalue(stdt, etdt, sumdivisioncode)
                sumdata(result, d)

    elif sumdivisioncode[-1] != sumdivisioncode[-2]:
        boldfonts(8)
        c.drawString(200, d, "Group Total : ")
        c.drawAlignedString(430, d, str("%.2f" % float(SumGrpOpnTotal)))
        c.drawAlignedString(480, d, str("%.2f" % float(SumGrpRecTotal)))
        c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssTotal)))
        # c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssRetTotal)))
        c.drawAlignedString(580, d, str("%.2f" % float(SumGrpChlRetTotal)))
        SumGrpOpnTotal = 0
        SumGrpRecTotal = 0
        SumGrpIssTotal = 0
        SumGrpChlRetTotal = 0

        d = sumdvalue(stdt, etdt, sumdivisioncode)
        c.drawString(200, d, "Grand Total : ")
        c.drawAlignedString(430, d, str("%.2f" % float(SumGrandOpnTotal)))
        c.drawAlignedString(480, d, str("%.2f" % float(SumGrandRecTotal)))
        c.drawAlignedString(530, d, str("%.2f" % float(SumGrandIssTotal)))
        # c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssRetTotal)))
        c.drawAlignedString(580, d, str("%.2f" % float(SumGrandChlRetTotal)))
        SumGrandOpnTotal=0
        SumGrandRecTotal=0
        SumGrandIssTotal=0
        SumGrandChlRetTotal=0
        c.showPage()

        sumheader(stdt, etdt, sumdivisioncode)
        d = newpage()
        boldfonts(8)
        c.drawString(10,d,result['SERVICETYPE'])
        d = sumdvalue(stdt, etdt, sumdivisioncode)
        c.drawCentredString(300, d, result['ITEMGROUP'])
        d = sumdvalue(stdt, etdt, sumdivisioncode)
        fonts(7)
        sumdata(result, d)
