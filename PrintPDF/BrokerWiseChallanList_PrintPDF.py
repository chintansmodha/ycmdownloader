import textwrap

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
from datetime import date

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
# d = 730
d=500
divisioncode=[]
departmentname=[]
product=[]
agent=[]
broker=[]
brokergroup=[]
customer=[]
itemcount=[]
CompanyQuentityTotal=0
CompanyAmountTotal=0
pageno=0
LSRegistertyp=''
itemtotal=0
itemratetotal=0
itemamounttotal=0

totalquantity=0
totalprice=0
totalbrokerquantity=0
totalbrokerrate=0
totalbrokeramount=0

totalbrokergroupquantity=0
totalbrokergrouprate=0
totalbrokergroupamount=0

totalpartyquantity=0
totalpartyrate=0
totalpartyamount=0

totalcompanyquantity=0
totalcompanyprice=0
totalcompanyamount=0

totaldepartmentquentity=0
totaldepartmentagent=0
totaldepartmentprice=0
totalbox=0
totalcops=0


def page():
    global pageno
    pageno = pageno + 1
    return pageno
def fonts(size):
    global c
    c.setFont("MyOwnArial", size)
def dvalue():
    global d
    d=d-10
    return d
def dvalue5():
    global d
    d=d-5
    return d
def dvalue3():
    global d
    d=d-3
    return d
def dlocvalue(d):
    d=d-20
    return d
def dvaluex(stdt, etdt,result, divisioncode,LSRegistertype):
    global d
    if d > 40:
        # d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,result, divisioncode,LSRegistertype)
        return d
def newpage():
    global d
    d = 510
    # d = 730
    return d
def newrequest():
    global divisioncode
    global pageno
    global product
    global departmentname
    global agent
    global broker
    global brokergroup
    global customer
    global product
    # global warehouse
    divisioncode=[]
    departmentname=[]
    agent=[]
    broker=[]
    brokergroup=[]
    customer=[]
    product=[]
    # print(customer)

    pageno=0
    global d
    d=510
    # warehouse=[]
    product=0
def logic(result):
    divisioncode.append(result['DIVISIONNAME'])
    departmentname.append(result['COMPANYNAME'])
    # agent.append(result['BROKER'])
    broker.append(result['BROKERNAME'])
    brokergroup.append(result['BROKERGROUPNAME'])
    customer.append(result['PARTYNAME'])
    # print(customer)
    try:
        product.append(result['PRODUCT'])
    except:
         pass

    # print("from header end ")
