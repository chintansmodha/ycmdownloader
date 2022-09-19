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
c.setPageSize(landscape(A4))

d = 525
i = 1
pageno = 0
pageSize = 0
Xaxis = 0
Yaxis = 0

divisioncode = []
Itemname = []
Shadecode = []
LotNo = []
departmentTotal = []
departmentTotal2 = []
itemTotal = []
itemTotal2 = []

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

def dvalue(etdt,result, divisioncode,LSDay):
    global d
    if d > 20:
        d = d - 5
        return d
    else:
        d = newpage()
        # c.setPageSize(landscape(A4))
        c.showPage()
        header(etdt, divisioncode,LSDay)
        dvalue(etdt, result, divisioncode, LSDay)
        return d

def dvalueincrese():
    global d
    if d > 30 and d < 745:
        d = d + 10
    else:
        pass
    return d

def wrap(string, type, width, x, y, result, etdt, LSDay):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        e = e + 1
        if e < len(wrap_text):
            y = dvalue(etdt, result, divisioncode, LSDay)
            y = dvalue(etdt, result, divisioncode, LSDay)


def headerRef(etdt, divisioncode,LSDay):
    global pageSize, Xaxis, Yaxis, d
    # print(len(LSDay))
    if len(LSDay) <=4:
        # print('3')
        c.setPageSize(landscape(A4))
        pageSize = 4
        Xaxis = 842 #842
        Yaxis = 570 #596
        d = Yaxis - 50
    elif len(LSDay)> 4 and len(LSDay)<=8:
        # print('3-6')
        c.setPageSize(landscape(A3))
        pageSize = 3
        Xaxis = 1192 #1190.55
        Yaxis = 810 #842
        d = Yaxis - 50
    elif len(LSDay)> 8 and len(LSDay)<=14:
        # print('6-9')
        c.setPageSize(landscape(A2))
        pageSize = 2
        Xaxis = 1684 #1684
        Yaxis = 1150 # 1190
        d = Yaxis - 50
    elif len(LSDay)> 14 and len(LSDay)<=23:
        # print('9-12')
        c.setPageSize(landscape(A1))
        pageSize = 1
        Xaxis = 2384 #2384
        Yaxis = 1634 #1684
        d = Yaxis - 50
    elif len(LSDay)> 23:
        # print('12-15')
        c.setPageSize(landscape(A0))
        pageSize = 0
        Xaxis = 3372 #3371
        Yaxis = 2324 #2384
        d = Yaxis - 50

    header(etdt, divisioncode, LSDay)
    return d



