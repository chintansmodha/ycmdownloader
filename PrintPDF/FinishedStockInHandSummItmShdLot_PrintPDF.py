import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 740
i = 1
pageno = 0

divisioncode = []
Itemname = []
Itemtype = []
OpQty = OpBox = OpCops = 0
PQty = PBox = PCops = 0
IssueQty = IssueBox = IssueCops = 0
ClQty = ClBox = ClCops = 0
ItmtypOpQty = ItmtypOpBox = ItmtypOpCops = 0
ItmtypPQty = ItmtypPBox = ItmtypPCops = 0
ItmtypIssueQty = ItmtypIssueBox = ItmtypIssueCops = 0
ItmtypClQty = ItmtypClBox = ItmtypClCops = 0
DepOpQty = DepOpBox = DepOpCops = 0
DepPQty = DepPBox = DepPCops = 0
DepIssueQty = DepIssueBox = DepIssueCops = 0
DepClQty = DepClBox = DepClCops = 0

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
    c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header
    c.drawString(10, 765, "Lot No")
    c.drawString(80, 765, "Shade")
    c.drawCentredString(210, 765, "<----Opening----->")
    c.drawCentredString(330, 765, "<----Production----->")
    c.drawCentredString(430, 765, "<----Issue----->")
    c.drawCentredString(550, 765, "<----Closing----->")
    #Lowerline in header
    # Opening
    c.drawString(170, 755, "Qty")
    c.drawString(195, 755, "Box")
    c.drawString(225, 755, "Cops")
    # Production
    c.drawString(285, 755, "Qty")
    c.drawString(310, 755, "Box")
    c.drawString(340, 755, "Cops")
    # Issue
    c.drawString(390, 755, "Qty")
    c.drawString(420, 755, "Box")
    c.drawString(450, 755, "Cops")
    # Closing
    c.drawString(510, 755, "Qty")
    c.drawString(535, 755, "Box")
    c.drawString(565, 755, "Cops")


def data(result, d):
    fonts(7)
    c.drawString(11, d, str(result['LOTNO']))
    str1 = ''
    string = str1.join(result['SHADENAME'])
    wrap_text = textwrap.wrap(string, width=15,break_long_words=False)
    e = 0
    while e < len(wrap_text):
        c.drawString(80, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # c.drawString(70, d, str(result['SHADENAME']))
    c.drawAlignedString(180, d, str(result['OPNETWT']))
    c.drawAlignedString(215, d, str(result['OPBOXES']))
    c.drawAlignedString(245, d, str(result['OPCOPS']))
    c.drawAlignedString(290, d, str(result['PNETWT']))
    c.drawAlignedString(325, d, str(result['PBOXES']))
    c.drawAlignedString(360, d, str(result['PCOPS']))
    c.drawAlignedString(395, d, str(result['ISSUENETWT']))
    c.drawAlignedString(435, d, str(result['ISSUEBOXES']))
    c.drawAlignedString(470, d, str(result['ISSUECOPS']))
    c.drawAlignedString(515, d, str(result['CLNETWT']))
    c.drawAlignedString(550, d, str(result['CLBOXES']))
    c.drawAlignedString(585, d, str(result['CLCOPS']))
    if result['SALELOT'] != None:
        e = 0
        while e < len(wrap_text):
            d = dvalue()
            d = dvalue()
            e = e + 1
        c.drawString(11, d, "SaleLot :        " + str(result['SALELOT']))
    ItemWiseTotal(result)
    ItemTypeTotal(result)
    DepartmentTotal(result)
    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1


def logic(result):
    global divisioncode
    global Itemname
    global Itemtype
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])
    Itemtype.append(result['ITMTYPE'])

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode
    global Itemname
    global Itemtype
    global pageno
    divisioncode = []
    pageno = 0
    Itemname = []
    Itemtype = []

def ItemWiseTotal(result):
    global OpQty, OpBox, OpCops
    global PQty, PBox, PCops
    global IssueQty, IssueBox, IssueCops
    global ClQty, ClBox, ClCops
    OpQty = OpQty + float(result['OPNETWT'])#Opening
    OpBox = OpBox + int(result['OPBOXES'])
    OpCops = OpCops + int(result['OPCOPS'])
    PQty = PQty + float(result['PNETWT'])#Production
    PBox = PBox + int(result['PBOXES'])
    PCops = PCops + int(result['PCOPS'])
    IssueQty = IssueQty + float(result['ISSUENETWT'])#Issue
    IssueBox = IssueBox + int(result['ISSUEBOXES'])
    IssueCops = IssueCops + int(result['ISSUECOPS'])
    ClQty = ClQty + float(result['CLNETWT'])#Closing
    ClBox = ClBox + int(result['CLBOXES'])
    ClCops = ClCops + int(result['CLCOPS'])

