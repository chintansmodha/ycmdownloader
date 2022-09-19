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
item=[]
sumdivisioncode = []
sumitem=[]
CompanyAmountTotal = 0
pageno = 0

ItemQuantityTotal=0
ItemAmountTotal=0
GrandQuantityTotal=0
GrandAmountTotal=0
SumItemQuantityTotal=0
SumItemAmountTotal=0
SumGrandQuantityTotal=0
SumGrandAmountTotal=0
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
    c.drawCentredString(300, 780, "Purchase ItemWise From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "GRN. No.")
    c.drawString(60, 755, "Vch. Dt.")
    c.drawString(110, 755, "Bill. Dt.")
    c.drawString(160, 755, "Bill. No.")
    c.drawString(240, 755, "Supplier")
    c.drawString(460, 755, "Quantity")
    c.drawString(510, 755, "Rate")
    c.drawString(560, 755, "Amount")
    fonts(7)
def data(result, d):
    fonts(7)
    c.drawString(10, d, result['MRNNO'])
    c.drawString(60, d, str(result['FINDATE']))
    c.drawString(110, d, str(result['BILLDATE']))
    c.drawString(160, d, result['BILLNO'])
    c.drawString(240, d, result['SUPPLIER'])
    c.drawAlignedString(480, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(530, d, str(("%.2f" % float(result['RATE']))))
    c.drawAlignedString(580, d, str(("%.2f" % float(result['BASICVALUE']))))
    total(result)

def total(result):
    global ItemAmountTotal
    global ItemQuantityTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    ItemQuantityTotal = ItemQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    GrandAmountTotal = GrandAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    GrandQuantityTotal = GrandQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))

def logic(result):
    global divisioncode
    global item
    divisioncode.append(result['DIVCODE'])
    item.append(result['ITEM'])

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
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    divisioncode = []
    pageno = 0
    item=[]
    ItemQuantityTotal=0
    ItemAmountTotal=0
    GrandQuantityTotal=0
    GrandAmountTotal=0

def textsize(c, result, d, stdt, etdt):
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    d = dvalue(stdt,etdt,divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(item) == 1:
            header(stdt, etdt, divisioncode)
            boldfonts(9)
            c.drawCentredString(300,d,result['ITEM'])
            fonts(7)
            d = dvalue(stdt,etdt,divisioncode)
            data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if item[-1] == item[-2]:
            data(result, d)
        elif item[-1] != item[-2]:
            boldfonts(9)
            c.drawString(200, d, "Item Total : ")
            c.drawAlignedString(480, d, str("%.2f" % float(ItemQuantityTotal)))
            c.drawAlignedString(580, d, str("%.2f" % float(ItemAmountTotal)))
            ItemAmountTotal=0
            ItemQuantityTotal=0
            d = dvalue(stdt,etdt,divisioncode)
            d = dvalue(stdt,etdt,divisioncode)
            boldfonts(9)
            c.drawCentredString(300,d,result['ITEM'])
            fonts(7)
            d = dvalue(stdt,etdt,divisioncode)
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Item Total : ")
        c.drawAlignedString(480, d, str("%.2f" % float(ItemQuantityTotal)))
        c.drawAlignedString(580, d, str("%.2f" % float(ItemAmountTotal)))
        ItemAmountTotal=0
        ItemQuantityTotal=0
        d = dvalue(stdt,etdt,divisioncode)
        c.drawString(200, d, "Grand Total : ")
        c.drawAlignedString(480, d, str("%.2f" % float(GrandQuantityTotal)))
        c.drawAlignedString(580, d, str("%.2f" % float(GrandAmountTotal)))
        GrandQuantityTotal=0
        GrandAmountTotal=0
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        boldfonts(9)
        c.drawCentredString(300,d,result['ITEM'])
        d = dvalue(stdt,etdt,divisioncode)
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
        header(stdt, etdt, divisioncode)
        return d

def sumheader(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Purchase ItemWise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "Supplier")
    c.drawString(410, 755, "Vch. No.")
    c.drawString(460, 755, "Quantity")
    c.drawString(510, 755, "Brk Amt.")
    c.drawString(560, 755, "Bill Amt.")
    fonts(7)

def sumdata(result, d):
    fonts(7)
    c.drawString(10, d, result['SUPPLIER'])
    c.drawString(410, d, str(result['FINNO']))
    c.drawAlignedString(480, d, str(result['QUANTITY']))
    c.drawAlignedString(530, d, str(("%.3f" % float(result['BASICVALUE']))))
    c.drawAlignedString(580, d, str(("%.2f" % float(result['BILLAMOUNT']))))
    sumtotal(result)

def sumtotal(result):
    global SumItemAmountTotal
    global SumItemQuantityTotal
    global SumGrandAmountTotal
    global SumGrandQuantityTotal
    SumItemAmountTotal = SumItemAmountTotal + (float("%.2f" % float(result['BILLAMOUNT'])))
    SumItemQuantityTotal = SumItemQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    SumGrandAmountTotal = SumGrandAmountTotal + (float("%.2f" % float(result['BILLAMOUNT'])))
    SumGrandQuantityTotal = SumGrandQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))

