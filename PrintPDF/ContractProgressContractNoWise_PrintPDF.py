import textwrap
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 490
i = 1
y = 0
s = 1
k = 0
pageno = 0

divisioncode = []
Party = []
Broker  = []
Item = []
ItemTyp = []
ContNo = []
Shade = []
OrdNo = []
OrdQty = []

ConOrdQty = 0
ConChalQty = 0

BroOrdQty = 0
BroChalQty = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def dvalueset():
    global d
    d = 490
    return d

def SetDvalue():
    global d
    d = 0
    return d

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

def header(stdt,etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(400, 550, divisioncode[-1])
    fonts(9)
    c.drawString(10, 550, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(400, 530, "Contract Progress Report (Contract No. Wise) From  " + str(stdt.strftime(' %d  %B  %Y')) +
                        "  To  " + str(etdt.strftime(' %d  %B  %Y')))
    p = page()
    c.drawString(740, 530, "Page No." + str(p))
    c.line(0, 525, 900, 525)
    c.line(0, 495, 900, 495)
    fonts(9)
    # Upperline in header
    c.drawString(10, 515, "Cont No.")
    c.drawString(80, 515, "Item")
    c.drawString(315, 515, "CntQty")
    c.drawString(395, 515, "CntRate")
    c.drawString(430, 515, "Order No.")
    c.drawString(520, 515, "Lot No.")
    c.drawString(580, 515, "Order")
    c.drawString(675, 515, "OrdQty")
    c.drawString(710, 515, "Chal No.")
    c.drawString(785, 515, "ChalLot")
    # Lowerline
    c.drawString(10, 500, "Cont Dt.")
    c.drawString(80, 500, "Broker")
    c.drawString(315, 500, "PndQty")
    c.drawString(395, 500, "CntSta")
    c.drawString(430, 500, "Order Dt.")
    c.drawString(520, 500, "Shade")
    c.drawString(580, 505, "Status")
    c.drawString(675, 500, "PndQty")
    c.drawString(710, 500, "Chal Dt.")
    c.drawString(785, 500, "ChalQty")


def data(result, d):
    fonts(7)
    if result['CHALNO'] != None:
        c.drawString(711, d, str(result['CHALNO']))
    if result['CHALLOT'] != None:
        c.drawString(786, d, str(result['CHALLOT']))
    d = dvalue()
    d = dvalue()
    if result['CHALNO'] != None:
        c.drawString(711, d, str(result['CHALDT'].strftime('%d-%m-%Y')))
    if result['CHALQTY'] != None:
        c.drawAlignedString(800, d, str(result['CHALQTY']))
    ContractChalTotal(result)
    BrokerGroupChalTotal(result)

def PrintCont(result, d):
    fonts(7)
    if result['CONTNO'] != None:
        # c.drawString(10, d, ContNo[-1])
        c.drawAlignedString(330, d, str(result['CONTQTY']))
        c.drawAlignedString(410, d, str(result['CONTRACTRATE']))
    d = dvalue()
    d = dvalue()
    # if result['CONTDT'] != None:
    #     c.drawString(10, d, str(result['CONTDT'].strftime('%d-%m-%Y')))
    if result['CONTNO'] != None:
        c.drawAlignedString(330, d, str(result['CONTPENDQTY']))
        c.drawString(396, d, str(result['CONTSTATUS']))
    c.drawString(521, d, Shade[-1])
    d = dvalueincrese()

def PrintOrd(result, d):
    fonts(7)
    if result['ORDNO'] != None:
        c.drawString(435, d, OrdNo[-1])
        c.drawAlignedString(690, d, OrdQty[-1])
        # c.drawString(341, d, str(result['LOTNO']))
        c.drawString(581, d, str(result['ORDSTATUS']))
        d = dvalue()
        d = dvalue()
        c.drawString(435, d, str(result['ORDDT'].strftime('%d-%m-%Y')))
        c.drawAlignedString(690, d, str(result['ORDPNDQTY']))
        d = dvalueincrese()
        ContractOrdTotal(result)
        BrokerGroupOrdTotal(result)

def logic(result):
    global divisioncode, Party, Broker, Item, ItemTyp
    global ContNo, Shade, OrdNo, OrdQty
    divisioncode.append(result['COMPANY'])
    # Party.append(str(result['PARTY']))
    Broker.append(str(result['BROKER']))
    Item.append(str(result['ITEM']))
    ItemTyp.append(str(result['ITEMTYP']))
    ContNo.append(str(result['CONTNO']))
    Shade.append(str(result['SHADE']))
    OrdNo.append(str(result['ORDNO']))
    OrdQty.append(str(result['ORDQTY']))

def newpage():
    global d
    d = 490
    return d

def newrequest():
    global divisioncode, Party, Broker, Item, ItemTyp
    global ContNo, Shade, y, OrdNo, OrdQty
    global pageno
    divisioncode = []
    Party = []
    Broker = []
    Item = []
    ItemTyp = []
    ContNo = []
    Shade = []
    y = 0
    OrdNo = []
    OrdQty = []
    pageno = 0

def ItemNamePrint(d):
    global y,s
    str1 = ''
    string = str1.join(Item[-1])
    wrap_text = textwrap.wrap(string, width=50)
    s = 1
    e = 0
    while e < len(wrap_text):
        c.drawString(81, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
        s = s + 1
    y = d
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1

def ContractOrdTotal(result):
    global ConOrdQty
    if result['ORDQTY'] != None:
        ConOrdQty = ConOrdQty + float(result['ORDQTY'])
def ContractChalTotal(result):
    global ConChalQty
    if result['CHALQTY'] != None:
        ConChalQty = ConChalQty + float(result['CHALQTY'])

def ContractClean():
    global ConOrdQty, ConChalQty
    ConOrdQty = 0
    ConChalQty = 0

def BrokerGroupOrdTotal(result):
    global BroOrdQty
    if result['ORDQTY'] != None:
        BroOrdQty = BroOrdQty + float(result['ORDQTY'])
def BrokerGroupChalTotal(result):
    global BroChalQty
    if result['CHALQTY'] != None:
        BroChalQty = BroChalQty + float(result['CHALQTY'])

def BrokerGroupClean():
    global BroOrdQty, BroChalQty
    BroOrdQty = 0
    BroChalQty = 0

def ContractTotalPrint(d):
    boldfonts(7)
    c.drawString(520, d, "Contract Total: ")
    c.drawAlignedString(690, d, str('{0:1.3f}'.format(ConOrdQty)))
    c.drawAlignedString(800, d, str('{0:1.3f}'.format(ConChalQty)))
    fonts(7)

def BrokerGroupTotalPrint(d):
    boldfonts(7)
    c.drawString(520, d, "Broker Total: ")
    c.drawAlignedString(690, d, str('{0:1.3f}'.format(BroOrdQty)))
    c.drawAlignedString(800, d, str('{0:1.3f}'.format(BroChalQty)))
    fonts(7)

def textsize(c, result, d, stdt,etdt):
    d = dvalue()
    logic(result)
    global y, s, k
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt,etdt, divisioncode)
        fonts(7)
        if result['CONTNO'] != None:
            c.drawString(10, d, ContNo[-1])
            d = dvalue()
            d = dvalue()
        if result['CONTDT'] != None:
            c.drawString(10, d, str(result['CONTDT'].strftime('%d-%m-%Y')))
            d = dvalueincrese()
        # c.drawString(10, d, ContNo[-1])
        ItemNamePrint(d)
        c.drawString(81, y, Broker[-1])
        PrintCont(result,d)
        PrintOrd(result,d)
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if ContNo[-1] == ContNo[-2]:
            if Broker[-1] == Broker[-2]:
                if ItemTyp[-1] == ItemTyp[-2]:
                    if Item[-1] == Item[-2]:
                            if Shade[-1] == Shade[-2]:
                                if OrdNo[-1] == OrdNo[-2]:
                                    if OrdQty[-1] == OrdQty[-2]:
                                        data(result,d)
                                        k = 0
                                    elif OrdQty[-1] != OrdQty[-2]:
                                        PrintOrd(result, d)
                                        data(result, d)
                                        k = 0
                                elif OrdNo[-1] != OrdNo[-2]:
                                    PrintOrd(result, d)
                                    data(result, d)
                                    k = 0
                            elif Shade[-1] != Shade[-2]:
                                PrintCont(result,d)
                                PrintOrd(result, d)
                                data(result, d)
                                k = 0

                    elif Item[-1] != Item[-2]:#if d != 735:
                        # print("Item ", k)
                        if k != 1:
                            while s != 0:
                                d = dvalue()
                                s = s - 1
                        ItemNamePrint(d)
                        PrintCont(result, d)
                        PrintOrd(result, d)
                        data(result, d)
                        k = 0

                elif ItemTyp[-1] != ItemTyp[-2]:
                    if int(ConOrdQty) != 0:
                        ContractTotalPrint(d)
                        d = dvalue()
                        d = dvalue()
                        ContractClean()
                    if k != 1:
                        while s != 0:
                            d = dvalue()
                            s = s - 1
                    # d = dvalue()
                    # d = dvalue()
                    ItemNamePrint(d)
                    c.drawString(81, y, Broker[-1])
                    PrintCont(result, d)
                    PrintOrd(result, d)
                    data(result, d)
                    k = 0

            elif Broker[-1] != Broker[-2]:
                if int(ConOrdQty) != 0:
                    ContractTotalPrint(d)
                    d = dvalue()
                    d = dvalue()
                    ContractClean()
                BrokerGroupTotalPrint(d)
                d = dvalue()
                d = dvalue()
                BrokerGroupClean()
                if k != 1:
                    while s != 0:
                        d = dvalue()
                        s = s - 1
                ItemNamePrint(d)
                c.drawString(81, y, Broker[-1])
                PrintCont(result, d)
                PrintOrd(result, d)
                data(result, d)
                k = 0

        elif ContNo[-1] != ContNo[-2]:
            if int(ConOrdQty) != 0:
                ContractTotalPrint(d)
                d = dvalue()
                d = dvalue()
                ContractClean()
            BrokerGroupClean()
            if k != 1:
                while s != 0:
                    d = dvalue()
                    s = s - 1
            fonts(7)
            if result['CONTNO'] != None:
                c.drawString(10, d, ContNo[-1])
                d = dvalue()
                d = dvalue()
            if result['CONTDT'] != None:
                c.drawString(10, d, str(result['CONTDT'].strftime('%d-%m-%Y')))
                d = dvalueincrese()
            # c.drawString(10, d, ContNo[-1])
            ItemNamePrint(d)
            c.drawString(81, y, Broker[-1])
            PrintCont(result, d)
            PrintOrd(result, d)
            data(result, d)
            k = 0

    elif divisioncode[-1] != divisioncode[-2]:
        if int(ConOrdQty) != 0:
            ContractTotalPrint(d)
            d = dvalue()
            d = dvalue()
            ContractClean()
        # BrokerGroupTotalPrint(d)
        # d = dvalue()
        # d = dvalue()
        BrokerGroupClean()
        c.setPageSize(landscape(A4))
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        fonts(7)
        if result['CONTNO'] != None:
            c.drawString(10, d, ContNo[-1])
            d = dvalue()
            d = dvalue()
        if result['CONTDT'] != None:
            c.drawString(10, d, str(result['CONTDT'].strftime('%d-%m-%Y')))
            d = dvalueincrese()
        # c.drawString(10, d, ContNo[-1])
        ItemNamePrint(d)
        c.drawString(81, y, Broker[-1])
        PrintCont(result, d)
        PrintOrd(result, d)
        data(result, d)