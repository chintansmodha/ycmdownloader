import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date, datetime
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 505
pageno = 0

divisioncode = []
Party = []
BrokerGroup = []

freight = 0
gst = 0
insurance = 0
quantity = 0
baseamount = 0
dharaamount = 0
dharapaid = 0
dicountall = 0

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


def wrap(string, type, width, x, y):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - 10
        e = e + 1
    return s

def header(divisioncode, stdt, etdt):
    c.setTitle('Broker Wise RD')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(420, 565, divisioncode[-1])
    fonts(8)
    c.drawCentredString(420,550, 'Broker Wise RD (Without RD Invoices)  Report  ' + str(stdt.strftime("%d - %b - %Y")) + '  From  ' + str(etdt.strftime("%d - %b - %Y")))

    # Line
    c.line(0, 540, 850, 540)
    c.line(0, 510, 850, 510)

    #column Name
    c.drawString(10, 525, 'Inv No.')
    c.drawString(60, 525, 'Iss Date')
    c.drawString(110, 525, 'Freight')
    c.drawString(160, 525, 'GST')
    c.drawString(200, 525, 'Insur.')
    c.drawString(270, 525, 'Qty.')
    c.drawString(310, 525, 'Base Rt.')
    c.drawString(390, 525, 'Base Amt.')
    c.drawString(440, 525, 'Inv.Rt.')
    c.drawString(480, 525, 'Dh.Rt.')
    c.drawString(540, 525, 'Dh.Amt.')
    c.drawString(590, 525, 'Dh.Paid')
    c.drawString(640, 525, 'Dis All')
    c.drawString(680, 525, 'Yarn Type')
    wrap('Initial Com%',c.drawString,5,760, 525)
    # c.drawString(800, 520, 'Intial Com%')
    wrap('Balance Com', c.drawString, 5, 800, 525)
    # c.drawString(840, 520, 'Balance Com')

def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['INVOICENO']))
    c.drawString(60, d, str(result['ISSUEDT'].strftime('%d-%m-%Y')))
    c.drawAlignedString(120, d, str(result['FREIGHT']))
    c.drawAlignedString(165, d, str(result['GST']))
    c.drawAlignedString(210, d, str(result['INSUR']))
    c.drawAlignedString(275, d, str(result['QTY']))
    c.drawAlignedString(325, d, str(result['BASERT']))
    c.drawAlignedString(415, d, str(result['BASEAMT']))
    c.drawAlignedString(450, d, str(result['INVRT']))
    c.drawAlignedString(490, d, str(result['DHRT']))
    c.drawAlignedString(560, d, str(result['DHAMT']))
    c.drawAlignedString(610 , d, str(result['DHPAID']))
    c.drawAlignedString(660, d, str(result['DISALL']))
    c.drawString(681, d, str(result['YARNTYPE']))
    c.drawAlignedString(775, d, str(result['INTIALCOMPER']))
    c.drawAlignedString(815, d, str(result['BALANCECOMPER']))
    BrokergroupTotal(result)

def logic(result):
    global divisioncode, Party, BrokerGroup
    divisioncode.append(result['COMPANY'])
    Party.append(result['PARTY'])
    BrokerGroup.append(result['BROKERGRP'])

def newpage():
    global d
    d = 505
    return d

def newrequest():
    global divisioncode, Party, BrokerGroup
    global pageno
    divisioncode = []
    Party = []
    BrokerGroup = []
    pageno = 0

def BrokergroupTotal(result):
    global freight, gst, insurance, dharapaid
    global quantity, baseamount, dharaamount, dicountall

    freight += float(result['FREIGHT'])
    gst += float(result['GST'])
    insurance += float(result['INSUR'])
    quantity += float(result['QTY'])
    baseamount += float(result['BASEAMT'])
    dharaamount += float(result['DHAMT'])
    dharapaid += float(result['DHPAID'])
    dicountall += float(result['DISALL'])

def BrokerTotalPrint():
    global freight, gst, insurance, dharapaid
    global quantity, baseamount, dharaamount, dicountall
    boldfonts(7)
    c.drawString(10, d, 'Broker Group Total: ')
    c.drawAlignedString(120, d, str('{0:1.0f}'.format(freight)))
    c.drawAlignedString(165, d, str('{0:1.2f}'.format(gst)))
    c.drawAlignedString(210, d, str('{0:1.0f}'.format(insurance)))
    c.drawAlignedString(275, d, str('{0:1.2f}'.format(quantity)))
    c.drawAlignedString(415, d, str('{0:1.2f}'.format(baseamount)))
    c.drawAlignedString(560, d, str('{0:1.2f}'.format(dharaamount)))
    c.drawAlignedString(610, d, str('{0:1.0f}'.format(dharapaid)))
    c.drawAlignedString(660, d, str('{0:1.0f}'.format(dicountall)))
    freight = 0
    gst = 0
    insurance = 0
    quantity = 0
    baseamount = 0
    dharaamount = 0
    dharapaid = 0
    dicountall = 0
    fonts(7)



def textsize(c, result,d,stdt,etdt):
    d = dvalue()
    logic(result)

    if  len(divisioncode) == 1:
        header(divisioncode,stdt,etdt)
        boldfonts(7)
        c.drawCentredString(420, d, BrokerGroup[-1])
        fonts(7)
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Party[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if BrokerGroup[-1] == BrokerGroup[-2]:
            if Party[-1] == Party[-2]:
                data(result, d)

            elif Party[-1] != Party[-2]:
                d = dvalue()
                c.drawString(10, d, Party[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)

        elif BrokerGroup[-1] != BrokerGroup[-2]:
            d = dvalue()
            BrokerTotalPrint()
            c.setPageSize(landscape(A4))
            c.showPage()
            d = newpage()
            d = dvalue()
            header(divisioncode, stdt, etdt)
            boldfonts(7)
            c.drawCentredString(420, d, BrokerGroup[-1])
            fonts(7)
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, Party[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        d = dvalue()
        BrokerTotalPrint()
        c.setPageSize(landscape(A4))
        c.showPage()
        d = newpage()
        d = dvalue()
        header(divisioncode, stdt, etdt)
        boldfonts(7)
        c.drawCentredString(420, d, BrokerGroup[-1])
        fonts(7)
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Party[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)



