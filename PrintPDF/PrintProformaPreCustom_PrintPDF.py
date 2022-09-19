import textwrap

from num2words import num2words
from reportlab.lib.pagesizes import portrait, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number, format_currency, format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(portrait(A4)))
c.setPageSize(portrait(A4))
c2 = canvas.Canvas("1.pdf", pagesize=(portrait(A4)))
c2.setPageSize(portrait(A4))
d = 440
D = 655
i = 0
pageno = 0

divisioncode = []
invoiceno = []
comercialinvno = []
itemname = []
itemtype = []
lotno = []
hsncode = []
payment = []
Remark = []
countryofOrigin = []
iecno = []
gsttaxinvoiceno = []
description = []
eseal = []
seal = []
containerno = []
dates = []
place = []
stuffing = []
currency = []
grosswt = 0
netwt = 0
packages = 0
amount = 0
quantity = 0
#*****************
Goods = []
ComercialInvNo = []
IECNo = []
GstTaxInvNo = []
ESealNo = []
SealNo = []
ContainerNo = []
Date = []
Place = []
StuffingAt = []
SLL_DESCRIPTION1 = []
Ert_CircularNo = []

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
    global d
    d = 190
    return d

def Dvalue():
    global D
    D = D - 10
    return D

def DlocalValue():
    global D
    D = D - 5
    return D

def DValueIncrese():
    global D
    D = D + 10
    return D

def updateDvalue():
    global D
    D = 655
    return D


def wrap(string, type, width, x, y):
    global i
    wrap_text = textwrap.wrap(string, width=width, break_on_hyphens=True)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - 8
        e = e + 1
        i = i + 1
    return s


