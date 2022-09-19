from babel.numbers import format_currency
from reportlab.graphics.barcode import qr
from reportlab.lib.pagesizes import landscape, A4,A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import textwrap
from Global_Files import Connection_String as con
from Global_Files import AmmountINWords as amounttoword

import os.path
import zxing
import pyqrcode
import png
from PIL import Image

from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
#####################################################
# Author : Tejas Goswami
# Date : July-2021
#
#####################################################
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialItalic', 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBoldItalic', 'arialbi.ttf'))
c=canvas.Canvas("1.pdf")
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
printleft=200
printright=200
limit=110
# d = 720
# d = 700
t = 160
x = 200
totalnoofchallan=0
challancounter=0

no=0
divisioncode=[]
party=[]
item=[]
challanno=[]
invoiceno=[]
ShadeCode=[]
roundoff=[]
Lotno=[]
boxno=[]
remark=[]
unit=''
BoxesTotal=0
Grosswt=0
Tarewt=0
Netwt=0
Amount=0
NetAmount=0
Copswt=0
BoxCounter=0
totaltaxablevalue=0
totalmainGrosswt=0
totalmainNetwt=0
totalmainTarewt=0
totalmainCopswt=0
GTotalweight=0
Gbasicinvoicevalue=0
gexchangerate=0
pageno=1
pan=''
counter=0
# Particulardvalue=0
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

def fontsltalic(size):
    global c
    c.setFont("ArialItalic", size)
#
# def fontsbold(size):
#     global c
#     c.setFont("MyOwnArialBoldItalic", size)

def dvalue():
    global d
    if d > 20:
        d = d - 10
    return d
def xvalue():
    global x
    if x > 20:
        x = x - 10
    return x
# def dvalue(result, divisioncode):
#     global d
#     if d > 20:
#         d = d - 10
#         return d
#     else:
#         d = newpage()
#         c.showPage()
#         header(result, divisioncode[:-1])
#         return d
def dvaluegst():
    global d
    d = d + 10
    return d




def logic(result):
    # divisioncode.append(result['UNIT'])
    divisioncode.append(result['COMPANYNAME'])
    challanno.append(result['CHALLANNUMBER'])
    invoiceno.append(result['INVOICENO'])
    roundoff.append(result['ROUNDOFFVALUE'])
    # ShadeCode.append(result['SHADECODE'])
    # Lotno.append(result['LOTNO'])
    # boxno.append(result['BOXNO'])

def dlocvalue(d):
    d=d-20
    return d
# def newpage(c,result):
def newpage():
    global d
    d = 330
    # border(c,c,result)
    return d
def newrequest():
    global divisioncode
    global pageno
    global challanno
    global invoiceno
    global no
    global boxno
    global ShadeCode
    global Lotno
    global printleft
    global printright
    global x
    global limit
    global d
    no=0
    printleft = 200
    printright = 200
    limit = 110
    # d = 200
    d = 516
    x = 210
    divisioncode=[]
    pageno=1
    challanno=[]
    invoiceno=[]
    boxno=[]
    ShadeCode=[]
    Lotno=[]

def companyclean():
    global BoxesTotal
    global WeightTotal
    BoxesTotal = 0
    WeightTotal = 0

def textsize(c,result):
    global  GTotalweight
    # print(" from taxt size")
    fonts(9)
    logic(result)
    global d
    global pageno
    global Particulardvalue
    global t
    # print(result['CHALLANNUMBER'])
    if len(invoiceno) == 1:
        border(c,result)
        header(result)
        printparticular(result,"")
        Particulardvalue=d
        # t=d
        d=dvalue()
        printchallandetails(result)
        print("after if "+str(Particulardvalue))
    elif invoiceno[-1] == invoiceno[-2]:
        # d=dvalue()
        if challanno[-1] != challanno[-2]:
            printchallandetails(result)
        else:
            # c.drawAlignedString(425, t+20, str(float("%.3f" % float(GTotalweight))))
            # t=0
            GTotalweight=0
            str()
            printparticular(result,"")
            Particulardvalue = d
            # t=d
            d=dvalue()
            printchallandetails(result)

    elif invoiceno[-1]!= invoiceno[-2]:
        # print("from invoice numner not equal")
        # c.drawAlignedString(425, t+20, str(float("%.3f" % float(GTotalweight))))
        t=0
        GTotalweight=0
        pageno=0

        printtotalmain()
        getandprintFOBdeatils(invoiceno[-2])
        printInvoiceBasicValue(Gbasicinvoicevalue, d-10)
        printinvoicevalueinwords()
        # getandprinttaxdeatils(invoiceno[-2],roundoff[-2],result['EXPORTERREFERANCENO'],result['BUYERSPOREFNO'])
        if result['INVOICETYPE'] !='2':
            getretunableitemdeails(invoiceno[-2])
        # getretunableitemdeails('GSD0000021')
        c.showPage()
        p = page()
        fonts(9)
        border(c,result)
        header(result)
        d = 516
        printparticular(result,"")
        Particulardvalue = d
        # t=d
        d=dvalue()
        printchallandetails(result)
        # c.drawAlignedString(425, t+20, str(float("%.3f" % float(GTotalweight))))
        t=0

        # c.drawAlignedString(425, t, str(float("%.3f" % float(GTotalweight))))
        # t = 0

    print(result['LUT'])
    # print("after particular from 3")


def printlasttotal():
    global t
    # c.drawAlignedString(425, t, str(float("%.3f" % float(GTotalweight))))
    t = 0


def header(result):
    self = None
    global unit
    global Ginvoiceamount
    fonts(15)
    # c.drawImage("/WORKING.PNG",400,800)
    if (result['DIVISIONCODE'])=='101':
        c.drawImage( "Static/be_Bklon_Image.png", 510,745, width=50,height=50)
    else:
        c.drawImage( "Static/Bluechip.png", 510,745, width=50,height=50)
    c.drawCentredString(305, 800, result['COMPANYNAME'])
    fonts(8)
    c.drawCentredString(300, 785, "Works : "+result['PLANTADDRESS'])
    c.drawCentredString(300, 770, "Regd. Office : "+result['REGD_ADDRESS'])
    c.drawCentredString(300, 755, "Corp. Office : "+result['CORP_ADDRESS'])
    c.drawCentredString(300, 745, "Tel : 000000. Fax : 000000000")
    c.drawCentredString(300, 735, "Web site : "+str(result['COMPANYWEBURL'])+", Email id : "+str(result['COMPANYEMAIL']))

    fonts(9)
    c.drawString(25, 725, "GSTIN  : " +str(result['COMPANYGSTINNO']) )
    c.drawString(430, 725, "PAN  : "+str(result['COMPANYPANNO']) )
    c.drawString(430, 715, "CIN  : "+str(result['CINNO']) )
    c.drawString(25, 683, "NAME & ADDRES OF BUYER : " )
    c.drawString(410, 683, "NUMBER  ")
    c.drawString(520, 683, "DATE " )
    # fonts(11)
    fonts(9)
    c.drawString(25, 663, ("Buyer  : " +str( result['CUSTOMER'])))
    customeraddress=result['CUSTOMERADDRESS']
    ca=650
    if len(str(customeraddress))>50:
        lines = textwrap.wrap(str(customeraddress), 50, break_long_words=False)
        for i in lines:
            c.drawString(25, ca, str(i))
            ca=ca-12

    # c.drawString(25, 610, "GSTIN :  "+str(result['CUSTOMERGST']))
    c.drawString(25, ca-12, "GSTIN :  "+str(result['CUSTOMERGST']))
    c.drawString(180, ca-12, "PAN No. :  "+str(result['CUSTOMERPAN']))

    c.drawString(25, ca-24, "PLACE OF SUPPLY: "+str(result['GSTSTATECODE'])+" - "+str(result['GSTSTATE']))
    c.drawString(25, ca-35, "CONSIGNEE : " + str(result['CONSIGNEENAME']))
    # ca = 575
    ca = ca-45
    consigeeaddress = result['CONSIGNEEADDRESS']
    # ca = ca-24
    if len(str(consigeeaddress)) > 30:
        lines = textwrap.wrap(str(consigeeaddress), 30, break_long_words=False)                    #  check for the over lapping address  and add signed in qr code and note
        for i in lines:
            c.drawString(25, ca, str(i))
            ca = ca - 12
    else:
        c.drawString(25, ca, result['CONSIGNEEADDRESS'])

    c.drawString(310, 665, "GST INV.")
    c.drawString(400, 665, result['INVOICENO'])
    c.drawString(310, 655, "VEHICLE NO.")
    c.drawString(400, 655, str(result['TRUCKNO']))
    c.drawString(490, 665, result['INVOICEDATE'])
    # c.drawString(310, 635, "LR No.")
    # c.drawString(400, 635, result['LRNO'])
    # c.drawString(510, 635, result['LRDATE'] )
    c.drawString(310, 645, "LR No.")
    c.drawString(400, 645, result['LRNO'])
    c.drawString(490, 645, result['LRDATE'])

    c.drawString(310, 635, "EWAY BILL")
    ewaydetails = result['EWAYBILL']
    ewaybilldate = result['EWAYBILLDATE']
    c.drawString(400, 635, str(ewaydetails).strip())
    c.drawString(490, 635, str(ewaybilldate))

    c.drawString(310, 622, "MODE OF TRANSPORT")
    c.drawString(490, 622, str(result['SUPPLYMODE']))
    c.drawString(310, 610, "DATE & TIME OF SUPPLY")
    # c.drawString(500, 610, str(result['DATEOFREMOVALOFGOODS']))
    supplydate = str(result['DATEOFREMOVALOFGOODS'])
    # if len(str(supplydate)) > 10:
    #     ca = 611
    #     lines = textwrap.wrap(str(supplydate), 10, break_long_words=True)
    #     for i in lines:
    #         c.drawString(500, ca, str(i))
    #         ca=ca-9
    supplydate = str(result['INVOICEISSUEDATE'])
    supplytime = str(result['DATEOFREMOVALOFGOODS'])
    c.drawString(490, 610, str(supplydate) + " " + str(supplytime[11:22]))

    c.drawString(310, 593, "DISPATCH FROM")
    c.drawString(390, 593, ": " + str(result['DESPFROM']))
    c.drawString(310, 582, "DISPATCH TO")
    c.drawString(390, 582, ": " + str(result['DESPTO']))
    c.drawString(310, 572, "TRANSPORT          :")
    transportname = str(result['TRANSPORTERNAME'])
    c.drawString(395, 573, transportname[0:33])
    c.drawString(310, 562, "BROKER")
    c.drawString(390, 562, ": " + str(result['BROKERNAME']))
    # c.drawString(310, 550, "REF")
    # c.drawString(390, 550, ": "+str(result['REFERANCECODE']))
    # ewaydetails = result['EWAYBILL']
    # ewaybilldate = result['EWAYBILLDATE']
    # # print(ewaybilldate)
    # # print(result['EWAYBILLDATE'])
    # c.drawString(310, 560, "EWAY BILL No.")
    # c.drawString(390, 560,": "+ str(ewaydetails).strip() )
    # c.drawString(310, 549, "EWAY BILL  DATE")
    # c.drawString(390, 549,": "+str(ewaybilldate))

    # c.drawAlignedString(555, 375, str(float("%.3f" % float(result['INVOICEAMT']))))
    c.drawAlignedString(555, 275, str(format_currency("%.2f" % float(result['INVOICEAMT']), '', locale='en_IN')))

    # c.drawAlignedString(555, 275, str(("%.2f" % float(result['INVOICEAMT']))))
    Ginvoiceamount = result['INVOICEAMT']

    # c.drawAlignedString(555, 375, str(float("%.3f" % float(result['INVOICEAMT']))))
    # c.drawAlignedString(555, 275, str(("%.2f" % float(result['INVOICEAMT']))))
    # inwords = amounttoword.inwords(str(float("%.2f" % float(result['INVOICEAMT']))))
    # if len(str(inwords)) > 70:
    #     ca=265
    #     lines = textwrap.wrap(str(inwords), 70, break_long_words=False)
    #     for i in lines:
    #         c.drawString(25, ca, str(i))
    #         # c.drawString(25, ca, inwords)
    #         ca = ca - 10
    # else:
    #     # pass
    #     c.drawString(25, 260, inwords)
    # fonts(11)
    c.drawCentredString(450, 135, str("For " + result['COMPANYNAME']))
    # fonts(9)

    # generateQR_Code(result)  2

