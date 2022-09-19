from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 735

divisioncode = []
Itemname = []
OrdNo = []
# CustomerName = []
pageno = 0
date=[]
itemtotal = 0
itemcops = 0
itembox = 0
departmenttotal = 0
departmentcops = 0
departmentbox = 0
grandtotal = 0
grandcops = 0
grandbox = 0
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

def dvalue():
    global d
    d = d - 5
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
    c.drawString(10,  760, "Issue No")
    c.drawString(90,  760, "Iss. Dt")
    c.drawString(140, 760, "Issued To Dept")
    c.drawString(320, 760, "Lot No")
    c.drawString(380, 760, "Base Name")
    c.drawString(435, 760, "Quantity")
    c.drawString(480, 760, "Cops")
    c.drawString(510, 760, "Boxes")
    c.drawString(545, 760, "Status")


def data(result, d):
    fonts(7)
    # c.drawString(10, d, result['ISSUENO'])
    # c.drawString(60, d, result['ISSUEDT'].strftime('%d-%m-%Y'))
    c.drawString(140, d, (result['ISSUETODEPARTMENT']))
    c.drawString(320, d, result['LOTNO'])
    c.drawString(380, d, result['BASENAME'])
    c.drawAlignedString(455, d, str((result['QUANTITY'])))
    c.drawAlignedString(500, d, str(result['COPS']))
    c.drawAlignedString(532, d, str(result['BOXES']))
    c.drawString(545, d, result['STATUS'])


def logic(result):
    global divisioncode
    global Itemname
    global OrdNo
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCTNAME'])
    OrdNo.append(result['ISSUENO'])

def newpage():
    global d
    d = 735
    return d

def newrequest():
    global divisioncode
    global pageno
    global Itemname
    global OrdNo
    divisioncode = []
    pageno = 0
    Itemname=[]
    OrdNo = []

def total(result):
    global itemtotal, itemcops, itembox
    global departmenttotal, departmentcops, departmentbox
    global grandtotal, grandcops, grandbox

    itemtotal = itemtotal + float(result['QUANTITY'])
    itemcops += int(result['COPS'])
    itembox += int(result['BOXES'])
    departmenttotal = departmenttotal + float(result['QUANTITY'])
    departmentcops += int(result['COPS'])
    departmentbox += int(result['BOXES'])
    grandtotal = grandtotal + float(result['QUANTITY'])
    grandcops += int(result['COPS'])
    grandbox += int(result['BOXES'])

def itemtotalClean():
    global itemtotal, itemcops, itembox
    itemtotal = 0
    itemcops = 0
    itembox = 0

def departmenttotalClean():
    global departmenttotal, departmentcops, departmentbox
    departmenttotal = 0
    departmentcops = 0
    departmentbox = 0

def grandtotalClean():
    global grandtotal, grandcops, grandbox
    grandtotal = 0
    grandcops = 0
    grandbox = 0

def clean():
    global itemtotal, itemcops, itembox
    global departmenttotal, departmentcops, departmentbox
    global grandtotal, grandcops, grandbox
    itemtotal = 0
    itemcops = 0
    itembox = 0
    departmenttotal = 0
    departmentcops = 0
    departmentbox = 0
    grandtotal = 0
    grandcops = 0
    grandbox = 0

def textsize(c, result, d, stdt, etdt, Summary, IssueStatus):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
        clean()
        # c.drawString(10,735,Itemname[-1])
        fonts(7)
        if len(Itemname) == 1:
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, OrdNo[-1])
            c.drawString(90, d, result['ISSUEDT'].strftime('%d-%m-%Y'))
            # d = dvalue()
            data(result,d)
            total(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if Itemname [-1] == Itemname[-2]:
            if OrdNo[-1] == OrdNo[-2]:
                data(result,d)
                total(result)
            else:
                c.drawString(10, d, OrdNo[-1])
                c.drawString(90, d, result['ISSUEDT'].strftime('%d-%m-%Y'))
                data(result,d)
                total(result)
        else:
            d = dvalue()
            boldfonts(8)
            c.drawString (350, d, 'Item Total: ')
            c.drawAlignedString(455, d, str('{0:1.3f}'.format(itemtotal)))
            c.drawAlignedString(500, d, str(itemcops))
            c.drawAlignedString(532, d, str(itembox))
            itemtotalClean()
            d = dvalue()
            d = dvalue()
            fonts(7)
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, OrdNo[-1])
            c.drawString(90, d, result['ISSUEDT'].strftime('%d-%m-%Y'))
            # d = dvalue()
            data(result, d)
            total(result)



    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(8)
        d = dvalue()
        c.drawString(350, d, 'Item Total: ')
        c.drawAlignedString(455, d, str('{0:1.3f}'.format(itemtotal)))
        c.drawAlignedString(500, d, str(itemcops))
        c.drawAlignedString(532, d, str(itembox))
        d = dvalue()
        d = dvalue()
        c.drawString(350, d, 'Warehouse Total: ')
        c.drawAlignedString(455, d, str('{0:1.3f}'.format(departmenttotal)))
        c.drawAlignedString(500, d, str(departmentcops))
        c.drawAlignedString(532, d, str(departmentbox))
        itemtotalClean()
        departmenttotalClean()
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
        fonts(9)
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, OrdNo[-1])
        c.drawString(90, d, result['ISSUEDT'].strftime('%d-%m-%Y'))
        data(result, d)
        total(result)