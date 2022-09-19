from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 750
i = 1
pageno = 0

divisioncode = []
department = []
Itemname = []
Itemtype = []
Qty = Box = Cops = 0
ItmtypQty = ItmtypBox = ItmtypCops = 0
DepQty = DepBox = DepCops = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

def dvalue():
    global d
    d = d - 5
    return d

def dvalueincrese():
    global d
    d = d + 10
    return d

def header(stdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Stock In Hand (Item-Wise(Lot-Wise) Cl. Bal.)  As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Lot No.")
    c.drawString(80, 760, "Shade")
    c.drawString(250, 760, "Sale/Sec Lot No.")
    c.drawString(450, 760, "Qty")
    c.drawString(500, 760, "Box")
    c.drawString(555, 760, "Cops")


def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['LOTNO']))
    c.drawString(81, d, str(result['SHADENAME']))
    c.drawString(253, d, str(result['SALELOT']))
    c.drawAlignedString(460, d, str(result['NETWT']))
    c.drawAlignedString(515, d, str(result['BOXES']))
    c.drawAlignedString(575, d, str(result['COPS']))
    ItemWiseTotal(result)
    ItemTypeTotal(result)
    DepartmentTotal(result)


def logic(result):
    global divisioncode
    global Itemtype
    global Itemname
    divisioncode.append(result['DEPARTMENT'])
    Itemtype.append(result['ITMTYPE'])
    Itemname.append(result['PRODUCT'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global Itemtype
    global Itemname
    global pageno
    divisioncode = []
    Itemtype = []
    Itemname = []
    pageno = 0

def ItemWiseTotal(result):
    global Qty, Box, Cops
    Qty = Qty + float(result['NETWT'])
    Box = Box + int(result['BOXES'])
    Cops = Cops + int(result['COPS'])

def ItemWiseClean():
    global Qty, Box, Cops
    Qty = Box = Cops = 0

def ItemTypeTotal(result):
    global ItmtypQty, ItmtypBox, ItmtypCops
    ItmtypQty = ItmtypQty + float(result['NETWT'])
    ItmtypBox = ItmtypBox + int(result['BOXES'])
    ItmtypCops = ItmtypCops + int(result['COPS'])

def ItemTypeClean():
    global ItmtypQty, ItmtypBox, ItmtypCops
    ItmtypQty = ItmtypBox = ItmtypCops = 0

def DepartmentTotal(result):
    global DepQty, DepBox, DepCops
    DepQty = DepQty + float(result['NETWT'])
    DepBox = DepBox + int(result['BOXES'])
    DepCops = DepCops + int(result['COPS'])

def DepartmentClean():
    global DepQty, DepBox, DepCops
    DepQty = DepBox = DepCops = 0

def ItemwisePrint(d):
    boldfonts(7)
    c.drawString(250, d, "Item Total: ")
    c.drawAlignedString(460, d, str('{0:1.3f}'.format(Qty)))
    c.drawAlignedString(515, d, str(Box))
    c.drawAlignedString(575, d, str(Cops))
    fonts(7)

def ItemTypePrint(d):
    boldfonts(7)
    c.drawString(250, d, "ItemGrp Total: ")
    c.drawAlignedString(460, d, str('{0:1.3f}'.format(ItmtypQty)))
    c.drawAlignedString(515, d, str(ItmtypBox))
    c.drawAlignedString(575, d, str(ItmtypCops))
    fonts(7)

def DepartmentPrint(d):
    boldfonts(7)
    c.drawString(250, d, "Department Total: ")
    c.drawAlignedString(460, d, str('{0:1.3f}'.format(DepQty)))
    c.drawAlignedString(515, d, str(DepBox))
    c.drawAlignedString(575, d, str(DepCops))
    fonts(7)


def textsize(c, result, d, stdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Itemtype[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Itemtype[-1] == Itemtype[-2]:
            if Itemname[-1] == Itemname[-2]:
                data(result, d)

            else:
                ItemwisePrint(d)
                ItemWiseClean()
                d = dvalue()
                d = dvalue()
                c.drawString(10, d, Itemname[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)

        else:
            ItemwisePrint(d)
            d = dvalue()
            d = dvalue()
            ItemTypePrint(d)
            ItemWiseClean()
            ItemTypeClean()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            boldfonts(7)
            c.drawCentredString(300, d, Itemtype[-1])
            d = dvalue()
            d = dvalue()
            fonts(7)
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        ItemwisePrint(d)
        d = dvalue()
        d = dvalue()
        ItemTypePrint(d)
        d = dvalue()
        d = dvalue()
        DepartmentPrint(d)
        ItemWiseClean()
        ItemTypeClean()
        DepartmentClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Itemtype[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)


