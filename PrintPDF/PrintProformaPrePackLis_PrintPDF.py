import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 440
Yordno = 735
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
    c.setTitle('Packing List(PreShipment)')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    #Horizontal line
    c.line(15, 830, 580, 830)# Upper line
    c.drawCentredString(290, 815, "PACKING LIST")
    fonts(7)
    c.line(237, 812, 340, 812)# Underline
    c.line(15, 810, 580, 810)# Packing List Partn
    c.line(350, 755, 580, 755)# Buyers Ord No And packing list no
    c.line(15, 760, 350, 760)# factory add and corp add
    c.line(15, 730, 350, 730)# regd add and corp add
    c.line(15, 700, 580, 700)#prtn comp and consignee
    c.line(15, 630, 580, 630)#prtn buyer and consignee
    c.line(350, 580, 580, 580)# terms of delv and country orgin
    c.line(350, 550, 580, 550)# country orgin and sb No
    c.line(15, 560, 350, 560)#prtn pre-cariage by and buyer
    c.line(15, 550, 350, 550)#pre-cariage by and Fligt No
    c.line(15, 520, 350, 520)#Fligt No and port of dis
    c.line(15, 490, 580, 490)# Partn Desptn Goods And Buyer
    c.line(15, 470, 580, 470)# Desptn Goods an name of goods
    c.line(400, 115, 580, 115)#TOTAL
    c.line(15, 100, 580, 100)# order Refer And authorised sign
    c.line(15, 10, 580, 10)# Lower Line

    #Vertical Line
    c.line(15, 830, 15, 10)
    c.line(465, 580, 465, 550)# country origin and country dstn
    c.line(183, 560, 183, 490)# flight no and port of dis
    c.line(350, 810, 350, 490)# partn comp and Notifying Party
    c.line(150, 470, 150, 100)#shippng marks and desscpn of goods
    c.line(400, 490, 400, 100)#desscpn of goods and packages
    c.line(450, 490, 450, 100)#Pack and gr.wt
    c.line(515, 490, 515, 100)#Gr. Wt and Nt wt
    c.line(580, 830, 580, 10)

    #References Of Box
    boldfonts(4)
    c.drawString(18, 805, "Exporter/Consignor")
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
    c.drawString(20, 450, "Cont No.   "+ "        : " + str(result['CONTNO']))
    c.drawString(20, 440, "Seal No.   "+ "        : " + str(result['SEALNO']))
    c.drawString(20, 430, "E-Seal No. "+ "        : " + str(result['ESEALNO']))
    c.drawString(20, 420, "GR.WT.    " + str(result['WTUNIT']) + "        : ")
    c.drawString(20, 410, "NT.WT.     " + str(result['WTUNIT']) + "        : ")
    c.drawString(20, 400, "Measurement" + "        : " + str(result['MEASURE']))
    c.drawString(20, 390, "Packages   " + "        :  ")
    c.drawString(20, 150, "MASTER EXP")
    if result['MASTEREXPNO'] != None:
        c.drawString(20, 140, str(result['MASTEREXPNO']))
        c.drawString(20, 130, str(result['MASTEREXPDT'].strftime('%d-%m-%Y')))

    # ******** Right Side
    boldfonts(6)
    c.drawString(355, 800, "Packing List No. & Date")
    c.drawString(355, 745, "Buyer's Order No. & Date")
    c.drawString(355, 690, "Notifying Party: ")
    c.drawString(355, 620, "Terms Of Delivery And Payment")
    c.drawString(355, 570, "Country Of Origin Of Goods")
    c.drawString(470, 570, "Country Of Final Destination")
    c.drawString(20, 475, "Shipping Marks & No's/Container No.")
    c.drawString(155, 475, "Description Of Goods")
    c.drawString(155, 460, "No Of Cartons")
    c.line(155, 458, 195, 458)
    # c.drawAlignedString(175, 450, str(result['PACKAGES']))#No Of Cartons
    c.drawAlignedString(450, 475, "Packages")
    c.drawAlignedString(485, 475, "GR. WT. KG")
    c.drawAlignedString(550, 475, "NT. WT. KG")
    c.drawString(20, 90, "Declaration :")
    fonts(7)#Declaration
    string = 'We declare that this invoice shows the actual price of the goods described and that all particulars  ' \
             'are true and correct'
    wrap(string,c.drawString,105,20,80)
    boldfonts(6)
    c.drawString(20, 40, "Other Reference :")
    c.drawString(515, 20, "Authorised Signatory")
    boldfonts(7)
    c.drawAlignedString(570, 80, divisioncode[-1])

    # Data
    fonts(15)
    c.drawCentredString(182, 790, divisioncode[-1])
    fonts(7)
    wrap(str(result['FAC_ADDRESS']),c.drawCentredString,85,181,775)
    wrap(str(result['CORP_ADDRESS']),c.drawCentredString,100,181,750)
    fonts(6)
    c.drawString(20, 732, str(result['CORP_GSTIN']))
    c.drawString(150, 732, str(result['TAXID']))
    if result['IECNO'] != None:
        c.drawAlignedString(290, 732, str(result['IECNO']))
    fonts(7)
    wrap(str(result['REGD_ADDRESS']), c.drawCentredString, 95, 181, 720)
    fonts(6)
    c.drawAlignedString(340, 702, str(result['CINNO']))
    c.drawString(20, 680, str(result['CONSIGNEENAME']))
    wrap(str(result['CONSIGNEEADDRESS']),c.drawString,100,20,670)
    c.drawString(20, 610, str(result['BUYER']))
    wrap(str(result['BUYERADDRESS']), c.drawString, 100, 20, 600)
    c.drawString(355, 680, str(result['NOTIFYPRTYNAME']))
    wrap(str(result['NOTIFYPRTYADDRESS']), c.drawString, 60, 355, 670)
    fonts(7)
    c.drawString(355, 780, invoiceno[-1])
    c.drawString(355, Yordno, str(orderno[-1]))
    c.drawString(355, 610, str(result['TERMSOFDELV']))
    wrap(str(result['PAYMENT']),c.drawString,60,355,600)
    if result['COUNTRYOFORIGINOFGOODS'] != None:
        c.drawString(355, 560, str(result['COUNTRYOFORIGINOFGOODS']))
    if result['COUNTRYOFDESTN'] != None:
        c.drawString(470, 560, str(result['COUNTRYOFDESTN']))
    c.drawString(20, 530, str(result['VESSELFLIGHTNO']))
    c.drawString(20, 500, str(result['PORTOFDISCHARGE']))
    c.drawString(188, 530, str(result['PORTOFLOADING']))
    c.drawString(188, 500, str(result['FINALDESTINATION']))
    c.drawString(355, 530, "S/B NO.: " + str(result['SBNO']) + "                                    " + "       DT: " + str(result['SBDT']))
    c.drawString(355, 510, "B/L NO.: " + str(result['BLNO']) + "                                    " + "       DT: " + str(result['BLDT']))


