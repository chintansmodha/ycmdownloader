from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import portrait, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number, format_currency, format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(portrait(A4)))
c.setPageSize(portrait(A4))

d = 755
i = 0
pageno = 0

divisioncode = []
department = []
item = []
lotno = []

# Total Ref
lotCops = 0
lotGrossWt = 0
lotTareWt = 0
lotNetWt = 0

itmCops = 0
itmGrossWt = 0
itmTareWt = 0
itmNetWt = 0

deptCops = 0
deptGrossWt = 0
deptTareWt = 0
deptNetWt = 0

compCops = 0
compGrossWt = 0
compTareWt = 0
compNetWt = 0


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


def dvalue(c, result, stdt, etdt):
    global d
    if d < 30:
        c.setPageSize(portrait(A4))
        c.showPage()
        d = newpage()
        d = dvalue(c, result, stdt, etdt)
        header(stdt, etdt, divisioncode)
    else:
        d = d - 5
    return d


def dvalueincrese():
    global d
    d = d + 10
    return d


def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setTitle('Box Not Allowed For Despatch')
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    # c.drawString(10, 1610, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 785, "Box Are Not Allowed for despatch List From  " + str(
        stdt.strftime('%d  %b  %Y')) + "  To  " + str(
        etdt.strftime('%d  %b  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    # x 1700, y = 1200
    boldfonts(9)
    p = page()
    c.drawString(540, 785, "Page No." + str(p))
    c.line(0, 780, 600, 780)
    c.line(0, 760, 600, 760)
    fonts(9)
    # Upperline in header
    c.drawString(10, 765, "Box No.")
    c.drawString(80, 765, "Box Date")
    c.drawString(160, 765, "W-Type")
    c.drawString(240, 765, "Cops")
    c.drawString(330, 765, "Gross Wt.")
    c.drawString(420, 765, "Tare Wt.")
    c.drawString(550, 765, "Net Wt.")


def data(c, result, d, stdt, etdt):
    fonts(7)
    c.drawString(10, d, str(result['BOXNO']))
    c.drawString(81, d, str(result['BOXDT'].strftime('%d-%m-%Y')))
    c.drawString(170, d, str(result['WTYPE']))
    c.drawAlignedString(260, d, str(result['COPS']))
    c.drawAlignedString(353, d, str(result['GROSSWT']))
    c.drawAlignedString(438, d, str(result['TAREWT']))
    c.drawAlignedString(560, d, str(result['NETWT']))
    Total(result)


def logic(result):
    global divisioncode, department
    global item, lotno
    divisioncode.append(result['COMPANY'])
    department.append(result['DEPARTMENT'])
    item.append(str(result['ITEM']))
    lotno.append(str(result['LOTNO']))


def newpage():
    global d
    d = 755
    return d


def newrequest():
    global divisioncode, department
    global item, lotno
    global pageno
    divisioncode = []
    department = []
    pageno = 0
    item = []
    lotno = []


def Total(result):
    global lotCops, lotGrossWt, lotTareWt, lotNetWt
    global itmCops, itmGrossWt, itmTareWt, itmNetWt
    global deptCops, deptGrossWt, deptTareWt, deptNetWt
    global compCops, compGrossWt, compTareWt, compNetWt
    lotCops += int(result['COPS'])
    lotGrossWt += float(result['GROSSWT'])
    lotTareWt += float(result['TAREWT'])
    lotNetWt += float(result['NETWT'])

    itmCops += int(result['COPS'])
    itmGrossWt += float(result['GROSSWT'])
    itmTareWt += float(result['TAREWT'])
    itmNetWt += float(result['NETWT'])

    deptCops += int(result['COPS'])
    deptGrossWt += float(result['GROSSWT'])
    deptTareWt += float(result['TAREWT'])
    deptNetWt += float(result['NETWT'])

    compCops += int(result['COPS'])
    compGrossWt += float(result['GROSSWT'])
    compTareWt += float(result['TAREWT'])
    compNetWt += float(result['NETWT'])


def printLotTotal(c, result, stdt, etdt):
    global lotCops, lotGrossWt, lotTareWt, lotNetWt
    global d
    boldfonts(7)
    c.drawString(100, d, 'Lot Total: ')
    c.drawAlignedString(260, d, str(lotCops))
    c.drawAlignedString(353, d, str('{0:1.3f}'.format(lotGrossWt)))
    c.drawAlignedString(438, d, str('{0:1.3f}'.format(lotTareWt)))
    c.drawAlignedString(560, d, str('{0:1.3f}'.format(lotNetWt)))
    lotCops = 0
    lotGrossWt = 0
    lotTareWt = 0
    lotNetWt = 0
    fonts(7)


def printItmTotal(c, result, stdt, etdt):
    global itmCops, itmGrossWt, itmTareWt, itmNetWt
    global d
    boldfonts(7)
    d = dvalue(c, result, stdt, etdt)
    d = dvalue(c, result, stdt, etdt)
    c.drawString(100, d, 'Item Total: ')
    c.drawAlignedString(260, d, str(itmCops))
    c.drawAlignedString(353, d, str('{0:1.3f}'.format(itmGrossWt)))
    c.drawAlignedString(438, d, str('{0:1.3f}'.format(itmTareWt)))
    c.drawAlignedString(560, d, str('{0:1.3f}'.format(itmNetWt)))
    itmCops = 0
    itmGrossWt = 0
    itmTareWt = 0
    itmNetWt = 0
    fonts(7)


def printDeptTotal(c, result, stdt, etdt):
    global deptCops, deptGrossWt, deptTareWt, deptNetWt
    global d
    boldfonts(7)
    d = dvalue(c, result, stdt, etdt)
    d = dvalue(c, result, stdt, etdt)
    c.drawString(100, d, 'Dept Total: ')
    c.drawAlignedString(260, d, str(deptCops))
    c.drawAlignedString(353, d, str('{0:1.3f}'.format(deptGrossWt)))
    c.drawAlignedString(438, d, str('{0:1.3f}'.format(deptTareWt)))
    c.drawAlignedString(560, d, str('{0:1.3f}'.format(deptNetWt)))
    deptCops = 0
    deptGrossWt = 0
    deptTareWt = 0
    deptNetWt = 0
    fonts(7)


def printCompTotal(c, result, stdt, etdt):
    global compCops, compGrossWt, compTareWt, compNetWt
    global d
    boldfonts(7)
    d = dvalue(c, result, stdt, etdt)
    d = dvalue(c, result, stdt, etdt)
    c.drawString(100, d, 'Plant Total: ')
    c.drawAlignedString(260, d, str(compCops))
    c.drawAlignedString(353, d, str('{0:1.3f}'.format(compGrossWt)))
    c.drawAlignedString(438, d, str('{0:1.3f}'.format(compTareWt)))
    c.drawAlignedString(560, d, str('{0:1.3f}'.format(compNetWt)))
    compCops = 0
    compGrossWt = 0
    compTareWt = 0
    compNetWt = 0
    fonts(7)


def textsize(c, result, d, stdt, etdt):
    d = dvalue(c, result, stdt, etdt)
    logic(result)
    global i

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, department[-1])
        d = dvalue(c, result, stdt, etdt)
        d = dvalue(c, result, stdt, etdt)
        c.drawString(10, d, item[-1])
        d = dvalue(c, result, stdt, etdt)
        d = dvalue(c, result, stdt, etdt)
        c.drawString(60, d, lotno[-1])
        fonts(7)
        c.drawString(10, d, "Lot No: ")
        d = dvalue(c, result, stdt, etdt)
        d = dvalue(c, result, stdt, etdt)
        # fonts(7)
        data(c, result, d, stdt, etdt)

    elif divisioncode[-1] == divisioncode[-2]:
        if department[-1] == department[-2]:
            if item[-1] == item[-2]:
                if lotno[-1] == lotno[-2]:
                    data(c, result, d, stdt, etdt)

                elif lotno[-1] != lotno[-2]:
                    printLotTotal(c, result, stdt, etdt)
                    d = dvalue(c, result, stdt, etdt)
                    d = dvalue(c, result, stdt, etdt)
                    d = dvalue(c, result, stdt, etdt)
                    boldfonts(7)
                    c.drawString(60, d, lotno[-1])
                    fonts(7)
                    c.drawString(10, d, "Lot No: ")
                    d = dvalue(c, result, stdt, etdt)
                    d = dvalue(c, result, stdt, etdt)
                    data(c, result, d, stdt, etdt)

            elif item[-1] != item[-2]:
                printLotTotal(c, result, stdt, etdt)
                printItmTotal(c, result, stdt, etdt)
                d = dvalue(c, result, stdt, etdt)
                d = dvalue(c, result, stdt, etdt)
                d = dvalue(c, result, stdt, etdt)
                boldfonts(7)
                c.drawString(10, d, item[-1])
                d = dvalue(c, result, stdt, etdt)
                d = dvalue(c, result, stdt, etdt)
                c.drawString(60, d, lotno[-1])
                fonts(7)
                c.drawString(10, d, "Lot No: ")
                d = dvalue(c, result, stdt, etdt)
                d = dvalue(c, result, stdt, etdt)
                data(c, result, d, stdt, etdt)

        elif department[-1] != department[-2]:
            printLotTotal(c, result, stdt, etdt)
            printItmTotal(c, result, stdt, etdt)
            printDeptTotal(c, result, stdt, etdt)
            d = dvalue(c, result, stdt, etdt)
            d = dvalue(c, result, stdt, etdt)
            d = dvalue(c, result, stdt, etdt)
            boldfonts(7)
            c.drawCentredString(300, d, department[-1])
            d = dvalue(c, result, stdt, etdt)
            d = dvalue(c, result, stdt, etdt)
            c.drawString(10, d, item[-1])
            d = dvalue(c, result, stdt, etdt)
            d = dvalue(c, result, stdt, etdt)
            c.drawString(60, d, lotno[-1])
            fonts(7)
            c.drawString(10, d, "Lot No: ")
            d = dvalue(c, result, stdt, etdt)
            d = dvalue(c, result, stdt, etdt)
            # fonts(7)
            data(c, result, d, stdt, etdt)

    elif divisioncode[-1] != divisioncode[-2]:
        printLotTotal(c, result, stdt, etdt)
        printItmTotal(c, result, stdt, etdt)
        printDeptTotal(c, result, stdt, etdt)
        printCompTotal(c, result, stdt, etdt)
        c.setPageSize(portrait(A4))
        c.showPage()
        d = newpage()
        d = dvalue(c, result, stdt, etdt)
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, department[-1])
        d = dvalue(c, result, stdt, etdt)
        d = dvalue(c, result, stdt, etdt)
        c.drawString(10, d, item[-1])
        d = dvalue(c, result, stdt, etdt)
        d = dvalue(c, result, stdt, etdt)
        c.drawString(60, d, lotno[-1])
        fonts(7)
        c.drawString(10, d, "Lot No: ")
        d = dvalue(c, result, stdt, etdt)
        d = dvalue(c, result, stdt, etdt)
        # fonts(7)
        data(c, result, d, stdt, etdt)