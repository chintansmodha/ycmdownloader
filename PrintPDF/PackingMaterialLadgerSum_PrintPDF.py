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
opQty = 0
rQty = 0
IssueQty = 0
PalletBalance = 0
DepopQty = 0
DeprQty = 0
DepIssueQty = 0
DepBalance = 0


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
        d = d - 5
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
    fonts(9)
    c.drawCentredString(300, 780,"Packing Material Ledger Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    fonts(9)
    c.line(0, 760, 1000, 760)
    c.line(0, 740, 1000, 740)
    c.drawString(40, 745, "Supplier")
    c.drawString(350, 745, 'Op. Qty.')
    c.drawString(410, 745, 'Rec. Qty.')
    c.drawString(470, 745, 'Iss. Qty.')
    c.drawString(550, 745, 'Bal. Qty.')

def data(stdt,etdt,result,d):
    fonts(7)
    c.drawString(40, d, str(result['SUPPLIER']))
    c.drawAlignedString(365, d, str(int(float(result['OPQTY']))))
    c.drawAlignedString(425, d, str(int(float(result['RECDQTY']))))
    c.drawAlignedString(485, d, str(int(float(result['ISSQTY']))))
    c.drawAlignedString(565, d, str(int(float(result['BALANCE']))))
    Pallettotal(result)

def Pallettotal(result):
    global opQty, rQty, IssueQty, PalletBalance
    global DepopQty, DeprQty, DepIssueQty,DepBalance
    opQty = opQty + float(result['OPQTY'])
    rQty = rQty + float(result['RECDQTY'])
    IssueQty = IssueQty + float(result['ISSQTY'])
    PalletBalance = PalletBalance + float(result['BALANCE'])
    DepopQty = DepopQty + float(result['OPQTY'])
    DeprQty = DeprQty + float(result['RECDQTY'])
    DepIssueQty = DepIssueQty + float(result['ISSQTY'])
    DepBalance = DepBalance + float(result['BALANCE'])

def PalletTotalPrint(d):
    global opQty, rQty, IssueQty, PalletBalance
    fonts(7)
    c.drawString(40, d, 'Pallet Type Total: ')
    c.drawAlignedString(365, d, str(int(float(opQty))))
    c.drawAlignedString(425, d, str(int(float(rQty))))
    c.drawAlignedString(485, d, str(int(float(IssueQty))))
    c.drawAlignedString(565, d, str(int(float(PalletBalance))))
    opQty = 0
    rQty = 0
    IssueQty = 0
    PalletBalance = 0
    fonts(8)

def DepTotalPrint(d):
    global DepopQty, DeprQty, DepIssueQty,DepBalance
    fonts(7)
    c.drawString(40, d, 'Department Total: ')
    c.drawAlignedString(365, d, str(int(float(DepopQty))))
    c.drawAlignedString(425, d, str(int(float(DeprQty))))
    c.drawAlignedString(485, d, str(int(float(DepIssueQty))))
    c.drawAlignedString(565, d, str(int(float(DepBalance))))
    DepopQty = 0
    DeprQty = 0
    DepIssueQty = 0
    DepBalance = 0
    fonts(8)

def newpage():
    global d
    d = 730
    return d

def logic(result):
    plantcode.append(result['PLANTNAME'])
    itemtype.append(result['PALLETENAME'])
    supplier.append(result['SUPPLIER'])

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
    d = dvalue(stdt, etdt, result, plantcode)
    logic(result)
    global no, Balances
    if len(plantcode)==1:
        Balances = 0
        header(stdt,etdt,d,result,plantcode)
        fonts(8)
        c.drawString(10, d, str(itemtype[-1]))
        d = dvalue(stdt, etdt, result, plantcode)
        d = dvalue(stdt, etdt, result, plantcode)
        data(stdt,etdt,result,d)

    elif plantcode[-1] == plantcode[-2]:
        if itemtype[-1] == itemtype[-2]:
            data(stdt,etdt,result,d)

        elif itemtype[-1] != itemtype[-2]:
            PalletTotalPrint(d)
            d = dvalue(stdt, etdt, result, plantcode)
            d = dvalue(stdt, etdt, result, plantcode)
            fonts(8)
            c.drawString(10, d, str(itemtype[-1]))
            d = dvalue(stdt, etdt, result, plantcode)
            d = dvalue(stdt, etdt, result, plantcode)
            data(stdt, etdt, result, d)

    elif plantcode[-1] != plantcode[-2]:
        PalletTotalPrint(d)
        d = dvalue(stdt, etdt, result, plantcode)
        d = dvalue(stdt, etdt, result, plantcode)
        DepTotalPrint(d)
        c.showPage()
        d = newpage()
        d = dvalue(stdt, etdt, result, plantcode)
        header(stdt, etdt, d, result, plantcode)
        fonts(8)
        c.drawString(10, d, str(itemtype[-1]))
        d = dvalue(stdt, etdt, result, plantcode)
        d = dvalue(stdt, etdt, result, plantcode)
        data(stdt, etdt, result, d)