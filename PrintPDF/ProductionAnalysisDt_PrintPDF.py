import textwrap
from reportlab.lib.pagesizes import landscape,portrait , A4, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(portrait(A4)))
c.setPageSize(portrait(A4))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))
d = 745
i = 0
X = 0
sate = 0
total_iter = 0
p = 0
count = 0
dept_totaliter = 0
pageno = 0

divisioncode = []
Department = []
Itemname = []
ShadeName = []
ShadeCode =  []
LotNo = []
Quality = []
QultyCheck = []
PercentageQ = []
PercentageQX = []
LottotalQuality = []
LotTotal = []
ItmtotalQuality = []
ItmTotal = []
ShadeTotalQality = []
ShadeTotal = []
DeptTotalQuality = []
DeptTotal = []
Date = []
itemTotal = 0
shadeToal = 0
departmentTotal = 0
clmtotal = 0
lottotalclm = 0


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

def dvalue(stdt, etdt, divisioncode, department, Qualities):
    global d,sate,i
    if d > 80:
        d = d - 5
        return d
    else:
        d = newpage()
        c.showPage()
        while sate != 0:
            sate = sate - 1
            i = i - 1
        p = headers(stdt, etdt, divisioncode, department, Qualities)
        fonts(7)
        return d

def dvalues():
    global d
    d = d - 10
    return d

def dvalueincrese():
    global d
    d = d + 10
    return d

def wrap(string, type, width, x, d,stdt, etdt, divisioncode, department, Qualities):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, d, wrap_text[e])
        d = d - 10
        e = e + 1

    return s

def wrap_d(string, type, width, x, d,stdt, etdt, divisioncode, department, Qualities):
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text)-1:
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        e = e + 1

    return d

def header(stdt, etdt, divisioncode, department, Qualities):
    fonts(9)
    global i, QultyCheck, sate
    QultyCheck = []
    x = 480
    # Quality on header
    sate = 0
    ch = 0
    c.setPageSize(portrait(A4))
    while divisioncode[-1] == department[i]:
        c.drawString(x, 760, str(Qualities[i]))
        QultyCheck.append(Qualities[i])
        i = i + 1
        sate = sate + 1
        x = x + 70
        if x > 550 :
            ch = ch + 1
            c.setPageSize(landscape(A3))
            # c.line(600, 775, 1200, 775)
            # c.line(600, 755, 1200, 755)

        if i == len(department):
            break

    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Shade Item (Date) wise Production From " + str(stdt.strftime('%d-%b-%Y')) + " To " + str(
        etdt.strftime('%d-%b-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    if ch == 1:
        c.line(0, 775, 1200, 775)
        c.line(0, 755, 1200, 755)
    else:
        c.line(0, 775, 600, 775)
        c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, 'Shade')
    c.drawString(120, 760, 'Item')
    c.drawString(300, 760, 'Lot No.')
    c.drawString(380, 760, 'Date')
    c.drawString(x , 760,  'Total')
    # print(department)
    return x

def headers(stdt, etdt, divisioncode, department, Qualities):
    fonts(9)
    global i, QultyCheck, sate
    QultyCheck = []
    x = 480
    # Quality on header
    sate = 0
    ch = 0
    c.setPageSize(portrait(A4))
    while divisioncode[-2] == department[i]:
        c.drawString(x, 760, str(Qualities[i]))
        QultyCheck.append(Qualities[i])
        i = i + 1
        sate = sate + 1
        x = x + 70
        if x > 550 :
            ch = ch + 1
            c.setPageSize(landscape(A3))
            # c.line(600, 775, 1200, 775)
            # c.line(600, 755, 1200, 755)

        if i == len(department):
            break

    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-2])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Shade Item (Date) wise Production From " + str(stdt.strftime('%d-%b-%Y')) + " To " + str(
        etdt.strftime('%d-%b-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    if ch == 1:
        c.line(0, 775, 1200, 775)
        c.line(0, 755, 1200, 755)
    else:
        c.line(0, 775, 600, 775)
        c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, 'Shade')
    c.drawString(120, 760, 'Item')
    c.drawString(300, 760, 'Lot No.')
    c.drawString(380, 760, 'Date')
    c.drawString(x , 760,  'Total')
    # print(department)
    return x

