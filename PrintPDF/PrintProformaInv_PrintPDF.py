import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 525
dy = 190
i = 0
pageno = 0

divisioncode = []
invoiceno = []
itemname = []
itemtype = []
hsncode = []
payment = []
Remark = []
amount = 0

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

def updatedvalue():
    global dy
    dy = 190
    return dy

def dyvalue():
    global dy
    dy = dy - 5
    return dy

def wrap(string, type, width, x, y):
    global i
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - 10
        e = e + 1
        i = i + 1
    return s

def header(divisioncode, result):
    c.setTitle('Proforma Invoice')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 820, divisioncode[-1])
    fonts(8)
    if result['CORPORATEADD'] != None:
        #wrap(string, type, width, x, y)
        wrap(str(result['CORPORATEADD']),c.drawCentredString, 130, 300, 810)
    if result['REGDADD'] != None:
        #wrap(string, type, width, x, y)
        wrap(str(result['REGDADD']),c.drawCentredString, 130, 300, 790)
    # p = page()
    # c.drawString(540, 780, "Page No." + str(p))
    #HoriZontalLine
    c.line(15, 775, 580, 775)
    c.line(15, 745, 580, 745)# last Line Ref
    c.line(290, 705, 580, 705)# OrdNo, OrdDt ^
    c.line(290, 680, 580, 680)#RefNo^
    c.line(15, 645, 580, 645)#Buyer
    c.line(290, 605, 580, 605)  # Port Of Loading ^
    c.line(290, 565, 580, 565)  # Port Of Discharge^
    c.line(15, 545, 580, 545)# Notifying Party 555<--- y of shipment term
    c.line(290, 520, 580, 520)#Quantity , Rate, Amount
    c.line(290, 200, 580, 200)#Total Amount
    c.line(290, 80, 580, 80)#Authorised Sign
    c.line(15, 10, 580, 10)
    #VerticalLine
    c.line(15, 775, 15, 10)
    c.line(290, 745, 290, 10)
    c.line(580, 775, 580, 10)
    c.line(435, 745, 435, 645)#OrdDt & OrdNo Partion
    c.line(390, 545, 390, 200)#Quantity - Rate
    c.line(470, 545, 470, 80)  # Rate- Amount
    # Upperline in header
    boldfonts(9)
    c.drawCentredString(280, 755, "PROFORMA INVOICE" )
    c.line(235, 752, 325, 752)#underline of PROFORMA INVOICE
    boldfonts(7)
    c.drawString(20, 735, "BUYER :")
    c.drawString(295, 735, 'PROFORMA INVOICE NO :')
    c.drawString(440, 735, 'DATE :')
    c.drawString(295, 695, 'REFRENCE NO :')
    c.drawString(295, 670, 'COUNTRY OF ORIGIN :')
    c.drawString(440, 670, 'COUNTRY OF DESTINATION :')
    c.drawString(20, 635, 'NOTIFYING PARTY :')
    c.drawString(295, 635, 'PORT OF LOADING :')
    c.drawString(295, 595, 'PORT OF DISCHARGE :')
    c.drawString(20, 535, 'DESCRIPTION OF GOODS :')
    c.drawAlignedString(390, 535, 'QUANTITY ' + ' ' + str(result['UNIT']))
    c.drawAlignedString(470, 535, 'RATE PER ' + ' ' + str(result['UNIT']))
    c.drawAlignedString(470, 525, str(result['CURRENCY']))# rate CURRENCY
    c.drawAlignedString(580, 535, 'AMOUNT')
    c.drawAlignedString(580, 525, str(result['CURRENCY']))# AMOUNT CURRENCY
    c.drawString(20, 200, "INSTRUCTIONS :")
    c.drawString(20, 170, "REMITTANCE INSTRUCTION : ")
    fonts(7)
    c.drawString(20, 190, str(result['PAYMENTMET']))
    if result['PARNERBNK'] != None:
        c.drawString(20, 160, str(result['PARNERBNK']))
        c.drawString(20, 150, str(result['SWFTCODE']))
    if result['COMPANYBANK'] != None:
        c.drawString(20, 140, str(result['COMPANYBANK']))
        c.drawString(20, 130, str(result['COMPSWFTCD']))
        c.drawString(20, 120, str(result['COMPACOWNER']))
        c.drawString(20, 110, str(result['COMACNO']))
    wrap(str(Remark[-1]),c.drawString, 50, 20, 90)

    #Data
    fonts(7)
    c.drawString(20, 725, str(result['BUYER']))
    if result['BUYERADD'] != None:
        wrap(str(result['BUYERADD']), c.drawString, 45, 20, 715)
    c.drawString(295, 725, str(invoiceno[-1]))
    c.drawString(440, 725, str(result['INVOICEDT'].strftime('%d-%m-%Y')))
    c.drawString(295, 685, str(result['REFNO']))
    c.drawString(295, 660, str(result['COUNTRYOFORIGIN']).upper())
    c.drawString(440, 660, str(result['COUNTRYOFDSTN']))
    if result['NOTIFYINGPRTY'] != None:
        c.drawString(20, 625, str(result['NOTIFYINGPRTY']))
    if result['NOTIFYINGPRTYADD'] != None:
        wrap(str(result['NOTIFYINGPRTYADD']), c.drawString, 45, 20, 615)
    fonts(8)
    c.drawString(295, 625, str(result['PORTOFLOD']))
    wrap(str(result['PORTOFDIS']),c.drawString,50,295, 585)
    # c.drawString(295, 585, str(result['PORTOFDIS']))
    if result['SHIPMENTTERM'] != None:
        c.drawCentredString(435, 550, str(result['SHIPMENTTERM']))

    # Total
    boldfonts(8)
    depth = 0
    wrap(("Total " + str(result['SHIPMENTTERM']) + ' ' + str(result['CURRENCY'])), c.drawAlignedString, 35, 470, 190)
    if len(("Total " + str(result['SHIPMENTTERM']) + ' ' + str(result['CURRENCY']))) > 35:
        muldepth=round(len((("Total " + str(result['SHIPMENTTERM']) + ' ' + str(result['CURRENCY']))))/35)
        depth = depth + 10*muldepth
    # c.drawAlignedString(470, 190, "Total " +  str(result['SHIPMENTTERM']) + ' ' + str(result['CURRENCY']))

    #FREIGHT AND FOB VALUE
    boldfonts(7)
    c.drawAlignedString(470, 175-depth, "FOB VALUE  " + str(result['CURRENCY']))
    c.drawAlignedString(560, 175-depth, str(result['FOBVALUE']))
    if int(float(result['FREIGHTTVALUE'])) != 0:
        c.drawAlignedString(470, 165-depth, "FREIGHT  " + str(result['CURRENCY']))
        c.drawAlignedString(560, 165-depth, str(result['FREIGHTTVALUE']))
    if int(float(result['INSURANCE'])) != 0:
        c.drawAlignedString(470, 155-depth, "INSURANCE  " + str(result['CURRENCY']))
        c.drawAlignedString(560, 155-depth, str(result['INSURANCE']))
    # c.drawString(20, 535, 'DESCRIPTION OF GOODS :')
    # c.drawAlignedString(390, 535, 'QUANTITY')
    # c.drawAlignedString(470, 535, 'RATE PER (KGS)')
    # c.drawAlignedString(580, 535, 'AMOUNT')