def header(divisioncode, result):
    c.setTitle('Custom Invoice')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # Horizontal line
    c.line(15, 830, 580, 830)  # Upper line
    c.drawCentredString(290, 815, "INVOICE")
    fonts(7)
    c.drawCentredString(290, 806,
                        "SUPPLY MEANT FOR EXPORT UNDER LETTER OF UNDERTAKING WITHOUT PAYMENT OF INTERGATED TAX (IGST)")
    # c.line(237, 812, 340, 812)# Underline
    c.line(15, 802, 580, 802)  # Packing List Partn
    # c.line(350, 755, 580, 755)# Buyers Ord No And packing list no
    c.line(15, 760, 580, 760)  # factory add and corp add
    c.line(15, 730, 350, 730)  # regd add and corp add
    c.line(15, 700, 580, 700)  # prtn comp and consignee
    # c.line(350, 690, 580, 690)#prtn stuffing container and under duty drawback
    c.line(350, 680, 580, 680)  # under duty drawback and notify party
    c.line(15, 630, 350, 630)  # prtn buyer and consignee
    c.line(350, 610, 580, 610)  # notify party and country orgin
    c.line(350, 590, 580, 590)  # country orgin and ref No-----------
    c.line(15, 560, 580, 560)  # prtn pre-cariage by and buyer------->sb no
    c.line(15, 550, 350, 550)  # pre-cariage by and Fligt No
    c.line(15, 520, 350, 520)  # Fligt No and port of dis
    c.line(15, 490, 580, 490)  # Partn Desptn Goods And Buyer
    c.line(15, 470, 580, 470)  # Desptn Goods an name of goods
    c.line(15, 125, 580, 125)
    c.line(15, 105, 580, 105)  # order Refer And authorised sign
    c.line(15, 60, 580, 60)
    c.line(15, 10, 580, 10)  # Lower Line

    # Vertical Line
    c.line(15, 830, 15, 10)
    c.line(465, 610, 465, 590)  # country origin and country dstn
    c.line(183, 560, 183, 490)  # flight no and port of dis
    c.line(350, 802, 350, 490)  # partn comp and Notifying Party
    c.line(135, 470, 135, 60)  # shippng marks and desscpn of goods
    c.line(360, 490, 360, 60)  # desscpn of goods and packages
    c.line(410, 490, 410, 105)  # Pack and Quantity
    c.line(480, 490, 480, 105)  # Quantity and Rate
    c.line(520, 490, 520, 105)  # Rate And Amount
    c.line(250, 700, 250, 560)  # prtn byer and riht small box
    c.line(580, 830, 580, 10)

    # References Of Box
    boldfonts(4)
    c.drawString(18, 797, "Exporter")
    boldfonts(6)
    c.drawString(20, 690, "Consignee :")
    c.drawString(20, 620, "Buyer :")
    boldfonts(5)
    c.drawString(20, 553, "Pre-Carriage by")
    c.drawString(188, 553, "Place Of Receipt by Pre-Carrier")
    boldfonts(6)
    c.drawString(20, 540, "Vessel/Flight No. V. No.")
    c.drawString(188, 540, "Port Of Loading")
    c.drawString(20, 510, "Port Of Discharge")
    c.drawString(188, 510, "Final Destination")
    fonts(7)
    c.drawString(20, 460, "Cont Size  " + "        : " + str(result['CONTSIZE']))
    c.drawString(20, 450, "Cont No.   " + "        : " + containerno[-1])
    c.drawString(20, 440, "Seal No.   " + "        : " + seal[-1])
    c.drawString(20, 430, "E-Seal No. " + "        : " + eseal[-1])
    c.drawString(20, 420, "GR.WT.    " + str(result['WTUNIT']) + "   :  ")  # + str(result['GRWT']))
    c.drawString(20, 410, "NT.WT.     " + str(result['WTUNIT']) + "   :  ")  # + str(result['NETWT']))
    c.drawString(20, 400, "Measurement" + "        : " + str(result['MEASURE']))
    c.drawString(20, 390, "Packages   " + "        : ")
    c.drawString(20, 150, "MASTER EXP")
    if result['MASTEREXPNO'] != None:
        c.drawString(20, 140, str(result['MASTEREXPNO']))
        c.drawString(20, 130, str(result['MASTEREXPDT'].strftime('%d-%m-%Y')))
    c.drawString(20, 117, 'Amount Chargeable (In Words)')

    # ******** Right Side
    boldfonts(6)
    c.drawString(355, 795, "INVOICE NO. & Date")
    c.line(498, 802, 498, 792)
    c.drawString(500, 795, "IEC Branch Code : " + str(result['IECBRANCH']))  # between line
    c.line(498, 792, 580, 792)
    # c.drawString(355, 745, "Buyer's Order No. & Date")
    c.drawString(355, 673, "Notifying Party: ")
    c.drawString(355, 553, "Terms Of Delivery And Payment")
    c.drawString(355, 603, "Country Of Origin")
    c.drawString(470, 603, "Country Of Final Destination")
    c.drawString(20, 475, "Shipping Marks & No's/Container No.")
    c.drawString(155, 475, "Description Of Goods")
    c.drawString(155, 460, "No Of Cartons")
    c.line(155, 458, 195, 458)  # underline No Of Cartons
    c.drawCentredString(445, 460, str(result['PRIMARYUMCODE']))  # Quant unit
    c.drawCentredString(500, 460, str(currency[-1]))  # Rate unit
    c.drawCentredString(550, 460, str(currency[-1]))  # Amount Unit
    # c.drawAlignedString(175, 450, str(result['PACKAGES']))  # No Of Cartons
    c.drawAlignedString(410, 475, "Packages")
    c.drawAlignedString(480, 475, "Quantity")
    c.drawAlignedString(520, 475, "Rate")
    c.drawAlignedString(580, 475, "Amount")
    c.drawString(20, 50, "Declaration :")
    fonts(7)  # Declaration
    string = 'We declare that this invoice shows the actual price of the goods described and that all particulars  ' \
             'are true and correct'
    string1 = 'I/WE UNDERTAKE TO ABIDE BY PROVISIONS OF FEMA 1999, AS AMENDED FROM TIME TO TIME , INCL. REALIZATION / REPATRIATION ' \
              'OF FOREIGN EXCHANGE TO /FROM INDIA '
    wrap(string, c.drawString, 105, 20, 40)
    fonts(6)
    wrap(string1, c.drawString, 105, 20, 20)
    boldfonts(6)
    # c.drawString(20, 40, "Other Reference :")
    c.drawString(515, 15, "Authorised Signatory")
    boldfonts(7)
    c.drawAlignedString(570, 50, divisioncode[-1])

    # Data
    fonts(15)
    c.drawCentredString(182, 786, divisioncode[-1])
    fonts(7)
    wrap(str(result['FAC_ADDRESS']), c.drawCentredString, 85, 181, 775)
    wrap(str(result['CORP_ADDRESS']), c.drawCentredString, 100, 181, 750)
    fonts(6)
    c.drawString(20, 732, str(result['CORP_GSTIN']))
    c.drawString(150, 732, str(result['TAXID']))
    if result['IECNO'] != None:
        c.drawAlignedString(290, 732, iecno[-1])
    fonts(7)
    wrap(str(result['REGD_ADDRESS']), c.drawCentredString, 95, 181, 720)
    fonts(6)
    c.drawAlignedString(340, 702, str(result['CINNO']))
    c.drawString(20, 680, str(result['CONSIGNEENAME']))
    wrap(str(result['CONSIGNEEADDRESS']), c.drawString, 60, 20, 670)
    if result['EPCGLICENSE'] != '':
        c.drawString(255, 685, 'EPCG  LICENSE: ' + str(result['EPCGLICENSE']))
        c.drawString(255,675, 'DT: ' + str(result['EPCGLICENSEDATE']))
    # if result['SLL_DESCRIPTION'] != None:
    #     wrap(result['SLL_DESCRIPTION'],c.drawString,25, 255, 660)
        # c.drawString(255,660, result['SLL_DESCRIPTION'])
    c.drawString(20, 610, str(result['BUYER']))
    wrap(str(result['BUYERADDRESS']), c.drawString, 60, 20, 600)
    if result['ADVLICENSE'] != None:
        c.drawString(255, 615, 'ADVANCE  LICENSE: ' + str(result['ADVLICENSE']))
        c.drawString(255,605, 'DT: ' + str(result['ADVLICENSEDATE']))
    else:
        s = 'I/WE INTEND TO CLAIM BENIFITS UNDER THE REMISSION OF DUTIES AND TAXES ON EXPORTED ' \
            'PRODUCTS (RODTEP) SCHEME(YES)'
        wrap(s, c.drawString, 25, 255, 615)
    c.drawString(355, 665, str(result['NOTIFYPRTYNAME']))
    wrap(str(result['NOTIFYPRTYADDRESS']), c.drawString, 50, 355, 655)
    fonts(7)
    c.drawString(355, 787, invoiceno[-1])
    c.line(350, 783, 580, 783)  # line after invoice no-----------------
    boldfonts(7)
    if result['ADCODE'] != None:
        wrap(str(result['ADCODE']).upper(), c.drawString, 40, 355, 775)
    else:
        c.drawString(355, 775, 'AD Code: ')
    fonts(7)
    c.drawString(355, 750, result['STUFFINGGT'])
    wrap(result['SLL_DESCRIPTION'],c.drawString,55, 355, 740)
    wrap(stuffing[-1], c.drawString, 65, 355, 720)
    wrap('UNDER  '+ str(result['SCHEME']), c.drawString, 50, 355, 692)
    # c.drawString(355, 745, "Stuffing of container")
    # c.drawString(355, 780, str(result['ORDNOANDDT']))
    if result['REFNOANDDT'] != None:
        c.drawString(355, 582, 'Ref No.: ' + str(result['REFNOANDDT']))
    c.drawString(355, 546, str(result['TERMSOFDELV']))
    wrap(str(result['PAYMENT']), c.drawString, 60, 355, 538)
    if result['COUNTRYOFORIGIN'] != None:
        c.drawString(355, 595, str(result['COUNTRYOFORIGIN']).upper())
    if result['COUNTRYOFDESTN'] != None:
        c.drawString(470, 595, str(result['COUNTRYOFDESTN']))
    c.drawString(20, 530, str(result['VESSELFLIGHTNO']))
    c.drawString(20, 500, str(result['PORTOFDISCHARGE']))
    c.drawString(188, 530, str(result['PORTOFLOADING']))
    c.drawString(188, 500, str(result['FINALDESTINATION']))
    c.drawString(355, 505,
                 "S/B NO.: " + str(result['SBNO']) + "                                    " + "       DT: " + str(
                     result['SBDT']))
    c.drawString(355, 492,
                 "B/L NO.: " + str(result['BLNO']) + "                                    " + "       DT: " + str(
                     result['BLDT']))

    # ex Rate, Gst.inv value in inr gst in INR , fob , freight , insurance, cfrorcif
    boldfonts(7)
    c.drawString(140, 96, 'EX RATE @ INR' + '       : ' + str(result['EXRATE']))
    if result['GSTINVVALUEINR'] != None:
        c.drawString(140, 88, 'GST.INV VALUE IN INR' + '        : ' + str(result['GSTINVVALUEINR']))
    if result['GSTININR'] != None:
        c.drawString(140, 80, 'GST IN INR @ 0.00%' + '      : ' + str(result['GSTININR']))

    if result['FOBVALUE'] != None:
        if int(float(result['FOBVALUE'])) != 0:
            c.drawString(365, 96, 'FOB Value    ' + str(currency[-1]) + '        : ')
            c.drawAlignedString(560, 96, str('{0:1.4f}'.format(float(result['FOBVALUE']))))
    if result['FREIGHT'] != None:
        if int(float(result['FREIGHT'])) != 0:
            c.drawString(365, 86, 'FREIGHT  ' + str(currency[-1]) + '        : ')
            c.drawAlignedString(560, 86, str('{0:1.4f}'.format(float(result['FREIGHT']))))
    if result['INSURANCE'] != None:
        if int(float(result['INSURANCE'])) != 0:
            c.drawString(365, 76, 'INSURANCE    ' + str(currency[-1]) + '        : ')
            c.drawAlignedString(560, 76, str('{0:1.4f}'.format(float(result['INSURANCE']))))
            c.drawString(365, 66, 'CIF Value    ' + str(currency[-1]) + '       : ')
            c.drawAlignedString(560, 66, str('{0:1.4f}'.format(float(result['CIFVALUE']))))
        else:
            if int(float(result['FREIGHT'])) != 0:
                c.drawString(365, 66, 'CFR Value    ' + str(currency[-1]) + '       : ')
                c.drawAlignedString(560, 66, str('{0:1.4f}'.format(float(result['CFRVALUE']))))
            else:
                c.drawString(365, 66, 'Total    ' + str(currency[-1]) + '       : ')
                c.drawAlignedString(560, 66, str('{0:1.4f}'.format(float(result['CFRVALUE']))))


