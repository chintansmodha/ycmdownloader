import textwrap
from reportlab.lib.pagesizes import landscape, portrait, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(portrait(A4)))
c.setPageSize(portrait(A4))
d = 740
i = 1
y = 0
s = 1
k = 0
pageno = 0

divisioncode = []
Party = []
Broker  = []
Item = []
Plant = []
BrokerGroup = []

# Total Ref
itemQnt = 0
itemAmt = 0

plantQnt = 0
plantAmt = 0

partyQnt = 0
partyAmt = 0

brokerQnt = 0
brokerAmt = 0

brokergroupQnt = 0
brokergroupAmt = 0

grandbrokergroupAmt = 0
grandbrokergroupQnt = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def dvalueset():
    global d
    d = 740
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

def dvalues(c,stdt,etdt, divisioncode):
    global d
    if d > 20:
        d = d - 5
        return d
    else:
        c.showPage()
        d = newpage()
        header(stdt,etdt, divisioncode)
        boldfonts(7)
        return d


def dvalueincrese():
    global d
    if d < 740:
        d = d + 10
    return d

def header(stdt,etdt, divisioncode):
    fonts(15)
    c.setTitle("Agent Lifting Details")
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    # c.drawString(10, 550, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Agent Wise Lifting Item Wise Details From  " + str(stdt.strftime(' %d  %b  %Y')) +
                        "  To  " + str(etdt.strftime(' %d  %b  %Y')))
    p = page()
    c.drawString(540, 775, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    fonts(9)

    # Upperline in header
    c.drawString(10, 755, "Invoice No.")
    c.drawString(75, 755, "Invoice Date")
    c.drawString(140, 755, "Party")
    c.drawString(400, 755, "Rate")
    c.drawString(470, 755, "Quantity")
    c.drawString(555, 755, "Amount")


def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['INVNO']))
    c.drawString(76, d, str(result['BILLDT'].strftime('%d-%m-%Y')))
    c.drawString(142, d, str(result['PARTY']))
    c.drawAlignedString(410, d, str(result['RATE']))
    c.drawAlignedString(485, d, str(result['QUANTITY']))
    c.drawAlignedString(565, d, str(result['AMOUNT']))
    ItemTotal(result)
    PlantTotal(result)
    BrokerTotal(result)
    BrokerGroupTotal(result)
    GrandTotal(result)

def logic(result, LSMergePlant):
    global divisioncode, Party, Broker
    global Plant, BrokerGroup, Item
    divisioncode.append(result['COMPANY'])
    Party.append(str(result['PARTY']))
    Broker.append(str(result['AGENT']))
    if int(LSMergePlant) == 0:
        Plant.append(str(result['PLANT']))
    else:
        Plant.append('')
    Item.append(str(result['ITEM']))
    BrokerGroup.append(str(result['AGENTGRP']))

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode, Party, Broker
    global Plant, BrokerGroup, Item, y, OrdNo, OrdQty
    global pageno
    global itemAmt, itemQnt
    global plantAmt, plantQnt
    global partyAmt, partyQnt
    global brokerAmt, brokerQnt
    global brokergroupAmt, brokergroupQnt, grandbrokergroupAmt, grandbrokergroupQnt
    divisioncode = []
    Party = []
    Broker  = []
    Item = []
    Plant = []
    BrokerGroup = []
    y = 0
    pageno = 0
    itemQnt = 0
    itemAmt = 0

    plantQnt = 0
    plantAmt = 0

    partyQnt = 0
    partyAmt = 0

    brokerQnt = 0
    brokerAmt = 0

    brokergroupQnt = 0
    brokergroupAmt = 0

    grandbrokergroupAmt = 0
    grandbrokergroupQnt = 0

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

def ItemTotal(result):
    global itemAmt, itemQnt
    itemAmt = itemAmt + float(result['AMOUNT'])
    itemQnt = itemQnt + float(result['QUANTITY'])

def PlantTotal(result):
    global plantAmt, plantQnt
    plantAmt = plantAmt + float(result['AMOUNT'])
    plantQnt = plantQnt + float(result['QUANTITY'])

def Partyotal(result):
    global partyAmt, partyQnt
    partyAmt = partyAmt + float(result['AMOUNT'])
    partyQnt = partyQnt + float(result['QUANTITY'])

def BrokerTotal(result):
    global brokerAmt, brokerQnt
    brokerAmt = brokerAmt + float(result['AMOUNT'])
    brokerQnt = brokerQnt + float(result['QUANTITY'])

def BrokerGroupTotal(result):
    global brokergroupAmt, brokergroupQnt
    brokergroupAmt = brokergroupAmt + float(result['AMOUNT'])
    brokergroupQnt = brokergroupQnt + float(result['QUANTITY'])

def GrandTotal(result):
    global grandbrokergroupQnt, grandbrokergroupAmt
    grandbrokergroupAmt = grandbrokergroupAmt + float(result['AMOUNT'])
    grandbrokergroupQnt = grandbrokergroupQnt + float(result['QUANTITY'])

def ItemTotalPrint():
    global itemAmt, itemQnt
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(itemAmt)))
    c.drawAlignedString(485, d, str('{0:1.3f}'.format(itemQnt)))
    itemAmt = 0
    itemQnt = 0

def PlantTotalPrint():
    global plantAmt, plantQnt
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(plantAmt)))
    c.drawAlignedString(485, d, str('{0:1.3f}'.format(plantQnt)))
    plantAmt = 0
    plantQnt = 0

