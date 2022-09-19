from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 735

divisioncode = []
Itemname = []
OrdNo = []
CustomerName = []
pageno = 0
date=[]
DocumentType = []
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
    c.drawCentredString(300, 780, "Order Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header
    c.drawString(10, 765, "Order No")
    c.drawString(10, 755, "Order Dt")
    c.drawString(60, 765, "Customer")
    c.drawString(60, 755, "Broker")
    c.drawString(190, 765, " Item")
    c.drawString(190, 755, "Shade")
    c.drawString(360, 755, "Lot No")
    c.drawString(440, 765, "Ord Qty")
    c.drawString(440, 755, "Rate")
    c.drawString(500, 765, "Chal No")
    c.drawString(500, 755, "Chal Dt")
    c.drawString(555, 765, "Desp Qty")
    c.drawString(555, 755, "Status")

def data(result, d):
    fonts(7)
    OrdNo.append(result['ORDNO'])
    CustomerName.append(result['CUSTOMERNAME'])
    if len(OrdNo) == 1:
        c.drawString(10, d, result['ORDNO'])
        c.drawString(10, d-8, result['ORDDATE'].strftime('%d-%m-%Y'))
        c.drawString(60, d, result['CUSTOMERNAME'])
        c.drawString(60, d - 8, result['BROKER'])
        c.drawString(190, d, result['PRODUCTNAME'])
        c.drawString(190, d-8, result['SHADENAME'])
        c.drawAlignedString(465, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
        c.drawAlignedString(455, d - 8, str(format_currency(float(result['RATE']), '', locale='en_IN')))
        c.drawAlignedString(585, d, str(format_decimal(float(result['DESPQTY']), locale='en_IN')))
        c.drawString(560, d-8, result['PROGRESSSTATUS'])

    elif OrdNo[-1] == OrdNo[-2]:
        if CustomerName[-1] == CustomerName[-2]:
            c.drawString(190, d, result['PRODUCTNAME'])
            c.drawString(190, d-8, result['SHADENAME'])
            c.drawAlignedString(465, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
            c.drawAlignedString(455, d - 8, str(format_currency(float(result['RATE']), '', locale='en_IN')))
            c.drawAlignedString(585, d, str(format_decimal(float(result['DESPQTY']), locale='en_IN')))
            c.drawString(560, d - 8, result['PROGRESSSTATUS'])
        elif CustomerName[-1] != CustomerName[-2]:
            c.drawString(10, d, result['ORDNO'])
            c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
            c.drawString(60, d, result['CUSTOMERNAME'])
            c.drawString(60, d - 8, result['BROKER'])
            c.drawString(190, d, result['PRODUCTNAME'])
            c.drawString(190, d-8, result['SHADENAME'])
            c.drawAlignedString(465, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
            c.drawAlignedString(455, d - 8, str(format_currency(float(result['RATE']), '', locale='en_IN')))
            c.drawAlignedString(585, d, str(format_decimal(float(result['DESPQTY']), locale='en_IN')))
            c.drawString(560, d - 8, result['PROGRESSSTATUS'])
    elif OrdNo[-1] != OrdNo[-2]:
        c.drawString(10, d, result['ORDNO'])
        c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
        c.drawString(60, d, result['CUSTOMERNAME'])
        c.drawString(60, d - 8, result['BROKER'])
        c.drawString(190, d, result['PRODUCTNAME'])
        c.drawString(190, d-8, result['SHADENAME'])
        c.drawAlignedString(465, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
        c.drawAlignedString(455, d - 8, str(format_currency(float(result['RATE']), '', locale='en_IN')))
        c.drawAlignedString(585, d, str(format_decimal(float(result['DESPQTY']), locale='en_IN')))
        c.drawString(560, d - 8, result['PROGRESSSTATUS'])


def logic(result):
    global divisioncode
    global Itemname
    global DocumentType
    divisioncode.append(result['BUSINESSUNITNAME'])
    Itemname.append(result['ITEMTYPE'])
    DocumentType.append(result['DOCUMENTTYPE'])
def newpage():
    global d
    d = 735
    return d

def newrequest():
    global divisioncode
    global pageno
    global Itemname
    global DocumentType
    global OrdNo
    global CustomerName
    divisioncode = []
    pageno = 0
    Itemname=[]
    DocumentType = []
    OrdNo = []
    CustomerName = []


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if len(DocumentType) == 1:
        if len(divisioncode) == 1:
            if len(Itemname) ==1:
                header(stdt, etdt, divisioncode)
                fonts(9)
                c.drawString(10,735,Itemname[-1])
                c.drawString(80,780,DocumentType[-1])
                fonts(7)
                # d = dvalue()
                data(result,d)
    elif DocumentType[-1] == DocumentType[-2]:
        if divisioncode[-1] == divisioncode[-2]:
            if Itemname[-1] == Itemname[-2]:
                if d>=20:
                    d = dsize()
                data(result,d)

            elif Itemname[-1]!=Itemname[-2]:
                c.showPage()
                d = newpage()
                header(stdt, etdt, divisioncode)
                fonts(9)
                c.drawString(10,d,Itemname[-1])
                c.drawString(80, 780, DocumentType[-1])
                fonts(7)
                d = dvalue()
                data(result,d)

        elif divisioncode[-1] != divisioncode[-2]:
            c.showPage()
            d = newpage()
            header(stdt, etdt, divisioncode)
            fonts(9)
            c.drawString(10, d, Itemname[-1])
            c.drawString(80,780,DocumentType[-1])
            d = dvalue()
            fonts(7)
            data(result, d)

    elif DocumentType[-1] != DocumentType[-2]:
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode)
        fonts(9)
        c.drawString(10, d, Itemname[-1])
        c.drawString(80,780,DocumentType[-1])
        d = dvalue()
        fonts(7)
        data(result, d)
