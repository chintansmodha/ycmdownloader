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
lotcopstotal = 0
lotgrosstotal = 0
lottarewttotal = 0
lotnettotal = 0
depttotal = 0
deptcopstotal = 0
deptgrosstotal = 0
depttarewttotal = 0
deptnetwttotal = 0
itemtotal = 0
itemcopstotal = 0
itemgrosstotal = 0
itemtarewttotal = 0
itemnetwttotal = 0
Comptotal = 0
Compcopstotal = 0
Compgrosstotal = 0
Comptarewttotal = 0
Compnetwttotal = 0

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
    c.drawCentredString(300, 780, "Packing Report From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 755, 600, 755)
    # Upperline in header
    c.drawString(10, 760, "Sr")
    c.drawString(30, 760, "Box No")
    c.drawString(100, 760, "CS")
    c.drawString(120, 760, "BT")
    c.drawString(180, 760, "Tw")
    c.drawString(210, 760, "WT")
    c.drawString(240, 760, "PS")
    c.drawString(260, 760, "Cops")
    c.drawString(310, 760, "Gross Wt")
    c.drawString(380, 760, "Tare Wt")
    c.drawString(460, 760, "Net Wt")
    c.drawString(540, 760, "Remarks")



def data(result, d, i):
    fonts(7)
    c.drawString(10, d, str(i))
    c.drawString(30, d, str(result['BOXNO']))
    c.drawString(100, d, str(result['CS']))
    c.drawString(120, d, str(result['BT']))
    c.drawString(182, d, str(result['TW']))
    c.drawString(212, d, str(result['WT']))
    c.drawString(243, d, str(result['PS']))
    c.drawAlignedString(280, d, str(result['COPS']))
    c.drawAlignedString(330, d, str(result['GROSSWT']))
    c.drawAlignedString(400, d, str(result['TAREWT']))
    c.drawAlignedString(480, d, str(result['NETWT']))
    c.drawString(540, d, str(result['REMARKS'])[1:15])

    i = SerialNo()
    Itemtotal(result)
    Companytotal(result)


def logic(result):
    global divisioncode
    global Department
    global Itemname
    global ShadeName
    global ShadeCode
    global LotNo
    divisioncode.append(result['COMPNAME'])
    Itemname.append(result['PRODUCT'])
    LotNo.append(result['LOTNO'])
    ShadeName.append(result['SHADENAME'])
    Department.append(result['DEPARTMENT'])
    # if result['SHADECODE'] != None:
    #     ShadeCode.append(result['SHADECODE'])
    # OrdNo.append(result['ISSUENO'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global Department
    global Itemname
    global ShadeName
    global ShadeCode
    global LotNo
    global pageno
    divisioncode = []
    Department = []
    pageno = 0
    Itemname=[]
    ShadeName = []
    ShadeCode = []
    LotNo = []

def LotClean():
    global  lotcopstotal
    global lotgrosstotal
    global lotnettotal
    global lottarewttotal
    lotcopstotal = 0
    lotgrosstotal = 0
    lottarewttotal = 0
    lotnettotal = 0

def LotTotal(result):
    global lotcopstotal
    global lotgrosstotal
    global lotnettotal
    global lottarewttotal
    lotcopstotal = lotcopstotal + int(result['COPS'])
    lotgrosstotal = lotgrosstotal + float(result['GROSSWT'])
    lottarewttotal = lottarewttotal + float(result['TAREWT'])
    lotnettotal = lotnettotal + float(result['NETWT'])

def ItemClean():
    global itemtotal
    global itemcopstotal
    global itemgrosstotal
    global itemtarewttotal
    global itemnetwttotal
    itemtotal = 0
    itemcopstotal = 0
    itemgrosstotal = 0
    itemtarewttotal = 0
    itemnetwttotal = 0

def Itemtotal(result):
    global itemcopstotal
    global itemgrosstotal
    global itemtarewttotal
    global itemnetwttotal
    itemcopstotal = itemcopstotal  + int(result['COPS'])
    itemgrosstotal = itemgrosstotal  + float(result['GROSSWT'])
    itemtarewttotal = itemtarewttotal  + float(result['TAREWT'])
    itemnetwttotal = itemnetwttotal  + float(result['NETWT'])

def departmentClean():
    global depttotal
    global deptcopstotal
    global deptgrosstotal
    global depttarewttotal
    global deptnetwttotal
    depttotal = 0
    deptcopstotal = 0
    deptgrosstotal = 0
    depttarewttotal = 0
    deptnetwttotal = 0

def departmenttotal(result):
    # global depttotal
    global deptcopstotal
    global deptgrosstotal
    global depttarewttotal
    global deptnetwttotal
    # depttotal = depttotal + i
    deptcopstotal = deptcopstotal  + int(result['COPS'])
    deptgrosstotal = deptgrosstotal  + float(result['GROSSWT'])
    depttarewttotal = depttarewttotal  + float(result['TAREWT'])
    deptnetwttotal = deptnetwttotal  + float(result['NETWT'])

def CompanyClean():
    global Comptotal
    global Compcopstotal
    global Compgrosstotal
    global Comptarewttotal
    global Compnetwttotal
    Comptotal = 0
    Compcopstotal = 0
    Compgrosstotal = 0
    Comptarewttotal = 0
    Compnetwttotal = 0

def Companytotal(result):
    global Compcopstotal
    global Compgrosstotal
    global Comptarewttotal
    global Compnetwttotal
    Compcopstotal = Compcopstotal  + int(result['COPS'])
    Compgrosstotal = Compgrosstotal  + float(result['GROSSWT'])
    Comptarewttotal = Comptarewttotal  + float(result['TAREWT'])
    Compnetwttotal = Compnetwttotal  + float(result['NETWT'])

def Total():
    global depttotal, itemtotal, Comptotal
    depttotal = depttotal + i - 1
    itemtotal = itemtotal + i - 1
    Comptotal = Comptotal + i - 1

def LotTotalPrint(d,i):
    Total()
    boldfonts(7)
    c.drawString(130, d, "Lot Total: ")
    c.drawString(210, d, str(i - 1))
    c.drawAlignedString(280, d, str(lotcopstotal))
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(lotgrosstotal)))
    c.drawAlignedString(400, d, str('{0:1.3f}'.format(lottarewttotal)))
    c.drawAlignedString(480, d, str('{0:1.3f}'.format(lotnettotal)))
    fonts(7)