def header(stdt,etdt,divisioncode,lslotno,LSRegistertype):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(430, 560, divisioncode[-1])
    fonts(9)
    if LSRegistertype=='0':
        c.drawCentredString(430  , 550, "Broker Wise Challan  Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    else:
        c.drawCentredString(430  , 550, "Party Wise Challan  Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(770,550,"Page No."+str(p))
    c.line(0, 542, 850, 542)
    c.line(0, 522, 850, 522)
    #Upperline in header
    c.drawString(10, 530, "Inv No.")
    c.drawString(70, 530, "Inv Date")
    c.drawString(120, 530, "Shade")
    c.drawCentredString(210, 530, "Boxes")
    c.drawCentredString(250, 530, "Quanitiy")
    c.drawCentredString(300, 530, "Item Rt.")
    c.drawCentredString(358, 530, "Amount")

    # c.drawCentredString(600, 530, "Transporter")
    if lslotno=='1':
        c.drawCentredString(810, 530, "Lot No")
    # else:

    # else:
    #     c.drawCentredString(460, 530, "PartyName")
    #     c.drawCentredString(600, 530, "Transporter")

    if LSRegistertype=='0':
        c.drawCentredString(460, 530, "PartyName")
        c.drawCentredString(580, 530, "Transporter")
    else:
        c.drawCentredString(460, 530, "Transporter")
    fonts(7)

def textsize(c, result, d, stdt, etdt, lslotno, LSRegistertype):
    fonts(7)
    logic(result)
    LSRegistertyp=LSRegistertype
    # printdetail(result,d)
    if d< 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt, result, divisioncode, LSRegistertype)

    if len(departmentname) == 1:
        header(stdt, etdt, divisioncode, lslotno, LSRegistertype)
        fonts(7)
        printbrokergroup(result)
        if LSRegistertype == '0':
            printbroker(result)
        else:
            printbroker(result)
            printparty(result)
        printcompanyname(result)
        printproduct(result)
        printdetailh(stdt, etdt,result, lslotno,LSRegistertype)
    elif departmentname[-1] == departmentname[-2]:
        if brokergroup[-1] != brokergroup[-2]:
            printitemtotal(d)
            # printpartytotal(d)
            # printbrokertotal(d)
            # printbrokergrouptotal(d)
            # printbrokergroup(result)
            if LSRegistertype == '0':
                printbrokertotal(d)
                printbrokergrouptotal(d)
                printbrokergroup(result)
                printbroker(result)
            else:
                printpartytotal(d)
                printbrokergroup(result)
                printbroker(result)
                printparty(result)
            printcompanyname(result)
            printproduct(result)
            printdetailh(stdt, etdt,result, lslotno,LSRegistertype)
            # print('Invoice number : - ' + str(result['INVOICENO']) + ' Product : -  ' + str(result['PRODUCT']))
        else:
            if broker[-1] != broker[-2]:
                printitemtotal(d)
                # printbrokertotal(d)
                if LSRegistertype == '0':
                    printbrokertotal(d)
                    printbroker(result)
                else:
                    printpartytotal(d)
                    printbrokergroup(result)
                    printparty(result)
                printproduct(result)
                printdetailh(stdt, etdt,result, lslotno,LSRegistertype)

            else:
                printdetail(stdt, etdt,result, d, lslotno,LSRegistertype)
    elif departmentname[-1] != departmentname[-2]:
        printitemtotal(d)
        # printcustomertotal(d)
        # printcompanytotal(d)
        if LSRegistertype=='0':
            printbrokertotal(d)
        else:
            printpartytotal(d)
        printcompanytotal(d)
        # printdepartmenttotal(d)
        d = dvalue()
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode, lslotno, LSRegistertype)
        printdepartment(result, d)
        # if agent[-1]!=agent[-2]:
        if broker[-1] != broker[-2]:
            # printitemtotal(d)
            if LSRegistertype == '0':
                printbroker(result)
            else:
                printparty(result)
            printsubdetail(result)
            d = dvalue()
            printdetail(stdt, etdt,result, d, lslotno,LSRegistertype)
            # printtotal(d)
        else:
            d = dvalue()
            printdetail(stdt, etdt,result, d, lslotno,LSRegistertype)
        # if product[-1] != product[-2]:
        #     printitemtotal(d)
        # dvaluex(stdt, etdt, result, divisioncode, LSRegistertype)
    print("after textsize")

def printdetailh(stdt, etdt,result,lslotno,LSRegistertype):
    fonts(7)
    d=dvalue()

    c.drawString(10, d, result['INVOICENO'])
    c.drawString(70, d, result['INVOICEDATE'].strftime('%d-%m-%Y'))
    c.drawString(120, d, result['SHADENAME'])
    c.drawString(210, d, "0")  # BOXES VALUE TO ADD HERE
    c.drawAlignedString(250, d, ("%.3f" % float(result['QUANTITY'])))
    c.drawAlignedString(295, d, str(format_currency("%.2f" % float(result['INVRATE']), '', locale='en_IN')))
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(result['ITEMAMOUNT']), '', locale='en_IN')))
    if lslotno == '1':
        c.drawCentredString(810, d, "1234567890")

    if LSRegistertype=='0':
        c.drawString(440, d, str(result['PARTYNAME']))
        c.drawString(580, d, result['TRANSPORTERNAME1'])
    else:
        c.drawString(440, d, result['TRANSPORTERNAME1'])
    total(result)