def ItemWiseClean():
    global OpQty, OpBox, OpCops
    global PQty, PBox, PCops
    global IssueQty, IssueBox, IssueCops
    global ClQty, ClBox, ClCops
    OpQty = OpBox = OpCops = 0
    PQty = PBox = PCops = 0
    IssueQty = IssueBox = IssueCops = 0
    ClQty = ClBox = ClCops = 0

def ItemTypeTotal(result):
    global ItmtypOpQty, ItmtypOpBox, ItmtypOpCops
    global ItmtypPQty, ItmtypPBox, ItmtypPCops
    global ItmtypIssueQty, ItmtypIssueBox, ItmtypIssueCops
    global ItmtypClQty, ItmtypClBox, ItmtypClCops
    ItmtypOpQty = ItmtypOpQty + float(result['OPNETWT'])  # Opening
    ItmtypOpBox = ItmtypOpBox + int(result['OPBOXES'])
    ItmtypOpCops = ItmtypOpCops + int(result['OPCOPS'])
    ItmtypPQty = ItmtypPQty + float(result['PNETWT'])  # Production
    ItmtypPBox = ItmtypPBox + int(result['PBOXES'])
    ItmtypPCops = ItmtypPCops + int(result['PCOPS'])
    ItmtypIssueQty = ItmtypIssueQty + float(result['ISSUENETWT'])  # Issue
    ItmtypIssueBox = ItmtypIssueBox + int(result['ISSUEBOXES'])
    ItmtypIssueCops = ItmtypIssueCops + int(result['ISSUECOPS'])
    ItmtypClQty = ItmtypClQty + float(result['CLNETWT'])  # Closing
    ItmtypClBox = ItmtypClBox + int(result['CLBOXES'])
    ItmtypClCops = ItmtypClCops + int(result['CLCOPS'])

def ItemTypeClean():
    global ItmtypOpQty, ItmtypOpBox, ItmtypOpCops
    global ItmtypPQty, ItmtypPBox, ItmtypPCops
    global ItmtypIssueQty, ItmtypIssueBox, ItmtypIssueCops
    global ItmtypClQty, ItmtypClBox, ItmtypClCops
    ItmtypOpQty = ItmtypOpBox = ItmtypOpCops = 0
    ItmtypPQty = ItmtypPBox = ItmtypPCops = 0
    ItmtypIssueQty = ItmtypIssueBox = ItmtypIssueCops = 0
    ItmtypClQty = ItmtypClBox = ItmtypClCops = 0

def DepartmentTotal(result):
    global DepOpQty, DepOpBox, DepOpCops
    global DepPQty, DepPBox, DepPCops
    global DepIssueQty, DepIssueBox, DepIssueCops
    global DepClQty, DepClBox, DepClCops
    DepOpQty = DepOpQty + float(result['OPNETWT'])  # Opening
    DepOpBox = DepOpBox + int(result['OPBOXES'])
    DepOpCops = DepOpCops + int(result['OPCOPS'])
    DepPQty = DepPQty + float(result['PNETWT'])  # Production
    DepPBox = DepPBox + int(result['PBOXES'])
    DepPCops = DepPCops + int(result['PCOPS'])
    DepIssueQty = DepIssueQty + float(result['ISSUENETWT'])  # Issue
    DepIssueBox = DepIssueBox + int(result['ISSUEBOXES'])
    DepIssueCops = DepIssueCops + int(result['ISSUECOPS'])
    DepClQty = DepClQty + float(result['CLNETWT'])  # Closing
    DepClBox = DepClBox + int(result['CLBOXES'])
    DepClCops = DepClCops + int(result['CLCOPS'])

def DepartmentClean():
    global DepOpQty, DepOpBox, DepOpCops
    global DepPQty, DepPBox, DepPCops
    global DepIssueQty, DepIssueBox, DepIssueCops
    global DepClQty, DepClBox, DepClCops
    DepOpQty = DepOpBox = DepOpCops = 0
    DepPQty = DepPBox = DepPCops = 0
    DepIssueQty = DepIssueBox = DepIssueCops = 0
    DepClQty = DepClBox = DepClCops = 0

