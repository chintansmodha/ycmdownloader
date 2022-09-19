from FormLoad import PackingMaterialLedger_FormLoad as PMLFL
from reportlab.lib.pagesizes import portrait, A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from datetime import datetime
import textwrap

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(portrait(A3)))
c.setPageSize(portrait(A3))
d = 730
no=0
pageno=0
plantcode=[]
itemtype=[]
supplier=[]
Balance = []
Balances = 0
GrandReceivedTotal=0
GrandIssuedTotal=0
ReceivedQuantityTotal=0
IssuedQuantityTotal=0

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

def dvalue(stdt, etdt,result, plantcode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,result,d ,plantcode[:-1])
        return d

def header(stdt,etdt,d,result,plantcode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, plantcode[-1])
    fonts(9)
    format = '%d-%m-%Y %I:%M %p'
    datestring = datetime.now(tz=None)
    date = datetime.strftime(datestring, format)
    c.drawString(10, 770, date)
    boldfonts(9)
    c.drawCentredString(300, 780, "Packing Material Ledger From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    fonts(9)
    c.line(0, 760, 1000, 760)
    c.line(0, 740, 1000, 740)
    c.drawString(10, 750, str("DATE"))
    c.drawString(50, 750, str("TYPE"))
    c.drawString(100, 750, str("DOC. NUMBER"))
    c.drawString(180, 750, str("CHAL/EXCINV. NO"))
    c.drawString(280, 750, str("CHAL/EXCINV. DATE"))
    c.drawString(400, 750, str("RECD QTY"))
    c.drawString(460, 750, str("ISS. QTY"))
    c.drawString(520, 750, str("BALANCE"))
    c.drawString(10, 730, str("CUSTOMER:"))
    c.drawString(70, 730, str(result['CUSTOMER']))
    c.drawString(300, 730, str("PALLETE TYPE:"))
    f = 730
    if len(str(result['PALLETNAME'])) > 45:

        lines = textwrap.wrap(str(result['PALLETNAME']), 45, break_long_words=False)
        for i in lines:
            c.drawString(370, f, str(i))
            f = f - 10
    else:
        c.drawString(370, f, str(result['PALLETNAME']))
        f = f - 10

def data(stdt,etdt,result,d):
    # d=620
    global no
    no = no + 1
    fonts(7)
    c.drawString(10, d, str(result['INVDATE'].strftime('%d-%m-%Y')))
    c.drawString(50, d, str(result['TYPEOF']))
    c.drawString(100, d, str(result['INVNO']))
    c.drawString(180, d, str(""))
    c.drawString(280, d, str(""))
    c.drawAlignedString(430, d, str(("%.0f" % float(result['RECEIVEDQUANTITY']))))
    c.drawAlignedString(490, d, str(("%.0f" % float(result['ISSUEDQUANTITY']))))
    # c.drawString(520, d, str(("%.0f" % float(result['BALANCE']))))
    total(result)
    return d

def total(result):
    global GrandReceivedTotal
    global GrandIssuedTotal
    global ReceivedQuantityTotal
    global IssuedQuantityTotal
    GrandReceivedTotal = GrandReceivedTotal + float("%.0f" % float(result['RECEIVEDQUANTITY']))
    GrandIssuedTotal = GrandIssuedTotal + float("%.0f" % float(result['ISSUEDQUANTITY']))
    ReceivedQuantityTotal=ReceivedQuantityTotal+float("%.0f" % float(result['RECEIVEDQUANTITY']))
    IssuedQuantityTotal = IssuedQuantityTotal + float("%.0f" % float(result['ISSUEDQUANTITY']))

def grandtotal():
    boldfonts(7)
    global GrandReceivedTotal
    global GrandIssuedTotal
    c.drawString(10, d, str(plantcode[-1]) + " TOTAL : ")
    c.drawAlignedString(430, d, str("%.0f" % float(GrandReceivedTotal)))
    c.drawAlignedString(490, d, str(("%.0f" % float(GrandIssuedTotal))))
    fonts(7)

def printtotal(d):
    # d = 620
    global ReceivedQuantityTotal
    global IssuedQuantityTotal
    boldfonts(7)
    c.drawAlignedString(430, d , str(("%.0f" % float(ReceivedQuantityTotal))))
    c.drawAlignedString(490, d , str(("%.0f" % float(IssuedQuantityTotal))))
    ReceivedQuantityTotal=0
    IssuedQuantityTotal=0
    fonts(7)
    boldfonts(7)
    c.drawString(280, d, "PALLETE TYPE TOTAL:")
    fonts(7)


def companyclean():
    global GrandReceivedTotal
    global GrandIssuedTotal
    GrandReceivedTotal=0
    GrandIssuedTotal=0


def newpage():
    global d
    d = 720
    return d

def logic(result):
    plantcode.append(result['PLANTNAME'])
    itemtype.append(result['PALLETNAME'])
    supplier.append(result['CUSTOMER'])
    Balance.append(result['BALANCE'])

def newrequest():
    global plantcode
    global itemtype, Balance
    global no
    global pageno
    pageno=0
    no = 0
    plantcode=[]
    itemtype=[]
    Balance = []

def textsize(c, result, d, stdt, etdt):
    # print(result['PALLETNAME'])
    d = dvalue(stdt, etdt, result, plantcode)
    logic(result)
    global no,Balances
    if len(plantcode) == 1:
        Balances = 0
        header(stdt, etdt, d, result, plantcode)
        data(stdt, etdt, result, d)
        Balances = Balances + float(Balance[-1])
        c.drawAlignedString(550, d, str(("%.0f" % float(Balances))))
    elif plantcode[-2] == plantcode[-1]:
        if itemtype[-1] == itemtype[-2]:
            data(stdt, etdt, result, d)
            Balances = Balances + float(Balance[-1])
            c.drawAlignedString(550, d, str(("%.0f" % float(Balances))))

        elif itemtype[-1] != itemtype[-2]:
            Balances = 0
            printtotal(d)
            d = dvalue(stdt, etdt, result, plantcode)
            fonts(9)
            d = dvalue(stdt, etdt, result, plantcode)
            c.drawString(10, d, str("CUSTOMER:"))
            c.drawString(70, d, str(supplier[-1]))
            c.drawString(300, d, str("PALLETE TYPE:"))
            if len(str(itemtype[-1])) > 45:

                lines = textwrap.wrap(str(itemtype[-1]), 45, break_long_words=False)
                for i in lines:
                    c.drawString(370, d, str(i))
                    d = d - 10
            else:
                c.drawString(370, d, str(itemtype[-1]))
                d = d - 10
            d = dvalue(stdt, etdt, result, plantcode)
            data(stdt, etdt, result, d)
            Balances = Balances + float(Balance[-1])
            c.drawAlignedString(550, d, str(("%.0f" % float(Balances))))

    elif plantcode[-2] != plantcode[-1]:
        Balances = 0
        printtotal(d)
        d = dvalue(stdt, etdt, result, plantcode)
        no = 0
        grandtotal()
        companyclean()
        c.showPage()
        d = newpage()
        header(stdt, etdt, d,result, plantcode)
        data(stdt, etdt, result, d)
        Balances = Balances + float(Balance[-1])
        c.drawAlignedString(550, d, str(("%.0f" % float(Balances))))