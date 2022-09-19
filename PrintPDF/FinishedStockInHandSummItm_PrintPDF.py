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
Itemtype = []
OpBal = Receipt = Issue = ClBal = 0
DepOpBal = DepReceipt = DepIssue = DepClBal = 0

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

def header(stdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Stock In Hand (Item - Wise Summary) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Item Description")
    c.drawString(185, 760, "Shade")
    c.drawString(340, 760, "op. Bal.")
    c.drawString(410, 760, "Receipt")
    c.drawString(480, 760, "Issue")
    c.drawString(555, 760, "Cl. Bal.")


def data(result, d):
    fonts(7)
    str1 = ''
    string = str1.join(result['PRODUCT'])
    wrap_text = textwrap.wrap(string, width=35)
    e = 0
    while e < len(wrap_text):
        c.drawString(10, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(10, d, str(result['PRODUCT']))
    fonts(6)
    c.drawString(185, d, str(result['SHADE']))
    fonts(7)
    c.drawAlignedString(355, d, str(result['OPNETWT']))
    c.drawAlignedString(430, d, str(result['RNETWT']))
    c.drawAlignedString(490, d, str(result['ISSUENETWT']))
    c.drawAlignedString(574, d, str(result['CLNETWT']))
    CompanyTotal(result)
    DepartmentTotal(result)
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1


def logic(result):
    global divisioncode
    global department
    divisioncode.append(result['COMPNAME'])
    department.append(result['DEPARTMENT'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global department
    global pageno
    divisioncode = []
    department = []
    pageno = 0

def DepartmentTotal(result):
    global DepOpBal, DepReceipt, DepIssue, DepClBal
    DepOpBal = DepOpBal + float(result['OPNETWT'])
    DepReceipt = DepReceipt + float(result['RNETWT'])
    DepIssue = DepIssue + float(result['ISSUENETWT'])
    DepClBal = DepClBal + float(result['CLNETWT'])

def DepartmentClean():
    global DepOpBal, DepReceipt, DepIssue, DepClBal
    DepOpBal = DepReceipt = DepIssue = DepClBal = 0

def CompanyTotal(result):
    global OpBal, Receipt, Issue, ClBal
    OpBal = OpBal + float(result['OPNETWT'])
    Receipt = Receipt + float(result['RNETWT'])
    Issue = Issue + float(result['ISSUENETWT'])
    ClBal = ClBal + float(result['CLNETWT'])

def CompanyClean():
    global OpBal, Receipt, Issue, ClBal
    OpBal = Receipt = Issue = ClBal = 0


def textsize(c, result, d, stdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        CompanyClean()
        DepartmentClean()
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawString(10, d, department[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if department[-1] == department[-2]:
            data(result, d)
        else:
            d = dvalue()
            boldfonts(7)
            c.drawString(150, d, "Department Total: ")
            c.drawAlignedString(355, d, str('{0:1.3f}'.format(DepOpBal)))
            c.drawAlignedString(430, d, str('{0:1.3f}'.format(DepReceipt)))
            c.drawAlignedString(490, d, str('{0:1.3f}'.format(DepIssue)))
            c.drawAlignedString(574, d, str('{0:1.3f}'.format(DepClBal)))
            DepartmentClean()
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, department[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.drawString(150, d, "Department Total: ")
        c.drawAlignedString(355, d, str('{0:1.3f}'.format(DepOpBal)))
        c.drawAlignedString(430, d, str('{0:1.3f}'.format(DepReceipt)))
        c.drawAlignedString(490, d, str('{0:1.3f}'.format(DepIssue)))
        c.drawAlignedString(574, d, str('{0:1.3f}'.format(DepClBal)))
        d = dvalue()
        d = dvalue()
        c.drawString(150, d, "Company Total: ")
        c.drawAlignedString(355, d, str('{0:1.3f}'.format(OpBal)))
        c.drawAlignedString(430, d, str('{0:1.3f}'.format(Receipt)))
        c.drawAlignedString(490, d, str('{0:1.3f}'.format(Issue)))
        c.drawAlignedString(574, d, str('{0:1.3f}'.format(ClBal)))
        DepartmentClean()
        CompanyClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, divisioncode)
        boldfonts(7)
        c.drawString(10, d, department[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

