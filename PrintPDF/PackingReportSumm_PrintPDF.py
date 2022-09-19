from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 740

pageno = 0

divisioncode = []
Department = []
Itemname = []
ShadeName = []
LotNo = []

i = 0
netwt = 0
netwtS = 0
cops = 0
Box = 0
Boxes = 0
Compnetwt = 0
CompnetwtS = 0
Compcops = 0
CompBox = 0
CompBoxes = 0
Deptnetwt = 0
DeptnetwtS = 0
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


def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Packing Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    # Upperline in header
    c.drawString(10, 765, "Quality")
    c.drawString(60, 765, "Lot No")
    c.drawString(130, 765, "Shade")
    c.drawString(250, 765, "Boxes")
    c.drawString(300, 765, "Cops")
    c.drawString(380, 765, "Net Wt.")
    c.drawString(430, 765, "Perc")
    c.drawString(530, 765, "To Date")
    c.drawString(490, 755, "Net Wt.")
    c.drawString(560, 755, "Boxes")



def data(result, d):
    fonts(7)

    # if int(float(result['TONETWT'])) != 0:
    c.drawString(10, d, str(result['QUALITY']))
    c.drawString(61, d, str(result['LOTNO']))
    c.drawString(131, d, str(result['SHADENAME']))
    c.drawAlignedString(270, d, str(result['BOXES']))
    c.drawAlignedString(320, d, str(result['COPS']))
    c.drawAlignedString(395, d, str(result['NETWT']))
    c.drawAlignedString(505, d, str(result['TONETWT']))
    c.drawAlignedString(575, d, str(result['TOBOXES']))
    TotalWeight(result)
    DepartmentTotal(result)


def logic(result):
    global divisioncode
    global Department
    global Itemname
    global ShadeName
    global LotNo
    divisioncode.append(result['COMPNAME'])
    Itemname.append(result['PRODUCT'])
    Department.append(result['DEPARTMENT'])
    # ShadeName.append(result[''])
    # OrdNo.append(result['ISSUENO'])

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode
    global Department
    global Itemname
    global ShadeName
    global LotNo
    global pageno
    divisioncode = []
    Department = []
    pageno = 0
    Itemname=[]
    ShadeName = []
    LotNo = []

def TotalWeight(result):
    global  netwt, netwtS, cops
    global  Box
    global Boxes
    # if int(float(result['TONETWT'])) != 0:
    netwt = netwt + float(result['NETWT'])
    netwtS = netwtS + float(result['TONETWT'])
    cops = cops + int(result['COPS'])
    Box = Box + int(result['BOXES'])
    Boxes = Boxes + int(result['TOBOXES'])

def CleanWt():
    global netwt, netwtS, cops
    global Box
    global Boxes
    netwt = netwtS = cops = 0
    Box = 0
    Boxes = 0

def DepartmentTotal(result):
    global Deptnetwt
    global DeptnetwtS
    global Deptcops
    global DeptBoxes
    global DeptBox
    Deptnetwt = Deptnetwt + float(result['NETWT'])
    DeptnetwtS = DeptnetwtS + float(result['TONETWT'])
    Deptcops = Deptcops + int(result['COPS'])
    DeptBox = DeptBox + int(result['BOXES'])
    DeptBoxes = DeptBoxes + int(result['TOBOXES'])

def DepartmentClean():
    global Deptnetwt
    global DeptnetwtS
    global Deptcops
    global DeptBoxes
    global DeptBox
    Deptnetwt = 0
    DeptnetwtS = 0
    Deptcops = 0
    DeptBoxes = 0
    DeptBox = 0

def CompanyTotal(result):
    global Compnetwt
    global CompnetwtS
    global Compcops
    global CompBoxes
    global CompBox
    Compnetwt = Compnetwt + float(result['NETWT'])
    CompnetwtS = CompnetwtS + float(result['TONETWT'])
    Compcops = Compcops + int(result['COPS'])
    CompBox = CompBox + int(result['BOXES'])
    CompBoxes = CompBoxes + int(result['TOBOXES'])

def CompanyClean():
    global Compnetwt
    global CompnetwtS
    global Compcops
    global CompBoxes
    global CompBox
    Compnetwt = 0
    CompnetwtS = 0
    Compcops = 0
    CompBoxes = 0
    CompBox = 0