def header(etdt, divisioncode,LSDay):
    global Xaxis, Yaxis, d
    c.setTitle('FinshedStockInHandAgeing')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(Xaxis/2, Yaxis, divisioncode[-1])
    fonts(9)
    c.drawString(10, Yaxis, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(Xaxis/2, Yaxis-15, "Stock In Hand (Ageing) As On  " + str(etdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(etdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(Xaxis-200, Yaxis-15, "Page No." + str(p))
    c.line(0, Yaxis-20, Xaxis, Yaxis-20)
    c.line(0, Yaxis-40, Xaxis, Yaxis-40)
    # Upperline in header
    c.drawString(10, Yaxis-35, "Item")
    c.drawString(220, Yaxis-35, 'ShadeCode')
    c.drawString(300, Yaxis-35, 'Lot No.')
    c.drawString(340, Yaxis-35, 'gradeGrp')
    X = 400
    i = 0
    while i <= len(LSDay):
        if i == 0:
            c.drawString(X, Yaxis-35, 'Upto' + str(LSDay[i]))
        elif i == len(LSDay):
            c.drawString(X, Yaxis-35, 'Above ' + str(LSDay[i-1]))
        else:
            c.drawString(X, Yaxis-35, str(int(LSDay[i - 1])+1) + ' - ' + str(LSDay[i]))
        i += 1
        X += 80
    c.drawString(X, Yaxis-35, 'Total')


    # ************** Set d Value
    # d = Yaxis-45
    # return d



def data(result, d, LSDay, etdt,divisioncode):
    global departmentTotal, itemTotal, itemTotal2, departmentTotal2
    if len(Itemname) != 1:
        if itemTotal != []:
            if Itemname[-1] != Itemname[-2]:
                ItemTotal(etdt, result, d, divisioncode, LSDay)
                d = dvalue(etdt,result,divisioncode,LSDay)
                d = dvalue(etdt, result, divisioncode, LSDay)
                d = dvalue(etdt, result, divisioncode, LSDay)
    n = 0
    itemcount = 0
    n2 = 0
    itemcount2 = 0
    if departmentTotal != []:
        n = 1
    if itemTotal != []:
        itemcount = 1
    if departmentTotal2 != []:
        n2 = 1
    if itemTotal2 != []:
        itemcount2 = 1
    fonts(7)
    # c.drawString(10, d, str(result['ITEM']))
    # c.drawString(300, d, str(result['LOTNO']))
    X = 400
    i = 0
    # strin = I
    while i <= len(LSDay):
        if i == 0:
            c.drawAlignedString(X+15, d, str(result['LESS'+str(LSDay[i])]))
            # print(result['QUALITYGROUP'])
            if n == 0:
                if str(result['QUALITYGROUP']).strip() =='I' :
                    departmentTotal.append(float(result['LESS'+str(LSDay[i])]))
            elif n==1:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    departmentTotal[i] += float(result['LESS'+str(LSDay[i])])
            if n2 == 0:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    departmentTotal2.append(float(result['LESS' + str(LSDay[i])]))
            elif n2 == 1:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    departmentTotal2[i] += float(result['LESS' + str(LSDay[i])])

            if itemcount == 0:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    itemTotal.append(float(result['LESS'+str(LSDay[i])]))
            elif itemcount == 1:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    itemTotal[i] += float(result['LESS'+str(LSDay[i])])
            if itemcount2 == 0:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    itemTotal2.append(float(result['LESS' + str(LSDay[i])]))
            elif itemcount2 == 1:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    itemTotal2[i] += float(result['LESS' + str(LSDay[i])])


        elif i == len(LSDay):
            c.drawAlignedString(X+20, d, str(result['ABOVE'+str(LSDay[i-1])]))
            if n == 0:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    departmentTotal.append(float(result['ABOVE' + str(LSDay[i-1])]))
            elif n==1:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    departmentTotal[i] += float(result['ABOVE' + str(LSDay[i-1])])
            if n2 == 0:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    departmentTotal2.append(float(result['ABOVE' + str(LSDay[i-1])]))
            elif n2==1:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    departmentTotal2[i] += float(result['ABOVE' + str(LSDay[i-1])])

            if itemcount == 0:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    itemTotal.append(float(result['ABOVE' + str(LSDay[i-1])]))
            elif itemcount == 1:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    itemTotal[i] += float(result['ABOVE' + str(LSDay[i-1])])
            if itemcount2 == 0:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    itemTotal2.append(float(result['ABOVE' + str(LSDay[i-1])]))
            elif itemcount2==1:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    itemTotal2[i] += float(result['ABOVE' + str(LSDay[i-1])])


        else:
            c.drawAlignedString(X+15, d, str(result['LESS'+str(LSDay[i])]))
            if n == 0:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    departmentTotal.append(float(result['LESS' + str(LSDay[i])]))
            elif n==1:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    departmentTotal[i] += float(result['LESS' + str(LSDay[i])])
            if n2 == 0:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    departmentTotal2.append(float(result['LESS' + str(LSDay[i])]))
            elif n2==1:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    departmentTotal2[i] += float(result['LESS' + str(LSDay[i])])

            if itemcount == 0:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    itemTotal.append(float(result['LESS' + str(LSDay[i])]))
            elif itemcount == 1:
                if str(result['QUALITYGROUP']).strip() == 'I':
                    itemTotal[i] += float(result['LESS' + str(LSDay[i])])
            if itemcount2 == 0:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    itemTotal2.append(float(result['LESS' + str(LSDay[i])]))
            elif itemcount2==1:
                if str(result['QUALITYGROUP']).strip() == 'II':
                    itemTotal2[i] += float(result['LESS' + str(LSDay[i])])
        i += 1
        X += 80


    c.drawAlignedString(X+10, d, str(result['TOTAL']))
    if n == 0:
        if str(result['QUALITYGROUP']).strip() == 'I':
            departmentTotal.append(float(result['TOTAL']))
    elif n==1:
        if str(result['QUALITYGROUP']).strip() == 'I':
            departmentTotal[i] += float(result['TOTAL'])
    if n2 == 0:
        if str(result['QUALITYGROUP']).strip() == 'II':
            departmentTotal2.append(float(result['TOTAL']))
    elif n2 == 1:
        if str(result['QUALITYGROUP']).strip() == 'II':
            departmentTotal2[i] += float(result['TOTAL'])

    if itemcount == 0:
        if str(result['QUALITYGROUP']).strip() == 'I':
            itemTotal.append(float(result['TOTAL']))
    elif itemcount == 1:
        if str(result['QUALITYGROUP']).strip() == 'I':
            itemTotal[i] += float(result['TOTAL'])
    if itemcount2 == 0:
        if str(result['QUALITYGROUP']).strip() == 'II':
            itemTotal2.append(float(result['TOTAL']))
    elif itemcount2 == 1:
        if str(result['QUALITYGROUP']).strip() == 'II':
            itemTotal2[i] += float(result['TOTAL'])


    # print('depTotal', Itemname)
    if len(Itemname) == 1:
        c.drawString(224, d, str(result['SHADECODE']))
        c.drawString(300, d, str(result['LOTNO']))
        c.drawString(350, d, str(result['QUALITYGROUP']))
        wrap(str(result['ITEM']),c.drawString,45,10,d,result,etdt,LSDay)
        # c.drawString(10, d, str(result['ITEM']))

    elif Itemname[-1] == Itemname[-2]:
        if Shadecode[-1] == Shadecode[-2]:
            if LotNo[-1] == LotNo[-2]:
                c.drawString(350, d, str(result['QUALITYGROUP']))
            elif LotNo[-1] != LotNo[-2]:
                c.drawString(300, d, str(result['LOTNO']))
                c.drawString(350, d, str(result['QUALITYGROUP']))
        elif Shadecode[-1] != Shadecode[-2]:
            c.drawString(224, d, str(result['SHADECODE']))
            c.drawString(300, d, str(result['LOTNO']))
            c.drawString(350, d, str(result['QUALITYGROUP']))

    elif Itemname[-1] != Itemname[-2]:
        c.drawString(224, d, str(result['SHADECODE']))
        c.drawString(300, d, str(result['LOTNO']))
        c.drawString(350, d, str(result['QUALITYGROUP']))
        wrap(str(result['ITEM']), c.drawString, 45, 10, d, result, etdt, LSDay)
        # c.drawString(10, d, str(result['ITEM']))
    # print(departmentTotal)


def logic(result):
    global divisioncode
    global Itemname
    global Shadecode
    global LotNo
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['ITEM'])
    LotNo.append(result['LOTNO'])
    Shadecode.append(result['SHADECODE'])

def newpage():
    global d
    d = 525
    return d

def newrequest():
    global divisioncode
    global Itemname
    global Shadecode
    global LotNo
    global pageSize
    global pageno
    divisioncode = []
    pageno = 0
    Itemname = []
    Shadecode = []
    LotNo = []
    pageSize = 0

def DepartmentTotal(etdt, result, d, divisioncode, LSDay):
    boldfonts(7)
    global departmentTotal, departmentTotal2
    if departmentTotal2 == []:
        c.drawString(300, d, 'Department Total: ')
        X = 400
        i = 0
        while i < len(departmentTotal):
            if i == len(departmentTotal)-2:
                c.drawAlignedString(X+20, d, str('{0:1.3f}'.format(departmentTotal[i])))
            elif i == len(departmentTotal)-1 :
                c.drawAlignedString(X + 10, d, str('{0:1.3f}'.format(departmentTotal[i])))
            else:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(departmentTotal[i])))

            i += 1
            X += 80
    else:
        c.drawString(300, d, 'Department Total: ')
        X = 400
        i = 0
        while i < len(departmentTotal):
            if i == len(departmentTotal) - 2:
                c.drawAlignedString(X + 20, d, str('{0:1.3f}'.format(departmentTotal[i])))
            elif i == len(departmentTotal) - 1:
                c.drawAlignedString(X + 10, d, str('{0:1.3f}'.format(departmentTotal[i])))
            else:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(departmentTotal[i])))

            i += 1
            X += 80

        d = dvalue(etdt, result, divisioncode, LSDay)
        d = dvalue(etdt, result, divisioncode, LSDay)

        c.drawString(350, d, 'II: ')
        X = 400
        i = 0
        while i < len(departmentTotal2):
            if i == len(departmentTotal2) - 2:
                c.drawAlignedString(X + 20, d, str('{0:1.3f}'.format(departmentTotal2[i])))
            elif i == len(departmentTotal2) - 1:
                c.drawAlignedString(X + 10, d, str('{0:1.3f}'.format(departmentTotal2[i])))
            else:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(departmentTotal2[i])))

            i += 1
            X += 80

    departmentTotal = []
    departmentTotal2 = []
    fonts(7)

