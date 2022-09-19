from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal
import textwrap

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 745

divisioncode = []
Itemname = []
IssueDept = []
# OrdNo = []
# CustomerName = []
itemlineCount = 0
count = 0
pageno = 0
date=[]
itemtotal = 0
itembox = 0
itemcops = 0
issuedepttotal = 0
issuebox = 0
issuecops = 0
depttotal = 0
deptbox = 0
deptcops = 0
grandtotal = 0
grandbox = 0
grandcops = 0
# DocumentType = []
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


def dvalue(stdt, etdt, divisioncode, Summary, IssueStatus):
    global d
    if d<30:
        c.showPage()
        d = newpage()
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
    else:
        d = d - 5
    return d

def dincrease():
    global d
    d = d + 10
    return d

def wrap(string,d):
    global itemlineCount
    text = textwrap.wrap(string, 50)
    itemlineCount = 0
    while itemlineCount < len(text):
        c.drawString(10, d, str(text[itemlineCount]))
        d = d - 10
        itemlineCount += 1
    return d

def header(stdt, etdt, divisioncode, Summary, IssueStatus):
    c.setTitle("Material Issue Register [ "+ Summary +" ][ "+ IssueStatus + " ]")
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, "Material Issue Register [ "+ Summary +" ] From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) +" [ "+ IssueStatus + " ]" )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header
    c.drawString(10, 760, "Item Name")
    c.drawString(275, 760, "Lot No.")
    c.drawString(365, 760, "Quantity")
    c.drawString(430, 760, "Cops")
    c.drawString(490, 760, "Boxes")
    c.drawString(540, 760, "Status")


def data(result, d):
    fonts(7)
    # c.drawString(10, d, result['ISSUENO'])
    # c.drawString(60, d, result['ISSUEDT'].strftime('%d-%m-%Y'))
    # c.drawString(120, d, (result['ISSUETODEPARTMENT']))
    c.drawString(275, d, result['LOTNO'])
    # c.drawString(380, d, result['BASENAME'])
    # c.drawString(188, d, result['PRODUCTNAME'])
    c.drawAlignedString(385, d, str((result['QUANTITY'])))
    c.drawAlignedString(452, d, str(result['COPS']))
    c.drawAlignedString(512, d, str(result['BOXES']))
    c.drawString(540, d, result['STATUS'])
    total(result)


def logic(result):
    global divisioncode
    global Itemname
    global IssueDept
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCTNAME'])
    IssueDept.append(result['ISSUETODEPARTMENT'])

def newpage():
    global d
    d = 745
    return d

def newrequest():
    global divisioncode
    global pageno
    global Itemname
    global IssueDept
    divisioncode = []
    pageno = 0
    Itemname = []
    IssueDept = []

def total(result):
    global issuedepttotal, issuebox, issuecops
    global itemtotal, itembox, itemcops
    global depttotal, deptbox, deptcops
    global grandtotal, grandbox, grandcops
    issuedepttotal =  issuedepttotal + float(result['QUANTITY'])
    issuecops += int(result['COPS'])
    issuebox += int(result['BOXES'])
    depttotal = depttotal + float(result['QUANTITY'])
    deptcops += int(result['COPS'])
    deptbox += int(result['BOXES'])
    itemtotal = itemtotal + float(result['QUANTITY'])
    itemcops += int(result['COPS'])
    itembox += int(result['BOXES'])
    grandtotal = grandtotal + float(result['QUANTITY'])
    grandcops += int(result['COPS'])
    grandbox += int(result['BOXES'])

def issueTotalClean():
    global issuedepttotal, issuebox, issuecops
    issuedepttotal = 0
    issuebox = 0
    issuecops = 0


def deptTotalClean():
    global depttotal, deptbox, deptcops
    depttotal = 0
    deptbox = 0
    deptcops = 0


def itemTotalClean():
    global itemtotal, itembox, itemcops
    itemtotal = 0
    itembox = 0
    itemcops = 0


def grandTotalClean():
    global grandtotal, grandbox, grandcops
    grandtotal = 0
    grandcops = 0
    grandbox = 0

def Clean():
    global issuedepttotal, issuebox, issuecops
    global itemtotal, itembox, itemcops
    global depttotal, deptbox, deptcops
    global grandtotal, grandbox, grandcops
    itemtotal = 0
    itembox = 0
    itemcops = 0
    issuedepttotal = 0
    issuebox = 0
    issuecops = 0
    depttotal = 0
    deptbox = 0
    deptcops = 0
    grandtotal = 0
    grandbox = 0
    grandcops = 0

