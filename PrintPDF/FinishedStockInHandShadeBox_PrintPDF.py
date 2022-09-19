import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 750
i = 1
pageno = 0

divisioncode = []
department = []
Itemname = []
shade = []
lotno = []
shdeboxcount = 0
itemshdecount = 0
itemboxcount = 0
deptboxcount = 0

# total ref
shdecops = 0
shdegross = 0
shdetare = 0
shdeNtwt = 0

itmcops = 0
itmgross = 0
itmtare = 0
itmNtwt = 0

deptcops = 0
deptgross = 0
depttare = 0
deptNtwt = 0

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

def dvalue(c, result, stdt):
    global d
    if d<30:
        c.showPage()
        d = newpage()
        d = dvalue(c, result, stdt)
        header(stdt, divisioncode)
        boldfonts(7)
    else:
        d = d - 5
    return d

def dvalueincrese():
    global d
    if d > 30 and d < 745:
        d = d + 10
    else:
        pass
    return d

def wrap(string, type, width, x, y, result, stdt):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = dvalue(c, result, stdt)
        y = dvalue(c, result, stdt)
        e = e + 1
    d = dvalueincrese()
    # y = dvalueincrese()

def header(stdt, divisioncode):
    fonts(15)
    c.setTitle('FinishedStockInHand ShadeBoxWise')
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Stock In Hand (ShadeWise Boxes in Hand)  As On " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    # c.drawString()
    # c.setDash(3,3)# Dash Linne
    # c.line(0, 730, 600, 730)
    # c.setDash([], 0)  # continuous
    c.drawString(10, 760, 'Box No.')
    c.drawString(90, 760, 'Date')
    c.drawString(180, 760, 'Cops')
    c.drawString(280, 760, 'Gross Wt.')
    c.drawString(350, 760, 'Tare Wt.')
    c.drawString(470, 760, 'Net Wt.')
    c.drawString(520, 760, 'PSz')
    c.drawString(557, 760, 'WTp')


def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['BOXNO']))
    c.drawString(90, d, str(result['BOXDT'].strftime(' %d-%m-%Y')))
    c.drawAlignedString(195, d, str(result['COPS']))
    c.drawAlignedString(303, d, str(result['GROSSWT']))
    c.drawAlignedString(367, d, str(result['TAREWT']))
    c.drawAlignedString(483, d, str(result['NETWT']))
    c.drawString(525, d, str(result['PSZ']))
    c.drawString(560, d, str(result['WTYPE']))
    Total(result)


