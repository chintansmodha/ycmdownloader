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
unit=[]
sumdivisioncode = []
sumitem=[]
prdivisioncode=[]
pritem=[]
prunit=[]
supdivisioncode=[]
supitem=[]
supunit=[]
CompanyAmountTotal = 0
pageno = 0

ItemQuantityTotal=0
ItemAmountTotal=0
CompanyQuantityTotal=0
CompanyAmountTotal=0
GrandQuantityTotal=0
GrandAmountTotal=0

SumItemQuantityTotal=0
SumItemAmountTotal=0
SumGrandQuantityTotal=0
SumGrandAmountTotal=0

PrItemQuantityTotal=0
PrItemAmountTotal=0
PrGrandQuantityTotal=0
PrGrandAmountTotal=0
PrCompanyAmountTotal = 0
PrCompanyQuantityTotal = 0

supItemQuantityTotal=0
supItemAmountTotal=0
supItemRateTotal=0
supGrandQuantityTotal=0
supGrandAmountTotal=0
supGrandRateTotal=0
supCompanyAmountTotal = 0
supCompanyQuantityTotal = 0
supCompanyRateTotal=0

supcounter=0
supcounter1=0
prcounter=0
counter=0

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
    c.drawCentredString(300, 780, "Purchase Item Group Wise Item Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    
    # Upperline in header
    c.drawString(10, 755, "Group")
    c.drawString(60, 755, "Item Name")
    c.drawString(440, 755, "Quantity")
    c.drawString(520, 755, "Amount")
    c.drawString(570, 755, "Rate")
    fonts(7)

def data(result, d):
    fonts(7)
    c.drawString(60, d, str(result['ITEM']))
    c.drawAlignedString(460, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(540, d, str(("%.2f" % float(result['BASICVALUE']))))
    c.drawAlignedString(580, d, str(("%.2f" % float(result['RATE']))))
    total(result)

def total(result):
    global ItemAmountTotal
    global ItemQuantityTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    global CompanyAmountTotal
    global CompanyQuantityTotal
    ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    ItemQuantityTotal = ItemQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    GrandAmountTotal = GrandAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    GrandQuantityTotal = GrandQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    CompanyQuantityTotal = CompanyQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))

def logic(result):
    global divisioncode
    global item
    global unit
    divisioncode.append(result['PLANT'])
    item.append(result['ITEMGROUP'])
    unit.append(result['DIVCODE'])

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global divisioncode
    global unit
    global pageno
    global item
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    divisioncode = []
    pageno = 0
    item=[]
    unit=[]
    ItemQuantityTotal=0
    ItemAmountTotal=0
    GrandQuantityTotal=0
    GrandAmountTotal=0