def data(result, d):
    fonts(7)
    str1 = ''
    string = str1.join(result['ITEM'])
    wrap_text = textwrap.wrap(string, width=55)
    e = 0
    while e < len(wrap_text):
        c.drawString(140, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(155, d, str(result['ITEM']))
    c.drawAlignedString(405, d, str(result['BOXES']))
    c.drawAlignedString(465, d, str(result['PRIMARYQTY']))
    c.drawAlignedString(505, d, str(result['RATE']))
    c.drawAlignedString(560, d, str(result['AMOUNT']))
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1
    TotalWT(result)
    # Goods.append(str(result['ITEM']))
    Newappend(result)


def logic(result):
    global divisioncode, currencyiecno,  dates,  place,  stuffing, iecno
    global  gsttaxinvoiceno,  description,  eseal,  seal,  containerno
    global invoiceno, Remark, itemtype, lotno, comercialinvno
    global itemname, hsncode, payment, countryofOrigin
    global Goods
    divisioncode.append(result['COMPANY'])
    invoiceno.append(result['INVOICENOANDDT'])
    # itemname.append(result['ITEM'])
    itemtype.append(result['ITMTYP'])
    lotno.append(result['LOTNO'])
    hsncode.append(result['HSNCODE'])
    # payment.append(result['PAYMENT'])
    # Remark.append(result['REMARKS'])
    countryofOrigin.append(result['COUNTRYOFORIGIN'])
    currency.append(result['CURRENCY'])
    iecno.append(str(result['IECNO']))
    # gsttaxinvoiceno.append(str(result['']))
    # description.append(str(result['']))
    eseal.append(str(result['ESEALNO']))
    seal.append(str(result['SEALNO']))
    containerno.append(str(result['CONTNO']))
    # dates.append(str(result['']))
    # place.append(str(result['']))
    stuffing.append(str(result['STUFFINGOFCONTAINERAT']))
    comercialinvno.append(str(result['COMMERCIALINVNO']))


def newpage():
    global d
    d = 440
    return d


def newrequest():
    global divisioncode, lotno, currency, currencyiecno,  dates,  place,  stuffing
    global  gsttaxinvoiceno,  description,  eseal,  seal,  containerno, iecno
    global invoiceno, Remark, itemtype, comercialinvno
    global itemname, hsncode, payment, countryofOrigin
    global Goods
    global pageno
    divisioncode = []
    pageno = 0
    invoiceno = []
    itemname = []
    hsncode = []
    payment = []
    Remark = []
    itemtype = []
    lotno = []
    countryofOrigin = []
    currency = []
    iecno = []
    gsttaxinvoiceno = []
    description = []
    eseal = []
    seal = []
    containerno = []
    dates = []
    place = []
    stuffing = []
    comercialinvno = []

#*********************** ExminationReport ************************************
def Newappend(result):
    global Goods,ComercialInvNo, IECNo, GstTaxInvNo, ESealNo,SealNo
    global  ContainerNo, Date, Place, StuffingAt, SLL_DESCRIPTION1
    global Ert_CircularNo
    Goods.append(str(result['ITEM']))
    IECNo.append(str(result['IECNO']))
    # GstTaxInvNo.append(str(result['']))
    ESealNo.append(str(result['ESEALNO']))
    SealNo.append(str(result['SEALNO']))
    ContainerNo.append(str(result['CONTNO']))
    # Date.append(str(result['']))
    # Place.append(str(result['']))
    StuffingAt.append(str(result['STUFFINGOFCONTAINERAT'] + ' ' + result['STUFFINGEXMGT']))
    ComercialInvNo.append(str(result['COMMERCIALINVNO']))
    Date.append(result['INVOICEDT'])
    Place.append(result['PLACE'])
    SLL_DESCRIPTION1.append(result['SLL_DESCRIPTION'])
    if result['CIRCULARNO'] != None:
        Ert_CircularNo.append(result['CIRCULARNO'])
    else:
        Ert_CircularNo.append('')


def NewRequest():
    global Goods, ComercialInvNo, IECNo, GstTaxInvNo, ESealNo, SealNo
    global ContainerNo, Date, Place, StuffingAt,SLL_DESCRIPTION1, Ert_CircularNo
    Goods = []
    ComercialInvNo = []
    IECNo = []
    GstTaxInvNo = []
    ESealNo = []
    SealNo = []
    ContainerNo = []
    Date = []
    Place = []
    StuffingAt = []
    SLL_DESCRIPTION1 = []
    Ert_CircularNo = []
#*************************************************************


def TotalWT(result):
    global grosswt, netwt, packages, amount, quantity
    packages = packages + int(result['BOXES'])
    if result['GROSSWT'] != None:
        grosswt = grosswt + float(result['GROSSWT'])
    if result['NETWT'] != None:
        netwt = netwt + float(result['NETWT'])
    amount = amount + float(result['AMOUNT'])
    quantity = quantity + float(result['PRIMARYQTY'])

# Exmination Report **********************************************
sr = 1
li = 0
Y = 0
def SerialNo():
    global sr
    sr = sr + 1
    return sr

def SetSerialNo():
    global sr
    sr = 1
    return sr
def Data(Goods,D,sr,li):
    # print(sr)
    fonts(7)
    c.drawString(174, D, str(sr))
    str1 = ''
    string = str1.join(Goods[li])
    wrap_text = textwrap.wrap(string, width=55)
    e = 0
    while e < len(wrap_text):
        c.drawString(190, D, wrap_text[e])
        D = DlocalValue()
        D = DlocalValue()
        e = e + 1


def ExminationReport(Goods,D,sr):
    global Y
    # print(sr)
    #horizontal line
    c.line(25, 825, 575, 825)
    c.line(25, 15, 575, 15)
    # vertical Line
    c.line(25, 825, 25, 15)
    c.line(575, 825, 575, 15)
    boldfonts(13)
    c.drawCentredString(300, 800, 'EXAMINATION REPORT SELF SEALING OF EXPORT GOODS')
    c.line(113, 797, 487, 797)
    fonts(7)
    string = 'AS PER BOARD CIRCULAR NO.  '  + Ert_CircularNo[0] +  '  C.EX. DATED  ISSUED UNDER  ' + SLL_DESCRIPTION1[0]
    wrap(string,c.drawString,70,30,775)
    c.drawString(30, 745, 'ISSUED BY :- ')
    string = 'CERTIFIED THAT DESCRIPTION AND VALUE OF THE GOODS COVERED BY THIS COMMERCIAL INVOICE NO. '\
             + ComercialInvNo[0] + ' ' \
             'HAVE BEEN CHECKED BY ME AND THE GOODS HAVE BEEN PACKED AND SEALED WITH ' \
             'ONE TIME LOCK SEAL UNDER MY SUPERVISION '
    wrap(string,c.drawString,100, 30, 715)
    # c.drawString(30, 725, 'CERTIFIED THAT DESCRIPTION AND VALUE OF THE GOODS COVERED BY THIS COMMERCIAL INVOICE NO. '
    #                       '   HAVE BEEN CHECKED BY ME AND THE GOODS HAVE BEEN PACKED AND SEALED WITH '
    #                       'ONE TIME LOCK SEAL UNDER MY SUPERVISION ')
    c.drawString(30, 675, 'IEC NO.')
    c.drawString(170, 675 , ': ' + IECNo[0])
    c.drawString(30, 665, 'GST TAX INVOICE NO.')
    c.drawString(170, 665, ': ')
    c.drawString(30, 655, 'DESCRIPTION ')
    c.drawString(170, 655, ': ')
    length = len(Goods)
    while length != 0:
        Data(Goods,D,sr,li)
        D = DlocalValue()
        length = length - 1
        sr = SerialNo()
    D = DlocalValue()
    D = DValueIncrese()
    c.drawString(190, D, '(All details as per invoice)')
    D = DlocalValue()
    D = DlocalValue()
    D = Dvalue()
    D = Dvalue()
    c.drawString(30, D, 'E-SEAL NO.')
    c.drawString(170, D , ': ' + ESealNo[0])
    D = Dvalue()
    c.drawString(30, D, 'CONTAINER NO.')
    c.drawString(170, D , ': ' + ContainerNo[0])
    D = Dvalue()
    c.drawString(30, D, 'SEAL NO.')
    c.drawString(170, D , ': ' + SealNo[0])
    D = Dvalue()
    D = Dvalue()
    Y = Y + D
    c.drawString(30, D, 'GROSS WEIGHT')
    c.drawString(170, D , ': ')
    D = Dvalue()
    c.drawString(30, D, 'NET WEIGHT')
    c.drawString(170, D , ': ')
    D = Dvalue()
    c.drawString(30, D, 'TOTAL NO. OF PACKAGES')
    c.drawString(170, D , ': ')
    D = Dvalue()
    D = Dvalue()
    c.drawString(30, D, 'DATE')
    c.drawString(170, D , ': ' + Date[0])
    D = Dvalue()
    c.drawString(30, D, 'PLACE')
    c.drawString(170, D , ': ' +  Place[0])
    D = Dvalue()
    c.drawString(30, D, 'STUFFING OF CONTAINER AT')
    c.drawString(170, D , ': ')
    wrap(StuffingAt[0],c.drawString,90,174,D)

#*********************************************************************
def TotalClean():
    global grosswt
    global netwt
    global packages, amount, quantity, Y
    grosswt = 0
    netwt = 0
    packages = 0
    amount = 0
    quantity = 0
    Y = 0


def textsize(c, result,goods,D,sr):
    d = dvalue()
    logic(result)
    global i
    # '{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(divisioncode, result)
        c.drawString(140, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)
        # Newappend(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1] == invoiceno[-2]:
            if itemtype[-1] == itemtype[-2]:
                if lotno[-1] == lotno[-2]:
                    data(result, d)
                    # Newappend(result)

                elif lotno[-1] != lotno[-2]:
                    c.drawString(155, d, "LOTNO. :  " + lotno[-2])
                    d = dvalue()
                    d = dvalue()
                    data(result, d)
                    # Newappend(result)

            elif itemtype[-1] != itemtype[-2]:
                c.drawString(155, d, "LOTNO. :  " + lotno[-2])
                d = dvalue()
                d = dvalue()
                c.drawString(155, d, "HSNCODE :  " + hsncode[-2])
                d = dvalue()
                d = dvalue()
                c.drawString(140, d, itemtype[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)
                # Newappend(result)

        elif invoiceno[-1] != invoiceno[-2]:
            c.drawString(155, d, "LOTNO. :  " + lotno[-2])
            d = dvalue()
            d = dvalue()
            c.drawString(155, d, "HSNCODE :  " + hsncode[-2])
            d = dvalue()
            d = dvalue()
            c.drawString(155, d, "COUNTRY OF ORIGIN:  " + str(countryofOrigin[-2]).upper())
            # c.line(400, 115, 580, 115)
            c.drawString(490, 118, "<--Total ")
            c.drawAlignedString(405, 118, str(packages))
            c.drawAlignedString(465, 118, str('{0:1.3f}'.format(quantity)))
            c.drawAlignedString(560, 110, str('{0:1.4f}'.format(amount)))
            # shiping marks
            c.drawString(85, 420, str('{0:1.3f}'.format(grosswt)))
            c.drawString(85, 410, str('{0:1.3f}'.format(netwt)))
            c.drawString(85, 390, str(packages))
            c.drawAlignedString(175, 450, str(packages))  # No Of Cartons
            # Amounts in words
            str1 = str(num2words(str('{0:1.4f}'.format(amount)), lang='en', to='currency', separator=' and',
                                 cents=True, currency=str(currency[-2]).strip())).replace(',','')
            wrap(str(currency[-2]).strip() + ' ' + str1, c.drawString, 55, 140, 117)
            #************************************************ExminationReport
            c.showPage()
            ExminationReport(Goods,D,sr)
            c.drawString(170, 665, ': ' + invoiceno[-2])
            c.drawString(170, Y, ': ' + str(grosswt))
            c.drawString(170, Y - 10, ': ' + str(netwt))
            c.drawString(170, Y - 20, ': ' + str(packages))
            NewRequest()
            sr = SetSerialNo()
            D = updateDvalue()
            TotalClean()
            #***************************************
            c.setPageSize(portrait(A4))
            c.showPage()
            d = newpage()
            d = dvalue()
            header(divisioncode, result)
            c.drawString(140, d, itemtype[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)
            # Newappend(result)

    elif divisioncode[-1] != divisioncode[-2]:
        c.drawString(155, d, "LOTNO. :  " + lotno[-2])
        d = dvalue()
        d = dvalue()
        c.drawString(155, d, "HSNCODE :  " + hsncode[-2])
        d = dvalue()
        d = dvalue()
        c.drawString(155, d, "COUNTRY OF ORIGIN:  " + str(countryofOrigin[-2]).upper())
        # c.line(400, 115, 580, 115)
        c.drawString(490, 118, "<--Total ")
        c.drawAlignedString(405, 118, str(packages))
        c.drawAlignedString(465, 118, str('{0:1.3f}'.format(quantity)))
        c.drawAlignedString(560, 110, str('{0:1.4f}'.format(amount)))
        # shiping marks
        c.drawString(85, 420, str('{0:1.3f}'.format(grosswt)))
        c.drawString(85, 410, str('{0:1.3f}'.format(netwt)))
        c.drawString(85, 390, str((packages)))
        c.drawAlignedString(175, 450, str(packages))  # No Of Cartons
        # Amounts in words
        str1 = str(num2words(str('{0:1.4f}'.format(amount)), lang='en', to='currency', separator=' and',
                             cents=True, currency=str(currency[-2]).strip())).replace(',','')
        wrap(str(currency[-2]).strip() + ' ' + str1, c.drawString, 55, 140, 117)
        # ************************************************ExminationReport
        c.showPage()
        ExminationReport(Goods, D, sr)
        c.drawString(170, 665, ': ' + invoiceno[-2])
        c.drawString(170, Y, ': ' + str(grosswt))
        c.drawString(170, Y - 10, ': ' + str(netwt))
        c.drawString(170, Y - 20, ': ' + str(packages))
        NewRequest()
        sr = SetSerialNo()
        D = updateDvalue()
        TotalClean()
        # ***************************************
        c.setPageSize(portrait(A4))
        c.showPage()
        d = newpage()
        d = dvalue()
        header(divisioncode, result)
        c.drawString(140, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)
        # Newappend(result)
