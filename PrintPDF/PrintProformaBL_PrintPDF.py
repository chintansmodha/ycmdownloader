import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 470
Yordno = 760
i = 0
pageno = 0

divisioncode = []
invoiceno = []
orderno = []
lotno = []
itemname = []
itemtype = []
hsncode = []
payment = []
Remark = []
countryofOrigin = []
grosswt = 0
netwt = 0
packages = 0

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

def yordnovalue():
    global Yordno
    Yordno = Yordno - 8
    return Yordno

def wrap(string, type, width, x, y):
    global i
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - 8
        e = e + 1
        i = i + 1
    return s

def header(divisioncode, result,Yordno):
    c.setTitle('BL Instructions')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    #Horizontal line
    c.line(15, 830, 580, 830)# Upper line
    c.drawCentredString(290, 815, "B/L INSTRUCTIONS")
    fonts(7)
    # c.line(227, 812, 347, 812)# Underline
    c.line(15, 810, 580, 810)# Packing List Partn
    c.line(15, 740, 310, 740)#Company
    c.line(15, 660, 310, 660)#Consignee And Buyer
    c.line(15, 580, 580, 580)#Buyer And vesel
    c.line(165, 560, 580, 560)  # voy  and Port of Dis
    c.line(15, 540, 580, 540)#port of loading  and Port of Dis
    c.line(15, 520, 580, 520)# Partn Desptn Goods And Buyer
    c.line(15, 510, 580, 510)#Partn Desptn Goods And Buyer
    #Right
    c.line(310, 797, 580, 797)# Bl No
    c.line(310, 767, 580, 767)#Booking No.
    c.line(310, 700, 580, 700)#Notify party
    c.line(310, 630, 580, 630)#Notify Party 2***********
    #bottom
    c.line(15, 100, 580, 100)#
    c.line(15, 70, 580, 70)#Freight & total number
    c.line(15, 40, 328, 40)# Number Sequence
    c.line(160, 25, 328, 25)#place of issue and date
    c.line(15, 10, 580, 10)# Lower Line

    #Vertical Line
    c.line(15, 830, 15, 10)
    c.line(165, 580, 165, 520)#port of loading  and Port of Dis *** Mid
    c.line(310, 810, 310, 520)# partn comp and Notifying Party**************MID
    c.line(160, 490, 160, 10)#shippng marks and desscpn of goods
    #Bottom
    c.line(244, 100, 244, 70)
    c.line(328, 100, 328, 10)
    c.line(412, 100, 412, 70)
    c.line(496, 100, 496, 70)
    c.line(580, 830, 580, 10)

    #References Of Box Left
    boldfonts(4)
    c.drawString(18, 805, "Exporter")
    boldfonts(6)
    c.drawString(20, 733, "Consignee :")
    c.drawString(20, 653, "Buyer :")
    boldfonts(6)
    c.drawString(20, 573, "Vessel")
    boldfonts(5)
    c.drawString(170, 573, "Voy. No.")
    c.drawString(170, 553, "Port Of Loading")
    c.drawString(20, 533, "Port Of Discharge")
    c.drawString(170, 533, "Final Destination")
    # References Of Box Right
    boldfonts(6)
    c.drawString(315, 802, 'B/L NO :')
    c.drawString(315, 790, 'Booking No :')
    c.drawString(315, 760, "NOTIFY PARTY :")
    c.drawString(315, 693, "2ND NOTIFY :")
    boldfonts(5)
    c.drawString(315, 573, "Onward Inland Routing")
    c.drawString(315, 553, "Place Of Receipt")
    c.drawString(315, 533, "Place Of Delivery")
    #After line  c.line(15, 510, 580, 510)
    fonts(7)
    c.drawCentredString(290, 512,"PARTICULAR FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE")
    c.drawString(20, 501, "Kind Of Packages: Description Of Goods: Marks And Numbers: Container No/ Seal No.")
    boldfonts(8)
    c.drawCentredString(80, 492, 'S.MARKS')
    c.drawCentredString(80, 492, '________')
    c.drawString(165, 492, 'No. Of Cartons')
    c.drawString(165, 492, '_____________')
    # c.drawAlignedString(355, 124, "Total")#Total
    # c.drawString(20, 70, "Amount Chargeable")#Amount
    # fonts(6)
    # c.drawString(20, 60, "(In Words)")
    fonts(7)
    c.drawString(20, 482, "Cont Size  ")
    c.drawString(90, 482, ": " + str(result['CONTSIZE']))
    c.drawString(20, 472, "Cont No.   ")
    c.drawString(90, 472, ": " + str(result['CONTNO']))
    c.drawString(20, 462, "Seal No.   ")
    c.drawString(90, 462, ": " + str(result['SEALNO']))
    c.drawString(20, 452, "E-Seal No. ")
    c.drawString(90, 452, ": " + str(result['ESEALNO']))
    c.drawString(20, 442, "GR.WT.    " + str(result['WTUNIT']))
    c.drawString(90, 442, ": ")
    c.drawString(20, 432, "NT.WT.     " + str(result['WTUNIT']))
    c.drawString(90, 432, ": ")
    c.drawString(20, 422, "Measurement" + str(result['MEASURE']))
    c.drawString(90, 422, ": ")
    c.drawString(20, 412, "Packages")
    c.drawString(90, 412, ": ")
    # c.drawString(20, 150, "MASTER EXP")

    #******Bottom ***********
    boldfonts(6)
    c.drawString(20, 93, "Freight And Charges")
    c.drawString(165, 93, "Rate :")
    c.drawString(249, 93, "Unit :")
    c.drawString(333, 93, "Currency :")
    c.drawString(417, 93, "Prepaid")
    c.drawString(501, 93, "Collect")
    a = 'Total number Of containers or packages received by carrier'
    wrap(a,c.drawString,45,20,63)
    c.drawString(20, 43, "Carruer's Receipt ")
    c.drawString(165, 63, 'Declared Value')
    c.drawString(20, 33, 'Number & Sequence of Original BL(s)')
    c.drawString(165, 33, 'Place Of Issue of BL :')
    c.drawString(165, 18, 'Date of Issue of BL : ')


    # ******** Left Side
    boldfonts(9)
    c.drawString(18, 795, divisioncode[-1])
    fonts(7)
    wrap(str(result['CORP_ADDRESS']),c.drawString,80,18,785)
    c.drawString(18, 767, str(result['PHONENO']))
    c.drawString(18, 758, str(result['CINIECNO']))
    c.drawString(18,749,str(result['CROP_GSTIN_TAXID']))
    # **********CONSIGNEE AND  BUYER
    c.drawString(18, 725, str(result['CONSIGNEENAME']))
    wrap(str(result['CONSIGNEEADDRESS']), c.drawString, 60, 18, 717)
    c.drawString(18, 645, str(result['BUYER']))
    wrap(str(result['BUYERADDRESS']),c.drawString,60,18,637)

           #*********Vessel voy portofDis, ---> Left
    c.drawString(18, 563, str(result['VESSELFLIGHTNO']))
    c.drawString(18, 523, str(result['PORTOFDISCHARGE']))
          #-------> Right
    c.drawString(170, 543, str(result['PORTOFLOADING']))
    c.drawString(170, 523, str(result['FINALDESTINATION']))

    # **********Right DATA
    fonts(7)
    c.drawString(360, 802, str(result['BLNO']))
    if result['BOOKINGNO'] != None:
        c.drawString(360, 790, str(result['BOOKINGNO']))
        #***********NOTIFY pARTY
    c.drawString(315, 752, str(result['NOTIFYPRTYNAME']))
    wrap(str(result['NOTIFYPRTYADDRESS']), c.drawString, 50, 315, 743)
        # ***********NOTIFY pARTY2
    # c.drawString(315, 752, str(result['NOTIFYPRTYNAME2']))
    # wrap(str(result['NOTIFYPRTYADDRESS2']), c.drawString, 50, 315, 743)
    #******** onwardInland, PlaceRecpt, PlaceDel
    # c.drawString(315, 563, str(result['']))
    c.drawString(315, 543, str(result['PLACEOFRECEIPT']))
    c.drawString(315, 523, str(result['PLACEOFDELV']))

    # Bottom Data
    c.drawString(20, 160, 'MASTER EXP')
    if result['MASTEREXPNO'] != None:
        c.drawString(20, 150, result['MASTEREXPNO'])
        c.drawString(20, 140, str(result['MASTEREXPDT'].strftime('%d-%m-%Y')))
    if result['FREIGHTTVALUE'] != None:
        c.drawString(20,85, 'Freight : ' + str(result['FREIGHTTVALUE']))
        c.drawString(20, 75, 'FOB : ' + str('{0:1.3f}'.format((float(result['ORDERTOTAL']) - float(result['FREIGHTTVALUE'])))))
    else:
        c.drawString(20, 75, 'FOB : ' + str('{0:1.3f}'.format((result['ORDERTOTAL']))))
    c.drawString(165, 83, str(result['EXRATE']))
    c.drawString(249, 83, str(result['WTUNIT']))
    c.drawString(333, 83, str(result['CURRENCY']) )
    if result['PLACEOFISSUEBL'] != None:
        c.drawString(166, 25, str(result['PLACEOFISSUEBL']))
    if result ['DATEOFISSUEBL'] != None:
        c.drawString(166, 10, str(result['DATEOFISSUEBL']))
    c.drawString(20, 23, result['NOOFSEQ'])

    # Data


