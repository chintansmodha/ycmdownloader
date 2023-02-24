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

company=[]
asset=[]
mainaccount=[]
account=[]


def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

TotalPartyAmt=0
TotalcompanyAmt=0
pageno=0

grdQty=0
grdFrt=0

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

def dvalue(stdt, etdt, company):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, company,despatch)
        return d

def header(stdt,etdt,company,asset):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    boldfonts(8)
    c.drawCentredString(310, 810, "company wise despatch summary From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
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
    if result['company']!=None:
        c.drawString(20, d, str(result['company']))
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
    global grdQty
    global grdFrt
    if result['QUANTITY']!=None:
        TotalBrokerQty=TotalBrokerQty+(float("%.2f"%float(result['QUANTITY'])))
        grdQty=grdQty+(float("%.2f"%float(result['QUANTITY'])))
    if result['FREIGHT']!=None:
        TotalBrokerAmt=TotalBrokerAmt+(float("%.2f"%float(result['FREIGHT'])))
        grdFrt=grdFrt+(float("%.2f"%float(result['FREIGHT'])))

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

def grandtotalprint(d,stdt,etdt):
    boldfonts(9)
    global grdFrt
    global grdQty

    c.drawString(10,(d),"Grand Total:")
    c.drawAlignedString(460,(d),str(round(grdQty,2)))
    c.drawAlignedString(520,(d),str(round(grdFrt,2)))
    grdFrt=0
    grdQty=0

def logic(result):
    company.append(result['COMPANY'])
    asset.append(result['GLTYPE'])
    mainaccount.append(result['MAINACCOUNT'])
    account.append(result['ACCOUNT'])

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global company
    global pageno
    global asset
    global mainaccount
    global account
    global TotalBrokerAmt
    global TotalBrokerQty
    global TotalPartyAmt
    global TotalPartyQty
    global d
    d = 760
    company=[]
    pageno=0
    asset=[]
    mainaccount=[]
    account=[]
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
    global company
    global despatch
    global party
    company=[]
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


def textsize(c,result, d,opbal, stdt, etdt):
    d=dvalue(stdt, etdt, company)
    logic(result)
    if len(company) == 1:
        header(stdt,etdt,company,asset)
        c.drawString(10,d,result['COMPANY'])
        d= dvalue(stdt, etdt, company)
        data(result, d)                

    elif company[-1] == company[-2]:
        if asset[-1] == asset[-2]:
            if mainaccount[-1] == mainaccount[-2]:
                if account[-1] == account[-2]:
                    data(result, d)
                elif account[-1] != account[-2]:
                    printAccountTotal(d)
                    d= dvalue(stdt, etdt, company)
                    d= dvalue(stdt, etdt, company)
                    data(d)
            elif mainaccount[-1] != mainaccount[-2]:
                printAccountTotal(d)
                d= dvalue(stdt, etdt, company)
                d= dvalue(stdt, etdt, company)
                printMainAccountTotal()
                d= dvalue(stdt, etdt, company)
                d= dvalue(stdt, etdt, company)
                data(d)
        elif asset[-1] == asset[-2]:
            printAccountTotal(d)
            d= dvalue(stdt, etdt, company)
            d= dvalue(stdt, etdt, company)
            printMainAccountTotal()
            d= dvalue(stdt, etdt, company)
            d= dvalue(stdt, etdt, company)
            printAssetTotal()
            c.setPageSize(A4)
            c.showPage()
            header(stdt, etdt, company,asset)
            d=newpage()
            data(d)
                
                
    elif company[-1] != company[-2]:
        printAccountTotal(d)
        d= dvalue(stdt, etdt, company)
        d= dvalue(stdt, etdt, company)
        printMainAccountTotal()
        d= dvalue(stdt, etdt, company)
        d= dvalue(stdt, etdt, company)
        printAssetTotal()
        d= dvalue(stdt, etdt, company)
        d= dvalue(stdt, etdt, company)
        printCompanyTotal()
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, company,asset)
        d=newpage()
        data(d)
           