def border(c, result):
    global Gbasicinvoicevalue
    c.setFillColorRGB(0, 0, 0)
    # Box For Whole page
    fonts(7)
    c.line(20, 820, 580, 820)  # first horizontal line
    c.drawString(260, 813, "Subject to Silvassa Jurisdiction.")
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.line(20, 820, 20, 20)  # first vertical line
    c.line(580, 820, 580, 20)  # right vertical border  line
    fonts(12)
    c.drawCentredString(310, 700, "TAX INVOICE")
    # c.drawString(545,355,"Page no : "+page())
    c.line(20, 695, 580, 695)  # second horizontal line
    c.line(20, 675, 580, 675)  # third horizontal line
    fonts(8)
    c.line(305, 695, 305, 545)  # --- vertical line after address
    c.line(390, 695, 390, 633)  # --- verical line before challan number
    c.line(305, 632, 580, 632)  # --- horizantal line after EWAY BILL no
    c.line(485, 695, 485, 605)  # --- vertical line before date AND TIME Details
    c.line(305, 605, 580, 605)  # --- horizantal line after Date and time  of supply
    # c.line(675, 675, 260, 675)  # center vertical line  short line for address and header deatils  |
    c.line(20, 545, 580,545)  # line after Ref  horizontal line
    # c.drawString(30, 536, "CHALLAN No.")
    c.drawString(25, 536, "Item Description")
    c.drawString(310, 536, "HSN Code")
    c.drawString(370, 536, "INVOICE BOXES")
    # c.drawString(400, 536, "QUANITIY")
    # c.drawString(440, 536, "UOM")
    c.drawString(480, 536, "RATE")
    c.drawString(530, 536, "Amount (Rs)")
    c.drawString(25, 526, "CHALLAN No.")
    c.drawString(85, 526, "REFERANCE No.")
    c.drawString(150, 526, "Buyer Ref No.")
    c.drawString(250, 526, "LOT No.")
    c.drawString(310, 526, "SHADE CODE")
    c.drawString(370, 526, "CHALLAN BOX")
    c.drawString(435, 526, "QTY")
    c.line(20, 521, 580, 521)  # fourth horizontal line

    c.line(20, 285, 580, 285)  # horizontal line before bank deatils
    # c.drawString(25, 275, "INVOICE VALUE IN WORDS :")
    # c.drawString(350, 275, "TOTAL INVOICE VALUE : ")
    c.line(20, 250, 580, 250)  # horizontal line before bank deatils
    c.drawString(120, 240, "TAX PAYABLE ON REVERSE CHARGE : NO ")
    # c.drawString(25, 290, "Invoice Remarks : "+str(result['PLANTINVOICEREMARKS']))  1

    c.drawString(300, 240, "Returnables : ")
    c.drawString(100, 170, "LUT : ")
    LUT = result['LUT']
    ca = 170
    if len(str(LUT)) > 50:
        lines = textwrap.wrap(str(LUT), 50, break_long_words=False)
        for i in lines:
            c.drawString(120, ca, str(i))
            ca = ca - 12

    # printbankandtaxdetails(result)
    printFOBValues(result)
    Gbasicinvoicevalue=result['BASICVALUE']
    printmessage()
    c.line(20, 145, 580, 145)  # fifth horizontal line

    c.line(305, 145, 305, 65)  # --- vertical line after address
    printsignature()
    c.line(20, 65, 580, 65)
    printnotice(40, result)
    c.line(20, 20, 580, 20)  # last vertical line

def printparticular(result,MSG):
    # d=516
    global d
    global Amount
    global totaltaxablevalue
    # if challanno[-1]!= challanno[-2]:
    d=d-5
    PRODUCT=result['PRODUCT']
    if len(str(PRODUCT)) > 60:
        ca=d
        lines = textwrap.wrap(str(PRODUCT), 60, break_long_words=False)
        for i in lines:
            # c.drawString(90, ca, str(i))
            c.drawString(25, ca, str(i))
            ca = ca - 10
    else:
        c.drawString(22, d, result['PRODUCT'])
    c.drawString(310,d, result['HSNCODE'])
    # c.drawString(330, d-10, result['SHADECODE'])
    # c.drawString(270, d-10, result['LOTNUMBER'])
    c.drawString(270, d, MSG)
    c.drawString(400, d, str(result['DIRECT_BOXES']))
    # getItemRateAndItemAmount(result['INVOICENO'])
    # c.drawAlignedString(425, d, str(invoiceqty))
    # c.drawString(450, d, result['UOM'])
    # c.drawAlignedString(495, d, str(("%.2f" % float(result['INVRATE']))))
    invoiceqty = str("%.3f" % float(result['QUANTITY']))
    c.drawAlignedString(438, d, invoiceqty + ' ' + str(result['UOM']))
    c.drawAlignedString(495, d, str(format_currency("%.2f" % float(result['INVRATE']), '', locale='en_IN')))
    # c.drawAlignedString(555, d, str(("%.2f" % float(result['ITEMAMOUNT']))))
    c.drawAlignedString(560, d, str(format_currency("%.2f" % float(result['ITEMAMOUNT']), '', locale='en_IN')))
    Amount = Amount + float("%.2f" % float(result['ITEMAMOUNT']))
    totaltaxablevalue = totaltaxablevalue + float("%.2f" % float(result['ITEMAMOUNT']))
    # c.drawAlignedString(425, d, str("%.3f" % float(result['TOTALQUANTITY'])))
    # customeraddress = result['CONSIGNEEADDRESS']
    # ca = 650
    # if len(str(customeraddress)) > 30:
    #     lines = textwrap.wrap(str(customeraddress), 30, break_long_words=False)
    #     for i in lines:
    #         c.drawString(25, ca, str(i))
    #         ca = ca - 12
    # c.drawString(25, d-10, result['CHALLANNUMBER'])
    # c.drawString(90, d-10, result['CHALLANQUANTITY']+' '+result['CHALLANUOM'])
    # c.drawString(195, d - 10, result['REFERANCECODE'])
    # total(result)
    # elif challanno[-1]== challanno[-2]:

def printchallandetails(result):
    global GTotalweight
    global d
    fontsltalic(9)
    # printlotnumber(result)
    # GTotalweight=    GTotalweight+float("%.3f" % float(result['CHALLANQUANTITY']))
    c.drawString(25, d -2, result['CHALLANNUMBER'])
    c.drawString(90, d - 2, result['REFERANCECODE'])
    c.drawString(150, d - 2, str(result['OURREFERANCEVALUE']))
    c.drawString(250, d - 2, str(result['LOTNUMBER']))
    shadecode = result['SHADECODE']
    c.drawString(310,d-2,shadecode[0:16])
    # c.drawString(328,d-10,shadecode[13:32])
    # ca = d-2
    # if len(str(shadecode)) > 10:
    #     lines = textwrap.wrap(str(shadecode), 10, break_long_words=False)
    #     print("line : ----- "+str(lines))
    #     for i in lines:
    #         c.drawString(330, ca, str(i))
    #         ca = ca - 10
    # c.drawString(330, d-2, result['SHADECODE'])
    # c.drawString(300, d-2, str(result['BUYERREFFERANCEVALUE']))
    # c.drawString(400, d - 2, str(result['TOTALCHALLANINBOX']))
    getandprintchallanbox(result['INVOICENO'],result['CHALLANNUMBER'])
    # c.drawAlignedString(495, d, str(format_currency("%.2f" % float(result['CHALLANPRICE']), '', locale='en_IN')))
    # c.drawString(555, d - 2, "amount")CHALLANNETVALUE
    # c.drawAlignedString(555, d, str(format_currency("%.2f" % float(result['CHALLANNETVALUE']), '', locale='en_IN')))
    challanqty=str("%.3f" % float(result['CHALLANQUANTITY']))
    c.drawAlignedString(438, d-2, challanqty + ' ' +str(result['CHALLANUOM']))
    fonts(9)
    # ewaydetails=result['EWAYBILL']
    # ewaybilldate=result['EWAYBILLDATE']
    # c.drawString(90, d - 12, str(ewaydetails).strip()+"        "+str(ewaybilldate))
    # getItemRateAndItemAmount(result['INVOICENO'])
    # d=dvalue()
    # c.drawString(160, d-2, result['REFERANCECODE'])

    # c.drawString(255, d-2, str(result['BUYERREFFERANCEVALUE']))
    # c.drawString(330, d-2, result['SHADECODE'])
    # c.drawString(270, d-2 , result['LOTNUMBER'])
# def printparticular(result,MSG):
#     # d=516
#     global d
#     global t
#     # if challanno[-1]!= challanno[-2]:
#     d=d-5
#     t=d
#     c.drawString(270,d, result['HSNCODE'])
#     # c.drawString(330, d-10, result['SHADECODE'])
#     # c.drawString(270, d-10, result['LOTNUMBER'])
#     c.drawString(270, d, MSG)
#     c.drawString(350, d, str(result['DIRECT_BOXES']))
#     # invoiceqty = str(float("%.3f" % float(result['QUANTITY'])))
#     # c.drawAlignedString(425, d, str(float("%.3f" % float(result['QUANTITY']))))
#     # c.drawAlignedString(425, d, str(invoiceqty))
#     c.drawString(450, d, result['UOM'])
#     c.drawAlignedString(495, d, str(("%.2f" % float(result['INVRATE']))))
#     c.drawAlignedString(555, d, str(("%.2f" % float(result['ITEMAMOUNT']))))
#     # customeraddress = result['CONSIGNEEADDRESS']
#     # ca = 650
#     # if len(str(customeraddress)) > 30:
#     #     lines = textwrap.wrap(str(customeraddress), 30, break_long_words=False)
#     #     for i in lines:
#     #         c.drawString(25, ca, str(i))
#     #         ca = ca - 12
#     # c.drawString(25, d-10, result['CHALLANNUMBER'])
#     # c.drawString(90, d-10, result['CHALLANQUANTITY']+' '+result['CHALLANUOM'])
#     # c.drawString(195, d - 10, result['REFERANCECODE'])
#     PRODUCT = result['PRODUCT']
#     if len(str(PRODUCT)) > 50:
#         ca = d
#         lines = textwrap.wrap(str(PRODUCT), 50, break_long_words=False)
#         for i in lines:
#             # c.drawString(90, ca, str(i))
#             c.drawString(25, ca, str(i))
#             ca = ca - 10
#         d = dvalue()
#     else:
#         c.drawString(25, d, result['PRODUCT'])
#     total(result)
#     # elif challanno[-1]== challanno[-2]:
#
# def printchallandetails(result):
#     global GTotalweight
#     # printlotnumber(result)
#     GTotalweight=    GTotalweight+float("%.3f" % float(result['CHALLANQUANTITY']))
#     c.drawString(25, d -2, result['CHALLANNUMBER'])
#     challanqty=str(float("%.3f" % float(result['CHALLANQUANTITY'])))
#     c.drawAlignedString(130, d-2, challanqty + ' ' +str(result['CHALLANUOM']))
#     c.drawString(195, d-2, result['REFERANCECODE'])
#     c.drawString(330, d-2, result['SHADECODE'])
#     c.drawString(270, d-2 , result['LOTNUMBER'])
def printInvoiceBasicValue(BASICVALUE,p):
    c.drawString(400, p, "Total Basic Value : ")
    c.drawAlignedString(560, p, str(format_currency("%.2f" % float(BASICVALUE), '', locale='en_IN')))

def getItemRateAndItemAmount(invoicenumber):
    global Amount
    global totaltaxablevalue
    itemrate=0
    itemamount=0
    sqlitemrate = " Select calculatedvalue, IndTaxDetail.* " \
        " From plantinvoiceline, IndTaxDetail " \
        " JOIN PLANTINVOICE ON PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
        " Where plantinvoiceline.plantinvoicecode = '"+invoicenumber +"' " \
        "  AND    indtaxdetail.AbsUniqueID = Plantinvoiceline.AbsUniqueID " \
        " And    indtaxdetail.ITaxCOde In ('INR','DNV') " \
        " And    indtaxdetail.TaxCategoryCode = 'OTH' "
    print(sqlitemrate)
    stmt = con.db.prepare(con.conn, sqlitemrate)
    con.db.execute(stmt)
    resultitemrate = con.db.fetch_both(stmt)
    if resultitemrate != False:
        while resultitemrate != False:
            itemrate = float(resultitemrate['CALCULATEDVALUE'])
            # p = p - 10
            resultitemrate = con.db.fetch_both(stmt)
    c.drawAlignedString(495, d, str(format_currency("%.2f" % float(itemrate), '', locale='en_IN')))
    resultitemrate=''
    itemrate=''

    sqlitemamount=" Select calculatedvalue, IndTaxDetail.* " \
        " From plantinvoiceline, IndTaxDetail " \
        " JOIN PLANTINVOICE ON PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
        " Where plantinvoiceline.plantinvoicecode='"+invoicenumber+"' " \
        " AND    indtaxdetail.AbsUniqueID = Plantinvoiceline.AbsUniqueID " \
        " And    indtaxdetail.ITaxCOde In ('998','PPU') " \
        " And    indtaxdetail.TaxCategoryCode = 'OTH' "
    print(sqlitemamount)
    stmt = con.db.prepare(con.conn, sqlitemamount)
    con.db.execute(stmt)
    resultitemamount = con.db.fetch_both(stmt)
    if resultitemamount != False:
        while resultitemamount != False:
            itemamount = float(resultitemamount['CALCULATEDVALUE'])
            # p = p - 10
            resultitemamount = con.db.fetch_both(stmt)
    c.drawAlignedString(560, d, str(format_currency("%.2f" % float(itemamount), '', locale='en_IN')))
    resultitemrate=''
    itemrate=''
    # total(resultitemamount)
    print(itemamount)
    Amount = Amount + float("%.2f" % float(itemamount))
    totaltaxablevalue=totaltaxablevalue+float("%.2f" % float(itemamount))

def printbankandtaxdetails(result):
    c.drawString(120, 200, "IRN : ")
    irnvalue = result['IRNVALUE']
    irn = 200
    if len(str(irnvalue)) > 30:
        print("in irn if")
        lines = textwrap.wrap(str(irnvalue), 30, break_long_words=True)
        for i in lines:
            c.drawString(150, irn, str(i))
            irn = irn - 10
    else:
        print("in irn else")
    c.drawString(310, 180, "BANK NAME ")
    c.drawString(370, 180, ": "+str(result['BANKNAME']))
    c.drawString(310, 170, "BANK BRANCH")
    c.drawString(370, 170, ": "+str(result['BRANCHNAME']))
    c.drawString(310, 160, "ACCOUNT No.")
    c.drawString(370, 160, ": "+str(result['ACCOUNTNUMBER']))
    c.drawString(310, 150, "IFC Code")
    c.drawString(370, 150, ": "+str(result['BANKIFSCCODE']))

def printFOBValues(result):
    global gexchangerate
    c.drawString(310, 200, "Currency                      :")
    c.drawAlignedString(575, 200, ": " + str(result['ORDERCURRENCYCODE']))
    c.drawString(310, 190, "Exchange Rate (INR)  :")
    c.drawAlignedString(560, 190, str(format_currency("%.2f" % float(result['EXCHANGERATEOFCONTRACT']), '', locale='en_US')))
    gexchangerate=result['EXCHANGERATEOFCONTRACT']
    # print(gexchangerate)
    # c.drawAlignedString(560, 190, ": " + str(result['EXCHANGERATEOFCONTRACT']))
    c.drawString(310, 180, "FOB Value ")
    # c.drawAlignedString(575, 180, ": " + str(result['ACCOUNTNUMBER']))
    c.drawString(310, 170, "FREIGHT")
    # c.drawAlignedString(575, 170, ": " + str(result['BANKIFSCCODE']))
    c.drawString(310, 160, "Insurance")
    # c.drawAlignedString(575, 160, ": " + str(result['BANKIFSCCODE']))
    c.drawString(310, 150, "Total Value in ")
    # c.drawAlignedString(575, 150, ": " + str(result['BANKIFSCCODE']))