def textsize(c, result, d, stdt, etdt):
    global ItemQuantityTotal
    global ItemAmountTotal
    global GrandAmountTotal
    global GrandQuantityTotal
    global CompanyQuantityTotal
    global CompanyAmountTotal
    d = dvalue(stdt,etdt,divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(unit)==1:
            if len(item) == 1:
                header(stdt, etdt, divisioncode)
                boldfonts(9)
                c.drawString(10,d,result['DIVCODE'])
                d = dvalue(stdt,etdt,divisioncode)
                c.drawString(40,d,result['ITEMGROUP'])
                fonts(7)
                d = dvalue(stdt,etdt,divisioncode)
                data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if unit[-1] == unit[-2]:
            if item[-1] == item[-2]:
                data(result, d)
            elif item[-1] != item[-2]:
                boldfonts(9)
                c.drawString(200, d, "Item Group Total : ")
                c.drawAlignedString(460, d, str("%.2f" % float(ItemQuantityTotal)))
                c.drawAlignedString(540, d, str("%.2f" % float(ItemAmountTotal)))
                ItemAmountTotal=0
                ItemQuantityTotal=0
                d = dvalue(stdt,etdt,divisioncode)
                d = dvalue(stdt,etdt,divisioncode)
                boldfonts(9)
                c.drawString(40,d,result['ITEMGROUP'])
                fonts(7)
                d = dvalue(stdt,etdt,divisioncode)
                data(result, d)

        elif unit[-1] != unit[-2]:
            boldfonts(9)
            c.drawString(200, d, "Item Total : ")
            c.drawAlignedString(460, d, str("%.2f" % float(ItemQuantityTotal)))
            c.drawAlignedString(540, d, str("%.2f" % float(ItemAmountTotal)))
            ItemAmountTotal=0
            ItemQuantityTotal=0
            d = dvalue(stdt,etdt,divisioncode)
            c.drawString(200, d, "Company Total : ")
            c.drawAlignedString(460, d, str("%.2f" % float(CompanyQuantityTotal)))
            c.drawAlignedString(540, d, str("%.2f" % float(CompanyAmountTotal)))
            CompanyQuantityTotal=0
            CompanyAmountTotal=0
            d = dvalue(stdt,etdt,divisioncode)
            d = dvalue(stdt,etdt,divisioncode)
            c.drawString(10,d,result['DIVCODE'])
            d = dvalue(stdt,etdt,divisioncode)
            c.drawString(40,d,result['ITEMGROUP'])
            fonts(7)
            d = dvalue(stdt,etdt,divisioncode)
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Item Total : ")
        c.drawAlignedString(460, d, str("%.2f" % float(ItemQuantityTotal)))
        c.drawAlignedString(540, d, str("%.2f" % float(ItemAmountTotal)))
        ItemAmountTotal=0
        ItemQuantityTotal=0
        d = dvalue(stdt,etdt,divisioncode)
        c.drawString(200, d, "Company Total : ")
        c.drawAlignedString(460, d, str("%.2f" % float(CompanyQuantityTotal)))
        c.drawAlignedString(540, d, str("%.2f" % float(CompanyAmountTotal)))
        CompanyQuantityTotal=0
        CompanyAmountTotal=0
        c.showPage()
        header(stdt, etdt, divisioncode)
        d = newpage()
        boldfonts(9)
        c.drawString(40,d,result['ITEMGROUP'])
        d = dvalue(stdt,etdt,divisioncode)
        fonts(7)
        data(result, d)

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
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
    c.drawCentredString(300, 780, "Production Item Group Wise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "Item Group")
    c.drawString(410, 755, "Quantity")
    c.drawString(480, 755, "Amount")
    c.drawString(550, 755, "Avg. Rate")
    fonts(7)

def sumdata(result, d):
    fonts(7)
    c.drawString(10, d, result['ITEMGROUP'])
    c.drawAlignedString(430, d, str(result['QUANTITY']))
    c.drawAlignedString(510, d, str(("%.3f" % float(result['BASICVALUE']))))
    c.drawAlignedString(570, d, str(("%.2f" % float(result['RATE']))))
    sumtotal(result)

def sumtotal(result):
    global SumItemAmountTotal
    global SumItemQuantityTotal
    global SumGrandAmountTotal
    global SumGrandQuantityTotal
    SumItemAmountTotal = SumItemAmountTotal + (float("%.2f" % float(result['RATE'])))
    SumItemQuantityTotal = SumItemQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    SumGrandAmountTotal = SumGrandAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    SumGrandQuantityTotal = SumGrandQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))

def sumlogic(result):
    global sumdivisioncode
    global sumitem
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
    global sumdivisioncode
    global pageno
    global sumitem
    global SumItemQuantityTotal
    global SumItemAmountTotal
    global SumGrandAmountTotal
    global SumGrandQuantityTotal
    sumdivisioncode = []
    pageno = 0
    sumitem=[]
    SumItemQuantityTotal=0
    SumItemAmountTotal=0
    SumGrandQuantityTotal=0
    SumGrandAmountTotal=0

def sumcompanyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0