def printdetail(stdt, etdt,result,d,lslotno,LSRegistertype):
    fonts(7)
    # d=dvalue()
    c.drawString(10, d, result['INVOICENO'])
    c.drawString(70, d, result['INVOICEDATE'].strftime('%d-%m-%Y'))
    c.drawString(120, d, result['SHADENAME'])
    c.drawString(210, d, "0")  # BOXES VALUE TO ADD HERE
    c.drawAlignedString(250, d, ("%.3f" % float(result['QUANTITY'])))
    c.drawAlignedString(295, d, str(format_currency("%.2f" % float(result['INVRATE']), '', locale='en_IN')))
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(result['ITEMAMOUNT']), '', locale='en_IN')))
    if lslotno == '1':
        c.drawCentredString(810, d, "1234567890")

    if LSRegistertype == '0':
        c.drawString(440, d, str(result['PARTYNAME']))
        c.drawString(580, d, result['TRANSPORTERNAME1'])
    else:
        c.drawString(440, d, result['TRANSPORTERNAME1'])
    total(result)


    # print("totalquantity from printdetails after    : " + str(totalquantity))
def total(result):
    global LSRegistertyp
    global itemtotal
    global itemratetotal
    global itemamounttotal

    global totalquantity
    global totalbrokerquantity
    global totalbrokerrate
    global totalbrokeramount

    global totalpartyquantity
    global totalpartyrate
    global totalpartyamount

    global totalbrokergroupquantity
    global totalbrokergrouprate
    global totalbrokergroupamount

    global totalcompanyprice
    global totalcompanyamount
    global totalcompanyquantity

    global totaldepartmentquentity
    itemtotal = itemtotal + (float("%.3f" % float(result['QUANTITY'])))
    itemratetotal = itemratetotal + (float("%.3f" % float(result['INVRATE'])))
    itemamounttotal = itemamounttotal + (float("%.3f" % float(result['ITEMAMOUNT'])))

    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalbrokerquantity = totalbrokerquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalbrokerrate = totalbrokerrate + (float("%.3f" % float(result['INVRATE'])))
    totalbrokeramount = totalbrokeramount + (float("%.3f" % float(result['ITEMAMOUNT'])))

    totalbrokergroupquantity = totalbrokergroupquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalbrokergrouprate = totalbrokergrouprate + (float("%.3f" % float(result['INVRATE'])))
    totalbrokergroupamount = totalbrokergroupamount + (float("%.3f" % float(result['ITEMAMOUNT'])))

    totalpartyquantity = totalpartyquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalpartyrate = totalpartyrate + (float("%.3f" % float(result['INVRATE'])))
    totalpartyamount = totalpartyamount + (float("%.3f" % float(result['ITEMAMOUNT'])))

    totalcompanyquantity = totalcompanyquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalcompanyprice = totalcompanyprice + (float("%.3f" % float(result['INVRATE'])))
    totalcompanyamount = totalcompanyamount + (float("%.3f" % float(result['ITEMAMOUNT'])))

    totaldepartmentquentity = totaldepartmentquentity + (float("%.3f" % float(result['QUANTITY'])))

def printproduct(result):
    d = dvalue()
    c.drawString(10, d, "Item                  : "+str(result['PRODUCT']))
    # d=dvalue5()

def printsubdetail(result):
    # d=dvalue()
    # c.drawCentredString(300, d, result['BROKERGROUPNAME'])
    # d=dvalue()
    # c.drawString(10, d, "Broker              : "+str(result['BROKERNAME']))
    d=dvalue()
    c.drawString(10, d, "Company        : "+str(result['COMPANYNAME']))
    # d=dvalue()
    # c.drawString(10, d, "Item      : "+str(result['PRODUCT']))

def printbroker(result):
    d = dvalue()
    c.drawString(10, d, "Broker              : " + str(result['BROKERNAME']))

def printparty(result):
    d = dvalue()
    c.drawString(10, d, "Party                : " + str(result['PARTYNAME']))

def printbrokergroup(result):
    d = dvalue()
    c.drawCentredString(430, d, result['BROKERGROUPNAME'])

def printcompanyname(result):
    d = dvalue()
    c.drawString(10, d, "Company         : " + str(result['COMPANYNAME']))

def printdepartment(result,d):
    c.drawString(10, d, result['COMPANYNAME'])

