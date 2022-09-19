from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 745

divisioncode = []
pageno = 0
DocumentType = []
Item = []
Shade = []
Remark = ''
Item_Total = 0
Shade_Total = 0
ItemBalQty_Total = 0
ShadeBalQty_Total = 0
Grand_Total =0
GrandBal_Total =0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 10
    return d

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, "Pending Orders List From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header as COLUMN NAME
    c.drawString(10, 760, "Order No")
    c.drawString(60, 760, "Order Dt")
    c.drawString(110, 760, "Customer")
    c.drawString(220, 760, "Despatch To")
    c.drawString(300, 760, "Lot No")
    c.drawString(350, 760, " Broker")
    c.drawString(470, 760, "Ord Qty")
    c.drawString(515, 760, "Bal Qty")
    c.drawString(560, 760, "Rate")

def data(result, d):
    fonts(7)
    c.drawString(10, d, result['ORDNO'])
    c.drawString(60, d, result['ORDDATE'].strftime('%d-%m-%Y'))
    c.drawString(110, d, result['CUSTOMERNAME'])
    c.drawString(225, d - 8, result['DESPTO'])
    c.drawString(350, d, result['BROKER'])
    c.drawAlignedString(500, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
    c.drawAlignedString(545, d, str(format_number(float(result['PENDINGQTY']), locale='en_IN')))
    c.drawAlignedString(575, d, str(format_currency(float(result['RATE']), '', locale='en_IN')))

def logic(result):
    global divisioncode
    global Item
    global Shade
    # global DocumentType
    divisioncode.append(result['BUSINESSUNITNAME'])
    Item.append(result['PRODUCTNAME'])
    Shade.append(result['SHADENAME'])

def newpage():
    global d
    d = 745
    return d

def newrequest():
    global divisioncode
    global pageno
    global Item
    global Shade
    # global DocumentType
    divisioncode = []
    pageno = 0
    Item=[]
    Shade = []

def ItemTotal(result):
    global Item_Total
    global Shade_Total
    global ItemBalQty_Total
    global ShadeBalQty_Total
    global Grand_Total
    global GrandBal_Total
    global Remark
    Shade_Total = Shade_Total + float(result['ORDERQTY'])
    Item_Total = Item_Total + + float(result['ORDERQTY'])
    ShadeBalQty_Total = ShadeBalQty_Total + float(result['PENDINGQTY'])
    ItemBalQty_Total = ItemBalQty_Total + float(result['PENDINGQTY'])
    Grand_Total = Grand_Total + float(result['ORDERQTY'])
    GrandBal_Total = GrandBal_Total + float(result['PENDINGQTY'])
    Remark = Remark + result['REMARK']

def ShadeTotalClean():
    global Shade_Total
    global ShadeBalQty_Total
    ShadeBalQty_Total = 0
    Shade_Total = 0

def ItemTotalClean():
    global Item_Total
    global ItemBalQty_Total
    global Remark
    ItemBalQty_Total = 0
    Item_Total = 0
    Remark = ''

def GrandTotalClean():
    global Grand_Total
    global GrandBal_Total
    Grand_Total =0
    GrandBal_Total =0

def textsize(c, result, d, stdt, etdt,LCRemarks):
    d = dvalue()
    global Item_Total
    global ItemBalQty_Total
    global ShadeBalQty_Total
    global Shade_Total
    global Grand_Total
    global GrandBal_Total
    global Remark
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        ItemTotalClean()
        ShadeTotalClean()
        GrandTotalClean()
        fonts(8)
        if len(Shade)==1:
            c.drawString(10 , d, Shade[-1])
            d = dvalue()
            fonts(7)
            if len(Item)==1:
                c.drawString(60, d, Item[-1])
                d = dvalue()
                data(result, d)
                ItemTotal(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if Shade[-1] == Shade[-2]:
            fonts(8)
            if Item[-1] != Item[-2]:
                if LCRemarks == ['1']:
                    fonts(8)
                    if Remark == '':
                        c.drawString(19, d, "Remarks :")
                    else:
                        c.drawString(19, d, Remark)
                    d = dvalue()
                c.drawAlignedString(350, d, "Item Total : ")
                c.drawAlignedString(500, d, str(format_number(float(Item_Total), locale='en_IN')))
                c.drawAlignedString(540, d, str(format_number(float(ItemBalQty_Total), locale='en_IN')))
                ItemTotalClean()
                c.drawString(60, d, Item[-1])
                d = dvalue()
                data(result, d)
                ItemTotal(result)

            if Item[-1] == Item[-2]:
                fonts(7)
                data(result,d)
                ItemTotal(result)

        elif Shade[-1] != Shade[-2]:
            fonts(8)
            if LCRemarks == ['1']:
                fonts(8)
                if Remark == '':
                    c.drawString(19, d, "Remarks :")
                else:
                    c.drawString(19, d, Remark)
                d = dvalue()
            c.drawAlignedString(350, d, "Item Total : ")
            c.drawAlignedString(500, d, str(format_number(float(Item_Total), locale='en_IN')))
            c.drawAlignedString(545, d, str(format_number(float(ItemBalQty_Total), locale='en_IN')))
            d = dvalue()
            # d = dsize()
            c.drawAlignedString(350, d, "Shade Total : ")
            c.drawAlignedString(500, d, str(format_number(float(Shade_Total), locale='en_IN')))
            c.drawAlignedString(545, d, str(format_number(float(ShadeBalQty_Total), locale='en_IN')))
            # d = dvalue()
            ShadeTotalClean()
            ItemTotalClean()
            c.drawString(10, d, Shade[-1])
            d = dvalue()
            fonts(8)
            c.drawString(60, d, Item[-1])
            d = dvalue()
            data(result,d)
            ItemTotal(result)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(8)
        if LCRemarks == ['1']:
            fonts(8)
            if Remark == '':
                c.drawString(19, d, "Remarks :")
            else:
                c.drawString(19, d, Remark)
            d = dvalue()
        c.drawAlignedString(350, d, "Item Total : ")
        c.drawAlignedString(500, d, str(format_number(float(Item_Total), locale='en_IN')))
        c.drawAlignedString(545, d, str(format_number(float(ItemBalQty_Total), locale='en_IN')))
        d = dvalue()
        c.drawAlignedString(350, d, "Shade Total : ")
        c.drawAlignedString(500, d, str(format_number(float(Shade_Total), locale='en_IN')))
        c.drawAlignedString(545, d, str(format_number(float(ShadeBalQty_Total), locale='en_IN')))
        d = dvalue()
        c.drawAlignedString(350, d, "Grand Total : ")
        c.drawAlignedString(500, d, str(format_number(float(Grand_Total), locale='en_IN')))
        c.drawAlignedString(545, d, str(format_number(float(GrandBal_Total), locale='en_IN')))
        ShadeTotalClean()
        ItemTotalClean()
        GrandTotalClean()

        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        c.drawString(10, d, Shade[-1])
        d = dvalue()
        fonts(7)
        c.drawString(60, d, Item[-1])
        d = dvalue()
        data(result, d)
        ItemTotal(result)