def data(result, d):
    fonts(7)
    str1 = ''
    string = str1.join(result['ITEM'])
    wrap_text = textwrap.wrap(string, width=55)
    e = 0
    while e < len(wrap_text):
        c.drawString(155, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(155, d, str(result['ITEM']))
    c.drawAlignedString(448, d, str(result['ITMPACKAGES']))
    c.drawAlignedString(500, d, str(result['ITMGROSSWT']))
    c.drawAlignedString(565, d, str(result['ITMNETWT']))
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
    orderno.append(result['ORDNOANDDT'])
    # payment.append(result['PAYMENT'])
    # Remark.append(result['REMARKS'])
    countryofOrigin.append(result['COUNTRYOFORIGIN'])
    lotno.append(result['LOTNO'])

def newpage():
    global d
    d = 440
    return d

def newrequest():
    global divisioncode, lotno
    global invoiceno, Remark, itemtype
    global itemname, hsncode, payment, countryofOrigin
    global pageno, Yordno
    divisioncode = []
    pageno = 0
    Yordno = 735
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
    packages = packages + int(result['ITMPACKAGES'])
    grosswt = grosswt + float(result['ITMGROSSWT'])
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
        c.drawString(155, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1] == invoiceno[-2]:
            if orderno[-1] == orderno[-2]:
                if itemtype[-1] == itemtype[-2]:
                    if lotno[-1] == lotno[-2]:
                        data(result,d)

                    elif lotno[-1] != lotno[-2]:
                        c.drawString(155, d , "Lot No. :   " + str(lotno[-2]))
                        d = dvalue()
                        d = dvalue()
                        data(result, d)

                elif itemtype[-1] != itemtype[-2]:
                    c.drawString(155, d, "Lot No. :   " + str(lotno[-2]))
                    d = dvalue()
                    d = dvalue()
                    c.drawString(155, d, "HSNCODE :  " + hsncode[-2])
                    d = dvalue()
                    d = dvalue()
                    c.drawString(155, d, itemtype[-1])
                    d = dvalue()
                    d = dvalue()
                    data(result, d)

            elif orderno[-1] != orderno[-2]:
                Yordno = yordnovalue()
                c.drawString(355, Yordno, str(orderno[-1]))
                data(result, d)

        elif invoiceno[-1] != invoiceno[-2]:
            c.drawString(155, d, "Lot No. :   " + str(lotno[-2]))
            d = dvalue()
            d = dvalue()
            c.drawString(155, d, "HSNCODE :  " + hsncode[-2])
            d = dvalue()
            d = dvalue()
            c.drawString(155, d, "COUNTRY OF ORIGIN:  " + str(countryofOrigin[-2]).upper())

            c.drawString(380, 105, "Total ")
            c.drawAlignedString(448, 105, str(packages))
            c.drawAlignedString(500, 105, str('{0:1.3f}'.format(grosswt)))
            c.drawAlignedString(565, 105, str('{0:1.3f}'.format(netwt)))
            # ************** groos wt and nt wt at shipping marks, packages
            c.drawString(85, 420, str('{0:1.3f}'.format(grosswt)))
            c.drawString(85, 410, str('{0:1.3f}'.format(netwt)))
            c.drawString(85, 390, str(packages))
            boldfonts(6)
            c.drawAlignedString(175, 450, str(packages))  # No Of Cartons
            fonts(7)
            TotalClean()
            c.showPage()
            d = newpage()
            d = dvalue()
            header(divisioncode, result,Yordno)
            c.drawString(155, d, itemtype[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        c.drawString(155, d, "Lot No. :   " + str(lotno[-2]))
        d = dvalue()
        d = dvalue()
        c.drawString(155, d, "HSNCODE :  " + hsncode[-2])
        d = dvalue()
        d = dvalue()
        c.drawString(155, d, "COUNTRY OF ORIGIN:  " + str(countryofOrigin[-2]).upper())

        c.drawString(380, 105, "Total ")
        c.drawAlignedString(448, 105, str(packages))
        c.drawAlignedString(500, 105, str('{0:1.3f}'.format(grosswt)))
        c.drawAlignedString(565, 105, str('{0:1.3f}'.format(netwt)))
        # ************** groos wt and nt wt at shipping marks, packages
        c.drawString(85, 420, str('{0:1.3f}'.format(grosswt)))
        c.drawString(85, 410, str('{0:1.3f}'.format(netwt)))
        c.drawString(85, 390, str(packages))
        boldfonts(6)
        c.drawAlignedString(175, 450, str(packages))  # No Of Cartons
        fonts(7)
        TotalClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(divisioncode, result,Yordno)
        c.drawString(155, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)