def printcustomertotal(d):
    d=dvalue()
    # c.line(380, d+8, 590, d+8)
    global totalquantity
    # print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(200, d, "Party Total :")
    c.drawAlignedString(250, d, "0")  # Boxes
    c.drawAlignedString(310, d, "0")  # Cops for this 2 value sir will tell to use then have to use field to display
    c.drawAlignedString(362, d, str(("%.3f" % float(totalquantity))))
    # d=dvalue()

    totalquantity=0

def printbrokertotal(d):
    d=dvalue()
    global totalbrokerquantity
    global totalbrokerrate
    global totalbrokeramount
    # print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(200, d, "Broker Total :")
    c.drawAlignedString(250, d, str(("%.3f" % float(totalbrokerquantity))))
    # c.drawAlignedString(310, d, str(format_currency("%.2f" % float(totalbrokerrate), '', locale='en_IN')))  # Cops for this 2 value sir will tell to use then have to use field to display
    # c.drawString(560, d, "Net Wt ")
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(totalbrokeramount), '', locale='en_IN')))
    # d=dvalue()

    totalbrokerquantity=0
    totalbrokerrate=0
    totalbrokeramount=0

def printpartytotal(d):
    global totalpartyrate
    global totalpartyamount
    global totalpartyquantity
    # print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(200, d, "Party Total :")
    c.drawAlignedString(250, d, str(("%.3f" % float(totalpartyquantity))))
    # c.drawAlignedString(310, d, str(format_currency("%.2f" % float(totalpartyrate), '', locale='en_IN')))  # Cops for this 2 value sir will tell to use then have to use field to display
    # c.drawString(560, d, "Net Wt ")
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(totalpartyamount), '', locale='en_IN')))
    # d=dvalue()

    totalpartyquantity=0
    totalpartyrate=0
    totalpartyamount=0

def printbrokergrouptotal(d):
    d=dvalue()
    global totalbrokergroupquantity
    global totalbrokergrouprate
    global totalbrokergroupamount
    # print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(200, d, "Broker Group Total :")
    c.drawAlignedString(250, d, str(("%.3f" % float(totalbrokergroupquantity))))
    # c.drawAlignedString(310, d, str(format_currency("%.2f" % float(totalbrokergrouprate), '', locale='en_IN')))  # Cops for this 2 value sir will tell to use then have to use field to display
    # c.drawString(560, d, "Net Wt ")
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(totalbrokergroupamount), '', locale='en_IN')))
    # d=dvalue()

    totalbrokergroupquantity=0
    totalbrokergrouprate=0
    totalbrokergroupamount=0

def printitemtotal(d):
    d=dvalue()
    global itemtotal
    global itemratetotal
    global itemamounttotal

    # print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(200, d, "Item Total :")
    c.drawAlignedString(250, d, str(("%.3f" % float(itemtotal))))
    # c.drawAlignedString(310, d, str(format_currency("%.2f" % float(itemratetotal), '', locale='en_IN')))
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(itemamounttotal), '', locale='en_IN')))
    itemtotal=0
    itemratetotal=0
    itemamounttotal=0

def printcompanytotal(d):
    d=dvalue()
    global totalcompanyprice
    global totalcompanyamount
    global totalcompanyquantity

    # print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(200, d, "Company Total :")
    c.drawAlignedString(250, d, str(("%.3f" % float(totalcompanyquantity))))
    # c.drawAlignedString(310, d, str(format_currency("%.2f" % float(totalcompanyprice), '', locale='en_IN')))
    c.drawAlignedString(362, d, str(format_currency("%.2f" % float(totalcompanyamount), '', locale='en_IN')))
    totalcompanyprice=0
    totalcompanyamount=0
    totalcompanyquantity=0


def printdepartmenttotal(d):
    d=dvalue()
    global totaldepartmentquentity
    # print("totalquantity from printtotal "+str(totaldepartmentquentity))
    c.drawAlignedString(200, d, "Department Total :")
    c.drawAlignedString(250, d, "0") # Boxes
    # c.drawAlignedString(310, d, "0") # Cops for this 2 value sir will tell to use then have to use field to display
    # c.drawString(560, d, "Net Wt ")
    c.drawAlignedString(400, d, str(("%.3f" % float(totaldepartmentquentity))))
    # d=dvalue()

    totaldepartmentquentity=0