def ItemTotal(etdt, result, d, divisioncode, LSDay):
    boldfonts(7)
    global itemTotal, itemTotal2
    if itemTotal2 == []:
        c.drawString(300, d, 'Item Total: ')
        X = 400
        i = 0
        while i < len(itemTotal):
            if i == len(itemTotal)-2:
                c.drawAlignedString(X+20, d, str('{0:1.3f}'.format(itemTotal[i])))
            elif i == len(itemTotal)-1 :
                c.drawAlignedString(X + 10, d, str('{0:1.3f}'.format(itemTotal[i])))
            else:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(itemTotal[i])))

            i += 1
            X += 80
    else:
        c.drawString(300, d, 'Item Total: ')
        X = 400
        i = 0
        while i < len(itemTotal):
            if i == len(itemTotal) - 2:
                c.drawAlignedString(X + 20, d, str('{0:1.3f}'.format(itemTotal[i])))
            elif i == len(itemTotal) - 1:
                c.drawAlignedString(X + 10, d, str('{0:1.3f}'.format(itemTotal[i])))
            else:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(itemTotal[i])))

            i += 1
            X += 80

        d = dvalue(etdt, result, divisioncode, LSDay)
        d = dvalue(etdt, result, divisioncode, LSDay)

        c.drawString(350, d, 'II: ')
        X = 400
        i = 0
        while i < len(itemTotal2):
            if i == len(itemTotal2) - 2:
                c.drawAlignedString(X + 20, d, str('{0:1.3f}'.format(itemTotal2[i])))
            elif i == len(itemTotal2) - 1:
                c.drawAlignedString(X + 10, d, str('{0:1.3f}'.format(itemTotal2[i])))
            else:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(itemTotal2[i])))

            i += 1
            X += 80

    itemTotal = []
    itemTotal2 = []
    fonts(7)


def textsize(c, result, d, etdt, LSDay):
    d = dvalue(etdt,result, divisioncode,LSDay)
    logic(result)
    # print('rohit  ', A4)
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        d = headerRef(etdt, divisioncode,LSDay)
        data(result, d, LSDay, etdt,divisioncode)

    elif divisioncode[-1] == divisioncode[-2]:
        # if Itemname[-1] == Itemname[-2]:
        data(result, d, LSDay, etdt,divisioncode)

        # else:

    elif divisioncode[-1] != divisioncode[-2]:
        ItemTotal(etdt, result, d, divisioncode, LSDay)
        d = dvalue(etdt, result, divisioncode, LSDay)
        d = dvalue(etdt, result, divisioncode, LSDay)
        DepartmentTotal(etdt, result, d, divisioncode, LSDay)
        d = newpage()
        c.showPage()
        d = dvalue(etdt, result, divisioncode, LSDay)
        d = headerRef(etdt, divisioncode,LSDay)
        data(result, d, LSDay, etdt,divisioncode)


