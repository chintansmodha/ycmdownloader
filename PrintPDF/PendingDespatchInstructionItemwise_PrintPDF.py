from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 735

divisioncode = []
Itemname = []
pageno = 0
DocumentType = []
OrdNo = []
CustomerName = []
Broker  = []
Item = []
Remark = ''
Item_Total =0
Grand_Total =0
ItemBAL_Total = 0
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

def dsize():
    global d
    d = d - 3
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
    c.drawString(10, 765, "Order No")
    c.drawString(10, 755, "Order Dt")
    c.drawString(60, 765, "Customer")
    c.drawString(60, 755, "Despatch To")
    c.drawString(190, 765, " Broker ")
    c.drawString(190, 755, "Shade")
    c.drawString(360, 755, "Lot No")
    c.drawString(440, 765, "Ord Qty")
    c.drawString(440, 755, "Rate")
    # c.drawString(500, 765, "Chal No")
    # c.drawString(500, 755, "Chal Dt")
    c.drawString(550, 765, "Bal Qty")
    # c.drawString(555, 755, "Status")

def data(result, d):
    fonts(7)
    c.drawString(190, d, result['BROKER'])
    c.drawString(190, d-8, result['SHADENAME'])
    c.drawAlignedString(465, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
    c.drawAlignedString(455, d - 8, str(format_currency(float(result['RATE']), '', locale='en_IN')))
    c.drawAlignedString(580, d, str(format_number(float(result['PENDINGQTY']), locale='en_IN')))


def logic(result):
    global divisioncode
    global Itemname
    global Broker
    global OrdNo
    global CustomerName
    global Item
    # global DocumentType
    divisioncode.append(result['BUSINESSUNITNAME'])
    Itemname.append(result['ITEMTYPE'])
    Broker.append(result['BROKER'])
    OrdNo.append(result['ORDNO'])
    CustomerName.append(result['CUSTOMERNAME'])
    Item.append(result['PRODUCTNAME'])
    # DocumentType.append(result['DOCUMENTTYPE'])

def newpage():
    global d
    d = 735
    return d

def newrequest():
    global divisioncode
    global pageno
    global Itemname
    global DocumentType
    global Broker
    global OrdNo
    global CustomerName
    global Item
    divisioncode = []
    pageno = 0
    Itemname=[]
    DocumentType = []
    Broker = []
    OrdNo = []
    CustomerName = []
    Item = []

def Remarks(result):
    global Remark
    Remark = Remark + result['REMARK']

def RemarksClean():
    global Remark
    Remark = ''

def ItemTotal(result):
    global Item_Total
    global Grand_Total
    global ItemBAL_Total
    global GrandBal_Total
    Item_Total = Item_Total + float(result['ORDERQTY'])
    ItemBAL_Total = ItemBAL_Total + float(result['PENDINGQTY'])
    Grand_Total = Grand_Total + float(result['ORDERQTY'])
    GrandBal_Total = GrandBal_Total + float(result['PENDINGQTY'])

def ItemTotalClean():
    global Item_Total
    global ItemBAL_Total
    Item_Total =0
    ItemBAL_Total = 0

def GrandTotalClean():
    global Grand_Total
    global GrandBal_Total
    Grand_Total =0
    GrandBal_Total =0

def textsize(c, result, d, stdt, etdt,LCRemarks):
    d = dvalue()
    logic(result)
    global Item_Total
    global Grand_Total
    global ItemBAL_Total
    global GrandBal_Total

    if len(divisioncode) == 1:
        if len(Item) == 1:
            header(stdt, etdt, divisioncode)
            fonts(9)
            ItemTotalClean()
            GrandTotalClean()
            RemarksClean()
            c.drawString(10, 735, Item[-1])
            fonts(7)
            if len(OrdNo) ==1 :
                c.drawString(10, d, result['ORDNO'])
                c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
                c.drawString(60, d, result['CUSTOMERNAME'])
                c.drawString(60, d - 8, result['DESPTO'])
                data(result,d)
                ItemTotal(result)
                Remarks(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if Item[-1] == Item[-2]:
            if OrdNo[-1] == OrdNo[-2]:
                if CustomerName[-1] == CustomerName[-2]:
                    data(result, d)
                    ItemTotal(result)
                    Remarks(result)
                else:
                    if LCRemarks == ['1']:
                        fonts(8)
                        if Remark == '':
                            c.drawString(19, d, "Remarks :")
                        else:
                            c.drawString(19, d, Remark)
                        d = dvalue()
                        d = dvalue()
                        RemarksClean()

                    c.drawString(10, d, result['ORDNO'])
                    c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
                    c.drawString(60, d, result['CUSTOMERNAME'])
                    c.drawString(60, d - 8, result['DESPTO'])
                    data(result, d)
                    ItemTotal(result)
                    Remarks(result)

            elif OrdNo[-1] != OrdNo[-2]:
                if LCRemarks == ['1']:
                    fonts(8)
                    if Remark == '':
                        c.drawString(19, d, "Remarks :")
                    else:
                        c.drawString(19, d, Remark)
                    d = dvalue()
                    d = dvalue()
                    RemarksClean()

                fonts(7)
                c.drawString(10, d, result['ORDNO'])
                c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
                c.drawString(60, d, result['CUSTOMERNAME'])
                c.drawString(60, d - 8, result['DESPTO'])
                data(result, d)
                ItemTotal(result)
                Remarks(result)

        elif Item[-1] != Item[-2]:
            if LCRemarks == ['1']:
                fonts(8)
                if Remark == '':
                    c.drawString(19, d, "Remarks :")
                else:
                    c.drawString(19, d, Remark)
                d = dvalue()
                d = dvalue()

            fonts(8)
            c.drawAlignedString(400, d, "Item Total: ")
            c.drawAlignedString(465, d, str(format_number(float(Item_Total), locale='en_IN')))
            c.drawAlignedString(580, d, str(format_number(float(ItemBAL_Total), locale='en_IN')))
            ItemTotalClean()
            RemarksClean()
            d = dvalue()
            fonts(9)
            c.drawString(10, d, Item[-1])
            fonts(7)
            d = dvalue()
            c.drawString(10, d, result['ORDNO'])
            c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
            c.drawString(60, d, result['CUSTOMERNAME'])
            c.drawString(60, d - 8, result['DESPTO'])
            data(result, d)
            Remarks(result)
            ItemTotal(result)

    elif divisioncode[-1] != divisioncode[-2]:
        if LCRemarks == ['1']:
            fonts(8)
            if Remark == '':
                c.drawString(19, d, "Remarks :")
            else:
                c.drawString(19, d, Remark)
            d = dvalue()

        fonts(8)
        c.drawAlignedString(400, d, "Item Total: ")
        c.drawAlignedString(465, d, str(format_number(float(Item_Total), locale='en_IN')))
        c.drawAlignedString(580, d, str(format_number(float(ItemBAL_Total), locale='en_IN')))
        d = dvalue()
        c.drawAlignedString(400, d, "Grand Total: ")
        c.drawAlignedString(465, d, str(format_number(float(Grand_Total), locale='en_IN')))
        c.drawAlignedString(580, d, str(format_number(float(GrandBal_Total), locale='en_IN')))
        GrandTotalClean()
        d = dsize()
        c.showPage()
        d = newpage()
        ItemTotalClean()
        RemarksClean()
        header(stdt, etdt, divisioncode)
        fonts(9)
        c.drawString(10, d, Item[-1])
        fonts(7)
        d = dvalue()
        c.drawString(10, d, result['ORDNO'])
        c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
        c.drawString(60, d, result['CUSTOMERNAME'])
        c.drawString(60, d - 8, result['DESPTO'])
        data(result, d)
        Remarks(result)
        ItemTotal(result)


