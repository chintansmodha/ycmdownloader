from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal
# from simple_colors import black

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
import textwrap

c = canvas.Canvas("1.pdf")
d = 735

divisioncode = []
Itemname = []
# OrdNo = []
# CustomerName = []
IssueDept = []
pageno = 0
date=[]
IssueDepttotal = 0
Issuebox = 0
Issuecops = 0
Depttotal = 0
Deptbox = 0
Deptcops = 0
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

def dvalue():
    global d
    d = d - 5
    return d

def dvalueaddstep():
    global d
    d = d + 15
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
    c.drawString(10, 760, "Issued To Dept")
    c.drawString(185, 760, "Item Name")
    c.drawString(435, 760, "Quantity")
    c.drawString(480, 760, "Cops")
    c.drawString(510, 760, "Boxes")
    c.drawString(545, 760, "Status")


def data(result, d):
    fonts(7)
    # c.drawString(188, d, result['PRODUCTNAME'])
    c.drawAlignedString(455, d, str((result['QUANTITY'])))
    c.drawAlignedString(500, d, str(result['COPS']))
    c.drawAlignedString(530, d, str(result['BOXES']))
    c.drawString(547, d, result['STATUS'])
    wrap_text = textwrap.wrap(result['PRODUCTNAME'], 50, break_long_words=False)
    # print(str(wrap_text)[1:-2])
    # print(str(wrap_text)[1:-2].split().pop(0))
    # print(black('hello', 'bold'))
    e = 0
    while e < len(wrap_text):
        c.drawString(188, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e += 1
    d = dvalueaddstep()

def logic(result):
    global divisioncode
    global IssueDept
    divisioncode.append(result['DEPARTMENT'])
    IssueDept.append(result['ISSUETODEPARTMENT'])

def newpage():
    global d
    d = 735
    return d

def newrequest():
    global divisioncode
    global pageno
    global IssueDept
    divisioncode = []
    pageno = 0
    IssueDept = []

def total(result):
    global IssueDepttotal, Issuecops, Issuebox
    global Depttotal, Deptcops, Deptbox
    global grandtotal, grandcops, grandbox
    IssueDepttotal = IssueDepttotal + float(result['QUANTITY'])
    Issuecops += int(result['COPS'])
    Issuebox += int(result['BOXES'])
    Depttotal = Depttotal + float(result['QUANTITY'])
    Deptcops += int(result['COPS'])
    Deptbox += int(result['BOXES'])
    grandtotal = grandtotal + float(result['QUANTITY'])
    grandcops += int(result['COPS'])
    grandbox += int(result['BOXES'])

def issueTotalClean():
    global IssueDepttotal, Issuecops, Issuebox
    IssueDepttotal = 0
    Issuebox = 0
    Issuecops = 0

def depttotalClean():
    global Depttotal, Deptcops, Deptbox
    Depttotal = 0
    Deptbox = 0
    Deptcops = 0

def grandtotalClean():
    global grandtotal, grandcops, grandbox
    grandtotal = 0
    grandbox = 0
    grandcops = 0

def Clean():
    global IssueDepttotal, Issuecops, Issuebox
    global Depttotal, Deptcops, Deptbox
    global grandtotal, grandcops, grandbox
    IssueDepttotal = 0
    Issuebox = 0
    Issuecops = 0
    Depttotal = 0
    Deptbox = 0
    Deptcops = 0
    grandtotal = 0
    grandbox = 0
    grandcops = 0

def textsize(c, result, d, stdt, etdt, Summary, IssueStatus):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
        fonts(7)
        Clean()

        if len(IssueDept) == 1:
            c.drawString(10, d, IssueDept[-1])
            data(result,d)
            total(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if IssueDept[-1] == IssueDept[-2]:
            data(result,d)
            total(result)

        else:
            boldfonts(8)
            d = dvalue()
            c.drawString(250, d, 'Issued To Whouse Total:')
            c.drawAlignedString(455, d, str('{0:1.3f}'.format(IssueDepttotal)))
            c.drawAlignedString(500, d, str(Issuecops))
            c.drawAlignedString(530, d, str(Issuebox))
            issueTotalClean()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            fonts(7)
            c.drawString(10, d, IssueDept[-1])
            data(result, d)
            total(result)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(8)
        d = dvalue()
        d = dvalue()
        c.drawString(250, d, 'Issued To Whouse Total: ')
        c.drawAlignedString(455, d, str('{0:1.3f}'.format(IssueDepttotal)))
        c.drawAlignedString(500, d, str(Issuecops))
        c.drawAlignedString(530, d, str(Issuebox))
        d = dvalue()
        d = dvalue()
        c.drawString(250, d, 'Warehouse Total: ')
        c.drawAlignedString(455, d, str('{0:1.3f}'.format(Depttotal)))
        c.drawAlignedString(500, d, str(Deptcops))
        c.drawAlignedString(530, d, str(Deptbox))
        issueTotalClean()
        depttotalClean()
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode, Summary, IssueStatus)
        d = dvalue()
        fonts(7)
        c.drawString(10, d, IssueDept[-1])
        data(result, d)
        total(result)