def printlotnumber(result):
    invoiceno=result['INVOICENO']
    sqllotnumber="Select  COALESCE(ValueString, LotNo.LotCode) As LotNo " \
        "From StockTransaction LotNo " \
        "Join    Lot             On      LotNo.LotCode = Lot.Code " \
        "left join adstorage     on Lot.AbsUniqueId = adstorage.UniqueId " \
        "						And AdStorage.FieldName = 'SaleLot' " \
        "JOIN SALESDOCUMENTLINE  ON LOTNO.ORDERCODE = SALESDOCUMENTLINE.PREVIOUSCODE  " \
        "JOIN SALESDOCUMENT 	    ON  SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE  " \
        "						AND SALESDOCUMENT.DocumentTypeType = '06' " \
        "JOIN PLANTINVOICE  		ON  SALESDOCUMENT.PROVISIONALCODE=PLANTINVOICE.CODE    " \
        "Where LotNo.TemplateCode = 'S04' and LotNo.TRANSACTIONDETAILNUMBER=1  " \
        "						AND LOTNO.ORDERCODE=SALESDOCUMENTLINE.PREVIOUSCODE " \
        "						AND PLANTINVOICE.CODE='"+invoiceno +"'" \
        "order by ordercode LIMIT 1 "
    stmt = con.db.prepare(con.conn, sqllotnumber)
    con.db.execute(stmt)
    resultlotno = con.db.fetch_both(stmt)
    if resultlotno != False:
        while resultlotno != False:
            c.drawString(280, d, resultlotno['LOTNO'])
            # p = p - 10
            resultlotno= con.db.fetch_both(stmt)

    # c.drawString(400, p, "Total Taxable Value : ")
    # c.drawAlignedString(555, p, str(float("%.2f" % float(totaltaxablevalue))))

def printsignature():
    fonts(11)
    # c.drawCentredString(450, 190, +str())
    fonts(9)
    c.drawString(35, 70, "This is Computer Generated Invoice, does not require Signature.")
    c.drawCentredString(450, 70, "Authorised Signatory")

def printmessage():

    fonts(7)
    # messsge="The above Goods are sold as per the Rule & Reguataions of The Bombay Yarn Merchants Association & Exchange Ltd. If any dispute arise  about this transaction, the same shall have to be referred to THE  BOMBAY YARN MERCHANTS ASSOCIATION & EXCHANGE LTD, Mumbai for  decision  under its arbitration rules & regulation and award made there under shall be binding upon the parties & Subject to Mumbai Jurisdication Only."
    # if len(str(messsge)) > 64:
        # t = 200
        # lines = textwrap.wrap(str(messsge), 64, break_long_words=False)
        # for i in lines:
        #     c.drawString(25, t, str(i))
        #     t = t - 10
    global t
    t=160
    c.drawString(25,135,"The  above  Goods are  sold  as  per the  Rule  &  Reguataions of  The  Bombay  Yarn " )
    c.drawString(25, 125,"Marchants Association & Exchange Ltd. If any dispute arise about this transaction, the  " )
    c.drawString(25, 115,"same shall  have to be  referred to " )
    boldfonts(7)
    c.drawString(132, 115,"THE BOMBAY YARN MERCHANTS  ASSOCIATION " )
    c.drawString(23, 105," & EXCHANGE LTD," )
    fonts(7)
    c.drawString(90, 105,"Mumbai  for decision  under its  arbitration  rules &  regulation  and " )
    c.drawString(25, 95,"award  made  there  under  shall  be  binding  upon  the  parties  &  Subject  to  Mumbai " )
    c.drawString(25, 85,"Jurisdication Only." )

def printnotice(d,result):
    fonts(7)
    note = "CAUTION : Any complaint regarding the quality and weight to Crimped /Texturised /Twisted / Dyed yarn must be made within eight days after the reciept pf the gpps. The Complaints received thereafter will not be entertained. our responsibilty regarding the Quality of yarn ceases, once the goods are converted into Cloth."
    if len(str(note)) > 170:
        t = 55
        lines = textwrap.wrap(str(note), 170, break_long_words=False)
        for i in lines:
            c.drawString(25, t, str(i))
            t = t - 10
    c.drawString(25, 35, "N.B.:(1) Bill is to be paid on due date. if the same is not paid on due date,interest will be charged @ 30% p.a. from due date of realisation of your cheque.")
    c.drawString(41, 25, "(2) Certified that the particulars given above are true and correct")

# add Freight Amount
# Insurance Percentage to total and tax also then make final total

def printtotalmain():
    global Amount
    global NetAmount

    # c.drawAlignedString(555, 375, str(float("%.3f" % float(Amount))))

    totalmainGrosswt=0
    totalmainNetwt=0
    totalmainTarewt=0
    totalmainCopswt=0
    BoxCounter=0

def total(result):
    global Amount
    global totaltaxablevalue
    Amount = Amount + float("%.2f" % float(result['ITEMAMOUNT']))
    totaltaxablevalue=totaltaxablevalue+float("%.2f" % float(result['ITEMAMOUNT']))

def printtotalinwords():
    global Amount
    inwords=amounttoword.inwords(Amount)
    # c.drawString(25, 290, inwords)

# def getandprinttaxdeatils(invoicenotax,roundoffvalue):
#     global counter
#     global totaltaxablevalue
#     global Amount
#     global NetAmount
#     global Ginvoiceamount
#     global Gbasicinvoicevalue
#     NetAmount=0
#     invoiceno=invoicenotax
#     roundoffamountvalue=roundoffvalue
#     c.line(20, d-10, 580, d-10)
#     p=d-20
#     # printInvoiceBasicValue(Gbasicinvoicevalue, p)
#     p=d-20
#
#     sqltaxdetails=" Select InvCharges.ChargeName as CHARGENAME ,Sum(InvCharges.ChargeVALUE) as CHARGEVALUE From " \
#     "        ( " \
#     "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
#     "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
#     "                FROM IndTaxDetail " \
#     "                        JOIN PLANTINVOICELINE   ON     INDTAXDETAIL.AbsUniqueID 	= PLANTINVOICELINE.AbsUniqueID  " \
#     "                        JOIN ITax               ON     IndTaxDetail.ITaxCode    	= Itax.Code " \
#     "                WHERE PLANTINVOICELINE.plantinvoicecode 							= '"+invoiceno +"'" \
#     "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
#     "                        AND (ITax.TaxCategoryCode IN('FRT', 'INS') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF')) " \
#     "                group by ITax.LONGDESCRIPTION   " \
#     "        Union " \
#     "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
#     "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE " \
#     "                FROM IndTaxDetail " \
#     "                        JOIN PLANTINVOICE       ON     INDTAXDETAIL.AbsUniqueID       = PLANTINVOICE.AbsUniqueID  " \
#     "                        JOIN ITax               ON     IndTaxDetail.ITaxCode          = Itax.Code " \
#     "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
#     "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
#     "                        AND (ITax.TaxCategoryCode IN('FRT', 'INS') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF')) " \
#     "                group by ITax.LONGDESCRIPTION   " \
#     "        ) As InvCharges " \
#     " Group By InvCharges.ChargeName " \
#     " Order By InvCharges.ChargeName " \
#
#     stmt = con.db.prepare(con.conn, sqltaxdetails)
#     con.db.execute(stmt)
#     resulttax = con.db.fetch_both(stmt)
#     if resulttax != False:
#         while resulttax != False:
#             c.drawString(350, p, resulttax['CHARGENAME'])
#             c.drawAlignedString(555, p, str(("%.2f" % float(resulttax['CHARGEVALUE']))))
#             totaltaxablevalue=totaltaxablevalue+ float(resulttax['CHARGEVALUE'])
#             p=p-10
#             resulttax = con.db.fetch_both(stmt)
#
#     c.drawString(400, p, "Total Taxable Value : ")
#     c.drawAlignedString(555, p, str(float("%.2f" % float(totaltaxablevalue))))
#     # c.drawAlignedString(555, p, str(totaltaxablevalue))
#     p = p - 10
#     # NetAmount=0
#     sqlgsttaxdetail=" Select InvGST.GSTName as CHARGENAME , Sum(InvGST.ChargeVALUE) As ChargeValue From " \
#         "        ( " \
#         "                SELECT ITax.LONGDESCRIPTION  as GSTName " \
#         "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
#         "                FROM IndTaxDetail " \
#         "                        JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID  " \
#         "                        JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code " \
#         "                WHERE PLANTINVOICELINE.plantinvoicecode                         = '"+invoiceno +"'" \
#         "                        And IndTaxDetail.CALCULATEDVALUER                        <> 0 " \
#         "                        AND ITax.TaxCategoryCode IN ('GST') " \
#         "                group by ITax.LONGDESCRIPTION   " \
#         "        Union " \
#         "                SELECT ITax.LONGDESCRIPTION  as GSTName " \
#         "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
#         "                FROM IndTaxDetail " \
#         "                        JOIN PLANTINVOICE ON     INDTAXDETAIL.AbsUniqueID = PLANTINVOICE.AbsUniqueID  " \
#         "                        JOIN ITax       ON       IndTaxDetail.ITaxCode = Itax.Code " \
#         "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
#         "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
#         "                        AND ITax.TaxCategoryCode IN('GST') " \
#         "                group by ITax.LONGDESCRIPTION   " \
#         "        ) As InvGST " \
#         " Group By InvGST.GSTName " \
#         " Order By InvGST.GSTName " \
#
#     stmt = con.db.prepare(con.conn, sqlgsttaxdetail)
#     con.db.execute(stmt)
#     resultgsttax = con.db.fetch_both(stmt)
#     if resultgsttax != False:
#         while resultgsttax != False:
#             counter = counter + 1
#             c.drawString(350, p, resultgsttax['CHARGENAME'])
#             c.drawAlignedString(555, p, str(("%.2f" % float(resultgsttax['CHARGEVALUE']))))
#             p = p - 10
#             NetAmount = totaltaxablevalue + float("%.2f" % float(resultgsttax['CHARGEVALUE']))
#             resultgsttax = con.db.fetch_both(stmt)
#
#     sqlgstroundeddetail = " Select InvROF.ROFName  as CHARGENAME , Sum(InvROF.ChargeVALUE) As ChargeValue From " \
#         "        ( " \
#         "                SELECT ITax.LONGDESCRIPTION  as ROFName " \
#         "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
#         "                FROM IndTaxDetail " \
#         "                        JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID  " \
#         "                        JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code " \
#         "                WHERE PLANTINVOICELINE.plantinvoicecode                         = '"+invoiceno +"'" \
#         "                        And IndTaxDetail.CALCULATEDVALUER                        <> 0 " \
#         "                        AND ITax.TaxCategoryCode IN ('ROF') " \
#         "                group by ITax.LONGDESCRIPTION   " \
#         "        Union " \
#         "                SELECT ITax.LONGDESCRIPTION  as ROFName " \
#         "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
#         "                FROM IndTaxDetail " \
#         "                        JOIN PLANTINVOICE ON     INDTAXDETAIL.AbsUniqueID = PLANTINVOICE.AbsUniqueID  " \
#         "                        JOIN ITax       ON       IndTaxDetail.ITaxCode = Itax.Code " \
#         "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
#         "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
#         "                        AND ITax.TaxCategoryCode IN('ROF') " \
#         "                group by ITax.LONGDESCRIPTION   " \
#         "        ) As InvROF " \
#         " Group By InvROF.ROFName " \
#         " Order By InvROF.ROFName " \
#
#     stmt = con.db.prepare(con.conn, sqlgstroundeddetail)
#     con.db.execute(stmt)
#     resultgstrounded = con.db.fetch_both(stmt)
#     if resultgstrounded != False:
#         while resultgstrounded != False:
#             counter = counter + 1
#             c.drawString(350, p, resulttax['CHARGENAME'])
#             c.drawAlignedString(555, p, str(("%.2f" % float(resulttax['CHARGEVALUE']))))
#             p = p - 10
#             NetAmount = NetAmount + float("%.2f" % float(resultgstrounded['CHARGEVALUE']))
#             resultgstrounded = con.db.fetch_both(stmt)
#     c.drawString(350, p,"Roundoff ")
#     # c.drawAlignedString(555, p, str(float("%.2f" % float(roundoffamountvalue))))
#     c.drawAlignedString(555, p, str(("%.2f" % float(roundoffamountvalue))))
#     NetAmount=0
#     totaltaxablevalue=0
#
#     inwords = amounttoword.inwords(str(float("%.2f" % float(Ginvoiceamount))))
#     if len(str(inwords)) > 70:
#         ca = 265
#         lines = textwrap.wrap(str(inwords), 70, break_long_words=False)
#         for i in lines:
#             c.drawString(25, ca, str(i))
#             # c.drawString(25, ca, inwords)
#             ca = ca - 10
#     else:
#         # pass
#         c.drawString(25, 260, inwords)
#     getUnSignandEsignAndLUT(invoiceno)