def sumlogic(result):
    global sumdivisioncode
    global sumitem
    sumdivisioncode.append(result['DIVCODE'])
    sumitem.append(result['ITEM'])

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
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    divisioncode = []
    pageno = 0
    item=[]
    ItemQuantityTotal=0
    ItemAmountTotal=0
    GrandQuantityTotal=0
    GrandAmountTotal=0

def sumcompanyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0

def sumtextsize(c, result, d, stdt, etdt):
    global SumItemQuantityTotal
    global SumItemAmountTotal
    global SumGrandAmountTotal
    global SumGrandQuantityTotal
    d = sumdvalue(stdt,etdt,sumdivisioncode)
    sumlogic(result)
    if len(sumdivisioncode) == 1:
        if len(sumitem) == 1:
            sumheader(stdt, etdt, sumdivisioncode)
            boldfonts(9)
            c.drawCentredString(300,d,result['ITEM'])
            fonts(7)
            d = sumdvalue(stdt,etdt,sumdivisioncode)
            sumdata(result, d)

    elif sumdivisioncode[-1] == sumdivisioncode[-2]:
        if sumitem[-1] == sumitem[-2]:
            sumdata(result, d)
        elif sumitem[-1] != sumitem[-2]:
            boldfonts(9)
            c.drawString(200, d, "Item Total : ")
            c.drawAlignedString(480, d, str("%.2f" % float(SumItemQuantityTotal)))
            c.drawAlignedString(580, d, str("%.2f" % float(SumItemAmountTotal)))
            SumItemAmountTotal=0
            SumItemQuantityTotal=0
            d = dvalue(stdt,etdt,sumdivisioncode)
            d = dvalue(stdt,etdt,sumdivisioncode)
            boldfonts(9)
            c.drawCentredString(300,d,result['ITEM'])
            fonts(7)
            d = dvalue(stdt,etdt,sumdivisioncode)
            sumdata(result, d)

    elif sumdivisioncode[-1] != sumdivisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Item Total : ")
        c.drawAlignedString(480, d, str("%.2f" % float(SumItemQuantityTotal)))
        c.drawAlignedString(580, d, str("%.2f" % float(SumItemAmountTotal)))
        SumItemAmountTotal=0
        SumItemQuantityTotal=0
        d = dvalue(stdt,etdt,sumdivisioncode)
        c.drawString(200, d, "Grand Total : ")
        c.drawAlignedString(480, d, str("%.2f" % float(SumGrandQuantityTotal)))
        c.drawAlignedString(580, d, str("%.2f" % float(SumGrandAmountTotal)))
        SumGrandQuantityTotal=0
        SumGrandAmountTotal=0
        c.showPage()

        sumheader(stdt, etdt, sumdivisioncode)
        d = newpage()
        boldfonts(9)
        c.drawCentredString(300,d,result['ITEM'])
        d = sumdvalue(stdt,etdt,sumdivisioncode)
        fonts(7)
        sumdata(result, d)


        