def sumtextsize(c, result, d, stdt, etdt):
    global SumItemQuantityTotal
    global SumItemAmountTotal
    global SumGrandAmountTotal
    global SumGrandQuantityTotal
    global counter
    counter = counter + 1
    d = sumdvalue(stdt,etdt,sumdivisioncode)
    sumlogic(result)
    if len(sumdivisioncode) == 1:
        sumheader(stdt, etdt, sumdivisioncode)
        d = sumdvalue(stdt,etdt,sumdivisioncode)
        sumdata(result, d)

    elif sumdivisioncode[-1] == sumdivisioncode[-2]:
        sumdata(result, d)

    elif sumdivisioncode[-1] != sumdivisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Grand Total : ")
        c.drawAlignedString(430, d, str("%.2f" % float(SumGrandQuantityTotal)))
        c.drawAlignedString(510, d, str("%.2f" % float(SumGrandAmountTotal)))
        c.drawAlignedString(570, d, str("%.2f" % float(SumItemAmountTotal/counter-1)))
        SumGrandQuantityTotal=0
        SumGrandAmountTotal=0
        SumItemAmountTotal=0
        print(counter)
        counter=1
        c.showPage()

        sumheader(stdt, etdt, sumdivisioncode)
        d = newpage()
        sumdata(result, d)

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