def PartyTotalPrint():
    global partyAmt, partyQnt
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(partyAmt)))
    c.drawAlignedString(485, d, str('{0:1.3f}'.format(partyQnt)))
    partyAmt = 0
    partyQnt = 0

def BrokerTotalPrint():
    global brokerAmt, brokerQnt
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(brokerAmt)))
    c.drawAlignedString(485, d, str('{0:1.3f}'.format(brokerQnt)))
    brokerAmt = 0
    brokerQnt = 0

def BrokerGroupTotalPrint():
    global brokergroupAmt, brokergroupQnt
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(brokergroupAmt)))
    c.drawAlignedString(485, d, str('{0:1.3f}'.format(brokergroupQnt)))
    brokergroupAmt = 0
    brokergroupQnt = 0

def GrandTotalPrint():
    global grandbrokergroupQnt, grandbrokergroupAmt
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(grandbrokergroupAmt)))
    c.drawAlignedString(485, d, str('{0:1.3f}'.format(grandbrokergroupQnt)))
    grandbrokergroupAmt = 0
    grandbrokergroupQnt = 0


def textsize(c, result, d, stdt,etdt, LSMergePlant):
    d = dvalue()
    logic(result, LSMergePlant)
    global y, s, k
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, str(BrokerGroup[-1]))
        d = dvalues(c, stdt, etdt, divisioncode)
        d = dvalues(c, stdt, etdt, divisioncode)
        c.drawString(10, d, Broker[-1])
        d = dvalues(c, stdt, etdt, divisioncode)
        d = dvalues(c, stdt, etdt, divisioncode)
        if Plant[-1] != '':
            c.drawString(10, d, Plant[-1])
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
        c.drawString(10, d, Item[-1])
        d = dvalues(c, stdt, etdt, divisioncode)
        d = dvalues(c, stdt, etdt, divisioncode)
        data(result, d)

    elif divisioncode[-2] == divisioncode[-1]:
        if BrokerGroup[-1] == BrokerGroup[-2]:
            if Broker[-1] == Broker[-2]:
                if Plant[-1] == Plant[-2]:
                    if Item[-1] == Item[-2]:
                        data(result, d)

                    else:
                        boldfonts(7)
                        c.drawString(300, d , "Item Total: ")
                        ItemTotalPrint()
                        d = dvalues(c, stdt, etdt, divisioncode)
                        d = dvalues(c, stdt, etdt, divisioncode)
                        d = dvalues(c, stdt, etdt, divisioncode)
                        c.drawString(10, d, Item[-1])
                        d = dvalues(c, stdt, etdt, divisioncode)
                        d = dvalues(c, stdt, etdt, divisioncode)
                        data(result, d)

                else:
                    boldfonts(7)
                    c.drawString(300, d , "Item Total: ")
                    ItemTotalPrint()
                    d = dvalues(c, stdt, etdt, divisioncode)
                    d = dvalues(c, stdt, etdt, divisioncode)
                    if Plant[-1] != '':
                        c.drawString(300, d , "Company Total: ")
                        PlantTotalPrint()
                        d = dvalues(c, stdt, etdt, divisioncode)
                        d = dvalues(c, stdt, etdt, divisioncode)
                        d = dvalues(c, stdt, etdt, divisioncode)
                    if Plant[-1] != '':
                        c.drawString(10, d, Plant[-1])
                        d = dvalues(c, stdt, etdt, divisioncode)
                        d = dvalues(c, stdt, etdt, divisioncode)
                    c.drawString(10, d, Item[-1])
                    d = dvalues(c, stdt, etdt, divisioncode)
                    d = dvalues(c, stdt, etdt, divisioncode)
                    data(result, d)

            else:
                boldfonts(7)
                c.drawString(300, d , "Item Total: ")
                ItemTotalPrint()
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
                if Plant[-1] != '':
                    c.drawString(300, d , "Company Total: ")
                    PlantTotalPrint()
                    d = dvalues(c, stdt, etdt, divisioncode)
                    d = dvalues(c, stdt, etdt, divisioncode)
                c.drawString(300, d , "Broker Total: ")
                BrokerTotalPrint()
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
                c.drawString(10, d, Broker[-1])
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
                if Plant[-1] != '':
                    c.drawString(10, d, Plant[-1])
                    d = dvalues(c, stdt, etdt, divisioncode)
                    d = dvalues(c, stdt, etdt, divisioncode)
                c.drawString(10, d, Item[-1])
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
                data(result, d)
        else:
            boldfonts(7)
            c.drawString(300, d , "Item Total: ")
            ItemTotalPrint()
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            if Plant[-1] != '':
                c.drawString(300, d , "Company Total: ")
                PlantTotalPrint()
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
            c.drawString(300, d , "Broker Total: ")
            BrokerTotalPrint()
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            c.drawString(300, d , "Broker Group Total: ")
            BrokerGroupTotalPrint()
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            c.drawCentredString(300, d, BrokerGroup[-1])
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            c.drawString(10, d, Broker[-1])
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            if Plant[-1] != '':
                c.drawString(10, d, Plant[-1])
                d = dvalues(c, stdt, etdt, divisioncode)
                d = dvalues(c, stdt, etdt, divisioncode)
            c.drawString(10, d, Item[-1])
            d = dvalues(c, stdt, etdt, divisioncode)
            d = dvalues(c, stdt, etdt, divisioncode)
            data(result, d)