def ItemTotalPrint(d,i):
    boldfonts(7)
    c.drawString(130, d, "Item Total: ")
    c.drawString(210, d, str(itemtotal))
    c.drawAlignedString(280, d, str(itemcopstotal))
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(itemgrosstotal)))
    c.drawAlignedString(400, d, str('{0:1.3f}'.format(itemtarewttotal)))
    c.drawAlignedString(480, d, str('{0:1.3f}'.format(itemnetwttotal)))
    fonts(7)

def DepartmentTotalPrint(d):
    boldfonts(7)
    c.drawString(130, d, "Dept Total: ")
    c.drawString(210, d, str(depttotal))
    c.drawAlignedString(280, d, str(deptcopstotal))
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(deptgrosstotal)))
    c.drawAlignedString(400, d, str('{0:1.3f}'.format(depttarewttotal)))
    c.drawAlignedString(480, d, str('{0:1.3f}'.format(deptnetwttotal)))
    fonts(7)

def CompanyTotalPrint(d):
    boldfonts(7)
    c.drawString(130, d, "Company Total: ")
    c.drawString(210, d, str(Comptotal))
    c.drawAlignedString(280, d, str(Compcopstotal))
    c.drawAlignedString(330, d, str('{0:1.3f}'.format(Compgrosstotal)))
    c.drawAlignedString(400, d, str('{0:1.3f}'.format(Comptarewttotal)))
    c.drawAlignedString(480, d, str('{0:1.3f}'.format(Compnetwttotal)))
    fonts(7)


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, "Lot No. : " + LotNo[-1])
        if str(ShadeName[-1]) != 'None':
            c.drawString(150, d, "Shade : " + str(ShadeName[-1]))

        d = dvalue()
        d = dvalue()
        data(result, d, i)
        LotTotal(result)
        departmenttotal(result)


    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            if Itemname[-1] == Itemname[-2]:
                if LotNo[-1] == LotNo[-2]:
                    data(result,d,i)
                    LotTotal(result)
                    departmenttotal(result)

                else:
                    # c.drawString(130, d, "Lot Total: ")
                    # c.drawString(210, d, str(i-1))
                    # c.drawAlignedString(280, d, str(lotcopstotal))
                    # c.drawAlignedString(330, d, str('{0:1.3f}'.format(lotgrosstotal)))
                    # c.drawAlignedString(400, d, str('{0:1.3f}'.format(lottarewttotal)))
                    # c.drawAlignedString(480, d, str('{0:1.3f}'.format(lotnettotal)))
                    LotTotalPrint(d, i)
                    SetSerialNo()
                    LotClean()
                    fonts(7)
                    d = dvalue()
                    d = dvalue()
                    c.drawString(10, d, "Lot No. : " + LotNo[-1])
                    if str(ShadeName[-1]) != 'None':
                        c.drawString(150, d, "Shade : " + str(ShadeName[-1]))
                    d = dvalue()
                    d = dvalue()
                    data(result,d,i)
                    LotTotal(result)
                    departmenttotal(result)

            else:
                boldfonts(7)
                # c.drawString(130, d, "Lot Total: ")
                # c.drawString(210, d, str(i-1))
                # c.drawAlignedString(280, d, str(lotcopstotal))
                # c.drawAlignedString(330, d, str('{0:1.3f}'.format(lotgrosstotal)))
                # c.drawAlignedString(400, d, str('{0:1.3f}'.format(lottarewttotal)))
                # c.drawAlignedString(480, d, str('{0:1.3f}'.format(lotnettotal)))
                LotTotalPrint(d, i)
                d = dvalue()
                d = dvalue()
                ItemTotalPrint(d, i)
                LotClean()
                ItemClean()
                fonts(7)
                SetSerialNo()
                d = dvalue()
                d = dvalue()
                c.drawString(10, d, Itemname[-1])
                d = dvalue()
                d = dvalue()
                c.drawString(10, d, "Lot No. : " + LotNo[-1])
                if str(ShadeName[-1]) != 'None':
                    c.drawString(150, d, "Shade : " + str(ShadeName[-1]))

                d = dvalue()
                d = dvalue()
                data(result, d, i)
                LotTotal(result)
                departmenttotal(result)

        else:
            LotTotalPrint(d,i)
            d = dvalue()
            d = dvalue()
            ItemTotalPrint(d,i)
            d = dvalue()
            d = dvalue()
            DepartmentTotalPrint(d)
            LotClean()
            ItemClean()
            departmentClean()
            SetSerialNo()
            d = dvalue()
            d = dvalue()
            d = dvalue()
            boldfonts(7)
            c.drawCentredString(300, d, Department[-1])
            d = dvalue()
            d = dvalue()
            fonts(7)
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, "Lot No. : " + LotNo[-1])
            if str(ShadeName[-1]) != 'None':
                c.drawString(150, d, "Shade : " + str(ShadeName[-1]))

            d = dvalue()
            d = dvalue()
            data(result, d, i)
            LotTotal(result)
            departmenttotal(result)


    elif divisioncode[-1] != divisioncode[-2]:
        LotTotalPrint(d, i)
        d = dvalue()
        d = dvalue()
        ItemTotalPrint(d, i)
        d = dvalue()
        d = dvalue()
        DepartmentTotalPrint(d)
        d = dvalue()
        d = dvalue()
        CompanyTotalPrint(d)
        LotClean()
        ItemClean()
        departmentClean()
        CompanyClean()
        c.showPage()
        d = newpage()
        SetSerialNo()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, "Lot No. : " + LotNo[-1])
        if str(ShadeName[-1]) != 'None':
            c.drawString(150, d, "Shade : " + str(ShadeName[-1]))

        d = dvalue()
        d = dvalue()
        data(result, d, i)
        LotTotal(result)
        departmenttotal(result)