def getandprintFOBdeatils(invoicenotax):
    global counter
    global totaltaxablevalue
    global gexchangerate
    global NetAmount
    global Gbasicinvoicevalue
    global Ginvoiceamount
    NetAmount=0
    fobvalue=0
    insvalue=0
    frtvalue=0
    invoiceno=invoicenotax
    # roundoffamountvalue=roundoffvalue
    c.line(20, d, 580, d)
    f=190-10
    # c.drawCentredString(55, p,  EXPORTERREFERANCENO)
    # c.drawCentredString(250, p,  BUYERSPOREFNO)
    # printInvoiceBasicValue(Gbasicinvoicevalue,f)
    # f=f-10
    sqltaxdetails=" Select InvCharges.ChargeName as CHARGENAME ,Sum(InvCharges.ChargeVALUE) as CHARGEVALUE From " \
    "        ( " \
    "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
    "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
    "                FROM IndTaxDetail " \
    "                        JOIN PLANTINVOICELINE   ON     INDTAXDETAIL.AbsUniqueID 	= PLANTINVOICELINE.AbsUniqueID  " \
    "                        JOIN ITax               ON     IndTaxDetail.ITaxCode    	= Itax.Code " \
    "                WHERE PLANTINVOICELINE.plantinvoicecode 							= '"+invoiceno +"'" \
    "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
    "                        AND (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'FB3')" \
    "                        AND ITax.LONGDESCRIPTION='FOB' " \
    "                group by ITax.LONGDESCRIPTION   " \
    "        Union " \
    "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
    "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE " \
    "                FROM IndTaxDetail " \
    "                        JOIN PLANTINVOICE       ON     INDTAXDETAIL.AbsUniqueID       = PLANTINVOICE.AbsUniqueID  " \
    "                        JOIN ITax               ON     IndTaxDetail.ITaxCode          = Itax.Code " \
    "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
    "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
    "                        AND (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'FB3') " \
    "                        AND ITax.LONGDESCRIPTION='FOB' " \
    "                group by ITax.LONGDESCRIPTION   " \
    "        ) As InvCharges " \
    " Group By InvCharges.ChargeName " \
    " Order By InvCharges.ChargeName " \

    stmt = con.db.prepare(con.conn, sqltaxdetails)
    con.db.execute(stmt)
    resulttax = con.db.fetch_both(stmt)
    if resulttax != False:
        while resulttax != False:
            fobvalue=float(resulttax['CHARGEVALUE'])
            # c.drawAlignedString(560, f, str(format_currency("%.2f" % float(fobvalue), '', locale='en_IN')))
            totaltaxablevalue=totaltaxablevalue+ float(resulttax['CHARGEVALUE'])
            resulttax = con.db.fetch_both(stmt)

    f = f - 10
    sqlfobfrtdetails = " Select InvCharges.ChargeName as CHARGENAME ,Sum(InvCharges.ChargeVALUE) as CHARGEVALUE From " \
        "        ( " \
        "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
        "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
        "                FROM IndTaxDetail " \
        "                        JOIN PLANTINVOICELINE   ON     INDTAXDETAIL.AbsUniqueID 	= PLANTINVOICELINE.AbsUniqueID  " \
        "                        JOIN ITax               ON     IndTaxDetail.ITaxCode    	= Itax.Code " \
        "                WHERE PLANTINVOICELINE.plantinvoicecode 							= '" + invoiceno + "'" \
        "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
        "                        AND (ITax.TaxCategoryCode IN('FRT') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF'))" \
        "                group by ITax.LONGDESCRIPTION   " \
        "        Union " \
        "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
        "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE " \
        "                FROM IndTaxDetail " \
        "                        JOIN PLANTINVOICE       ON     INDTAXDETAIL.AbsUniqueID       = PLANTINVOICE.AbsUniqueID  " \
        "                        JOIN ITax               ON     IndTaxDetail.ITaxCode          = Itax.Code " \
        "                WHERE PLANTINVOICE.code = '" + invoiceno + "'" \
        "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
        "                        AND (ITax.TaxCategoryCode IN('FRT') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF'))" \
        "                group by ITax.LONGDESCRIPTION   " \
        "        ) As InvCharges " \
" Group By InvCharges.ChargeName " \
                                                                                                                                                                                          " Order By InvCharges.ChargeName "
    fobfrtstmt = con.db.prepare(con.conn, sqlfobfrtdetails)
    con.db.execute(fobfrtstmt)
    sqlfobfrtdetails = con.db.fetch_both(fobfrtstmt)
    if sqlfobfrtdetails != False:
        while sqlfobfrtdetails != False:
            frtvalue = float(sqlfobfrtdetails['CHARGEVALUE'])
            c.drawAlignedString(560, f, str(format_currency("%.2f" % float(frtvalue), '', locale='en_IN')))
            totaltaxablevalue = totaltaxablevalue + float(sqlfobfrtdetails['CHARGEVALUE'])
            sqlfobfrtdetails = con.db.fetch_both(fobfrtstmt)

    f=f-10
    sqlfobinsetails = " Select InvCharges.ChargeName as CHARGENAME ,Sum(InvCharges.ChargeVALUE) as CHARGEVALUE From " \
            "        ( " \
            "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
            "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
            "                FROM IndTaxDetail " \
            "                        JOIN PLANTINVOICELINE   ON     INDTAXDETAIL.AbsUniqueID 	= PLANTINVOICELINE.AbsUniqueID  " \
            "                        JOIN ITax               ON     IndTaxDetail.ITaxCode    	= Itax.Code " \
            "                WHERE PLANTINVOICELINE.plantinvoicecode 							= '" + invoiceno + "'" \
            "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
            "                        AND (ITax.TaxCategoryCode IN('INS') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF'))  " \
            "                group by ITax.LONGDESCRIPTION   " \
            "        Union " \
            "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
            "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE " \
            "                FROM IndTaxDetail " \
            "                        JOIN PLANTINVOICE       ON     INDTAXDETAIL.AbsUniqueID       = PLANTINVOICE.AbsUniqueID  " \
            "                        JOIN ITax               ON     IndTaxDetail.ITaxCode          = Itax.Code " \
            "                WHERE PLANTINVOICE.code = '" + invoiceno + "'" \
            "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
            "                        AND (ITax.TaxCategoryCode IN('INS') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF')) " \
            "                group by ITax.LONGDESCRIPTION   " \
            "        ) As InvCharges " \
            " Group By InvCharges.ChargeName " \
            " Order By InvCharges.ChargeName "
    fobinsstmt = con.db.prepare(con.conn, sqlfobinsetails)
    con.db.execute(fobinsstmt)
    sqlfobinsetails = con.db.fetch_both(fobinsstmt)
    if sqlfobinsetails != False:
        while sqlfobinsetails != False:
            insvalue = float(sqlfobinsetails['CHARGEVALUE'])
            c.drawAlignedString(560, f, str(format_currency("%.2f" % float(insvalue), '', locale='en_IN')))
            totaltaxablevalue = totaltaxablevalue + float(sqlfobinsetails['CHARGEVALUE'])
            sqlfobinsetails = con.db.fetch_both(fobinsstmt)

    totalexportamountvalue=fobvalue+frtvalue+insvalue
    totalexportamountvalue=float(totalexportamountvalue)/float(gexchangerate)
    fobvalue=float(fobvalue-frtvalue-insvalue)/float(gexchangerate)
    c.drawAlignedString(560, f+20, str(format_currency("%.2f" % float(fobvalue), '', locale='en_IN')))
    c.drawAlignedString(560, 170, str(format_currency("%.2f" % float(frtvalue), '', locale='en_IN')))
    c.drawAlignedString(560, 160, str(format_currency("%.2f" % float(insvalue), '', locale='en_IN')))
    c.drawAlignedString(560, 150, str(format_currency("%.2f" % float(totalexportamountvalue), '', locale='en_IN')))