def data(result, d):
    fonts(7)
    global X, clmtotal, PercentageQ, PercentageQX
    global ShadeTotal, ShadeTotalQality
    global DeptTotalQuality, DeptTotal
    global ItmtotalQuality, ItmTotal, itemTotal
    global LottotalQuality, LotTotal, lottotalclm

    c.drawAlignedString(X + 15, d, str(result['NETWT']))
    PercentageQ.append(float(result['NETWT']))
    PercentageQX.append(X+22)
    # q1=q1+float(result['NETWT'])
    clmtotal = clmtotal + float(result['NETWT'])
    itemTotal = itemTotal + float(result['NETWT'])
    lottotalclm = lottotalclm + float(result['NETWT'])
    LottotalQuality.append(result['QUALITY'])
    LotTotal.append(float(result['NETWT']))
    ItmtotalQuality.append(result['QUALITY'])
    ItmTotal.append(float(result['NETWT']))
    ShadeTotalQality.append(result['QUALITY'])
    ShadeTotal.append(float(result['NETWT']))
    DeptTotalQuality.append(result['QUALITY'])
    DeptTotal.append(float(result['NETWT']))
    DepartmentToatal(result)

def printshadequlitytotal():
    global q1
    c.drawAlignedString(  250, d, str(q1))
    q1=0

def logic(result):
    global divisioncode
    global Itemname, total
    global ShadeName, LotNo, Quality, Date
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(str(result['ITEM']))
    ShadeName.append(str(result['SHADE']))
    LotNo.append(str(result['LOTNO']))
    Quality.append(str(result['QUALITY']))
    Date.append(result['DATE'])


def newrequest():
    global divisioncode
    global Department
    global Itemname
    global ShadeName
    global ShadeCode, Quality
    global LotNo, pageno
    global PercentageQ, PercentageQX, ShadeTotalQality
    global ShadeTotal, ItmtotalQuality, ItmTotal
    divisioncode = []
    Department = []
    Itemname = []
    ShadeName = []
    ShadeCode = []
    LotNo = []
    Quality = []
    PercentageQ = []
    PercentageQX = []
    ShadeTotalQality = []
    ShadeTotal = []
    ItmtotalQuality = []
    ItmTotal = []
    pageno = 0

def newpage():
    global d
    d = 745
    return d

def DepartmentToatal(result):
    global shadeToal, departmentTotal
    shadeToal = shadeToal + float(result['NETWT'])
    departmentTotal = departmentTotal + float(result['NETWT'])

def shadeToatalClean():
    global shadeToal
    shadeToal = 0

def departmentClean():
    global departmentTotal, shadeToal
    global DeptTotalQuality,DeptTotal
    departmentTotal = 0
    shadeToal = 0
    DeptTotalQuality = []
    DeptTotal = []

def PrintClmTotal() :
    global clmtotal
    c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(clmtotal)))


