from reportlab.lib.pagesizes import  landscape,A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import datetime 

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 505

divisioncode=[]
agentgroup=[]
party=[]

TotalPartyQty=0
TotalBrokerQty=0
TotalPartyAmt=0
TotalBrokerAmt=0
pageno=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(landscape(A4))
        c.showPage()
        header(stdt, etdt, divisioncode,agentgroup)
        return d

def partytotal(result):
    global TotalPartyQty
    global TotalPartyAmt
    TotalPartyQty=TotalPartyQty+float(float("%.2f"%float(result['QUANTITY'])))
    TotalPartyAmt=TotalPartyAmt+(float("%.2f"%float(result['AMOUNT'])))


def brokertotal(result):
    global TotalBrokerQty
    global TotalBrokerAmt
    if result['QUANTITY']!=None:
        TotalBrokerQty=TotalBrokerQty+(float("%.2f"%float(result['QUANTITY'])))
    if result['AMOUNT']!=None:
        TotalBrokerAmt=TotalBrokerAmt+(float("%.2f"%float(result['AMOUNT'])))

def partytotalprint(d,stdt,etdt):
    global TotalPartyQty
    global TotalPartyAmt

    c.line(610,(d+5),830,(d+5))
    c.drawString(550,(d-5),"Total Party QTY:")
    c.drawString(700,(d-5),"Total Party Amt:")
    c.drawAlignedString(650,(d-5),str(round(TotalPartyQty,3)))
    c.drawAlignedString(810,(d-5),str(round(TotalPartyAmt,2)))

    c.line(610,(d-10),830,(d-10))
    TotalPartyQty=0
    TotalPartyAmt=0

def brokertotalprint(d,stdt,etdt):
    global TotalBrokerQty
    global TotalBrokerAmt

    c.drawAlignedString(620,(d),"Total Broker QTY:")
    c.drawAlignedString(760,(d),"Total Broker Amt:")
    c.drawAlignedString(650,(d),str(round(TotalBrokerQty,3)))
    c.drawAlignedString(810,(d),str(round(TotalBrokerAmt,2)))
    c.line(610,(d-5),830,(d-5))
    TotalBrokerQty=0
    TotalBrokerAmt=0

def logic(result):
    divisioncode.append(result['COMPANY'])
    agentgroup.append(result['AGENTGROUP'])
    party.append(result['PARTY'])

def newpage():
    global d
    d = 505
    return d

def newrequest():
    global divisioncode
    global pageno
    global agentgroup
    global party
    global TotalBrokerAmt
    global TotalBrokerQty
    global TotalPartyAmt
    global TotalPartyQty
    global d
    d = 505
    divisioncode=[]
    pageno=0
    agentgroup=[]
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
    global divisioncode
    global agentgroup
    global party
    TotalPartyQty=0
    TotalBrokerQty=0
    TotalPartyAmt=0
    TotalBrokerAmt=0
    divisioncode=[]
    pageno=0
    agentgroup=[]
    party=[]
   

def dlocvalue(d):
    d=d-20
    return d


def header(stdt,etdt,divisioncode,agentgroup):
    fonts(9)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(450, 580, divisioncode[-1]) 
    fonts(8)
    c.drawCentredString(450, 560, "PartyWiseAgentLiftingMiniatureCopyNo From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    # c.drawCentredString(450,530,agentgroup[-1])
    now = datetime.now()
    c.drawString(15,550,""+str(now))
    p=page()
    c.drawString(800,550,"Page No."+str(p))
    c.line(0, 540, 850, 540)
    c.line(0, 515, 850, 515)
    c.drawString(10, 525, "Voucher No.")
    c.drawString(80, 525, "Voucher Date")
    c.drawString(160, 525, "Invoice No.")
    c.drawString(220, 525, "Invoice Date")
    c.drawString(470, 525, "Invoice Amt.")
    c.drawString(620, 525, "OutStanding")
    c.drawString(700, 525, "Rate")
    c.drawString(770, 525, "INV Ammount")

def data(result,d):
    fonts(8)
    if result['INVNO']!=None:
        c.drawString(10, d, str(result['INVNO']))
    if result['INVDATE']!=None:
        c.drawString(80, d, str(result['INVDATE']))
    if result['LRNO']!=None:
        c.drawString(160, d, str(result['LRNO']))
    if result['ITEM']!=None:
        c.drawString(210, d, str(result['ITEM']))
    if result['TRANSPORTER']!=None:
        c.drawString(455, d, str(result['TRANSPORTER']))
    if result['QUANTITY']!=None:
        c.drawAlignedString(640, d, str(result['QUANTITY']))
    if result['RATE']!=None:
        c.drawAlignedString(710, d, str(result['RATE']))
    if result['AMOUNT']!=None:
        c.drawAlignedString(805, d, str(result['AMOUNT']))
    partytotal(result)
    brokertotal(result)



def textsize(c,result, d, stdt, etdt):
    d=dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(agentgroup) == 1:
            if len(party) == 1:
                header(stdt,etdt,divisioncode,agentgroup)
                c.drawString(10,d,agentgroup[-1])
                d = dvalue(stdt, etdt, divisioncode)
                c.drawString(10,d,party[-1])
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)                

    elif divisioncode[-1] == divisioncode[-2]:
        if agentgroup[-1] == agentgroup[-2]:
            if party[-1] == party[-2]:
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)

            elif party[-1] != party[-2]:
                d = dvalue(stdt, etdt, divisioncode)                
                partytotalprint(d,stdt,etdt)
                d = dvalue(stdt, etdt, divisioncode)                
                d = dvalue(stdt, etdt, divisioncode)                
                c.drawString(10, d, str(party[-1])) 
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
                d = dvalue(stdt, etdt, divisioncode)

           
        elif agentgroup[-1] != agentgroup[-2]:
            d = dvalue(stdt, etdt, divisioncode)  
            partytotalprint(d,stdt,etdt)
            d = dvalue(stdt, etdt, divisioncode)    
            d = dvalue(stdt, etdt, divisioncode)       
            brokertotalprint(d,stdt,etdt)
            d = dvalue(stdt, etdt, divisioncode)
            c.drawString(10, d, str(agentgroup[-1]))
            d = dvalue(stdt, etdt, divisioncode)
            c.drawString(10, d, str(party[-1]))
            d = dvalue(stdt, etdt, divisioncode)
            if party[-1] == party[-2]:
                data(result,d)
              

            elif party[-1] != party[-2]:
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
            
                
    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        d=dvalue(stdt, etdt, divisioncode)
        partytotalprint(d,stdt,etdt)
        d=dvalue(stdt, etdt, divisioncode)
        d = dvalue(stdt, etdt, divisioncode)           
        brokertotalprint(d,stdt,etdt)
        d = dvalue(stdt, etdt, divisioncode)
        c.setPageSize(landscape(A4))
        c.showPage()
        header(stdt, etdt, divisioncode,agentgroup)
        d=newpage()

        c.drawString(10, d, str(agentgroup[-1]))
        d = dvalue(stdt, etdt, divisioncode)
        c.drawString(10, d, str(party[-1]))
        d= dvalue(stdt, etdt, divisioncode)
        data(result,d)

            
          
           