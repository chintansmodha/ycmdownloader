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
i = 0
pageno = 0

divisioncode = []
Department = []
Itemtype = []
# CustomerName = []
itemtotal = 0
itemtotals = 0
cops = 0
Box = 0
Boxes = 0
Compitemtotal = 0
Compitemtotals = 0
Compcops = 0
CompBox = 0
CompBoxes = 0
Deptitemtotal = 0
Deptitemtotals = 0
Deptcops = 0
DeptBox = 0
DeptBoxes = 0
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

def dvalueincrease():
    global d
    d = d + 10
    return d


def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Packing List (ItemTypewise Summary) From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header
    c.drawString(10, 765, "Item Name")
    c.drawString(250, 765, "Boxes")
    c.drawString(300, 765, "Cops")
    c.drawString(380, 765, "Net Wt.")
    c.drawString(435, 765, "Perc")
    c.drawString(530, 765, "To Date")
    c.drawString(490, 755, "Net Wt.")
    c.drawString(560, 755, "Boxes")


def data(result, d):
    fonts(7)
    str1 = ''
    string = str1.join(result['PRODUCT'])
    wrap_text = textwrap.wrap(string, width=55)
    e = 0
    while e < len(wrap_text):
        c.drawString(10, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrease()
        f = f + 1
    # c.drawString(10, d, str(result['PRODUCT']))
    c.drawAlignedString(275, d, str(result['BOXES']))
    c.drawAlignedString(320, d, str(result['COPS']))
    c.drawAlignedString(400, d, str(result['NETWT']))
    # c.drawString(435, d, str(result['PERCENTAGE']))
    c.drawAlignedString(510, d, str(result['TONETWT']))
    c.drawAlignedString(585, d, str(result['BOX']))
    DepartmentTotal(result)

    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1


def logic(result):
    global divisioncode
    global Department
    global Itemtype
    divisioncode.append(result['COMPNAME'])
    Itemtype.append(result['ITMTYPE'])
    Department.append(result['DEPARTMENT'])

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode
    global Department
    global Itemtype
    global pageno
    divisioncode = []
    Department = []
    pageno = 0
    Itemtype=[]

def ItemTotal(result):
    global itemtotal
    global itemtotals
    global cops
    global Boxes
    global Box
    itemtotal = itemtotal + float(result['NETWT'])
    itemtotals = itemtotals + float(result['TONETWT'])
    cops = cops + int(result['COPS'])
    Boxes = Boxes + int(result['BOXES'])
    Box = Box + int(result['BOX'])

def CompanyTotal(result):
    global Compitemtotal
    global Compitemtotals
    global Compcops
    global CompBox
    global CompBoxes
    Compitemtotal = Compitemtotal + float(result['NETWT'])
    Compitemtotals = Compitemtotals + float(result['TONETWT'])
    Compcops = Compcops + int(result['COPS'])
    CompBoxes = CompBoxes + int(result['BOXES'])
    CompBox = CompBox + int(result['BOX'])

def DepartmentTotal(result):
    global Deptitemtotal
    global Deptitemtotals
    global Deptcops
    global DeptBox
    global DeptBoxes
    Deptitemtotal = Deptitemtotal + float(result['NETWT'])
    Deptitemtotals = Deptitemtotals + float(result['TONETWT'])
    Deptcops = Deptcops + int(result['COPS'])
    DeptBoxes = DeptBoxes + int(result['BOXES'])
    DeptBox = DeptBox + int(result['BOX'])

def ItemTotalClean():
    global itemtotal
    global itemtotals
    global cops
    global Boxes
    global Box
    itemtotal = 0
    itemtotals = 0
    cops = 0
    Boxes = 0
    Box = 0

def DepartmentClean():
    global Deptitemtotal
    global Deptitemtotals
    global Deptcops
    global DeptBox
    global DeptBoxes
    Deptitemtotal = 0
    Deptitemtotals = 0
    Deptcops = 0
    DeptBox = 0
    DeptBoxes = 0

def CompanyClean():
    global Compitemtotal
    global Compitemtotals
    global Compcops
    global CompBox
    global CompBoxes
    Compitemtotal = 0
    Compitemtotals = 0
    Compcops = 0
    CompBox = 0
    CompBoxes = 0


def textsize(c, result, d, stdt, etdt,netwt):
    d = dvalue()
    logic(result)
    global i

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        ItemTotalClean()
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        c. drawString(10, d, Itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)
        ItemTotal(result)
        CompanyTotal(result)
        i = 0
        if int(netwt[i]) != 0:
            PERCENTAGE = (float(result['NETWT']) / (float(netwt[i]))) * 100
            c.drawAlignedString(450, d, str(round(PERCENTAGE)) + "%")
        else:
            c.drawAlignedString(450, d, "0%")

    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            if Itemtype[-1] == Itemtype[-2]:
                data(result, d)
                ItemTotal(result)
                CompanyTotal(result)
                if int(netwt[i]) != 0:
                    PERCENTAGE = (float(result['NETWT']) / (float(netwt[i]))) * 100
                    c.drawAlignedString(450, d, str(round(PERCENTAGE)) + "%")
                else:
                    c.drawAlignedString(450, d, "0%")

            else:
                boldfonts(7)
                c.drawString(100, d, "Item Type Total: ")
                c.drawAlignedString(275, d, str(Boxes))
                c.drawAlignedString(320, d, str(cops))
                c.drawAlignedString(400, d, str('{0:1.3f}'.format(itemtotal)))
                c.drawAlignedString(510, d, str('{0:1.3f}'.format(itemtotals)))
                c.drawAlignedString(585, d, str(Box))
                ItemTotalClean()
                d = dvalue()
                d = dvalue()
                boldfonts(7)
                d = dvalue()
                c.drawString(10, d, Itemtype[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)
                ItemTotal(result)
                CompanyTotal(result)
                i = i + 1
                if int(netwt[i]) != 0:
                    PERCENTAGE = (float(result['NETWT']) / (float(netwt[i]))) * 100
                    c.drawAlignedString(450, d, str(round(PERCENTAGE)) + "%")
                else:
                    c.drawAlignedString(450, d, "0%")
        else:
            boldfonts(7)
            c.drawString(100, d, "Item Type Total: ")
            c.drawAlignedString(275, d, str(Boxes))
            c.drawAlignedString(320, d, str(cops))
            c.drawAlignedString(400, d, str('{0:1.3f}'.format(itemtotal)))
            c.drawAlignedString(510, d, str('{0:1.3f}'.format(itemtotals)))
            c.drawAlignedString(585, d, str(Box))
            d = dvalue()
            d = dvalue()
            c.drawString(100, d, "Dept Total: ")
            c.drawAlignedString(275, d, str(DeptBoxes))
            c.drawAlignedString(320, d, str(Deptcops))
            c.drawAlignedString(400, d, str('{0:1.3f}'.format(Deptitemtotal)))
            c.drawAlignedString(510, d, str('{0:1.3f}'.format(Deptitemtotals)))
            c.drawAlignedString(585, d, str(DeptBox))
            ItemTotalClean()
            DepartmentClean()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            c.drawCentredString(300, d, Department[-1])
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, Itemtype[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)
            ItemTotal(result)
            CompanyTotal(result)
            i = i + 1
            if int(netwt[i]) != 0:
                PERCENTAGE = (float(result['NETWT']) / (float(netwt[i]))) * 100
                c.drawAlignedString(450, d, str(round(PERCENTAGE)) + "%")
            else:
                c.drawAlignedString(450, d, "0%")


    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.drawString(100, d, "Item Type Total: ")
        c.drawAlignedString(275, d, str(Boxes))
        c.drawAlignedString(320, d, str(cops))
        c.drawAlignedString(400, d, str('{0:1.3f}'.format(itemtotal)))
        c.drawAlignedString(510, d, str('{0:1.3f}'.format(itemtotals)))
        c.drawAlignedString(585, d, str(Box))
        d = dvalue()
        d = dvalue()
        c.drawString(100, d, "Dept Total: ")
        c.drawAlignedString(275, d, str(DeptBoxes))
        c.drawAlignedString(320, d, str(Deptcops))
        c.drawAlignedString(400, d, str('{0:1.3f}'.format(Deptitemtotal)))
        c.drawAlignedString(510, d, str('{0:1.3f}'.format(Deptitemtotals)))
        c.drawAlignedString(585, d, str(DeptBox))
        d = dvalue()
        d = dvalue()
        c.drawString(100, d, "Company Total: ")
        c.drawAlignedString(275, d, str(CompBoxes))
        c.drawAlignedString(320, d, str(Compcops))
        c.drawAlignedString(400, d, str('{0:1.3f}'.format(Compitemtotal)))
        c.drawAlignedString(510, d, str('{0:1.3f}'.format(Compitemtotals)))
        c.drawAlignedString(585, d, str(CompBox))
        ItemTotalClean()
        DepartmentClean()
        CompanyClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt,etdt,divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)
        ItemTotal(result)
        CompanyTotal(result)
        i = i + 1
        if int(netwt[i]) != 0:
            PERCENTAGE = (float(result['NETWT']) / (float(netwt[i]))) * 100
            c.drawAlignedString(450, d, str(round(PERCENTAGE)) + "%")
        else:
            c.drawAlignedString(450, d, "0%")