def textsize(c, result,d, stdt, etdt,Total):
    d = dvalue()
    logic(result)
    global i

    if len(divisioncode) == 1:
        # i = 1
        CleanWt()
        CompanyClean()
        header(stdt, etdt, divisioncode)
        boldfonts(7)
        c.drawCentredString(300, d, Department[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        c.drawString(10, d, Itemname[-1])
        d = dvalue()
        d = dvalue()
        data(result,d)
        CompanyTotal(result)

        i = 0
        if int(Total[i]) !=0:
            percentage = (float(result['NETWT'])/float(Total[i])) * 100
            c.drawAlignedString(445, d, str(round(percentage)) + '%')
        else:
            c.drawAlignedString(445, d, '0%')



    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            if Itemname[-1] == Itemname[-2]:
                data(result,d)
                CompanyTotal(result)
                if int(Total[i]) != 0:
                    percentage = (float(result['NETWT']) / float(Total[i])) * 100
                    c.drawAlignedString(445, d, str(round(percentage)) + '%')
                else:
                    c.drawAlignedString(445, d, '0%')

            else:
                boldfonts(7)
                c.drawString(120, d, "Item Total: ")
                c.drawAlignedString(270, d, str(Box))
                c.drawAlignedString(320, d, str(cops))
                c.drawAlignedString(395, d, str('{0:1.3f}'.format(netwt)))
                c.drawAlignedString(505, d, str('{0:1.3f}'.format(netwtS)))
                c.drawAlignedString(575, d, str(Boxes))
                d = dvalue()
                CleanWt()
                fonts(7)
                d = dvalue()
                c.drawString(10, d, Itemname[-1])
                d = dvalue()
                d = dvalue()
                data(result, d)
                CompanyTotal(result)

                i = i + 1
                if int(Total[i]) != 0:
                    percentage = (float(result['NETWT']) / float(Total[i])) * 100
                    c.drawAlignedString(445, d, str(round(percentage)) + '%')
                else:
                    c.drawAlignedString(445, d, '0%')
        else:
            boldfonts(7)
            c.drawString(120, d, "Item Total: ")
            c.drawAlignedString(270, d, str(Box))
            c.drawAlignedString(320, d, str(cops))
            c.drawAlignedString(395, d, str('{0:1.3f}'.format(netwt)))
            c.drawAlignedString(505, d, str('{0:1.3f}'.format(netwtS)))
            c.drawAlignedString(575, d, str(Boxes))
            d = dvalue()
            d = dvalue()
            c.drawString(120, d, "Dept Total: ")
            c.drawAlignedString(270, d, str(DeptBox))
            c.drawAlignedString(320, d, str(Deptcops))
            c.drawAlignedString(395, d, str('{0:1.3f}'.format(Deptnetwt)))
            c.drawAlignedString(505, d, str('{0:1.3f}'.format(DeptnetwtS)))
            c.drawAlignedString(575, d, str(DeptBoxes))
            CleanWt()
            DepartmentClean()
            boldfonts(7)
            d = dvalue()
            d = dvalue()
            c.drawCentredString(300, d, Department[-1])
            d = dvalue()
            d = dvalue()
            fonts(7)
            c.drawString(10, d, Itemname[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)
            CompanyTotal(result)

            i = i + 1
            if int(Total[i]) != 0:
                percentage = (float(result['NETWT']) / float(Total[i])) * 100
                c.drawAlignedString(445, d, str(round(percentage)) + '%')
            else:
                c.drawAlignedString(445, d, '0%')


    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.drawString(120, d, "Item Total: ")
        c.drawAlignedString(270, d, str(Box))
        c.drawAlignedString(320, d, str(cops))
        c.drawAlignedString(395, d, str('{0:1.3f}'.format(netwt)))
        c.drawAlignedString(505, d, str('{0:1.3f}'.format(netwtS)))
        c.drawAlignedString(575, d, str(Boxes))
        d = dvalue()
        d = dvalue()
        c.drawString(120, d, "Dept Total: ")
        c.drawAlignedString(270, d, str(DeptBox))
        c.drawAlignedString(320, d, str(Deptcops))
        c.drawAlignedString(395, d, str('{0:1.3f}'.format(Deptnetwt)))
        c.drawAlignedString(505, d, str('{0:1.3f}'.format(DeptnetwtS)))
        c.drawAlignedString(575, d, str(DeptBoxes))
        d = dvalue()
        d = dvalue()
        c.drawString(120, d, "Company Total: ")
        c.drawAlignedString(270, d, str(CompBox))
        c.drawAlignedString(320, d, str(Compcops))
        c.drawAlignedString(395, d, str('{0:1.3f}'.format(Compnetwt)))
        c.drawAlignedString(505, d, str('{0:1.3f}'.format(CompnetwtS)))
        c.drawAlignedString(575, d, str(CompBoxes))
        CleanWt()
        DepartmentClean()
        CompanyClean()
    # if int(float(result['TONETWT'])) != 0:
        c.showPage()
        d = newpage()
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
        data(result, d)
        CompanyTotal(result)

        i = i + 1
        if int(Total[i]) != 0:
            percentage = (float(result['NETWT']) / float(Total[i])) * 100
            c.drawAlignedString(445, d, str(round(percentage)) + '%')
        else:
            c.drawAlignedString(445, d, '0%')
