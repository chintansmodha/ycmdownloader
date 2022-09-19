import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, portrait, A4, A1, A2, A0, A5,A3,A6, A7
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialItalic', 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBoldItalic', 'arialbi.ttf'))

c = canvas.Canvas("1.pdf")
c.setPageSize(portrait(A4))

d = 755
i = 1
pageno = 0
pageSize = 0
Xaxis = 0
Yaxis = 0

divisioncode = []
Itemname = []
LotNo = []
BaseLot = []

NetQty = 0
ConsQty = 0
StockQty = 0
TotalNetQty = 0
TotalConsQty = 0
TotalStockQty = 0

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

def dvalue(stdt,etdt,result, divisioncode):
    global d
    if d > 20:
        d = d - 5
        return d
    else:
        d = newpage()
        # c.setPageSize(landscape(A4))
        c.showPage()
        header(stdt, etdt, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        return d

def dvalueincrese():
    global d
    if d > 30 and d < 745:
        d = d + 10
    else:
        pass
    return d

def wrap(string, type, width, x, y, result, stdt, etdt):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        e = e + 1
        if e < len(wrap_text):
            y = dvalue(stdt,etdt,result, divisioncode)
            y = dvalue(stdt,etdt,result, divisioncode)



def header(stdt, etdt, divisioncode):
    c.setTitle('GenerateGainLossReport(ItemWise)')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    # c.drawString(10, Yaxis, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 785, "Generate Gain/Loss(LotWise) Report From  " + str(stdt.strftime(' %d  %B  %Y'))
    + ' To ' + str(etdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 785, "Page No." + str(p))
    # c.setDash(2,3)
    c.line(0, 780, 600, 780)
    c.line(0, 760, 600, 760)
    # Upperline in header
    # fonts(8)
    c.drawString(30, 765, 'Lot No. ')
    c.drawString(140, 765, 'ProductionQty ')
    c.drawString(220, 765, 'BaseLot ')
    c.drawString(300, 765, 'BOMPer ')
    c.drawString(390, 765, 'ConsumedQty ')
    c.drawString(510, 765, 'BaseLotStockQty ')


def data(result, d, stdt, etdt, divisioncode):
    fonts(7)
    c.drawString(221, d, str(result['BASELOT']))
    if result['INPUTPERC'] != None:
        c.drawAlignedString(320, d, str(result['INPUTPERC']))
    if result['CONSUMENETWT'] != None:
        c.drawAlignedString(415, d, str(result['CONSUMENETWT']))
    if len(Itemname) == 1:
        c.drawString(31, d, str(LotNo[-1]))
        c.drawAlignedString(170, d, str(result['NETWT']))
        if result['STKQTY'] != None:
            c.drawAlignedString(540, d, str(result['STKQTY']))
        ItemNetQty(result)
        TotalNetDeptQty(result)
        ItemStkQty(result)
        TotalStkDeptQty(result)
    elif Itemname[-1] == Itemname[-2]:
        if LotNo[-1] != LotNo[-2]:
            c.drawString(31, d, str(LotNo[-1]))
            c.drawAlignedString(170, d, str(result['NETWT']))
            ItemNetQty(result)
            TotalNetDeptQty(result)
        if BaseLot[-1] != BaseLot[-2]:
            if result['STKQTY'] != None:
                c.drawAlignedString(540, d, str(result['STKQTY']))
                ItemStkQty(result)
                TotalStkDeptQty(result)
    elif Itemname[-1] != Itemname[-2]:
        c.drawString(31, d, str(LotNo[-1]))
        c.drawAlignedString(170, d, str(result['NETWT']))
        if result['STKQTY'] != None:
            c.drawAlignedString(540, d, str(result['STKQTY']))
        ItemNetQty(result)
        TotalNetDeptQty(result)
        ItemStkQty(result)
        TotalStkDeptQty(result)
    ItemTotal(result)
    Total(result)


def logic(result):
    global divisioncode
    global Itemname
    global LotNo
    global BaseLot
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])
    LotNo.append(result['LOTNO'])
    BaseLot.append(str(result['BASELOT']))

def newpage():
    global d
    d = 755
    return d

def newrequest():
    global divisioncode
    global Itemname
    global LotNo
    global pageSize
    global pageno
    divisioncode = []
    pageno = 0
    Itemname = []
    LotNo = []
    pageSize = 0

def ItemNetQty(result):
    global NetQty
    NetQty += float(result['NETWT'])

def TotalNetDeptQty(result):
    global TotalNetQty
    TotalNetQty += float(result['NETWT'])

def ItemStkQty(result):
    global StockQty
    if result['STKQTY'] != None:
        StockQty += float(result['STKQTY'])

def TotalStkDeptQty(result):
    global TotalStockQty
    if result['STKQTY'] != None:
        TotalStockQty += float(result['STKQTY'])

def ItemTotal(result):
    global ConsQty, StockQty
    if result['CONSUMENETWT'] != None:
        ConsQty += float(result['CONSUMENETWT'])

def Total(result):
    global TotalConsQty
    if result['CONSUMENETWT'] != None:
        TotalConsQty += float(result['CONSUMENETWT'])

def PrintItemTotal():
    boldfonts(7)
    global NetQty, ConsQty, StockQty
    c.drawString(50, d, 'Item Total: ')
    c.drawAlignedString(170, d , str('{0:1.3f}'.format(NetQty)))
    c.drawAlignedString(415, d , str('{0:1.3f}'.format(ConsQty)))
    # c.drawAlignedString(540, d, str('{0:1.3f}'.format(StockQty)))
    NetQty = 0
    ConsQty = 0
    StockQty = 0
    fonts(7)

def PrintTotal():
    boldfonts(7)
    global TotalNetQty, TotalConsQty, TotalStockQty
    c.drawString(50, d, 'Department Total: ')
    c.drawAlignedString(170, d, str('{0:1.3f}'.format(TotalNetQty)))
    c.drawAlignedString(415, d, str('{0:1.3f}'.format(TotalConsQty)))
    # c.drawAlignedString(540, d, str('{0:1.3f}'.format(TotalStockQty)))
    TotalNetQty = 0
    TotalConsQty = 0
    TotalStockQty = 0
    fonts(7)


def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt,etdt,result, divisioncode)
    logic(result)
    # print('rohit  ', A4)
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(31, d, Itemname[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] == divisioncode[-2]:
        if Itemname[-1] == Itemname[-2]:
            data(result, d, stdt, etdt, divisioncode)
        elif Itemname[-1] != Itemname[-2]:
            PrintItemTotal()
            boldfonts(7)
            d = dvalue(stdt, etdt, result, divisioncode)
            d = dvalue(stdt, etdt, result, divisioncode)
            d = dvalue(stdt, etdt, result, divisioncode)
            c.drawString(31, d, Itemname[-1])
            d = dvalue(stdt, etdt, result, divisioncode)
            d = dvalue(stdt, etdt, result, divisioncode)
            data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] != divisioncode[-2]:
        PrintItemTotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        PrintTotal()
        c.showPage()
        d = newpage()
        d = dvalue(stdt, etdt, result, divisioncode)
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(31, d, Itemname[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        data(result, d, stdt, etdt, divisioncode)
