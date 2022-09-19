import textwrap
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 740
i = 0
p = 0
X = 0
total_itr = 0
count = 0
pageno = 0
clmtotal = 0

divisioncode = []
machine = []
Quality = []
QultyCheck = []
PercentageQ = []
PercentageQX = []
DeptTotalQuality = []
DeptTotal = []
departmentTotal = 0

total = 0

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

def dvalue():
    global d
    d = d - 5
    return d

def dvalueincrese():
    global d
    d = d + 10
    return d

def header(stdt,etdt, divisioncode, department, Qualities):
    global i, QultyCheck
    QultyCheck = []
    fonts(9)
    x = 90
    c.setFillColorRGB(0, 0, 0)
    while divisioncode[-1] == department[i]:
        c.drawString(x, 755, str(Qualities[i]))
        QultyCheck.append(Qualities[i])
        i = i + 1
        x = x + 70
        if i == len(department):
            break
    fonts(15)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Machinewise Gradewise Summary From  " + str(stdt.strftime(' %d  %b  %Y')) +
                        "  To  " + str(etdt.strftime(' %d  %b  %Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    fonts(9)
    # Upperline in header
    c.drawString(10, 755, 'Line/Machine')
    c.drawString(x, 755, 'Total')
    return x

def data(result, d):
    global X, clmtotal, PercentageQ, PercentageQX
    global DeptTotalQuality, DeptTotal
    fonts(7)
    c.drawAlignedString(X + 15, d, str(result['NETWT']))
    PercentageQ.append(float(result['NETWT']))
    PercentageQX.append(X + 22)
    DeptTotalQuality.append(result['QUALITY'])
    DeptTotal.append(float(result['NETWT']))
    clmtotal = clmtotal + float(result['NETWT'])
    DepartmentTotal(result)

def logic(result):
    global divisioncode, machine, Quality
    divisioncode.append(result['DEPARTMENT'])
    machine.append(result['MACHINE'])
    Quality.append(str(result['QUALITY']))

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode, machine, Quality
    global PercentageQ, PercentageQX
    global pageno
    divisioncode = []
    machine = []
    Quality = []
    PercentageQ = []
    PercentageQX = []
    pageno = 0

def DepartmentTotal(result):
    global departmentTotal
    departmentTotal = departmentTotal + float(result['NETWT'])

def DepartmentClean():
    global departmentTotal
    global DeptTotalQuality, DeptTotal
    DeptTotalQuality = []
    DeptTotal = []
    departmentTotal = 0

def PrintClmTotal() :
    global clmtotal
    c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(clmtotal)))

def textsize(c, result, d, stdt,etdt, department, Qualities):
    d = dvalue()
    logic(result)
    global X, p, PercentageQX, PercentageQ, clmtotal
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        clmtotal = 0
        p = header(stdt,etdt, divisioncode, department, Qualities)
        fonts(7)
        c.drawString(10, d, machine[-1])
        X = 90
        length = 0
        while length < len(QultyCheck):
            if Quality[-1] == QultyCheck[length]:
                break
            X = X + 70
            length = length + 1
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if machine[-1] == machine[-2]:
            d = dvalueincrese()
            X = 90
            length = 0
            while length < len(QultyCheck):
                if Quality[-1] == QultyCheck[length]:
                    break
                X = X + 70
                length = length + 1
            data(result, d)

        elif machine[-1] != machine[-2]:
            fonts(7)
            d = dvalueincrese()
            PrintClmTotal()
            l = 0
            totalSumPer = 0
            while l < len(PercentageQ):
                percentage = round(((float(PercentageQ[l]) / float(clmtotal)) * 100), 2)
                c.drawAlignedString(PercentageQX[l], d - 10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
                l = l + 1
            c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
            PercentageQX = []
            PercentageQ = []
            clmtotal = 0
            d = dvalue()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, machine[-1])
            X = 90
            length = 0
            while length < len(QultyCheck):
                if Quality[-1] == QultyCheck[length]:
                    break
                X = X + 70
                length = length + 1
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        d = dvalueincrese()
        PrintClmTotal()
        l = 0
        totalSumPer = 0
        while l < len(PercentageQ):
            percentage = round(((float(PercentageQ[l]) / float(clmtotal)) * 100), 2)
            c.drawAlignedString(PercentageQX[l], d - 10, str(percentage) + ' %')
            totalSumPer = totalSumPer + percentage
            l = l + 1
        c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
        d = dvalue()
        d = dvalue()
        d = dvalue()
        d = dvalue()
        boldfonts(7)
        c.drawString(10, d, 'Department Total: ')
        l = 0
        X = 90
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
                c.drawAlignedString(X + 22, d - 10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
            l = l + 1
            X = X + 70
        c.drawAlignedString(p + 15, d, str('{0:1.3f}'.format(departmentTotal)))
        c.drawAlignedString(p + 22, d - 10, str(totalSumPer) + ' %')
        PercentageQX = []
        PercentageQ = []
        clmtotal = 0
        DepartmentClean()
        fonts(7)
        c.showPage()
        d = newpage()
        d = dvalue()
        p = header(stdt, etdt, divisioncode, department, Qualities)
        fonts(7)
        c.drawString(10, d, machine[-1])
        X = 90
        length = 0
        while length < len(QultyCheck):
            if Quality[-1] == QultyCheck[length]:
                break
            X = X + 70
            length = length + 1
        data(result, d)