def prdvalue(stdt, etdt, prdivisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = prnewpage()
        c.showPage()
        prheader(stdt, etdt, prdivisioncode)
        return d

def prheader(stdt, etdt, prdivisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, prdivisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "Productiom Item Group Wise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    
    # Upperline in header
    c.drawString(10, 755, "Supplier")
    c.drawString(60, 755, "Item Group")
    c.drawString(420, 755, "Quantity")
    c.drawString(500, 755, "Amount")
    c.drawString(550, 755, "Avg. Rate")
    fonts(7)

def prdata(result, d):
    fonts(7)
    c.drawString(60, d, str(result['ITEMGROUP']))
    c.drawAlignedString(440, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(520, d, str(("%.2f" % float(result['BASICVALUE']))))
    c.drawAlignedString(570, d, str(("%.2f" % float(result['RATE']))))
    prtotal(result)

def prtotal(result):
    global PrItemAmountTotal
    global PrItemQuantityTotal
    global PrGrandAmountTotal
    global PrGrandQuantityTotal
    global PrCompanyAmountTotal
    global PrCompanyQuantityTotal 
    PrItemAmountTotal = PrItemAmountTotal + (float("%.2f" % float(result['RATE'])))
    PrItemQuantityTotal = PrItemQuantityTotal + (float("%.2f" % float(result['RATE'])))
    PrGrandAmountTotal = PrGrandAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    PrGrandQuantityTotal = PrGrandQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    PrCompanyAmountTotal = PrCompanyAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    PrCompanyQuantityTotal = PrCompanyQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))

def prlogic(result):
    global prdivisioncode
    global pritem
    global prunit
    prdivisioncode.append(result['DIVCODE'])
    pritem.append(result['ITEMGROUP'])
    prunit.append(result['SUPPLIER'])

def prdlocvalue(d):
    d = d - 20
    return d

def prnewpage():
    global d
    d = 730
    return d

def prnewrequest():
    global prdivisioncode
    global prunit
    global pageno
    global pritem
    global PrItemQuantityTotal
    global PrItemAmountTotal
    global PrGrandAmountTotal
    global PrGrandQuantityTotal
    prdivisioncode = []
    pageno = 0
    pritem=[]
    prunit=[]
    PrItemQuantityTotal=0
    PrItemAmountTotal=0
    PrGrandQuantityTotal=0
    PrGrandAmountTotal=0

def prtextsize(c, result, d, stdt, etdt):
    global PrItemQuantityTotal
    global PrItemAmountTotal
    global PrGrandAmountTotal
    global PrGrandQuantityTotal
    global PrCompanyQuantityTotal
    global PrCompanyAmountTotal
    global prcounter
    prcounter=prcounter+1
    d = prdvalue(stdt,etdt,prdivisioncode)
    prlogic(result)
    if len(prdivisioncode) == 1:
        if len(prunit)==1:
            if len(pritem) == 1:
                prheader(stdt, etdt, prdivisioncode)
                boldfonts(9)
                c.drawString(10,d,result['SUPPLIER'])
                fonts(7)
                d = prdvalue(stdt,etdt,prdivisioncode)
                prdata(result, d)

    elif prdivisioncode[-1] == prdivisioncode[-2]:
        if prunit[-1] == prunit[-2]:
            prdata(result, d)
        elif prunit[-1] != prunit[-2]:
            boldfonts(9)
            d = prdvalue(stdt,etdt,prdivisioncode)
            c.drawString(10,d,result['SUPPLIER'])
            fonts(7)
            d = prdvalue(stdt,etdt,prdivisioncode)
            prdata(result, d)

    elif prdivisioncode[-1] != prdivisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Company Total : ")
        c.drawAlignedString(440, d, str("%.2f" % float(PrCompanyQuantityTotal)))
        c.drawAlignedString(520, d, str("%.2f" % float(PrCompanyAmountTotal)))
        c.drawAlignedString(570, d, str("%.2f" % float(PrItemAmountTotal/(prcounter-1))))
        print(result['ITEMGROUP'],result['RATE'],PrItemAmountTotal,prcounter,PrItemAmountTotal/(prcounter-1))
        PrCompanyQuantityTotal=0
        PrCompanyAmountTotal=0
        PrItemAmountTotal=0
        prcounter=1
        c.showPage()
        prheader(stdt, etdt, prdivisioncode)
        d = newpage()
        boldfonts(9)
        c.drawString(10,d,result['SUPPLIER'])
        d = prdvalue(stdt,etdt,prdivisioncode)
        fonts(7)
        prdata(result, d)

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def supdvalue(stdt, etdt, supdivisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = supnewpage()
        c.showPage()
        supheader(stdt, etdt, supdivisioncode)
        return d

def supheader(stdt, etdt, supdivisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, supdivisioncode[-1])
    boldfonts(9)
    c.drawCentredString(300, 780, "supoductiom Item Group Wise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    
    # Upperline in header
    c.drawString(10, 755, "ItemGroup / Item / Supplier")
    c.drawString(420, 755, "Quantity")
    c.drawString(500, 755, "Amount")
    c.drawString(550, 755, "Avg. Rate")
    fonts(7)

def supdata(result, d):
    fonts(7)
    c.drawString(60, d, str(result['SUPPLIER']))
    c.drawAlignedString(440, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(520, d, str(("%.2f" % float(result['BASICVALUE']))))
    c.drawAlignedString(570, d, str(("%.2f" % float(result['RATE']))))
    suptotal(result)

def suptotal(result):
    global supItemAmountTotal
    global supItemQuantityTotal
    global supItemRateTotal
    global supGrandAmountTotal
    global supGrandQuantityTotal
    global supGrandRateTotal
    global supCompanyAmountTotal
    global supCompanyQuantityTotal 
    global supCompanyRateTotal
    supItemAmountTotal = supItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    supItemQuantityTotal = supItemQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    supItemRateTotal = supItemRateTotal + (float("%.2f" % float(result['RATE'])))
    supGrandAmountTotal = supGrandAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    supGrandQuantityTotal = supGrandQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    supCompanyAmountTotal = supCompanyAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
    supCompanyQuantityTotal = supCompanyQuantityTotal + (float("%.2f" % float(result['QUANTITY'])))
    supCompanyRateTotal = supCompanyRateTotal + (float("%.2f" % float(result['RATE'])))
    supGrandRateTotal = supGrandRateTotal + (float("%.2f" % float(result['RATE'])))

def suplogic(result):
    global supdivisioncode
    global supitem
    global supunit
    supdivisioncode.append(result['DIVCODE'])
    supitem.append(result['ITEM'])
    supunit.append(result['ITEMGROUP'])

def supdlocvalue(d):
    d = d - 20
    return d

def supnewpage():
    global d
    d = 730
    return d

def supnewrequest():
    global supdivisioncode
    global supunit
    global pageno
    global supitem
    global supcounter1
    global supcounter
    global supItemQuantityTotal
    global supItemAmountTotal
    global supGrandAmountTotal
    global supGrandQuantityTotal
    global supItemRateTotal
    global supCompanyRateTotal
    global supCompanyAmountTotal
    global supCompanyQuantityTotal
    global supGrandRateTotal
    supdivisioncode = []
    pageno = 0
    supitem=[]
    supunit=[]
    supItemQuantityTotal=0
    supItemAmountTotal=0
    supItemRateTotal=0
    supGrandQuantityTotal=0
    supGrandAmountTotal=0
    supGrandRateTotal=0
    supCompanyRateTotal=0
    supCompanyAmountTotal=0
    supCompanyQuantityTotal=0
    supcounter=0
    supcounter1=0

def suptextsize(c, result, d, stdt, etdt):
    global supItemQuantityTotal
    global supItemAmountTotal
    global supGrandAmountTotal
    global supGrandQuantityTotal
    global supCompanyQuantityTotal
    global supCompanyAmountTotal
    global supItemRateTotal
    global supCompanyRateTotal
    global supcounter
    global supcounter1
    supcounter1=supcounter1+1
    supcounter=supcounter+1
    d = supdvalue(stdt,etdt,supdivisioncode)
    suplogic(result)
    if len(supdivisioncode) == 1:
        if len(supunit)==1:
            if len(supitem) == 1:
                supheader(stdt, etdt, supdivisioncode)
                boldfonts(9)
                c.drawString(10,d,result['ITEMGROUP'])
                d = supdvalue(stdt,etdt,supdivisioncode)
                c.drawString(40,d,result['ITEM'])
                fonts(7)
                d = supdvalue(stdt,etdt,supdivisioncode)
                supdata(result, d)

    elif supdivisioncode[-1] == supdivisioncode[-2]:
        if supunit[-1] == supunit[-2]:
            if supitem[-1] == supitem[-2]:
                supdata(result, d)
            elif supitem[-1] != supitem[-2]:
                boldfonts(9)
                c.drawString(40,d,result['ITEM'])
                fonts(7)
                d = supdvalue(stdt,etdt,supdivisioncode)
                supdata(result, d)
        elif supunit[-1] != supunit[-2]:
            boldfonts(9)
            c.drawString(200, d, "Item Group Total : ")
            c.drawAlignedString(440, d, str("%.2f" % float(supItemQuantityTotal)))
            c.drawAlignedString(520, d, str("%.2f" % float(supItemAmountTotal)))
            c.drawAlignedString(570, d, str("%.2f" % float(supItemRateTotal/(supcounter-1))))
            supItemRateTotal=0
            supItemQuantityTotal=0
            supItemAmountTotal=0
            supcounter=1
            d = supdvalue(stdt,etdt,supdivisioncode)
            d = supdvalue(stdt,etdt,supdivisioncode)
            c.drawString(10,d,result['ITEMGROUP'])
            d = supdvalue(stdt,etdt,supdivisioncode)
            c.drawString(40,d,result['ITEM'])
            fonts(7)
            d = supdvalue(stdt,etdt,supdivisioncode)
            supdata(result, d)

    elif supdivisioncode[-1] != supdivisioncode[-2]:
        boldfonts(9)
        c.drawString(200, d, "Item Group Total : ")
        c.drawAlignedString(440, d, str("%.2f" % float(supItemQuantityTotal)))
        c.drawAlignedString(520, d, str("%.2f" % float(supItemAmountTotal)))
        c.drawAlignedString(570, d, str("%.2f" % float(supItemRateTotal/(supcounter-1))))
        supItemRateTotal=0
        supItemQuantityTotal=0
        supItemAmountTotal=0
        supcounter=1
        d = supdvalue(stdt,etdt,supdivisioncode)
        c.drawString(200, d, "Company Total : ")
        c.drawAlignedString(440, d, str("%.2f" % float(supCompanyQuantityTotal)))
        c.drawAlignedString(520, d, str("%.2f" % float(supCompanyAmountTotal)))
        c.drawAlignedString(570, d, str("%.2f" % float(supCompanyRateTotal/(supcounter1-1))))
        supCompanyQuantityTotal=0
        supCompanyAmountTotal=0
        supCompanyRateTotal=0
        supcounter1=1
        c.showPage()
        supheader(stdt, etdt, supdivisioncode)
        d = newpage()
        boldfonts(9)
        c.drawString(10,d,result['SUPPLIER'])
        d = supdvalue(stdt,etdt,supdivisioncode)
        fonts(7)
        supdata(result, d)        