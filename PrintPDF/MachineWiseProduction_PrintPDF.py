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
c.setPageSize(landscape(A3))

d = 760
i = 1
pageno = 0
pageSize = 0

divisioncode = []
Itemname = []
LotNo = []

st1 = 0
pq = 0
ss =0
others = 0
totals = 0
mth_st1 = 0
mth_pq = 0
mth_ss =0
mth_others = 0
mth_totals = 0
avgprod = 0


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
        c.setPageSize(landscape(A3))
        c.showPage()
        header(stdt, etdt, divisioncode)
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
    c.setTitle('MachineWiseProduction')
    fonts(15)
    # c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawString(30, 790, str((date.today()).strftime('%d/%m/%Y')))
    c.drawCentredString(421, 790, "Machine Wise Production on Date " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(700, 790, "Page No." + str(p))
    # c.setDash(2,3)
    c.line(0, 785, 1191, 785)
    c.line(0, 765, 1191, 765)
    # Upperline in header
    fonts(9)
    c.drawString(30, 770, 'Machine ')
    c.drawString(100, 770, 'Item Description ')
    c.drawString(300, 770, '1st')
    c.drawString(360, 770, 'PQ')
    c.drawString(420, 770, 'SS')
    c.drawString(480, 770, 'Others')
    c.drawString(560, 770, 'Total')
    c.drawString(600, 770, 'IInd %')
    c.drawString(680, 770, 'Mth. 1st')
    c.drawString(750, 770, 'Mth. PQ')
    c.drawString(820, 770, 'Mth. SS')
    c.drawString(890, 770, 'Mth. Others')
    c.drawString(980, 770, 'Mth. Total')
    c.drawString(1030, 770, 'Mth. IInd %')
    c.drawString(1110, 770, 'Mth. Avg.Prod.')



def data(result, d, stdt, etdt, divisioncode):
    fonts(7)
    c.drawString(31, d, str(result['MACHINE']))
    # c.drawString(101, d, str(result['ITEM']))
    c.drawAlignedString(300, d, str(result['TODAY_1STQTY']))
    c.drawAlignedString(360, d, str(result['TODAY_PQQTY']))
    c.drawAlignedString(420, d, str(result['TODAY_SSQTY']))
    c.drawAlignedString(490, d, str(result['TODAY_OTHERESQTY']))
    c.drawAlignedString(565, d, str(result['TODAY_TOTALQTY']))
    c.drawAlignedString(610, d, str(result['TODAY_IINDPERC']))
    c.drawAlignedString(700, d, str(result['MTH_1STQTY']))
    c.drawAlignedString(770, d, str(result['MTH_PQQTY']))
    c.drawAlignedString(840, d, str(result['MTH_SSQTY']))
    c.drawAlignedString(920, d, str(result['MTH_OTHERSQTY']))
    c.drawAlignedString(1000, d, str(result['MTH_TOTALQTY']))
    c.drawAlignedString(1050, d, str(result['MTH_IINDPERC']))
    c.drawAlignedString(1140, d, str(result['MTH_AVGPRO']))
    wrap(str(result['ITEM']),c.drawString,40,101,d,result,stdt,etdt)
    DepartmentTotal(result)


def logic(result):
    global divisioncode
    global Itemname
    global LotNo
    divisioncode.append(result['DEPARTMENT'])
    # Itemname.append(result['ITEM'])
    # LotNo.append(result['LOTNO'])

def newpage():
    global d
    d = 760
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

def DepartmentTotal(result):
    global st1,pq,ss,others,totals,mth_st1,mth_pq,mth_ss,mth_others,mth_totals,avgprod
    st1 += float(result['TODAY_1STQTY'])
    pq += float(result['TODAY_PQQTY'])
    ss += float(result['TODAY_SSQTY'])
    others += float(result['TODAY_OTHERESQTY'])
    totals += float(result['TODAY_TOTALQTY'])
    mth_st1 += float(result['MTH_1STQTY'])
    mth_pq += float(result['MTH_PQQTY'])
    mth_ss += float(result['MTH_SSQTY'])
    mth_others += float(result['MTH_OTHERSQTY'])
    mth_totals += float(result['MTH_TOTALQTY'])
    avgprod += float(result['MTH_AVGPRO'])

def PrintDepartmentTotal():
    global st1, pq, ss, others, totals, mth_st1, mth_pq, mth_ss, mth_others, mth_totals, avgprod
    boldfonts(7)
    c.drawString(101, d, 'Department Total: ')
    c.drawAlignedString(300, d, str('{0:1.3f}'.format(st1)))
    c.drawAlignedString(360, d, str('{0:1.3f}'.format(pq)))
    c.drawAlignedString(420, d, str('{0:1.3f}'.format(ss)))
    c.drawAlignedString(490, d, str('{0:1.3f}'.format(others)))
    c.drawAlignedString(565, d, str('{0:1.3f}'.format(totals)))
    if int(totals) != 0:
        c.drawAlignedString(610, d, str('{0:1.2f}'.format(round((others * 100/totals),3))))
    else:
        c.drawAlignedString(610, d, str('{0:1.2f}'.format(0)))
    c.drawAlignedString(700, d, str('{0:1.3f}'.format(mth_st1)))
    c.drawAlignedString(770, d, str('{0:1.3f}'.format(mth_pq)))
    c.drawAlignedString(840, d, str('{0:1.3f}'.format(mth_ss)))
    c.drawAlignedString(920, d, str('{0:1.3f}'.format(mth_others)))
    c.drawAlignedString(1000, d, str('{0:1.3f}'.format(mth_totals)))
    if int(mth_totals) != 0:
        c.drawAlignedString(1050, d, str('{0:1.2f}'.format(round((mth_others * 100/mth_totals),3))))
    else:
        c.drawAlignedString(1050, d, str('{0:1.2f}'.format(0)))
    c.drawAlignedString(1140, d, str('{0:1.3f}'.format(avgprod)))
    fonts(7)
    st1 = 0
    pq = 0
    ss = 0
    others = 0
    totals = 0
    mth_st1 = 0
    mth_pq = 0
    mth_ss = 0
    mth_others = 0
    mth_totals = 0
    avgprod = 0


def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt,etdt,result, divisioncode)
    logic(result)
    # print('rohit  ', A4)
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        boldfonts(8)
        c.drawString(30, d, divisioncode[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d, stdt, etdt, divisioncode)

    elif divisioncode[-1] != divisioncode[-2]:
        c.setDash(2,3)
        c.line(30, d, 1170, d)
        c.setDash([], 0)
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        PrintDepartmentTotal()
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        boldfonts(8)
        c.drawString(30, d, divisioncode[-1])
        d = dvalue(stdt, etdt, result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        data(result, d, stdt, etdt, divisioncode)