def ItemwiseTotalPrint(d):
    boldfonts(7)
    c.drawString(70, d, "Item Total: ")
    c.drawAlignedString(180, d, str('{0:1.3f}'.format(OpQty)))
    c.drawAlignedString(215, d, str(OpBox))
    c.drawAlignedString(245, d, str(OpCops))
    c.drawAlignedString(290, d, str('{0:1.3f}'.format(PQty)))
    c.drawAlignedString(325, d, str(PBox))
    c.drawAlignedString(360, d, str(PCops))
    c.drawAlignedString(395, d, str('{0:1.3f}'.format(IssueQty)))
    c.drawAlignedString(435, d, str(IssueBox))
    c.drawAlignedString(470, d, str(IssueCops))
    c.drawAlignedString(515, d, str('{0:1.3f}'.format(ClQty)))
    c.drawAlignedString(550, d, str(ClBox))
    c.drawAlignedString(585, d, str(ClCops))
    fonts(7)

def ItemTypeTotalPrint(d):
    boldfonts(7)
    c.drawString(70, d, "ItemGrp Total: ")
    c.drawAlignedString(180, d, str('{0:1.3f}'.format(ItmtypOpQty)))
    c.drawAlignedString(215, d, str(ItmtypOpBox))
    c.drawAlignedString(245, d, str(ItmtypOpCops))
    c.drawAlignedString(290, d, str('{0:1.3f}'.format(ItmtypPQty)))
    c.drawAlignedString(325, d, str(ItmtypPBox))
    c.drawAlignedString(360, d, str(ItmtypPCops))
    c.drawAlignedString(395, d, str('{0:1.3f}'.format(ItmtypIssueQty)))
    c.drawAlignedString(435, d, str(ItmtypIssueBox))
    c.drawAlignedString(470, d, str(ItmtypIssueCops))
    c.drawAlignedString(515, d, str('{0:1.3f}'.format(ItmtypClQty)))
    c.drawAlignedString(550, d, str(ItmtypClBox))
    c.drawAlignedString(585, d, str(ItmtypClCops))
    fonts(7)

def DepartmentTotalPrint(d):
    boldfonts(7)
    c.drawString(70, d, "Department Total: ")
    c.drawAlignedString(180, d, str('{0:1.3f}'.format(DepOpQty)))
    c.drawAlignedString(215, d, str(DepOpBox))
    c.drawAlignedString(245, d, str(DepOpCops))
    c.drawAlignedString(290, d, str('{0:1.3f}'.format(DepPQty)))
    c.drawAlignedString(325, d, str(DepPBox))
    c.drawAlignedString(360, d, str(DepPCops))
    c.drawAlignedString(395, d, str('{0:1.3f}'.format(DepIssueQty)))
    c.drawAlignedString(435, d, str(DepIssueBox))
    c.drawAlignedString(470, d, str(DepIssueCops))
    c.drawAlignedString(515, d, str('{0:1.3f}'.format(DepClQty)))
    c.drawAlignedString(550, d, str(DepClBox))
    c.drawAlignedString(585, d, str(DepClCops))
    fonts(7)


def textsize(c, result, d, stdt):
    d = dvalue()
    logic(result)
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        ItemWiseClean()
        ItemTypeClean()
        DepartmentClean()
        header(stdt, divisioncode,)
        boldfonts(7)
        c.drawCentredString(300, d, Itemtype[-1])
        fonts(7)
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Itemtype[-1] == Itemtype[-2]:
            if Itemname[-1] == Itemname[-2]:
                data(result, d)
            else:
                ItemwiseTotalPrint(d)
                d = dvalue()
                d = dvalue()
                ItemWiseClean()
                c.drawString(10, d, Itemname[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)

        else:
            ItemwiseTotalPrint(d)
            d = dvalue()
            d = dvalue()
            ItemTypeTotalPrint(d)
            d = dvalue()
            d = dvalue()
            d = dvalue()
            ItemWiseClean()
            ItemTypeClean()
            d = dvalue()
            boldfonts(7)
            c.drawCentredString(300, d, Itemtype[-1])
            fonts(7)
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        ItemwiseTotalPrint(d)
        d = dvalue()
        d = dvalue()
        ItemTypeTotalPrint(d)
        d = dvalue()
        d = dvalue()
        DepartmentTotalPrint(d)
        ItemWiseClean()
        ItemTypeClean()
        DepartmentClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, divisioncode,)
        boldfonts(7)
        c.drawCentredString(300, d, Itemtype[-1])
        fonts(7)
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

