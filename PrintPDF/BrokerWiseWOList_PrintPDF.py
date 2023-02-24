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
    c.drawCentredString(310, 820, transporter[-1]) 
    boldfonts(8)
    c.drawCentredString(310, 810, "Broker Wise Write Off List From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    p=page()
    c.drawString(500,800,"Page No."+str(p))
    c.line(0, 790, 650, 790)
    c.line(0, 770, 650, 770)
    c.drawString(10, 778, "Vch. Dt.")
    c.drawString(120, 778, "Chq. No.")
    c.drawString(230, 778, "Chq. Amt.")
    c.drawString(340, 778, "Breakup")
    c.drawString(450, 778, "Iss. Dt.")
    c.drawString(550, 778, "Adj. Amt.")

def data(result,d):
    fonts(8)
    if result['VCHDATE']!=None:
        c.drawString(10, d, str(result['VCHDATE']))
    if result['CHQNO']!=None:
        c.drawString(120, d, str(result['CHQNO']))
    if result['CHQAMT']!=None:
        c.drawAlignedString(250, d, str(result['CHQAMT']))
    if result['BREAKUP']!=None:
        c.drawString(340, d, str(result['BREAKUP']))
    if result['ISSDATE']!=None:
        c.drawString(450, d, str(result['ISSDATE']))
    if result['ADJAMT']!=None:
        c.drawAlignedString(570, d, str(result['ADJAMT']))
    partytotal(result)

def partytotal(result):
    global TotalPartyQty
    global TotalPartyAmt
    TotalPartyQty=TotalPartyQty+float(float("%.2f"%float(result['CHQAMT'])))
    TotalPartyAmt=TotalPartyAmt+(float("%.2f"%float(result['ADJAMT'])))


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
    boldfonts(8)
    c.drawString(10,d,"Cheque Total :")
    c.drawAlignedString(250,(d),str(round(TotalPartyQty,3)))
    c.drawAlignedString(570,(d),str(round(TotalPartyAmt,2)))
    TotalPartyQty=0
    TotalPartyAmt=0

def brokertotalprint(d,stdt,etdt):
    boldfonts(9)
    global TotalBrokerQty
    global TotalBrokerAmt

    c.drawString(10,(d),"Transporter Total:")
    c.drawAlignedString(235,(d),str(round(TotalBrokerQty,3)))
    c.drawAlignedString(295,(d),str(round(TotalBrokerAmt,2)))
    TotalBrokerQty=0
    TotalBrokerAmt=0

def logic(result):
    despatch.append(result['AGENTGROUP'])
    transporter.append(result['COMPANY'])
    party.append(result['AGENT'])

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
    global transporter
    global despatch
    global party
    transporter=[]
    party=[]
    despatch=[]
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
        if len(despatch) == 1:
            header(stdt,etdt,transporter,despatch)
            boldfonts(8)
            c.drawCentredString(310,d,despatch[-1])
            d = dvalue(stdt, etdt, transporter)
            c.drawString(10,d,party[-1])
            d = dvalue(stdt, etdt, transporter)
            data(result, d)                

    elif transporter[-1] == transporter[-2]:
        if despatch[-1] == despatch[-2]:
                data(result, d)
        elif despatch[-1] != despatch[-2]:
            boldfonts(8)
            d = dvalue(stdt, etdt, transporter)  
            partytotalprint(d,stdt,etdt)
            d = dvalue(stdt, etdt, transporter)    
            d = dvalue(stdt, etdt, transporter)
            c.drawCentredString(310,d,despatch[-1])
            d = dvalue(stdt, etdt, transporter)
            c.drawString(10,d,party[-1])
            d = dvalue(stdt, etdt, transporter)
            data(result, d)
                
    elif transporter[-1] != transporter[-2]:
        boldfonts(8)
        partytotalprint(d,stdt,etdt)
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, transporter,despatch)
        d=newpage()
        c.drawCentredString(310,d,despatch[-1])
        d = dvalue(stdt, etdt, transporter)
        c.drawString(10,d,party[-1])
        d = dvalue(stdt, etdt, transporter)
        data(result,d)         
           