def logic(result):
    global divisioncode
    global department
    global Itemname
    global shade
    global lotno
    divisioncode.append(result['PLANT'])
    department.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])
    shade.append(result['SHADENAME'])
    lotno.append(result['LOTNO'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global department
    global Itemname
    global shade
    global lotno
    global pageno
    divisioncode = []
    department = []
    Itemname = []
    shade = []
    lotno = []
    pageno = 0

def Total(result):
    global shdecops ,shdegross ,shdetare ,shdeNtwt
    global itmcops, itmgross, itmtare, itmNtwt
    global deptcops, deptgross, depttare, deptNtwt
    shdecops += int(result['COPS'])
    shdegross += float(result['GROSSWT'])
    shdetare += float(result['TAREWT'])
    shdeNtwt += float(result['NETWT'])

    itmcops += int(result['COPS'])
    itmgross += float(result['GROSSWT'])
    itmtare += float(result['TAREWT'])
    itmNtwt += float(result['NETWT'])

    deptcops += int(result['COPS'])
    deptgross += float(result['GROSSWT'])
    depttare += float(result['TAREWT'])
    deptNtwt += float(result['NETWT'])

def ShadeTotalClean():
    global shdecops, shdegross, shdetare, shdeNtwt
    shdecops = 0
    shdegross = 0
    shdetare = 0
    shdeNtwt = 0

def ItemTotalClean():
    global itmcops, itmgross, itmtare, itmNtwt
    itmcops = 0
    itmgross = 0
    itmtare = 0
    itmNtwt = 0

def PrintShadeTotal():
    boldfonts(7)
    global shdecops, shdegross, shdetare, shdeNtwt, shdeboxcount
    c.drawString(50, d, 'Shdae Total: ')
    c.drawAlignedString(130, d, str(shdeboxcount))
    c.drawAlignedString(195, d, str(shdecops))
    c.drawAlignedString(303, d, str('{0:1.3f}'.format(shdegross)))
    c.drawAlignedString(367, d, str('{0:1.3f}'.format(shdetare)))
    c.drawAlignedString(483, d, str('{0:1.3f}'.format(shdeNtwt)))
    shdecops = 0
    shdegross = 0
    shdetare = 0
    shdeNtwt = 0
    shdeboxcount = 0
    fonts(7)

def PrintItemTotal():
    boldfonts(7)
    global itmcops, itmgross, itmtare, itmNtwt, itemboxcount
    c.drawString(50, d, 'Item Total: ')
    c.drawAlignedString(130, d, str(itemboxcount))
    c.drawAlignedString(195, d, str(itmcops))
    c.drawAlignedString(303, d, str('{0:1.3f}'.format(itmgross)))
    c.drawAlignedString(367, d, str('{0:1.3f}'.format(itmtare)))
    c.drawAlignedString(483, d, str('{0:1.3f}'.format(itmNtwt)))
    itmcops = 0
    itmgross = 0
    itmtare = 0
    itmNtwt = 0
    itemboxcount = 0
    fonts(7)

def PrintDeptTotal():
    boldfonts(7)
    global deptcops, deptgross, depttare, deptNtwt, deptboxcount
    c.drawString(50, d, 'Dept Total: ')
    c.drawAlignedString(130, d, str(deptboxcount))
    c.drawAlignedString(195, d, str(deptcops))
    c.drawAlignedString(303, d, str('{0:1.3f}'.format(deptgross)))
    c.drawAlignedString(367, d, str('{0:1.3f}'.format(depttare)))
    c.drawAlignedString(483, d, str('{0:1.3f}'.format(deptNtwt)))
    deptcops = 0
    deptgross = 0
    depttare = 0
    deptNtwt = 0
    deptboxcount = 0
    fonts(7)

def textsize(c, result, d, stdt):
    d = dvalue(c, result, stdt)
    logic(result)
    global shdeboxcount, itemshdecount, itemboxcount, deptboxcount
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, department[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        c.drawString(10, d, Itemname[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        c.drawString(10, d, shade[-1])
        c.drawString(200, d, lotno[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        data(result, d)
        shdeboxcount += 1
        itemshdecount += 1
        itemboxcount += 1
        deptboxcount += 1

    elif divisioncode[-1] == divisioncode[-2]:
        if department[-1] == department[-2]:
            if Itemname[-1] == Itemname[-2]:
                if shade[-1] == shade[-2]:
                    data(result, d)
                    shdeboxcount += 1
                    itemboxcount += 1
                    deptboxcount += 1

                elif shade[-1] != shade[-2]:
                    if shdeboxcount >1:
                        PrintShadeTotal()
                        d = dvalue(c, result, stdt)
                    shdeboxcount = 0
                    ShadeTotalClean()
                    boldfonts(7)
                    d = dvalue(c, result, stdt)
                    c.drawString(10, d, shade[-1])
                    c.drawString(200, d, lotno[-1])
                    d = dvalue(c, result, stdt)
                    d = dvalue(c, result, stdt)
                    data(result, d)
                    shdeboxcount += 1
                    itemshdecount += 1
                    itemboxcount += 1
                    deptboxcount += 1

            elif Itemname[-1] != Itemname[-2]:
                if shdeboxcount > 1:
                    PrintShadeTotal()
                    d = dvalue(c, result, stdt)
                    d = dvalue(c, result, stdt)
                shdeboxcount = 0
                if itemshdecount > 1:
                    PrintItemTotal()
                    d = dvalue(c, result, stdt)
                itemshdecount = 0
                itemboxcount = 0
                ShadeTotalClean()
                ItemTotalClean()
                boldfonts(7)
                d = dvalue(c, result, stdt)
                c.drawString(10, d, Itemname[-1])
                d = dvalue(c, result, stdt)
                d = dvalue(c, result, stdt)
                c.drawString(10, d, shade[-1])
                c.drawString(200, d, lotno[-1])
                d = dvalue(c, result, stdt)
                d = dvalue(c, result, stdt)
                data(result, d)
                shdeboxcount += 1
                itemshdecount += 1
                itemboxcount += 1
                deptboxcount += 1

        elif department[-1] != department[-2]:
            if shdeboxcount > 1:
                PrintShadeTotal()
                d = dvalue(c, result, stdt)
                d = dvalue(c, result, stdt)
            shdeboxcount = 0
            if itemshdecount > 1:
                PrintItemTotal()
                d = dvalue(c, result, stdt)
                d = dvalue(c, result, stdt)
            itemshdecount = 0
            PrintDeptTotal()
            ShadeTotalClean()
            ItemTotalClean()
            itemboxcount = 0
            deptboxcount = 0
            c.showPage()
            d = newpage()
            d = dvalue(c, result, stdt)
            header(stdt, divisioncode)
            boldfonts(7)
            c.drawCentredString(300, d, department[-1])
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            c.drawString(10, d, Itemname[-1])
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            c.drawString(10, d, shade[-1])
            c.drawString(200, d, lotno[-1])
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
            data(result, d)
            shdeboxcount += 1
            itemshdecount += 1
            itemboxcount += 1
            deptboxcount += 1

    elif divisioncode[-1] != divisioncode[-2]:
        if shdeboxcount > 1:
            PrintShadeTotal()
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
        shdeboxcount = 0
        if itemshdecount > 1:
            PrintItemTotal()
            d = dvalue(c, result, stdt)
            d = dvalue(c, result, stdt)
        itemshdecount = 0
        PrintDeptTotal()
        ShadeTotalClean()
        ItemTotalClean()
        itemboxcount = 0
        deptboxcount = 0
        c.showPage()
        d = newpage()
        d = dvalue(c, result, stdt)
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, department[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        c.drawString(10, d, Itemname[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        c.drawString(10, d, shade[-1])
        c.drawString(200, d, lotno[-1])
        d = dvalue(c, result, stdt)
        d = dvalue(c, result, stdt)
        data(result, d)
        shdeboxcount += 1
        itemshdecount += 1
        itemboxcount += 1
        deptboxcount += 1