def data(result, d):
    fonts(7)
    str1 = ''
    string = str1.join(result['ITEM'])
    wrap_text = textwrap.wrap(string, width=75)
    e = 0
    while e < len(wrap_text):
        c.drawString(165, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(155, d, str(result['ITEM']))
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1
    TotalWT(result)


def logic(result):
    global divisioncode, lotno
    global invoiceno, Remark, itemtype, orderno
    global itemname, hsncode, payment, countryofOrigin
    divisioncode.append(result['COMPANY'])
    invoiceno.append(result['INVOICENOANDDT'])
    # itemname.append(result['ITEM'])
    itemtype.append(result['ITMTYP'])
    hsncode.append(result['HSNCODE'])
    # orderno.append(result['ORDNOANDDT'])
    # payment.append(result['PAYMENT'])
    # Remark.append(result['REMARKS'])
    countryofOrigin.append(result['COUNTRYOFORIGIN'])
    lotno.append(result['LOTNO'])

def newpage():
    global d
    d = 470
    return d

def newrequest():
    global divisioncode, lotno
    global invoiceno, Remark, itemtype
    global itemname, hsncode, payment, countryofOrigin
    global pageno, Yordno
    divisioncode = []
    pageno = 0
    Yordno = 760
    invoiceno = []
    itemname = []
    hsncode = []
    payment = []
    Remark = []
    itemtype = []
    countryofOrigin = []
    lotno = []

def TotalWT(result):
    global grosswt, netwt, packages
    if result['ITMPACKAGES'] != None:
        packages = packages + int(result['ITMPACKAGES'])
    if result['ITMGROSSWT'] !=None:
        grosswt = grosswt + float(result['ITMGROSSWT'])
    if result['ITMNETWT'] !=None:
        netwt = netwt + float(result['ITMNETWT'])

def TotalClean():
    global grosswt
    global netwt
    global packages
    grosswt = 0
    netwt = 0
    packages = 0

def textsize(c, result):
    d = dvalue()
    logic(result)
    global i, Yordno
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(divisioncode, result,Yordno)
        c.drawString(165, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1] == invoiceno[-2]:
            if itemtype[-1] == itemtype[-2]:
                if lotno[-1] == lotno[-2]:
                    data(result, d)
                else:
                    c.drawString(175, d, 'LOT NO.: ' + str(lotno[-2]))
                    d = dvalue()
                    d = dvalue()
                    data(result, d)
            else:
                c.drawString(175, d, 'LOT NO.: ' + str(lotno[-2]))
                d = dvalue()
                d = dvalue()
                c.drawString(165, d, itemtype[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)

        else:
            c.drawString(175, d, 'LOT NO.: ' + str(lotno[-2]))
            d = dvalue()
            d = dvalue()
            c.drawString(175,d, 'HSNCODE : ' + str(hsncode[-2]))
            d = dvalue()
            d = dvalue()
            c.drawString(175, d, "COUNTRY OF ORIGIN:  " + str(countryofOrigin[-1]).upper())
            # ************** groos wt and nt wt at shipping marks ,packages
            c.drawString(94, 442, str('{0:1.3f}'.format(grosswt)))
            c.drawString(94, 432, str('{0:1.3f}'.format(netwt)))
            c.drawString(94, 412, str(packages))
            boldfonts(6)
            c.drawCentredString(185, 482, str(packages))  # No Of Cartons
            fonts(7)
            TotalClean()
            c.showPage()
            d = newpage()
            d = dvalue()
            header(divisioncode, result, Yordno)
            c.drawString(165, d, itemtype[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        c.drawString(175, d, 'LOT NO.: ' + str(lotno[-2]))
        d = dvalue()
        d = dvalue()
        c.drawString(175, d, 'HSNCODE : ' + str(hsncode[-2]))
        d = dvalue()
        d = dvalue()
        c.drawString(175, d, "COUNTRY OF ORIGIN:  " + str(countryofOrigin[-1]).upper())
        # ************** groos wt and nt wt at shipping marks ,packages
        c.drawString(94, 442, str('{0:1.3f}'.format(grosswt)))
        c.drawString(94, 432, str('{0:1.3f}'.format(netwt)))
        c.drawString(94, 412, str(packages))
        boldfonts(6)
        c.drawCentredString(185, 482, str(packages))  # No Of Cartons
        fonts(7)
        TotalClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(divisioncode, result, Yordno)
        c.drawString(165, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)





