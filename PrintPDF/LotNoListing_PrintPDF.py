import textwrap

from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))
d = 730

plantcode=[]
resourceno=[]
lotno=[]
pageno=0

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
        c.setPageSize(landscape(A3))
        c.showPage()
        header(stdt, etdt,result, plantcode)
        fonts(7)
        return d

def dvalueInc():
    global d
    d = d + 10
    return d

def header(stdt,etdt,result,plantcode):
    fonts(15)
    c.drawCentredString(595, 800, plantcode[-1])
    c.setFillColorRGB(0, 0, 0)
    fonts(9)
    c.drawCentredString(595, 780, "Lot No. Wise List From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(1100,780,"Page No."+str(p))
    c.line(0, 760, 1190, 760)
    c.line(0, 740, 1190, 740)
    # Upperline in header
    c.drawString(10, 750, "LOT NO.")
    c.drawString(70, 750, "DENIER")
    c.drawString(130, 750, "ITEM")
    c.drawString(290, 750, "SHADE")
    c.drawString(480, 750, "LOT DATE")
    c.drawString(550, 750, "LDR")
    c.drawString(600, 750, "REMARKS")
    c.drawString(660, 750, "SALES ORDER NO.")
    c.drawString(750, 750, 'InputPerc')
    c.drawString(800, 750, 'PrevLotNo')
    c.drawString(850, 750, 'PrevLotBase')
    c.drawString(910, 750, 'PrevLotItem')
    c.drawString(1040, 750, 'PrevLotShade')
    c.drawString(1115, 750, 'PrevLotQuality')

def data(stdt,etdt,result,d):
    LENGTH = 0
    fonts(7)
    # Upperline in data
    c.drawString(10, d, result['LOTNO'])
    c.drawString(85, d, str(result['DENIER']))
    c.drawString(480, d, str(result['LOTDATE'].strftime('%d-%m-%Y')))
    c.drawString(550, d, str(("%.3f" % float(result['LDR']))))
    # c.drawString(600, d, result['LDRREMARKS'])
    if result['SALESORDERNO']!=None:
        c.drawString(700, d, str(result['SALESORDERNO']))
    c.drawString(290, d, str(result['SHADECODE']))
    if result['BOM_INPUTPERC'] != None:
        c.drawAlignedString(770, d, str(result['BOM_INPUTPERC']))
    if result['BOM_PREVLOTNO'] != None:
        c.drawString(795, d, str(result['BOM_PREVLOTNO']))
    if result['BOM_PREVLOTBASE']  != None:
        c.drawString(860, d, str(result['BOM_PREVLOTBASE']))
    c.drawString(1130, d, str(result['BOM_PREVLOTQUALITY']))
    # c.drawString(910, d, str(result['BOM_PREVLOTITEM']))

    if len(str(result['ITEM']))>25:
        lines = textwrap.wrap(str(result['ITEM']), 25, break_long_words=False)
        lenngth = 0
        for i in lines:
            c.drawString(130, d, str(i))
            d = dvalue(stdt, etdt, result, plantcode)
        while lenngth < len(lines):
            d = dvalueInc()
            lenngth = lenngth + 1
        LENGTH = lenngth -1
    else:
        c.drawString(130, d, str(result['ITEM']))
        # c.drawString(910, d, str(result['BOM_PREVLOTITEM']))
        d = dvalue(stdt, etdt, result, plantcode)
        d = dvalueInc()
        LENGTH = LENGTH + 1
        # c.drawString(600, d, result['LDRREMARKS'])
    if len(str(result['LDRREMARKS']))>25:
        lines = textwrap.wrap(str(result['LDRREMARKS']), 25, break_long_words=False)
        lenngth = 0
        for i in lines:
            c.drawString(600, d, str(i))
            d = dvalue(stdt, etdt, result, plantcode)
        while lenngth < len(lines):
            d = dvalueInc()
            lenngth = lenngth + 1
        LENGTH = lenngth -1
    else:
        c.drawString(600, d, str(result['LDRREMARKS']))
        # c.drawString(910, d, str(result['BOM_PREVLOTITEM']))
        d = dvalue(stdt, etdt, result, plantcode)
        d = dvalueInc()

    if len(str(result['BOM_PREVLOTITEM']))>25:
        lines = textwrap.wrap(str(result['BOM_PREVLOTITEM']), 25, break_long_words=False)
        length = 0
        for i in lines:
            c.drawString(910, d, str(i))
            d = dvalue(stdt, etdt, result, plantcode)
        while length < len(lines):
            d = dvalueInc()
            length = length + 1
        if LENGTH < length -1:
            LENGTH = length -1
    else:
        c.drawString(910, d, str(result['BOM_PREVLOTITEM']))
        # c.drawString(910, d, str(result['BOM_PREVLOTITEM']))
        d = dvalue(stdt, etdt, result, plantcode)
        d = dvalueInc()

    if len(str(result['BOM_PREVLOTSHADE']))>25:
        lines = textwrap.wrap(str(result['BOM_PREVLOTSHADE']), 25, break_long_words=False)
        length = 0
        for i in lines:
            c.drawString(1040, d, str(i))
            d = dvalue(stdt, etdt, result, plantcode)
        if LENGTH < length -1:
            LENGTH = length -1
    else:
        c.drawString(1040, d, str(result['BOM_PREVLOTSHADE']))
        # c.drawString(910, d, str(result['BOM_PREVLOTITEM']))
        d = dvalue(stdt, etdt, result, plantcode)
    if LENGTH != 0:
        while LENGTH != 0:
            d = dvalue(stdt, etdt, result, plantcode)
            LENGTH = LENGTH -1

def logic(result):
    plantcode.append(result['PLANTNAME'])
    resourceno.append(result['RESOURCENO'])
    lotno.append(result['LOTNO'])

def dlocvalue():
    global d
    d = d+20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global plantcode
    global resourceno
    global lotno
    global pageno
    global d
    d = 730
    plantcode=[]
    resourceno=[]
    lotno=[]
    pageno=0

def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt,etdt,result,plantcode)
    logic(result)
    if len(plantcode)==1:
        header(stdt, etdt,result,plantcode)
        boldfonts(7)
        c.drawString(10, d, str(resourceno[-1]))
        d = dvalue(stdt,etdt,result,plantcode)
        data(stdt,etdt,result, d)

    elif plantcode[-2] == plantcode[-1]:
        if resourceno[-2] == resourceno[-1]:
            data(stdt,etdt,result,d)
        elif resourceno[-2] != resourceno[-1]:
            boldfonts(7)
            c.drawString(10, d, str(resourceno[-1]))
            d = dvalue(stdt,etdt,result,plantcode)
            data(stdt,etdt,result, d)

    elif plantcode[-2] != plantcode[-1]:
        c.setPageSize(landscape(A3))
        c.showPage()
        header(stdt, etdt,result, plantcode)
        boldfonts(7)
        d=dvalue(stdt,etdt,result,plantcode)
        d = newpage()
        c.drawString(10, d, str(resourceno[-1]))
        d = dvalue(stdt, etdt, result, plantcode)
        data(stdt,etdt,result,d)
        # if resourceno[-2] == resourceno[-1]:
        #     d = dvalue(stdt, etdt, result, plantcode)
        #     data(stdt,etdt,result,d)
        # elif resourceno[-2] != resourceno[-1]:
        #     boldfonts(7)
        #     c.drawString(10, d, str(resourceno[-1]))
        #     d = dvalue(stdt,etdt,result,plantcode)
        #     data(stdt,etdt,result, d)

