import datetime

from babel.numbers import format_currency
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from Global_Files import Connection_String as con

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
d = 750
UnitName=[]
serialno=0
pageno = 0
GrandTotalWeight = 0
GrandTotalFreight = 0
GrandTotalGSt = 0
GSTTotal=0
Weigthtotal=0
companytotal=0
Freighttotal=0

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

def logic(result):
    UnitName.append(result['DIVISIONCODE'])

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global pageno
    global Weigthtotal
    global Freighttotal
    global GSTTotal
    global GrandTotalWeight
    global GrandTotalFreight
    global GrandTotalGSt
    global GSTTotal
    global BrokerGroupName
    global UnitName
    UnitName=[]
    BrokerGroupName=[]
    pageno = 0
    GrandTotalWeight=0
    GrandTotalFreight=0
    GrandTotalGSt=0
    Weigthtotal=0
    Freighttotal=0
    GSTTotal=0
    d=730

def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    if d < 40:
        d = newpage()
        c.showPage()
        header(stdt, etdt)
    if len(UnitName) == 1:
        header(stdt, etdt)
        fonts(12)
        d=dvalue()
        printcompanyname(result, d)
        d=dvalue()
        fonts(9)
        # printcompanyname(result,d)
        data(result, d)
    elif UnitName[-1] == UnitName[-2]:
        data(result, d)
    elif UnitName[-1] != UnitName[-2]:
        printotal(d)
        d=dvalue()
        printcompanyname(result,d)
        d=dvalue()
        data(result, d)


def header(stdt, etdt):
    now = datetime.datetime.now()
    print("Date: " + now.strftime("%Y-%m-%d"))  # this will print **2018-02-01** that is todays date
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, "Beekaylon Group of Companies")
    fonts(9)
    c.drawCentredString(300, 785,
                        "TRANSPORTERWISE FREIGHT / SERVICE TAX SUMMARY Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    c.drawString(10, 780, str(now.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 777, 600, 777)
    # Upperline in header
    c.drawString(10, 765, "Transporter Name")
    c.drawString(340, 765, "Quanitiy")
    c.drawString(430, 765, "Freight")
    c.drawString(510, 765, "Service Tax")
    c.line(0, 755, 600, 755)

def data(result, d):
    fonts(9)
    c.drawString(10, d-5, result['TRANSPORTERNAME'])
    c.drawAlignedString(360, d-5, ("%.3f"% float(result['QUANTITY'])))
    c.drawAlignedString(450, d -5,str(format_currency("%.2f" % float(result['CHARGEVALUE']), '', locale='en_IN')))
    c.drawAlignedString(550, d -5,str(format_currency("%.2f" % float(result['GSTCHARGEVALUE']), '', locale='en_IN')))
    total(result)

def printcompanyname(result,d):
    fonts(12)
    c.drawString(10, d, result['DIVISIONCODE'])
    fonts(9)
    # d=dvalue()

def printagentname(result,d):
    c.drawString(10, d, result['AGENTNAME'])
    # d=dvalue()

def printbroker(result,d):
    c.drawCentredString(300,d,result['BROKERGROUPNAME'])
    # d=dvalue()

def total(result):
    global GSTTotal
    global Weigthtotal
    global companytotal
    global Freighttotal
    Weigthtotal = Weigthtotal + (float("%.2f" % float(result['QUANTITY'])))
    Freighttotal = Freighttotal + (float("%.2f" % float(result['CHARGEVALUE'])))
    GSTTotal=GSTTotal + (float("%.2f" % float(result['GSTCHARGEVALUE'])))

def printotal(d):
    global Freighttotal
    global Weigthtotal
    global GSTTotal
    global GrandTotalWeight
    global GrandTotalFreight
    global GrandTotalGSt
    c.drawString(240,d-5,"Company Total : ")
    c.drawAlignedString(360, d-5, str(("%.3f" % float(Weigthtotal))))
    c.drawAlignedString(450, d-5, str(format_currency("%.2f" % float(Freighttotal), '', locale='en_IN')))
    c.drawAlignedString(550, d-5, str(format_currency("%.2f" % float(GSTTotal), '', locale='en_IN')))
    GrandTotalWeight = GrandTotalWeight + Weigthtotal
    GrandTotalFreight = GrandTotalFreight + Freighttotal
    GrandTotalGSt = GrandTotalGSt + GSTTotal
    Weigthtotal=0
    Freighttotal=0
    GSTTotal=0
    d=dvalue()

# def printbrokertotal():
#     global brokertotal
#     global grandtotal
#     d=dvalue()
#     c.drawAlignedString(430, d, "Broker Total : "+str(format_currency("%.2f" % float(brokertotal), '', locale='en_IN')))
#     # c.drawAlignedString(430, d-10, "Grand Total : "+str(format_currency("%.2f" % float(grandtotal), '', locale='en_IN')))
#     brokertotal=0

def printbrokergrouptotal():
    global brokergrouptotal
    global GSTTotal
    d=dvalue()
    c.drawAlignedString(430, d, "Broker Group Total : "+str(format_currency("%.2f" % float(brokergrouptotal), '', locale='en_IN')))
    # c.drawAlignedString(430, d-10, "Grand Total : "+str(format_currency("%.2f" % float(grandtotal), '', locale='en_IN')))
    brokergrouptotal=0

def printGrandtotal():
    global GrandTotalWeight
    global GrandTotalFreight
    global GrandTotalGSt
    d=dvalue()
    c.drawString(240, d - 5, "Grand Total : ")
    c.drawAlignedString(360, d , str(("%.3f" % float(GrandTotalWeight))))
    c.drawAlignedString(450, d , str(format_currency("%.2f" % float(GrandTotalFreight), '', locale='en_IN')))
    c.drawAlignedString(550, d , str(format_currency("%.2f" % float(GrandTotalGSt), '', locale='en_IN')))
    GrandTotalWeight = 0
    GrandTotalFreight = 0
    GrandTotalGSt = 0


