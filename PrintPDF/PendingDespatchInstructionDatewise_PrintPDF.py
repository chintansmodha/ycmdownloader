from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 745

divisioncode = []
Itemname = []
pageno = 0
DocumentType = []
OrdNo = []
CustomerName = []
Broker  = []
Remark = ''
Broker_Total =0
Grand_Total =0
BrokerBAL_Total = 0
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
    c.drawString(10, 765, "Order No")
    c.drawString(10, 755, "Order Dt")
    c.drawString(60, 765, "Customer")
    c.drawString(60, 755, "Despatch To")
    c.drawString(190, 765, " Item")
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
    c.drawString(190, d, result['PRODUCTNAME'])
    c.drawString(190, d-8, result['SHADENAME'])
    c.drawAlignedString(465, d, str(format_number(float(result['ORDERQTY']), locale='en_IN')))
    c.drawAlignedString(455, d - 8, str(format_currency(float(result['RATE']), '', locale='en_IN')))
    c.drawAlignedString(580, d, str(format_number(float(result['PENDINGQTY']), locale='en_IN')))

def logic(result):
    global divisioncode
    global Broker
    global OrdNo
    global CustomerName
    # global DocumentType
    divisioncode.append(result['BUSINESSUNITNAME'])
    Broker.append(result['BROKER'])
    OrdNo.append(result['ORDNO'])
    CustomerName.append(result['CUSTOMERNAME'])
    # DocumentType.append(result['DOCUMENTTYPE'])

def newpage():
    global d
    d = 745
    return d

def newrequest():
    global divisioncode
    global pageno
    global DocumentType
    global Broker
    global OrdNo
    global CustomerName
    divisioncode = []
    pageno = 0
    DocumentType = []
    Broker = []
    OrdNo = []
    CustomerName = []

def BrokerTotal(result):
    global Broker_Total
    global Grand_Total
    global BrokerBAL_Total
    global GrandBal_Total
    global Remark
    Broker_Total = Broker_Total + float(result['ORDERQTY'])
    BrokerBAL_Total = BrokerBAL_Total + float(result['PENDINGQTY'])
    Grand_Total = Grand_Total + float(result['ORDERQTY'])
    GrandBal_Total = GrandBal_Total + float(result['PENDINGQTY'])
    Remark = Remark + result['REMARK']

def BrokerTotalClean():
    global Broker_Total
    global BrokerBAL_Total
    global Remark
    Broker_Total =0
    BrokerBAL_Total = 0
    Remark = ''

def GrandTotalClean():
    global Grand_Total
    global GrandBal_Total
    Grand_Total =0
    GrandBal_Total =0

def textsize(c, result, d, stdt, etdt,LCRemarks):
    d = dvalue()
    logic(result)
    global Broker_Total
    global Grand_Total
    global BrokerBAL_Total
    global GrandBal_Total

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        fonts(9)
        BrokerTotalClean()
        GrandTotalClean()
        fonts(7)
        if len(OrdNo) ==1 :
            c.drawString(10, d, result['ORDNO'])
            c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
            c.drawString(60, d, result['CUSTOMERNAME'])
            c.drawString(60, d-8, result['DESPTO'])
            data(result,d)
            BrokerTotal(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if OrdNo[-1] == OrdNo[-2]:
            if CustomerName[-1] == CustomerName[-2]:
                data(result, d)
                BrokerTotal(result)
            else:
                if LCRemarks == ['1']:
                    fonts(8)
                    if Remark == '':
                        c.drawString(19, d, "Remarks :")
                    else:
                        c.drawString(19, d, Remark)
                    c.drawAlignedString(465, d, str(format_number(float(Broker_Total), locale='en_IN')))
                    c.drawAlignedString(580, d, str(format_number(float(BrokerBAL_Total), locale='en_IN')))
                    BrokerTotalClean()
                    d = dvalue()
                    d = dvalue()
                c.drawString(10, d, result['ORDNO'])
                c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
                c.drawString(60, d, result['CUSTOMERNAME'])
                c.drawString(60, d - 8, result['DESPTO'])
                data(result, d)
                BrokerTotal(result)
        elif OrdNo[-1] != OrdNo[-2]:
            if LCRemarks == ['1']:
                fonts(8)
                if Remark == '':
                    c.drawString(19, d, "Remarks :")
                else:
                    c.drawString(19, d, Remark)
                c.drawAlignedString(465, d, str(format_number(float(Broker_Total), locale='en_IN')))
                c.drawAlignedString(580, d, str(format_number(float(BrokerBAL_Total), locale='en_IN')))
                BrokerTotalClean()
                d = dvalue()
                d = dvalue()
            fonts(7)
            c.drawString(10, d, result['ORDNO'])
            c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
            c.drawString(60, d, result['CUSTOMERNAME'])
            c.drawString(60, d - 8, result['DESPTO'])
            data(result, d)
            BrokerTotal(result)

    elif divisioncode[-1] != divisioncode[-2]:
        if LCRemarks == ['1']:
            fonts(8)
            if Remark == '':
                c.drawString(19, d, "Remarks :")
            else:
                c.drawString(19, d, Remark)
            c.drawAlignedString(465, d, str(format_number(float(Broker_Total), locale='en_IN')))
            c.drawAlignedString(580, d, str(format_number(float(BrokerBAL_Total), locale='en_IN')))
            BrokerTotalClean()
            d = dvalue()
        fonts(8)
        d = dvalue()
        c.drawString(250, d, "Grand Total: ")
        c.drawAlignedString(465, d, str(format_number(float(Grand_Total), locale='en_IN')))
        c.drawAlignedString(580, d, str(format_number(float(GrandBal_Total), locale='en_IN')))
        GrandTotalClean()
        BrokerTotalClean()
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode)
        fonts(7)
        d =dvalue()
        c.drawString(10, d, result['ORDNO'])
        c.drawString(10, d - 8, result['ORDDATE'].strftime('%d-%m-%Y'))
        c.drawString(60, d, result['CUSTOMERNAME'])
        c.drawString(60, d - 8, result['DESPTO'])
        data(result, d)
        BrokerTotal(result)