def textsize(c, result, d, stdt, etdt, department, Qualities):
    # d = dvalue(stdt, etdt, divisioncode, department, Qualities)
    logic(result)
    global X, QultyCheck, p, PercentageQX, PercentageQ,clmtotal
    global ShadeTotal, ShadeTotalQality, itemTotal
    global ItmtotalQuality, ItmTotal
    global LottotalQuality, LotTotal, lottotalclm

    if len(divisioncode) == 1:
        X = 0
        p = 0
        departmentClean()
        clmtotal = 0
        itemTotal = 0
        lottotalclm = 0
        p = header(stdt, etdt, divisioncode, department, Qualities)
        fonts(7)
        c.drawString(10, d, ShadeName[-1])
        c.drawString(380, d, str(Date[-1].strftime('%d-%m-%Y')))
        wrap(Itemname[-1], c.drawString, 25, 120, d,stdt, etdt, divisioncode, department, Qualities)
        c.drawString(300, d, LotNo[-1])
        X = 480
        length = 0
        while length < len(QultyCheck):
            if Quality[-1] == QultyCheck[length]:
                break
            X = X + 70
            length = length + 1
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if ShadeName[-1] == ShadeName[-2]:
            if Itemname[-1] == Itemname[-2]:
                if LotNo[-1] == LotNo[-2]:
                    # d = dvalueincrese()
                    # if Date[-1] != Date[-2]:
                    #     d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    #     d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    length = 0
                    while length < len(QultyCheck):
                        if Quality[-1] == QultyCheck[length]:
                            break
                        X = X + 70
                        length = length + 1
                    data(result, d)

                elif LotNo[-1] != LotNo[-2]:
                    # d = dvalueincrese()
                    PrintClmTotal()
                    # d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    # d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    l = 0
                    totalSumPer = 0
                    while l < len(PercentageQ):
                        percentage = round(((float(PercentageQ[l]) / float(clmtotal)) * 100),2)
                        c.drawAlignedString(PercentageQX[l], d-10, str(percentage) + ' %')
                        totalSumPer = totalSumPer + percentage
                        l = l + 1
                    c.drawAlignedString(p+22, d-10, str(totalSumPer) + ' %')
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    boldfonts(7)
                    c.drawString(300, d, 'Lot Total: ')
                    l = 0
                    X = 480
                    totalSumPer = 0
                    while l < len(QultyCheck):
                        j = 0
                        sum = 0
                        while j < len(LottotalQuality):
                            if QultyCheck[l] == LottotalQuality[j]:
                                sum = sum + LotTotal[j]
                            j = j + 1
                        if int(sum) != 0:
                            c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                            percentage = round(((float(sum) / float(lottotalclm)) * 100), 2)
                            c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                            totalSumPer = totalSumPer + percentage
                        l = l + 1
                        X = X + 70
                    c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(lottotalclm)))
                    c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
                    PercentageQX = []
                    PercentageQ = []
                    LottotalQuality = []
                    LotTotal = []
                    lottotalclm = 0
                    clmtotal = 0
                    fonts(7)
                    d = wrap_d(Itemname[-2], c.drawString, 25, 120, d, stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                    c.drawString(300, d, LotNo[-1])
                    c.drawString(380, d, str(Date[-1].strftime('%d-%m-%Y')))
                    X = 480
                    length = 0
                    while length < len(QultyCheck):
                        if Quality[-1] == QultyCheck[length]:
                            break
                        X = X + 70
                        length = length + 1
                    data(result, d)
            elif Itemname[-1] != Itemname[-2]:
                # d = dvalueincrese()
                PrintClmTotal()
                l = 0
                totalSumPer = 0
                while l < len(PercentageQ):
                    percentage = round(((float(PercentageQ[l]) / float(clmtotal)) * 100), 2)
                    c.drawAlignedString(PercentageQX[l], d-10, str(percentage) + ' %')
                    totalSumPer = totalSumPer + percentage
                    l = l + 1
                c.drawAlignedString(p + 22, d-10, str(totalSumPer) + ' %')
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                boldfonts(7)
                c.drawString(300, d, 'Lot Total: ')
                l = 0
                X = 480
                totalSumPer = 0
                while l < len(QultyCheck):
                    j = 0
                    sum = 0
                    while j < len(LottotalQuality):
                        if QultyCheck[l] == LottotalQuality[j]:
                            sum = sum + LotTotal[j]
                        j = j + 1
                    if int(sum) != 0:
                        c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                        percentage = round(((float(sum) / float(lottotalclm)) * 100), 2)
                        c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                        totalSumPer = totalSumPer + percentage
                    l = l + 1
                    X = X + 70
                c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(lottotalclm)))
                c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                c.drawString(300, d, 'Item Total: ')
                l = 0
                X = 480
                totalSumPer = 0
                while l < len(QultyCheck):
                    j = 0
                    sum = 0
                    while j < len(ItmtotalQuality):
                        if QultyCheck[l] == ItmtotalQuality[j]:
                            sum = sum + ItmTotal[j]
                        j = j + 1
                    if int(sum) != 0:
                        c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                        percentage = round(((float(sum) / float(itemTotal)) * 100), 2)
                        c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                        totalSumPer = totalSumPer + percentage
                    l = l + 1
                    X = X + 70
                c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(itemTotal)))
                c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
                fonts(7)
                ItmtotalQuality = []
                ItmTotal = []
                PercentageQX = []
                PercentageQ = []
                LottotalQuality = []
                LotTotal = []
                lottotalclm = 0
                clmtotal = 0
                itemTotal = 0
                fonts(7)
                d = wrap_d(Itemname[-2], c.drawString, 25, 120, d,stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                d = dvalue(stdt, etdt, divisioncode, department, Qualities)
                wrap(Itemname[-1], c.drawString, 25, 120, d,stdt, etdt, divisioncode, department, Qualities)
                # c.drawString(120, d, Itemname[-1])
                c.drawString(300, d, LotNo[-1])
                c.drawString(380, d, str(Date[-1].strftime('%d-%m-%Y')))
                X = 480
                length = 0
                while length < len(QultyCheck):
                    if Quality[-1] == QultyCheck[length]:
                        break
                    X = X + 70
                    length = length + 1
                data(result, d)

        elif ShadeName[-1] != ShadeName[-2]:
            # d = dvalueincrese()
            PrintClmTotal()
            l = 0
            totalSumPer = 0
            while l < len(PercentageQ):
                percentage = round(((float(PercentageQ[l]) / float(clmtotal)) * 100), 2)
                c.drawAlignedString(PercentageQX[l], d-10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
                l = l + 1
            c.drawAlignedString(p + 22, d-10, str(totalSumPer) + ' %')
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            boldfonts(7)
            c.drawString(300, d, 'Lot Total: ')
            l = 0
            X = 480
            totalSumPer = 0
            while l < len(QultyCheck):
                j = 0
                sum = 0
                while j < len(LottotalQuality):
                    if QultyCheck[l] == LottotalQuality[j]:
                        sum = sum + LotTotal[j]
                    j = j + 1
                if int(sum) != 0:
                    c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                    percentage = round(((float(sum) / float(lottotalclm)) * 100), 2)
                    c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                    totalSumPer = totalSumPer + percentage
                l = l + 1
                X = X + 70
            c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(lottotalclm)))
            c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            c.drawString(300, d, 'Item Total: ')
            l = 0
            X = 480
            totalSumPer = 0
            while l < len(QultyCheck):
                j = 0
                sum = 0
                while j < len(ItmtotalQuality):
                    if QultyCheck[l] == ItmtotalQuality[j]:
                        sum = sum + ItmTotal[j]
                    j = j + 1
                if int(sum) != 0:
                    c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                    percentage = round(((float(sum) / float(itemTotal)) * 100), 2)
                    c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                    totalSumPer = totalSumPer + percentage
                l = l + 1
                X = X + 70
            c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(itemTotal)))
            c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            boldfonts(7)
            c.drawString(300, d, 'Shade Total: ')
            l = 0
            X = 480
            totalSumPer = 0
            while l < len(QultyCheck):
                j = 0
                sum = 0
                while j < len(ShadeTotalQality):
                    if QultyCheck[l] == ShadeTotalQality[j]:
                        sum = sum + ShadeTotal[j]
                    j = j + 1
                if int(sum) != 0:
                    c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                    percentage = round(((float(sum) / float(shadeToal)) * 100), 2)
                    c.drawAlignedString(X + 22, d-10, str(percentage) + ' %')
                    totalSumPer = totalSumPer + percentage
                l = l + 1
                X = X + 70
            c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(shadeToal)))
            c.drawAlignedString(p + 22, d-10, str(totalSumPer) + ' %')

            ItmtotalQuality = []
            ItmTotal = []
            PercentageQX = []
            PercentageQ = []
            ShadeTotal = []
            ShadeTotalQality = []
            LottotalQuality = []
            LotTotal = []
            lottotalclm = 0
            clmtotal = 0
            itemTotal = 0
            shadeToatalClean()
            fonts(7)
            d = wrap_d(Itemname[-2], c.drawString, 25, 120, d,stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            d = dvalue(stdt, etdt, divisioncode, department, Qualities)
            c.drawString(10, d, ShadeName[-1])
            wrap(Itemname[-1], c.drawString, 25, 120, d,stdt, etdt, divisioncode, department, Qualities)
            c.drawString(300, d, LotNo[-1])
            c.drawString(380, d, str(Date[-1].strftime('%d-%m-%Y')))
            X = 480
            length = 0
            while length < len(QultyCheck):
                if Quality[-1] == QultyCheck[length]:
                    break
                X = X + 70
                length = length + 1
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        # d = dvalueincrese()
        PrintClmTotal()
        l = 0
        totalSumPer = 0
        while l < len(PercentageQ):
            percentage = round(((float(PercentageQ[l]) / float(clmtotal)) * 100), 2)
            c.drawAlignedString(PercentageQX[l], d-10, str(percentage) + ' %')
            totalSumPer = totalSumPer + percentage
            l = l + 1
        c.drawAlignedString(p + 22, d-10, str(totalSumPer) + ' %')
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        boldfonts(7)
        c.drawString(300, d, 'Lot Total: ')
        l = 0
        X = 480
        totalSumPer = 0
        while l < len(QultyCheck):
            j = 0
            sum = 0
            while j < len(LottotalQuality):
                if QultyCheck[l] == LottotalQuality[j]:
                    sum = sum + LotTotal[j]
                j = j + 1
            if int(sum) != 0:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                percentage = round(((float(sum) / float(lottotalclm)) * 100), 2)
                c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
            l = l + 1
            X = X + 70
        c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(lottotalclm)))
        c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        c.drawString(300, d, 'Item Total: ')
        l = 0
        X = 480
        totalSumPer = 0
        while l < len(QultyCheck):
            j = 0
            sum = 0
            while j < len(ItmtotalQuality):
                if QultyCheck[l] == ItmtotalQuality[j]:
                    sum = sum + ItmTotal[j]
                j = j + 1
            if int(sum) != 0:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                percentage = round(((float(sum) / float(itemTotal)) * 100), 2)
                c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
            l = l + 1
            X = X + 70
        c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(itemTotal)))
        c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        boldfonts(7)
        c.drawString(300, d, 'Shade Total: ')
        l = 0
        X = 480
        totalSumPer = 0
        while l < len(QultyCheck):
            j = 0
            sum = 0
            while j < len(ShadeTotalQality):
                if QultyCheck[l] == ShadeTotalQality[j]:
                    sum = sum + ShadeTotal[j]
                j = j + 1
            if int(sum) != 0:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                percentage = round(((float(sum) / float(shadeToal)) * 100), 2)
                c.drawAlignedString(X + 22, d-10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
            l = l + 1
            X = X + 70
        c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(shadeToal)))
        c.drawAlignedString(p + 22, d-10, str(totalSumPer) + ' %')
        # Department total
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        boldfonts(7)
        c.drawString(300, d, 'Department Total: ')
        l = 0
        X = 480
        totalSumPer = 0
        while l < len(QultyCheck):
            j = 0
            sum = 0
            while j < len(DeptTotalQuality):
                if QultyCheck[l] == DeptTotalQuality[j]:
                    sum = sum + DeptTotal[j]
                j = j + 1
            if int(sum) != 0:
                c.drawAlignedString(X + 15, d, str('{0:1.3f}'.format(sum)))
                percentage = round(((float(sum) / float(departmentTotal)) * 100), 2)
                c.drawAlignedString(X + 22, d-10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
            l = l + 1
            X = X + 70
        c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(departmentTotal)))
        c.drawAlignedString(p + 22, d-10, str(totalSumPer) + ' %')
        ItmtotalQuality = []
        ItmTotal = []
        PercentageQX = []
        PercentageQ = []
        ShadeTotal = []
        ShadeTotalQality = []
        LottotalQuality = []
        LotTotal = []
        lottotalclm = 0
        clmtotal = 0
        itemTotal = 0
        departmentClean()
        c.showPage()
        d = newpage()
        # d = dvalue(stdt, etdt, divisioncode, department, Qualities)
        p = header(stdt, etdt, divisioncode, department, Qualities)
        fonts(7)
        c.drawString(10, d, ShadeName[-1])
        wrap(Itemname[-1], c.drawString, 25, 120, d,stdt, etdt, divisioncode, department, Qualities)
        fonts(7)
        c.drawString(300, d, LotNo[-1])
        c.drawString(380, d, str(Date[-1].strftime('%d-%m-%Y')))
        X = 480
        length = 0
        while length < len(QultyCheck):
            if Quality[-1] == QultyCheck[length]:
                break
            X = X + 70
            length = length + 1
        data(result, d)