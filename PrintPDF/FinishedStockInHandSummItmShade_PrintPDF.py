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

wrap_text = ''
divisioncode = []
department = []
Itemname = []
Itemtype = []
OpBal = Receipt = Issue = ClBal = 0
DepOpBal = DepReceipt = DepIssue = DepClBal = 0
CompOpBal = CompReceipt = CompIssue = CompClBal = 0

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
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d/%m/%y')))
    c.drawCentredString(300, 780, "Stock In Hand (Item Shade-wise Summary) From  " + str(stdt.strftime(' %d-%m-%Y'))
                        + "  To  " + str(etdt.strftime(' %d-%m-%Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Item/Shade Description")
    c.drawString(320, 760, "op. Bal.")
    c.drawString(400, 760, "Receipt")
    c.drawString(480, 760, "Issue")
    c.drawString(555, 760, "Cl. Bal.")


def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['SHADENAME']))
    c.drawAlignedString(330, d, str(result['OPNETWT']))
    c.drawAlignedString(420, d, str(result['RNETWT']))
    c.drawAlignedString(490, d, str(result['ISSUENETWT']))
    c.drawAlignedString(574, d, str(result['CLNETWT']))
    ItemWiseTotal(result)
    DepartmentTotal(result)
    CompanyTotal(result)


def logic(result):
    global divisioncode
    global department
    global Itemname
    divisioncode.append(result['COMPNAME'])
    department.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global department
    global Itemname
    global pageno
    divisioncode = []
    department = []
    Itemname = []
    pageno = 0

def ItemWiseTotal(result):
    global OpBal, Receipt, Issue, ClBal
    OpBal = OpBal + float(result['OPNETWT'])
    Receipt = Receipt + float(result['RNETWT'])
    Issue = Issue + float(result['ISSUENETWT'])
    ClBal = ClBal + float(result['CLNETWT'])

def ItemWiseClean():
    global OpBal, Receipt, Issue, ClBal
    OpBal = Receipt = Issue = ClBal = 0

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
    global CompOpBal, CompReceipt, CompIssue, CompClBal
    CompOpBal = CompOpBal + float(result['OPNETWT'])
    CompReceipt = CompReceipt + float(result['RNETWT'])
    CompIssue = CompIssue + float(result['ISSUENETWT'])
    CompClBal = CompClBal + float(result['CLNETWT'])

def CompanyClean():
    global CompOpBal, CompReceipt, CompIssue, CompClBal
    CompOpBal = CompReceipt = CompIssue = CompClBal = 0

def ItewiseTotalPrint(d):
    boldfonts(7)
    c.drawString(150, d, "Item Total: ")
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(OpBal)))
    c.drawAlignedString(420, d, str('{0:1.3f}'.format(Receipt)))
    c.drawAlignedString(490, d, str('{0:1.3f}'.format(Issue)))
    c.drawAlignedString(574, d, str('{0:1.3f}'.format(ClBal)))
    fonts(7)

def DepartmentTotalPrint(d):
    boldfonts(7)
    c.drawString(150, d, "Department Total: ")
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(DepOpBal)))
    c.drawAlignedString(420, d, str('{0:1.3f}'.format(DepReceipt)))
    c.drawAlignedString(490, d, str('{0:1.3f}'.format(DepIssue)))
    c.drawAlignedString(574, d, str('{0:1.3f}'.format(DepClBal)))
    fonts(7)

def CompanyTotalPrint(d):
    boldfonts(7)
    c.drawString(150, d, "Company Total: ")
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(CompOpBal)))
    c.drawAlignedString(420, d, str('{0:1.3f}'.format(CompReceipt)))
    c.drawAlignedString(490, d, str('{0:1.3f}'.format(CompIssue)))
    c.drawAlignedString(574, d, str('{0:1.3f}'.format(CompClBal)))
    fonts(7)

def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    global wrap_text

    if len(divisioncode) == 1:
        ItemWiseClean()
        DepartmentClean()
        CompanyClean()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(10, d, department[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if department[-1] == department[-2]:
            if Itemname[-1] == Itemname[-2]:
                data(result, d)
            else:

                ItewiseTotalPrint(d)
                d = dvalue()
                d = dvalue()
                ItemWiseClean()
                d = dvalue()
                fonts(7)
                c.drawString(10, d, Itemname[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)

        else:

            ItewiseTotalPrint(d)
            d = dvalue()
            d = dvalue()
            DepartmentTotalPrint(d)
            ItemWiseClean()
            DepartmentClean()
            d = dvalue()
            d = dvalue()
            boldfonts(7)
            c.drawString(10, d, department[-1])
            d = dvalue()
            d = dvalue()
            fonts(7)
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        ItewiseTotalPrint(d)
        d = dvalue()
        d = dvalue()
        DepartmentTotalPrint(d)
        d = dvalue()
        d = dvalue()
        CompanyTotalPrint(d)
        ItemWiseClean()
        DepartmentClean()
        CompanyClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawString(10, d, department[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)