def getandprinttaxdeatils(invoicenotax,roundoffvalue,EXPORTERREFERANCENO,BUYERSPOREFNO):
    global counter
    global totaltaxablevalue
    global Amount
    global NetAmount
    global Gbasicinvoicevalue
    global Ginvoiceamount
    NetAmount=0
    invoiceno=invoicenotax
    roundoffamountvalue=roundoffvalue
    c.line(20, d, 580, d)
    p=d-10
    c.drawCentredString(55, p,  EXPORTERREFERANCENO)
    c.drawCentredString(250, p,  BUYERSPOREFNO)
    printInvoiceBasicValue(Gbasicinvoicevalue,p)
    p=p-10
    sqltaxdetails=" Select InvCharges.ChargeName as CHARGENAME ,Sum(InvCharges.ChargeVALUE) as CHARGEVALUE From " \
    "        ( " \
    "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
    "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
    "                FROM IndTaxDetail " \
    "                        JOIN PLANTINVOICELINE   ON     INDTAXDETAIL.AbsUniqueID 	= PLANTINVOICELINE.AbsUniqueID  " \
    "                        JOIN ITax               ON     IndTaxDetail.ITaxCode    	= Itax.Code " \
    "                WHERE PLANTINVOICELINE.plantinvoicecode 							= '"+invoiceno +"'" \
    "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
    "                        AND (ITax.TaxCategoryCode IN('FRT', 'INS') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF')) " \
    "                group by ITax.LONGDESCRIPTION   " \
    "        Union " \
    "                SELECT ITax.LONGDESCRIPTION  as ChargeName " \
    "                    , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE " \
    "                FROM IndTaxDetail " \
    "                        JOIN PLANTINVOICE       ON     INDTAXDETAIL.AbsUniqueID       = PLANTINVOICE.AbsUniqueID  " \
    "                        JOIN ITax               ON     IndTaxDetail.ITaxCode          = Itax.Code " \
    "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
    "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
    "                        AND (ITax.TaxCategoryCode IN('FRT', 'INS') Or (ITax.TaxCategoryCode = 'OTH' And Itax.Code = 'GPF')) " \
    "                group by ITax.LONGDESCRIPTION   " \
    "        ) As InvCharges " \
    " Group By InvCharges.ChargeName " \
    " Order By InvCharges.ChargeName " \

    stmt = con.db.prepare(con.conn, sqltaxdetails)
    con.db.execute(stmt)
    resulttax = con.db.fetch_both(stmt)
    if resulttax != False:
        while resulttax != False:
            c.drawString(350, p, resulttax['CHARGENAME'])
            c.drawAlignedString(560, p, str(("%.2f" % float(resulttax['CHARGEVALUE']))))
            totaltaxablevalue=totaltaxablevalue+ float(resulttax['CHARGEVALUE'])
            p=p-10
            resulttax = con.db.fetch_both(stmt)
    # print("FRT tax value for : "+str(invoiceno)+" is "+str(totaltaxablevalue))
    # c.drawString(400, p, "Total Taxable Value : ")
    # # c.drawAlignedString(555, p, str(("%.2f" % float(totaltaxablevalue))))
    # c.drawAlignedString(560, p, str(format_currency("%.2f" % float(totaltaxablevalue), '', locale='en_IN')))
    # c.drawAlignedString(555, p, str(totaltaxablevalue))
    p = p - 10
    # NetAmount=0
    sqlgsttaxdetail=" Select InvGST.GSTName as CHARGENAME , Sum(InvGST.ChargeVALUE) As ChargeValue From " \
        "        ( " \
        "                SELECT ITax.LONGDESCRIPTION  as GSTName " \
        "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
        "                FROM IndTaxDetail " \
        "                        JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID  " \
        "                        JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code " \
        "                WHERE PLANTINVOICELINE.plantinvoicecode                         = '"+invoiceno +"'" \
        "                        And IndTaxDetail.CALCULATEDVALUER                        <> 0 " \
        "                        AND ITax.TaxCategoryCode IN ('IGS','CGS','SGS') " \
        "                group by ITax.LONGDESCRIPTION   " \
        "        Union " \
        "                SELECT ITax.LONGDESCRIPTION  as GSTName " \
        "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
        "                FROM IndTaxDetail " \
        "                        JOIN PLANTINVOICE ON     INDTAXDETAIL.AbsUniqueID = PLANTINVOICE.AbsUniqueID  " \
        "                        JOIN ITax       ON       IndTaxDetail.ITaxCode = Itax.Code " \
        "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
        "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
        "                        AND ITax.TaxCategoryCode IN('IGS','CGS','SGS') " \
        "                group by ITax.LONGDESCRIPTION   " \
        "        ) As InvGST " \
        " Group By InvGST.GSTName " \
        " Order By InvGST.GSTName " \

    stmt = con.db.prepare(con.conn, sqlgsttaxdetail)
    con.db.execute(stmt)
    resultgsttax = con.db.fetch_both(stmt)
    if resultgsttax != False:
        while resultgsttax != False:
            counter = counter + 1
            c.drawString(350, p, resultgsttax['CHARGENAME'])
            # c.drawAlignedString(555, p, str(("%.2f" % float(resultgsttax['CHARGEVALUE']))))
            c.drawAlignedString(560, p, str(format_currency("%.2f" % float(resultgsttax['CHARGEVALUE']), '', locale='en_IN')))

            p = p - 10
            NetAmount = totaltaxablevalue + float("%.2f" % float(resultgsttax['CHARGEVALUE']))
            resultgsttax = con.db.fetch_both(stmt)
    # print("Gst tax value for : "+str(invoiceno)+" is "+str(resultgsttax))

    sqlgsttaxdetail = " Select InvGST.GSTName as CHARGENAME , Sum(InvGST.ChargeVALUE) As ChargeValue From " \
      "        ( " \
      "                SELECT ITax.LONGDESCRIPTION  as GSTName " \
      "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
      "                FROM IndTaxDetail " \
      "                        JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID  " \
      "                        JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code " \
      "                WHERE PLANTINVOICELINE.plantinvoicecode                         = '" + invoiceno + "'" \
      "                        And IndTaxDetail.CALCULATEDVALUER                        <> 0 " \
      "                        AND ITax.TaxCategoryCode IN ('TCS') " \
      "                group by ITax.LONGDESCRIPTION   " \
      "        Union " \
      "                SELECT ITax.LONGDESCRIPTION  as GSTName " \
      "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
      "                FROM IndTaxDetail " \
      "                        JOIN PLANTINVOICE ON     INDTAXDETAIL.AbsUniqueID = PLANTINVOICE.AbsUniqueID  " \
      "                        JOIN ITax       ON       IndTaxDetail.ITaxCode = Itax.Code " \
      "                WHERE PLANTINVOICE.code = '" + invoiceno + "'" \
      "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
      "                        AND ITax.TaxCategoryCode IN('TCS') " \
      "                group by ITax.LONGDESCRIPTION   " \
      "        ) As InvGST " \
      " Group By InvGST.GSTName " \
      " Order By InvGST.GSTName "

    stmt = con.db.prepare(con.conn, sqlgsttaxdetail)
    con.db.execute(stmt)
    resultcsttax = con.db.fetch_both(stmt)
    if resultcsttax != False:
        while resultcsttax != False:
            counter = counter + 1
            c.drawString(350, p, resultcsttax['CHARGENAME'])
            # c.drawAlignedString(555, p, str(("%.2f" % float(resultcsttax['CHARGEVALUE']))))
            c.drawAlignedString(560, p, str(format_currency("%.2f" % float(resultcsttax['CHARGEVALUE']), '', locale='en_IN')))
            p = p - 10
            NetAmount = totaltaxablevalue + float("%.2f" % float(resultcsttax['CHARGEVALUE']))
            resultcsttax = con.db.fetch_both(stmt)
    # print("Gst tax value for : " + str(invoiceno) + " is " + str(resultcsttax))

    sqlgstroundeddetail = " Select InvROF.ROFName  as CHARGENAME , Sum(InvROF.ChargeVALUE) As ChargeValue From " \
        "        ( " \
        "                SELECT ITax.LONGDESCRIPTION  as ROFName " \
        "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
        "                FROM IndTaxDetail " \
        "                        JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID  " \
        "                        JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code " \
        "                WHERE PLANTINVOICELINE.plantinvoicecode                         = '"+invoiceno +"'" \
        "                        And IndTaxDetail.CALCULATEDVALUER                        <> 0 " \
        "                        AND ITax.TaxCategoryCode IN ('ROF') " \
        "                group by ITax.LONGDESCRIPTION   " \
        "        Union " \
        "                SELECT ITax.LONGDESCRIPTION  as ROFName " \
        "                        , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE   " \
        "                FROM IndTaxDetail " \
        "                        JOIN PLANTINVOICE ON     INDTAXDETAIL.AbsUniqueID = PLANTINVOICE.AbsUniqueID  " \
        "                        JOIN ITax       ON       IndTaxDetail.ITaxCode = Itax.Code " \
        "                WHERE PLANTINVOICE.code = '"+invoiceno +"'" \
        "                        And IndTaxDetail.CALCULATEDVALUER <> 0 " \
        "                        AND ITax.TaxCategoryCode IN('ROF') " \
        "                group by ITax.LONGDESCRIPTION   " \
        "        ) As InvROF " \
        " Group By InvROF.ROFName " \
        " Order By InvROF.ROFName " \

    stmt = con.db.prepare(con.conn, sqlgstroundeddetail)
    con.db.execute(stmt)
    resultgstrounded = con.db.fetch_both(stmt)
    if resultgstrounded != False:
        while resultgstrounded != False:
            counter = counter + 1
            c.drawString(350, p, resulttax['CHARGENAME'])
            # c.drawAlignedString(555, p, str(("%.2f" % float(resulttax['CHARGEVALUE']))))
            c.drawAlignedString(560, p, str(format_currency("%.2f" % float(resulttax['CHARGEVALUE']), '', locale='en_IN')))

            p = p - 10
            NetAmount = NetAmount + float("%.2f" % float(resultgstrounded['CHARGEVALUE']))
            resultgstrounded = con.db.fetch_both(stmt)

    # print("net value  value for : "+str(invoiceno)+" is "+str(NetAmount))
    # print("round off amount value value  value for : "+str(invoiceno)+" is "+str(roundoffamountvalue))

    c.drawString(350, p,"Roundoff ")
    # c.drawAlignedString(555, p, str(float("%.2f" % float(roundoffamountvalue))))
    # c.drawAlignedString(555, p, str(("%.2f" % float(roundoffamountvalue))))
    c.drawAlignedString(560, p, str(format_currency("%.2f" % float(roundoffamountvalue), '', locale='en_IN')))
    NetAmount=0
    totaltaxablevalue=0

    c.line(20, 285, 580, 285)  # horizontal line before bank deatils
    # c.drawString(25, 275, "INVOICE VALUE IN WORDS :")
    # c.drawString(350, 275, "TOTAL INVOICE VALUE : ")
    # inwords = amounttoword.inwords(str(float("%.2f" % float(Ginvoiceamount))))
    # if len(str(inwords)) > 70:
    #     ca=265
    #     lines = textwrap.wrap(str(inwords), 70, break_long_words=False)
    #     for i in lines:
    #         c.drawString(25, ca, str(i))
    #         # c.drawString(25, ca, inwords)
    #         ca = ca - 10
    # else:
    #     # pass
    #     c.drawString(25, 260, inwords)
    getUnSignandEsignAndLUT(invoiceno)