def data(result, d):
    fonts(7)
    c.drawString(30, d, str(result['SHADE']))
    c.drawAlignedString(370, d, str(result['QUANTITY']))
    c.drawAlignedString(455, d, str(result['RATE']))
    c.drawAlignedString(560, d, str(result['AMOUNT']))
    TotalAmount(result)

def logic(result):
    global divisioncode
    global invoiceno, Remark, itemtype
    global itemname, hsncode, payment
    divisioncode.append(result['COMPANY'])
    invoiceno.append(result['INVOICENO'])
    itemname.append(result['ITEM'])
    itemtype.append(result['ITMTYP'])
    hsncode.append(result['HSNCODE'])
    # payment.append(result['PAYMENTMET'])
    Remark.append(result['REMARKS'])

def newpage():
    global d
    d = 525
    return d

def newrequest():
    global divisioncode, dy
    global invoiceno, Remark, itemtype
    global itemname, hsncode, payment
    global pageno
    divisioncode = []
    pageno = 0
    invoiceno = []
    itemname = []
    hsncode = []
    payment = []
    Remark = []
    itemtype = []
    dy = 190

def TotalAmount(result):
    global amount
    amount += float(result['AMOUNT'])

def TotalClean():
    global amount
    amount = 0

def textsize(c, result):
    d = dvalue()
    logic(result)
    global i
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(divisioncode, result)
        c.drawString(20, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        i = 0
        fonts(7)
        wrap(str(itemname[-1]),c.drawString,60,20,d)
        while i != 1:
            d = dvalue()
            d = dvalue()
            i = i -1
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1] == invoiceno[-2]:
            if itemtype[-1] == itemtype[-2]:
                if itemname[-1] == itemname[-2]:
                    data(result, d)

                elif itemname[-1] != itemname[-2]:
                    c.drawCentredString(80,  d, hsncode[-2])
                    d = dvalue()
                    d = dvalue()
                    i = 0
                    fonts(7)
                    wrap(str(itemname[-1]),c.drawString,60,20,d)
                    while i != 1:
                        d = dvalue()
                        d = dvalue()
                        i = i - 1
                    d = dvalue()
                    d = dvalue()
                    data(result, d)

            elif itemtype[-1] != itemtype[-2]:
                c.drawCentredString(80, d, hsncode[-2])
                d = dvalue()
                d = dvalue()
                boldfonts(7)
                c.drawString(20, d, itemtype[-1])
                d = dvalue()
                d = dvalue()
                i = 0
                fonts(7)
                wrap(str(itemname[-1]), c.drawString, 60, 20, d)
                while i != 1:
                    d = dvalue()
                    d = dvalue()
                    i = i - 1
                d = dvalue()
                d = dvalue()
                data(result, d)

        elif invoiceno[-1] != invoiceno[-2]:
            c.drawCentredString(80, d, hsncode[-2])
            boldfonts(8)

            c.drawAlignedString(560, 190, str('{0:1.2f}'.format(amount)))
            c.drawAlignedString(560, 70, 'For ' +  divisioncode[-2])
            c.drawAlignedString(560, 20, "Authorised  Signatory")
            fonts(7)
            TotalClean()
            c.showPage()
            d = newpage()
            d = dvalue()
            header(divisioncode, result)
            c.drawString(20, d, itemtype[-1])
            d = dvalue()
            d = dvalue()
            i = 0
            fonts(7)
            wrap(str(itemname[-1]),c.drawString,60,20,d)
            while i != 1:
                d = dvalue()
                d = dvalue()
                i = i - 1
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        c.drawCentredString(80, d, hsncode[-2])
        boldfonts(8)

        c.drawAlignedString(560, 190, str('{0:1.2f}'.format(amount)))
        c.drawAlignedString(560, 70, 'For ' +  divisioncode[-2])
        c.drawAlignedString(560, 20, "Authorised  Signatory")
        fonts(7)
        TotalClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(divisioncode, result)
        c.drawString(20, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        i = 0
        fonts(7)
        wrap(str(itemname[-1]),c.drawString,60,20,d)
        while i != 1:
            d = dvalue()
            d = dvalue()
            i = i - 1
        d = dvalue()
        d = dvalue()
        data(result, d)