def textsize(c, result, d, stdt, etdt, Summary, IssueStatus):
    d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
    logic(result)
    global count, itemlineCount

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
        boldfonts(7)
        Clean()
        # if len(IssueDept) == 1:
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        c.drawString(10, d, IssueDept[-1])
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        fonts(7)
        wrap(Itemname[-1], d)
        data(result,d)

        count = count + 1

    elif divisioncode[-1] == divisioncode[-2]:
        if IssueDept[-1] == IssueDept[-2]:
            if Itemname[-1] == Itemname[-2]:
                data(result,d)

                count = count + 1

            else:
                if count > 1:
                    boldfonts(8)
                    c.drawString(250, d, 'Item Total: ')
                    c.drawAlignedString(385, d, str('{0:1.3f}'.format(itemtotal)))
                    c.drawAlignedString(452, d, str(itemcops))
                    c.drawAlignedString(512, d, str(itembox))
                    d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                    d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                    count = 0
                    itemTotalClean()
                    fonts(7)
                    if count < itemlineCount:
                        i = 0
                        while i < itemlineCount:
                            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                            i += 1
                else:
                    i = 0
                    while i <= itemlineCount:
                        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                        i += 1
                count = 0
                wrap(Itemname[-1], d)
                data(result,d)

                count = count + 1

        else:
            boldfonts(8)
            if count > 1:
                c.drawString(250, d, 'Item Total: ')
                c.drawAlignedString(385, d, str('{0:1.3f}'.format(itemtotal)))
                c.drawAlignedString(452, d, str(itemcops))
                c.drawAlignedString(512, d, str(itembox))
                d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                c.drawString(250, d, 'Issued To Whouse Total: ')
                c.drawAlignedString(385, d, str('{0:1.3f}'.format(issuedepttotal)))
                c.drawAlignedString(452, d, str(issuecops))
                c.drawAlignedString(512, d, str(issuebox))
                count = 0
                if count < itemlineCount:
                    i = 0
                    while i < itemlineCount:
                        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                        i += 1
            else:
                c.drawString(250, d, 'Issued To Whouse Total: ')
                c.drawAlignedString(385, d, str('{0:1.3f}'.format(issuedepttotal)))
                c.drawAlignedString(452, d, str(issuecops))
                c.drawAlignedString(512, d, str(issuebox))
                i = 0
                while i < itemlineCount:
                    d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                    i += 1
            issueTotalClean()
            itemTotalClean()
            count = 0
            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
            boldfonts(7)
            c.drawString(10, d, IssueDept[-1])
            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
            fonts(7)
            wrap(Itemname[-1], d)
            data(result, d)

            count = count + 1

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(8)
        if count > 1:
            c.drawString(250, d, 'Item Total: ')
            c.drawAlignedString(385, d, str('{0:1.3f}'.format(itemtotal)))
            c.drawAlignedString(452, d, str(itemcops))
            c.drawAlignedString(512, d, str(itembox))
            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
            d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
            # count = 0
            if count < itemlineCount:
                i = 0
                while i < itemlineCount:
                    d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
                    i += 1
        # else:
        #     i = 0
        #     while i < itemlineCount:
        #         d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        #         i += 1
        c.drawString(250, d, 'Issued To Whouse Total: ')
        c.drawAlignedString(385, d, str('{0:1.3f}'.format(issuedepttotal)))
        c.drawAlignedString(452, d, str(issuecops))
        c.drawAlignedString(512, d, str(issuebox))
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        c.drawString(250, d, 'Warehouse Total: ')
        c.drawAlignedString(385, d, str('{0:1.3f}'.format(depttotal)))
        c.drawAlignedString(452, d, str(deptcops))
        c.drawAlignedString(512, d, str(deptbox))
        issueTotalClean()
        deptTotalClean()
        itemTotalClean()
        count = 0
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        boldfonts(7)
        c.drawString(10, d, IssueDept[-1])
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        d = dvalue(stdt, etdt, divisioncode, Summary, IssueStatus)
        fonts(7)
        wrap(Itemname[-1], d)
        data(result, d)

        count = count + 1
