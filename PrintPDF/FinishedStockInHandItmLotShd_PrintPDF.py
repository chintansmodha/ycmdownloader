from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date, datetime
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 510
i = 1
pageno = 0

divisioncode = []
department = []
Itemname = []
Itemtype = []
ItmOpBl = 0
ItmRecpt = 0
ItmIssuBl = 0
ItmClBal = 0
DeptOpBl = 0
DeptRecpt = 0
DeptIssuBl = 0
DeptClBal = 0

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

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(425, 560, divisioncode[-1])
    fonts(9)
    c.drawString(10, 550, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(425, 540, "Stock In Hand (Item Lot Shade-Wise Summary) From  " + str(stdt.strftime(' %d-%m-%Y'))
                        + "  To  " + str(etdt.strftime(' %d-%m-%Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(750, 540, "Page No." + str(p))
    c.line(0, 535, 850, 535)
    c.line(0, 515, 850, 515)
    # Upperline in header
    c.drawString(10, 520, "Item")
    c.drawString(250, 520, "Merge No.")
    c.drawString(310, 520, "Shade")
    c.drawString(460, 520, "Op.Bal.")
    c.drawString(540, 520, "Receipt")
    c.drawString(620, 520, "Issue")
    c.drawString(700, 520, "Cl.Bal.")
    c.drawString(780, 520, "Last Prod Dt.")


def data(result, d):
    fonts(7)
    c.drawString(251, d, str(result['MERGENO']))
    c.drawString(311, d, str(result['SHADENAME']))
    c.drawAlignedString(475, d, str(result['OPNETWT']))
    c.drawAlignedString(555, d, str(result['RNETWT']))
    c.drawAlignedString(635, d, str(result['ISSUENETWT']))
    c.drawAlignedString(715, d, str(result['CLNETWT']))
    Date = datetime.strptime(str(result['LASTPRODDT']), '%Y-%m-%d').date()
    Date = Date.strftime('%d  %b  %y')
    c.drawString(782, d, str(Date))
    ItemTotal(result)
    DeptTotal(result)


def logic(result):
    global divisioncode
    global Itemname
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])

def newpage():
    global d
    d = 510
    return d

def newrequest():
    global divisioncode
    global Itemname
    global pageno
    divisioncode = []
    Itemname = []
    pageno = 0

def ItemTotal(result):
    global ItmOpBl, ItmRecpt
    global ItmIssuBl, ItmClBal
    ItmOpBl = ItmOpBl + float(result['OPNETWT'])
    ItmRecpt = ItmRecpt + float(result['RNETWT'])
    ItmIssuBl = ItmIssuBl + float(result['ISSUENETWT'])
    ItmClBal = ItmClBal + float(result['CLNETWT'])

def ItemClean():
    global  ItmOpBl, ItmRecpt
    global ItmIssuBl, ItmClBal
    ItmOpBl = ItmRecpt = 0
    ItmIssuBl = ItmClBal = 0

def DeptTotal(result):
    global DeptOpBl, DeptRecpt
    global DeptIssuBl, DeptClBal
    DeptOpBl = DeptOpBl + float(result['OPNETWT'])
    DeptRecpt = DeptRecpt + float(result['RNETWT'])
    DeptIssuBl = DeptIssuBl + float(result['ISSUENETWT'])
    DeptClBal = DeptClBal + float(result['CLNETWT'])

def DeptClean():
    global DeptOpBl, DeptRecpt
    global DeptIssuBl, DeptClBal
    DeptOpBl = DeptRecpt = 0
    DeptIssuBl = DeptClBal = 0

def ItemTotalPrint(d):
    boldfonts(7)
    c.drawString(350, d, "Item Total: ")
    c.drawAlignedString(475, d, str('{0:1.3f}'.format(ItmOpBl)))
    c.drawAlignedString(555, d, str('{0:1.3f}'.format(ItmRecpt)))
    c.drawAlignedString(635, d, str('{0:1.3f}'.format(ItmIssuBl)))
    c.drawAlignedString(715, d, str('{0:1.3f}'.format(ItmClBal)))
    ItemClean()
    fonts(7)

def DepartmentTotalPrint(d):
    boldfonts(7)
    c.drawString(350, d, "Department Total: ")
    c.drawAlignedString(475, d, str('{0:1.3f}'.format(DeptOpBl)))
    c.drawAlignedString(555, d, str('{0:1.3f}'.format(DeptRecpt)))
    c.drawAlignedString(635, d, str('{0:1.3f}'.format(DeptIssuBl)))
    c.drawAlignedString(715, d, str('{0:1.3f}'.format(DeptClBal)))
    DeptClean()
    fonts(7)


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Itemname[-1] == Itemname[-2]:
            data(result, d)

        else:
            ItemTotalPrint(d)
            d = dvalue()
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, Itemname[-1])
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        ItemTotalPrint(d)
        d = dvalue()
        d = dvalue()
        DepartmentTotalPrint(d)
        c.setPageSize(landscape(A4))
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        data(result, d)

