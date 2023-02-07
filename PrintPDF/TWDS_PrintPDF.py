from reportlab.lib.pagesizes import  A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from Global_Files import Connection_String as con
from datetime import datetime 
from datetime import date

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(A4))
c.setPageSize(A4)
d = 760

despatch=[]
transporter=[]
party=[]

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

TotalPartyAmt=0
TotaltransporterAmt=0
pageno=0

TotalPartyQty=0
TotalPartyAmt=0
TotalBrokerQty=0
TotalBrokerAmt=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt, etdt, transporter):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, transporter,despatch)
        return d

def header(stdt,etdt,transporter,despatch):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    boldfonts(8)
    c.drawCentredString(310, 810, "Transporter wise despatch summary From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    p=page()
    c.drawString(500,800,"Page No."+str(p))
    c.line(0, 790, 650, 790)
    c.line(0, 770, 650, 770)
    c.drawString(10, 778, "Company")
    c.drawString(440, 778, "Quantity")
    c.drawString(500, 778, "Freight")
    c.drawString(540, 778, "Service tax")

def data(result,d):
    fonts(8)
    if result['TRANSPORTER']!=None:
        c.drawString(20, d, str(result['TRANSPORTER']))
    if result['QUANTITY']!=None:
        c.drawAlignedString(460, d, str(result['QUANTITY']))
    if result['FREIGHT']!=None:
        c.drawAlignedString(520, d, str(result['FREIGHT']))
    partytotal(result)
    brokertotal(result)

def partytotal(result):
    global TotalPartyQty
    global TotalPartyAmt
    TotalPartyQty=TotalPartyQty+float(float("%.2f"%float(result['QUANTITY'])))
    TotalPartyAmt=TotalPartyAmt+(float("%.2f"%float(result['FREIGHT'])))


def brokertotal(result):
    global TotalBrokerQty
    global TotalBrokerAmt
    if result['QUANTITY']!=None:
        TotalBrokerQty=TotalBrokerQty+(float("%.2f"%float(result['QUANTITY'])))
    if result['FREIGHT']!=None:
        TotalBrokerAmt=TotalBrokerAmt+(float("%.2f"%float(result['FREIGHT'])))

def partytotalprint(d,stdt,etdt):
    global TotalPartyQty
    global TotalPartyAmt

    c.drawString(10,d,"Despatch Total :")
    c.drawAlignedString(235,(d-5),str(round(TotalPartyQty,3)))
    c.drawAlignedString(295,(d-5),str(round(TotalPartyAmt,2)))
    TotalPartyQty=0
    TotalPartyAmt=0

def brokertotalprint(d,stdt,etdt):
    boldfonts(9)
    global TotalBrokerQty
    global TotalBrokerAmt

    c.drawString(10,(d),"Company Total:")
    c.drawAlignedString(460,(d),str(round(TotalBrokerQty,3)))
    c.drawAlignedString(520,(d),str(round(TotalBrokerAmt,2)))
    TotalBrokerQty=0
    TotalBrokerAmt=0

def logic(result):
    transporter.append(result['COMPANY'])

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global transporter
    global pageno
    global despatch
    global party
    global TotalBrokerAmt
    global TotalBrokerQty
    global TotalPartyAmt
    global TotalPartyQty
    global d
    d = 760
    transporter=[]
    pageno=0
    despatch=[]
    party=[]
    TotalPartyQty=0
    TotalBrokerQty=0
    TotalPartyAmt=0
    TotalBrokerAmt=0

def companyclean():
    global pageno
    global TotalBrokerAmt
    global TotalBrokerQty
    global TotalPartyAmt
    global TotalPartyQty
    pageno =0
    TotalPartyQty=0
    TotalBrokerQty=0
    TotalPartyAmt=0
    TotalBrokerAmt=0

def dlocvalue(d):
    d=d-20
    return d


def textsize(c,result, d, stdt, etdt):
    d=dvalue(stdt, etdt, transporter)
    logic(result)
    if len(transporter) == 1:
        header(stdt,etdt,transporter,despatch)
        c.drawString(10,d,result['COMPANY'])
        d= dvalue(stdt, etdt, transporter)
        data(result, d)                

    elif transporter[-1] == transporter[-2]:
        data(result, d)
                
    elif transporter[-1] != transporter[-2]:
        fonts(7)          
        brokertotalprint(d,stdt,etdt)
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, transporter,despatch)
        d=newpage()
        c.drawString(10,d,result['COMPANY'])
        d= dvalue(stdt, etdt, transporter)
        data(result,d)         
           