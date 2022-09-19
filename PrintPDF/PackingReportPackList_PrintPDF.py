import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date, datetime
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))

d = 750
i = 1
pageno = 0

divisioncode = []
Department = []
Date = []
cops = 0
grosswt = 0
tarewt = 0
netwt = 0
deptcops = 0
deptgrosswt = 0
depttarewt = 0
deptnetwt = 0

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
    c.drawCentredString(600, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(600, 780, "Packing List From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(1040, 780, "Page No." + str(p))
    c.line(0, 775, 1200, 775)
    c.line(0, 755, 1200, 755)
    # Upperline in header
    c.drawString(10, 760, "Sr")
    c.drawString(30, 760, "Box No")
    c.drawString(135, 760, "Date")
    c.drawString(190, 760, "Lot No.")
    c.drawString(300, 760, "Item")
    c.drawString(550, 760, "Sale Lot")
    c.drawString(650, 760, "Shade")
    c.drawString(800, 760, "Cops")
    c.drawString(880, 760, "Gross Wt.")
    c.drawString(990, 760, "TareWt.")
    c.drawString(1100, 760, "Net Wt")



def data(result, d, i):
    fonts(8)
    c.drawString(10, d, str(i))
    c.drawString(31, d, str(result['BOXNO']))
    c.drawString(191, d, str(result['LOTNO']))
    # ********************** WRAP PRODUCT ****************************************
    str1 = ''
    string = str1.join(result['PRODUCT'])
    wrap_text = textwrap.wrap(string, width=50)
    e = 0
    while e < len(wrap_text):
        c.drawString(301, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrese()
        f = f + 1
    # *****************************************************************************
    # c.drawString(301, d, str(result['PRODUCT']))
    if result['SALELOT'] != None:
        c.drawString(551, d, str(result['SALELOT']))
    c.drawString(651, d, str(result['SHADENAME']))
    c.drawAlignedString(815, d, str(result['COPS']))
    c.drawAlignedString(900, d, str(result['GROSSWT']))
    c.drawAlignedString(1010, d, str(result['TAREWT']))
    c.drawAlignedString(1120, d, str(result['NETWT']))
    DepartmentTotal(result)
    # ******************* Wrap End *********************************
    g = 0
    while g < len(wrap_text)-1:
        d = dvalue()
        d = dvalue()
        g = g + 1
    # #***************************************************************


    i = SerialNo()


def logic(result):
    global divisioncode
    global Department
    global Date
    divisioncode.append(result['COMPNAME'])
    Department.append(result['DEPARTMENT'])
    Date.append(str(result['DATES'].strftime('%d-%m-%Y')))

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global Department
    global Date
    global pageno
    divisioncode = []
    Department = []
    pageno = 0
    Date = []

def DepartmentTotal(result):
    global deptcops
    global deptgrosswt
    global deptnetwt
    global depttarewt
    deptcops = deptcops + int(result['COPS'])
    deptgrosswt = deptgrosswt + float(result['GROSSWT'])
    depttarewt = depttarewt + float(result['TAREWT'])
    deptnetwt = deptnetwt + float(result['NETWT'])

def DepartmentClean():
    global deptcops
    global deptgrosswt
    global deptnetwt
    global depttarewt
    deptcops = 0
    deptgrosswt = 0
    deptnetwt = 0
    depttarewt = 0

def CompanyTotal(result):
    global cops
    global grosswt
    global netwt
    global tarewt
    cops = cops + int(result['COPS'])
    grosswt = grosswt + float(result['GROSSWT'])
    tarewt = tarewt + float(result['TAREWT'])
    netwt = netwt + float(result['NETWT'])

def CompanyClean():
    global cops
    global grosswt
    global netwt
    global tarewt
    cops = 0
    grosswt = 0
    netwt = 0
    tarewt = 0


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        boldfonts(8)
        c.drawCentredString(600, d, Department[-1])
        d = dvalue()
        d = dvalue()
        fonts(8)
        c.drawString(125, d, Date[-1])
        data(result, d, i)
        CompanyTotal(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            if Date[-1] == Date[-2]:
                data(result, d, i)
                CompanyTotal(result)

            else:
                fonts(8)
                c.drawString(125, d, Date[-1])
                data(result, d, i)
                CompanyTotal(result)
        else:
            boldfonts(8)
            c.drawString(611, d, "Department Total: ")
            c.drawAlignedString(815, d, str(deptcops))
            c.drawAlignedString(900, d, str('{0:1.3f}'.format(deptgrosswt)))
            c.drawAlignedString(1010, d, str('{0:1.3f}'.format(depttarewt)))
            c.drawAlignedString(1120, d, str('{0:1.3f}'.format(deptnetwt)))
            DepartmentClean()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            c.drawCentredString(600, d, Department[-1])
            d = dvalue()
            d = dvalue()
            fonts(8)
            c.drawString(125, d, Date[-1])
            data(result, d, i)
            CompanyTotal(result)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(8)
        c.drawString(611, d, "Department Total: ")
        c.drawAlignedString(815, d, str(deptcops))
        c.drawAlignedString(900, d, str('{0:1.3f}'.format(deptgrosswt)))
        c.drawAlignedString(1010, d, str('{0:1.3f}'.format(depttarewt)))
        c.drawAlignedString(1120, d, str('{0:1.3f}'.format(deptnetwt)))
        d = dvalue()
        d = dvalue()
        c.drawString(611, d, "Company Total: ")
        c.drawAlignedString(815, d, str(cops))
        c.drawAlignedString(900, d, str('{0:1.3f}'.format(grosswt)))
        c.drawAlignedString(1010, d, str('{0:1.3f}'.format(tarewt)))
        c.drawAlignedString(1120, d, str('{0:1.3f}'.format(netwt)))
        CompanyClean()
        DepartmentClean()
        c.setPageSize(landscape(A3))
        c.showPage()
        SetSerialNo()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        boldfonts(8)
        c.drawCentredString(600, d, Department[-1])
        d = dvalue()
        d = dvalue()
        fonts(8)
        c.drawString(125, d, Date[-1])
        data(result, d, i)
        CompanyTotal(result)