def printinvoicevalueinwords():
    global Ginvoiceamount
    c.drawString(25, 275, "INVOICE VALUE IN WORDS :")
    c.drawString(350, 275, "TOTAL INVOICE VALUE : ")
    inwords = amounttoword.inwords(str(float("%.2f" % float(Ginvoiceamount))))
    if len(str(inwords)) > 70:
        ca = 265
        lines = textwrap.wrap(str(inwords), 70, break_long_words=False)
        for i in lines:
            c.drawString(25, ca, str(i))
            # c.drawString(25, ca, inwords)
            ca = ca - 10
    else:
        # pass
        c.drawString(25, 260, inwords)


def getretunableitemdeails(returninvoiceno):
    # '"+rinvoiceno +"'" \
    # print("from get returnable deatils")
    rinvoiceno=returninvoiceno
    # rinvoiceno='GSD0000021'
    # print(rinvoiceno)
    sqlreturanabledeatails=""

    sqlreturanabledeatails="Select " \
        "   PKG.InvNo, " \
        "   PKG.PalletTypeCode, " \
        "   PKG.PalletName, " \
        "   Sum(PKG.PalletQuantity) As PalletQuantity  " \
        "From " \
        "   ( " \
        "      Select " \
        "         PlantInvoice.CODE As InvNo, " \
        "         BKLE.PalletType1Code As PalletTypeCode, " \
        "         UGG.LongDescription As PalletName, " \
        "         BKLE.PalletQuantity1 As PalletQuantity  " \
        "      From " \
        "         PlantInvoice  " \
        "         JOIN " \
        "            SalesDocument SD  " \
        "            ON PlantInvoice.CODE = SD.PROVISIONALCODE  " \
        "            and SD.DocumentTypeType = '06'  " \
        "         JOIN " \
        "            SalesDocumentLine SDL  " \
        "            ON SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE  " \
        "            AND SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE  " \
        "            And SDL.DocumentTypeType = '06'  " \
        "         JOIN " \
        "            StockTransaction ST  " \
        "           ON SDL.PreviousCode = ST.OrderCode  " \
        "            AND ST.TemplateCode = 'S04'  " \
        "            And ST.TransactionDetailNumber =  " \
        "            ( " \
        "               Select " \
        "                  Min(ST1.TransactionDetailNumber) From StockTransaction ST1  " \
        "               Where " \
        "                  ST1.ContainerElementCode = ST.ContainerElementCode " \
        "            ) " \
        "         JOIN " \
        "            BKLElements BKLE  " \
        "            ON ST.CONTAINERELEMENTCODE = BKLE.Code  " \
        "            AND ST.CONTAINERSUBCODE01 = BKLE.SubCodeKey  " \
        "            AND BKLE.ItemTypeCode = 'CNT'  " \
        "         JOIN " \
        "            UserGenericGroup UGG  " \
        "            ON UGG.UserGenericGroupTypeCode = 'PKG'  " \
        "            AND BKLE.PalletType1Code = UGG.Code  " \
        "      Where " \
        "         BKLE.PalletType1Code is Not Null  " \
        "         And PlantInvoice.CODE = '"+rinvoiceno +"'" \
        "      Union " \
        "      Select " \
        "         PlantInvoice.CODE As InvNo, " \
        "         BKLE.PalletType2Code As PalletTypeCode, " \
        "         UGG.LongDescription As PalletName, " \
        "         BKLE.PalletQuantity2 As PalletQuantity  " \
        "      From " \
        "         PlantInvoice  " \
        "         JOIN " \
        "            SalesDocument SD  " \
        "            ON PlantInvoice.CODE = SD.PROVISIONALCODE  " \
        "            and SD.DocumentTypeType = '06'  " \
        "         JOIN " \
        "            SalesDocumentLine SDL  " \
        "            ON SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE  " \
        "            AND SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE  " \
        "            And SDL.DocumentTypeType = '06'  " \
        "         JOIN " \
        "            StockTransaction ST  " \
        "            ON SDL.PreviousCode = ST.OrderCode  " \
        "            AND ST.TemplateCode = 'S04'  " \
        "            And ST.TransactionDetailNumber =  " \
        "            ( " \
        "               Select " \
        "                  Min (ST1.TransactionDetailNumber)  " \
        "               From " \
        "                 StockTransaction ST1  " \
        "               Where " \
        "                  ST1.ContainerElementCode = ST.ContainerElementCode " \
        "            ) " \
        "         JOIN " \
        "            BKLElements BKLE  " \
        "            ON ST.CONTAINERELEMENTCODE = BKLE.Code  " \
        "            AND ST.CONTAINERSUBCODE01 = BKLE.SubCodeKey  " \
        "            AND BKLE.ItemTypeCode = 'CNT'  " \
        "         JOIN " \
        "            UserGenericGroup UGG  " \
        "            ON UGG.UserGenericGroupTypeCode = 'PKG' " \
        "            AND BKLE.PalletType2Code = UGG.Code  " \
        "      Where " \
        "         BKLE.PalletType2Code is Not Null  " \
        "         And PlantInvoice.CODE = '"+rinvoiceno +"'" \
        " Union  " \
        "         Select " \
        "            PlantInvoice.CODE As InvNo, " \
        "            BKLE.PalletType3Code As PalletTypeCode, " \
        "            UGG.LongDescription As PalletName, " \
        "            BKLE.PalletQuantity3 As PalletQuantity  " \
        "         From " \
        "            PlantInvoice  " \
        "            JOIN " \
        "               SalesDocument SD  " \
        "               ON PlantInvoice.CODE = SD.PROVISIONALCODE and SD.DocumentTypeType = '06'  " \
        "            JOIN " \
        "               SalesDocumentLine SDL  " \
        "               ON SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE AND SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE " \
        "               And SDL.DocumentTypeType = '06'  " \
        "            JOIN " \
        "               StockTransaction ST  " \
        "               ON SDL.PreviousCode = ST.OrderCode  " \
        "               AND ST.TemplateCode = 'S04'  " \
        "               And ST.TransactionDetailNumber =  " \
        "               ( " \
        "                  Select " \
        "                     Min(ST1.TransactionDetailNumber)  " \
        "                  From " \
        "                     StockTransaction ST1  " \
        "                  Where " \
        "                     ST1.ContainerElementCode = ST.ContainerElementCode " \
        "               ) " \
        "            JOIN " \
        "               BKLElements BKLE  " \
        "               ON ST.CONTAINERELEMENTCODE = BKLE.Code  " \
        "               AND ST.CONTAINERSUBCODE01 = BKLE.SubCodeKey  " \
        "               AND BKLE.ItemTypeCode = 'CNT'  " \
        "            JOIN " \
        "               UserGenericGroup UGG  " \
        "               ON UGG.UserGenericGroupTypeCode = 'PKG'  " \
        "               AND BKLE.PalletType3Code = UGG.Code  " \
        "         Where " \
        "            BKLE.PalletType3Code is Not Null  " \
        "            And PlantInvoice.CODE = '"+rinvoiceno +"'" \
        "         Union " \
        "         Select " \
        "            PlantInvoice.CODE As InvNo, " \
        "            BKLE.PalletType4Code As PalletTypeCode, " \
        "            UGG.LongDescription As PalletName, " \
        "            BKLE.PalletQuantity4 As PalletQuantity  " \
        "         From " \
        "            PlantInvoice  " \
        "            JOIN " \
        "               SalesDocument SD  " \
        "               ON PlantInvoice.CODE = SD.PROVISIONALCODE  " \
        "               and SD.DocumentTypeType = '06'  " \
        "            JOIN " \
        "               SalesDocumentLine SDL  " \
        "               ON SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE  " \
        "               AND SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE  " \
        "               And SDL.DocumentTypeType = ' 06'  " \
        "			JOIN StockTransaction ST        ON      SDL.PreviousCode      = ST.OrderCode AND     ST.TemplateCode         = 'S04' " \
        "               And ST.TransactionDetailNumber =  " \
        "               ( " \
        "                  Select " \
        "                     Min(ST1.TransactionDetailNumber)  " \
        "                  From " \
        "                     StockTransaction ST1  " \
        "                  Where " \
        "                     ST1.ContainerElementCode = ST.ContainerElementCode " \
        "               ) " \
        "            JOIN " \
        "               BKLElements BKLE " \
        "               ON ST.CONTAINERELEMENTCODE = BKLE.Code  " \
        "               AND ST.CONTAINERSUBCODE01 = BKLE.SubCodeKey  " \
        "               AND BKLE.ItemTypeCode = 'CNT'  " \
        "            JOIN " \
        "               UserGenericGroup UGG  " \
        "               ON UGG.UserGenericGroupTypeCode = 'PKG'  " \
        "               AND BKLE.PalletType4Code = UGG.Code  " \
        "         Where " \
        "            BKLE.PalletType4Code is Not Null  " \
        "            And PlantInvoice.CODE = '"+rinvoiceno +"'" \
        "         Union " \
        "         Select " \
        "            PlantInvoice.CODE As InvNo, " \
        "            BKLE.PalletType5Code As PalletTypeCode, " \
        "            UGG.LongDescription As PalletName, " \
        "            BKLE.PalletQuantity5 As PalletQuantity  " \
        "         From " \
        "            PlantInvoice  " \
        "            JOIN " \
        "               SalesDocument SD  " \
        "               ON PlantInvoice.CODE = SD.PROVISIONALCODE  " \
        "               and SD.DocumentTypeType = '06'  " \
        "            JOIN " \
        "               SalesDocumentLine SDL  " \
        "               ON SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE  " \
        "               AND SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE  " \
        "               And SDL.DocumentTypeType = '06'  " \
        "            JOIN " \
        "               StockTransaction ST  " \
        "               ON SDL.PreviousCode = ST.OrderCode  " \
        "               AND ST.TemplateCode = 'S05'  " \
        "               And ST.TransactionDetailNumber =  " \
        "               ( " \
        "                  Select " \
        "                     Min(ST1.TransactionDetailNumber)  " \
        "                  From " \
        "                     StockTransaction ST1  " \
        "                  Where " \
        "                     ST1.ContainerElementCode = ST.ContainerElementCode " \
        "               ) " \
        "            JOIN " \
        "               BKLElements BKLE  " \
        "               ON ST.CONTAINERELEMENTCODE = BKLE.Code  " \
        "               AND ST.CONTAINERSUBCODE01 = BKLE.SubCodeKey  " \
        "               AND BKLE.ItemTypeCode = 'CNT'  " \
        "            JOIN " \
        "               UserGenericGroup UGG  " \
        "               ON UGG.UserGenericGroupTypeCode = 'PKG' AND " \
        "               BKLE.PalletType5Code = UGG.Code Where BKLE.PalletType5Code is Not Null  " \
        "   ) " \
        "   As PKG  " \
        "Group By " \
        "   PKG.InvNo, " \
        "   PKG.PalletTypeCode, " \
        "   PKG.PalletName  " \
        "Order By " \
        "   InvNo, " \
        "   PalletName "
    global counter
    p=230
    # print(sqlreturanabledeatails)
    stmt = con.db.prepare(con.conn, sqlreturanabledeatails)
    con.db.execute(stmt)
    resultreturnable = con.db.fetch_both(stmt)
    # print(resultreturnable)
    if resultreturnable != False:
        while resultreturnable != False:
            c.drawString(300, p, resultreturnable['PALLETNAME'])
            c.drawAlignedString(560, p, str(float("%.0f" % float(resultreturnable['PALLETQUANTITY']))))
            p = p - 10
            resultreturnable = con.db.fetch_both(stmt)

    # print("after the sql queary")

