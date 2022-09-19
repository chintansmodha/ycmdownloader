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
Department = []
Itemname = []
ShadeName = []
ShadeCode =  []
LotNo = []
ItmBoxes = 0
ItmCops = 0
ItmGross = 0
ItmTare = 0
ItmNetwt = 0
DeptBoxes = 0
DeptCops = 0
DeptGross = 0
DeptTare = 0
DeptNetwt = 0
CompBoxes = 0
CompCops = 0
CompGross = 0
CompTare = 0
CompNetwt = 0

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

def SerialNo():
    global i
    i = i + 1
    return i

def SetSerialNo():
    global i
    i = 1
    return i

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Item-wise Production From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Lot No")
    c.drawString(90, 760, "WT")
    c.drawString(140, 760, "Boxes")
    c.drawString(220, 760, "Cops")
    c.drawString(330, 760, "Gross Wt")
    c.drawString(440, 760, "Tare Wt")
    c.drawString(550, 760, "Net Wt")



def data(result, d):
    fonts(7)
    c.drawString(11, d, str(result['LOTNO']))
    c.drawString(94, d, str(result['WT']))
    c.drawAlignedString(160, d, str(result['BOXES']))
    c.drawAlignedString(240, d, str(result['COPS']))
    c.drawAlignedString(350, d, str(result['GROSSWT']))
    c.drawAlignedString(460, d, str(result['TAREWT']))
    c.drawAlignedString(570, d, str(result['NETWT']))
    ItmwiseTotal(result)
    DepartmentTotal(result)
    CompanyTotal(result)


def logic(result):
    global divisioncode
    global Department
    global Itemname
    divisioncode.append(result['COMPNAME'])
    Itemname.append(result['PRODUCT'])
    Department.append(result['DEPARTMENT'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global Department
    global Itemname
    global pageno
    divisioncode = []
    Department = []
    Itemname = []
    pageno = 0

def ItmwiseTotal(result):
    global ItmBoxes
    global ItmCops
    global ItmGross, ItmTare, ItmNetwt
    ItmBoxes = ItmBoxes + int(result['BOXES'])
    ItmCops = ItmCops + int(result['COPS'])
    ItmGross = ItmGross + float(result['GROSSWT'])
    ItmTare = ItmTare + float(result['TAREWT'])
    ItmNetwt = ItmNetwt + float(result['NETWT'])

def ItmwiseClean():
    global ItmBoxes
    global ItmCops
    global ItmGross, ItmTare, ItmNetwt
    ItmBoxes = 0
    ItmCops = 0
    ItmGross = 0
    ItmTare = 0
    ItmNetwt = 0

def DepartmentTotal(result):
    global DeptBoxes
    global DeptCops
    global DeptGross, DeptTare, DeptNetwt
    DeptBoxes = DeptBoxes + int(result['BOXES'])
    DeptCops = DeptCops + int(result['COPS'])
    DeptGross = DeptGross + float(result['GROSSWT'])
    DeptTare = DeptTare + float(result['TAREWT'])
    DeptNetwt = DeptNetwt + float(result['NETWT'])

def DepartmentClean():
    global DeptBoxes
    global DeptCops
    global DeptGross, DeptTare, DeptNetwt
    DeptBoxes = 0
    DeptCops = 0
    DeptGross = 0
    DeptTare = 0
    DeptNetwt = 0

def CompanyTotal(result):
    global CompBoxes
    global CompCops
    global CompGross, CompTare, CompNetwt
    CompBoxes = CompBoxes + int(result['BOXES'])
    CompCops = CompCops + int(result['COPS'])
    CompGross = CompGross + float(result['GROSSWT'])
    CompTare = CompTare + float(result['TAREWT'])
    CompNetwt = CompNetwt + float(result['NETWT'])

def CompanyClean():
    global CompBoxes
    global CompCops
    global CompGross, CompTare, CompNetwt
    CompBoxes = 0
    CompCops = 0
    CompGross = 0
    CompTare = 0
    CompNetwt = 0


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        ItmwiseClean()
        CompanyClean()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            if Itemname[-1] == Itemname[-2]:
                data(result, d)

            else:
                boldfonts(7)
                c.drawString(30, d, "Item-Wise Total: ")
                c.drawAlignedString(160, d, str(ItmBoxes))
                c.drawAlignedString(240, d, str(ItmCops))
                c.drawAlignedString(350, d, str('{0:1.3f}'.format(ItmGross)))
                c.drawAlignedString(460, d, str('{0:1.3f}'.format(ItmTare)))
                c.drawAlignedString(570, d, str('{0:1.3f}'.format(ItmNetwt)))
                ItmwiseClean()
                d = dvalue()
                d = dvalue()
                d = dvalue()
                c.drawString(10, d, Itemname[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)
        else:
            boldfonts(7)
            c.drawString(30, d, "Item-Wise Total: ")
            c.drawAlignedString(160, d, str(ItmBoxes))
            c.drawAlignedString(240, d, str(ItmCops))
            c.drawAlignedString(350, d, str('{0:1.3f}'.format(ItmGross)))
            c.drawAlignedString(460, d, str('{0:1.3f}'.format(ItmTare)))
            c.drawAlignedString(570, d, str('{0:1.3f}'.format(ItmNetwt)))
            d = dvalue()
            d = dvalue()
            c.drawString(30, d, "Dept Total: ")
            c.drawAlignedString(160, d, str(DeptBoxes))
            c.drawAlignedString(240, d, str(DeptCops))
            c.drawAlignedString(350, d, str('{0:1.3f}'.format(DeptGross)))
            c.drawAlignedString(460, d, str('{0:1.3f}'.format(DeptTare)))
            c.drawAlignedString(570, d, str('{0:1.3f}'.format(DeptNetwt)))
            ItmwiseClean()
            DepartmentClean()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            c.drawCentredString(300, d, Department[-1])
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        # d = dvalue()
        c.drawString(30, d, "Item-Wise Total: ")
        c.drawAlignedString(160, d, str(ItmBoxes))
        c.drawAlignedString(240, d, str(ItmCops))
        c.drawAlignedString(350, d, str('{0:1.3f}'.format(ItmGross)))
        c.drawAlignedString(460, d, str('{0:1.3f}'.format(ItmTare)))
        c.drawAlignedString(570, d, str('{0:1.3f}'.format(ItmNetwt)))
        d = dvalue()
        d = dvalue()
        c.drawString(30, d, "Dept Total: ")
        c.drawAlignedString(160, d, str(DeptBoxes))
        c.drawAlignedString(240, d, str(DeptCops))
        c.drawAlignedString(350, d, str('{0:1.3f}'.format(DeptGross)))
        c.drawAlignedString(460, d, str('{0:1.3f}'.format(DeptTare)))
        c.drawAlignedString(570, d, str('{0:1.3f}'.format(DeptNetwt)))
        d = dvalue()
        d = dvalue()
        c.drawString(30, d, "Company Total: ")
        c.drawAlignedString(160, d, str(CompBoxes))
        c.drawAlignedString(240, d, str(CompCops))
        c.drawAlignedString(350, d, str('{0:1.3f}'.format(CompGross)))
        c.drawAlignedString(460, d, str('{0:1.3f}'.format(CompTare)))
        c.drawAlignedString(570, d, str('{0:1.3f}'.format(CompNetwt)))
        ItmwiseClean()
        DepartmentClean()
        CompanyClean()
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)
