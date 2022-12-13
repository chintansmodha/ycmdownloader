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

divisioncode=[]
agentgroup=[]
party=[]
item=[]

TotalPartyQty=0
TotalBrokerQty=0
TotalPartyAmt=0
TotalBrokerAmt=0
ItemTotalAmt=0
ItemTotalQty=0
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
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, divisioncode)
        return d

def header(stdt,etdt,divisioncode):
    fonts(9)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(310, 820, divisioncode[-1]) 
    fonts(8)
    c.drawCentredString(310, 810, "BrokerWiseSalesSummary From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    c.drawCentredString(310,800,agentgroup[-1])
    now = datetime.now()
    c.drawString(15,800,""+str(now))
    p=page()
    c.drawString(500,800,"Page No."+str(p))
    c.line(0, 790, 650, 790)
    c.line(0, 770, 650, 770)
    c.drawString(30, 778, "Item Name")
    c.drawString(400, 778, "Quantity")
    c.drawString(550, 778, "Ammount")

def data(result,d):
    fonts(8)
    if result['ITEM']!=None:
        c.drawString(30, d, str(result['ITEM']))
    if result['QUANTITY']!=None:
        c.drawAlignedString(410, d, str(result['QUANTITY']))
    if result['AMOUNT']!=None:
        c.drawAlignedString(560, d, str(result['AMOUNT']))
    partytotal(result)
    brokertotal(result)


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

    c.line(390,(d+5),590,(d+5))
    c.drawString(315,(d-5),"Total Party QTY:")
    c.drawString(460,(d-5),"Total Party Amt:")
    c.drawAlignedString(410,(d-5),str(round(TotalPartyQty,3)))
    c.drawAlignedString(560,(d-5),str(round(TotalPartyAmt,2)))

    c.line(390,(d-10),590,(d-10))
    TotalPartyQty=0
    TotalPartyAmt=0

def brokertotalprint(d,stdt,etdt):
    global TotalBrokerQty
    global TotalBrokerAmt

    c.drawAlignedString(380,(d),"Total Broker QTY:")
    c.drawAlignedString(520,(d),"Total Broker Amt:")
    c.drawAlignedString(410,(d),str(round(TotalBrokerQty,3)))
    c.drawAlignedString(560,(d),str(round(TotalBrokerAmt,2)))
    c.line(390,(d-5),590,(d-5))
    TotalBrokerQty=0
    TotalBrokerAmt=0

def logic(result):
    divisioncode.append(result['COMPANY'])
    agentgroup.append(result['AGENTGROUP'])
    party.append(result['PARTY'])
    item.append(result['ITEM'])

def newpage():
    global d
    d = 740
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
    d = 760
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
    pageno =0
    TotalPartyQty=0
    TotalBrokerQty=0
    TotalPartyAmt=0
    TotalBrokerAmt=0

def dlocvalue(d):
    d=d-20
    return d


def textsize(c,result, d, stdt, etdt):
    d=dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(item)==1:
            if len(agentgroup) == 1:
                if len(party) == 1:
                    header(stdt,etdt,divisioncode)
                    c.drawString(10,d,agentgroup[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    c.drawString(10,d,party[-1])
                    d = dvalue(stdt, etdt, divisioncode)
                    data(result, d)                

    elif divisioncode[-1] == divisioncode[-2]:
        if item[-1] == item[-2]:
            if agentgroup[-1] == agentgroup[-2]:
                if party[-1] == party[-2]:
                    data(result, d)
        elif item[-1]!=[-2]:
            if party[-1] != party[-2]:
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
                partytotalprint(d,stdt,etdt)        
                d = dvalue(stdt, etdt, divisioncode)        
                c.drawString(10, d, str(party[-1]))
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
                d = dvalue(stdt, etdt, divisioncode)
                
    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        d=dvalue(stdt, etdt, divisioncode)
        partytotalprint(d,stdt,etdt)
        d=dvalue(stdt, etdt, divisioncode)
        d = dvalue(stdt, etdt, divisioncode)           
        brokertotalprint(d,stdt,etdt)
        d = dvalue(stdt, etdt, divisioncode)
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, divisioncode)
        d=newpage()

        c.drawString(10, d, str(agentgroup[-1]))
        d = dvalue(stdt, etdt, divisioncode)
        c.drawString(10, d, str(party[-1]))
        d= dvalue(stdt, etdt, divisioncode)
        data(result,d)

        # if agentgroup[-1] != agentgroup[-2]:
        #     c.drawString(10, d, str(agentgroup[-1]))
        #     d = dvalue(stdt, etdt, divisioncode)
        #     if party[-1] == party[-2]:
        #         data(result,d)

        #     elif party[-1] != party[-2]:
        #         c.drawString(10, d, str(party[-1]))
        #         d = dvalue(stdt, etdt, divisioncode)
        #         data(result, d)
        #         d = dvalue(stdt, etdt, divisioncode)
        #         partytotalprint(d,stdt,etdt)
        #         d = dvalue(stdt, etdt, divisioncode)
        #         d = dvalue(stdt, etdt, divisioncode)
        #         brokertotalprint(d,stdt,etdt)

            
          
           