def getUnSignandEsignAndLUT(invoiceno):
    sql = ""
    sqllotnumber = " SELECT " \
                   "	 COALESCE('Remarks : ' || Note.Note,'') As PlantInvoiceRemarks  " \
                   "	, Coalesce(Plantinvoice.SIGNEDQRCODE,'') as SIGNEDQRCODE  " \
                   " From PlantInvoice  " \
                   " JOIN SALESDOCUMENT      ON PLANTINVOICE.CODE    = SALESDOCUMENT.PROVISIONALCODE " \
                   "				and SALESDOCUMENT.DocumentTypeType = '06' " \
                   " LEFT JOIN Note          ON  PlantInvoice.AbsUniqueId = Note.Fatherid  " \
                   " WHERE PlantInvoice.code='" + invoiceno + "'" \
                                                              " order by Plantinvoice.code LIMIT 1 "
    print(invoiceno)
    stmt = con.db.prepare(con.conn, sqllotnumber)
    con.db.execute(stmt)
    resultsqr = con.db.fetch_both(stmt)
    print(resultsqr)
    if resultsqr != False:
        while resultsqr != False:
            c.drawString(25, 290, "Invoice Remarks : " + str(resultsqr['PLANTINVOICEREMARKS']))
            SIGNEDQRCODE = resultsqr['SIGNEDQRCODE']
            char = len(SIGNEDQRCODE)
            if char > 0:
                print(SIGNEDQRCODE)
                s = str(SIGNEDQRCODE)  # url to open after scanning qr code
                url = pyqrcode.create(s)  # creating qr code
                img = "PlantInvoiceSQrcode.JPEG"  # name of image
                url.png(img, scale=1)  # saving image as png
                c.drawImage("PlantInvoiceSQrcode.JPEG", 25, 150, 90, 90)
                fonts(9)  # choose your font type and font size
                os.remove("PlantInvoiceSQrcode.JPEG")

            resultsqr = con.db.fetch_both(stmt)

def getandprintchallanbox(invoicenumber,challannumber):

    boxes = 0
    sqlbox = " SELECT pi.code, ST.Ordercode " \
          ", Max(ST.TRANSACTIONDETAILNUMBER) as totalbox " \
          "From  Plantinvoice PI " \
          "Join SalesDocument SD06         On pi.code = SD06.provisionalcode " \
          "                                and sd06.documenttypetype='06' " \
          "join salesdocumentline sdline06 on sdline06.salesdocumentprovisionalcode =        SD06.provisionalcode " \
          "                                and sdline06.documenttypetype='06' " \
          "join salesdocumentline sdline05 on sdline05.salesdocumentprovisionalcode = sdline06.PreviousCode " \
          "                                and sdline05.documenttypetype='05' " \
          "Join stocktransaction ST        On ST.OrderCode = sdline05.salesdocumentprovisionalcode " \
          "                                And St.TemplateCode = 'S04' " \
           "Where PI.Code = '" + invoicenumber + "'and ST.Ordercode ='"+challannumber+"' " \
          "Group BY pi.code,ST.ordercode " \
          "Order by pi.code "

    print(sqlbox)
    stmt = con.db.prepare(con.conn, sqlbox)
    con.db.execute(stmt)
    resultbox = con.db.fetch_both(stmt)
    if resultbox != False:
        while resultbox != False:
            boxes = resultbox['TOTALBOX']
            # p = p - 10
            resultbox = con.db.fetch_both(stmt)
    # c.drawAlignedString(425, d, str(format_currency("%.0f" % float(boxes), '', locale='en_IN')))
    c.drawString(400, d-2, str(boxes))