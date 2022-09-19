from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
d = 730
divisioncode = []
product = []
CompanyQuentityTotal = 0
CompanyAmountTotal = 0
pageno = 0
warehouse = []


def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 10
    return d


def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, "GRN Wise UnBilled Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 777, 600, 777)
    c.line(0, 750, 600, 750)
    # Upperline in header
    c.drawString(10, 755, "Grn No.")
    c.drawString(70, 755, "Grn Date")
    c.drawString(120, 755, "Supplier")
    c.drawString(460, 755, "Challan No.")
    c.drawString(520, 755, "Challan Date")


def data(result, d):
    fonts(7)
    c.drawString(10, d, result['MRNPREFIX'] + "-" + result['MRNCODE'])
    c.drawString(70, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))

    c.drawString(120, d, result['SUPPLIER'])
    if len(str(result['CHALNO'])) > 0:
        c.drawString(460, d, result['CHALNO'])

    LSCDATE = str(result['CHALDATE'].strftime('%d-%m-%y'))

    if LSCDATE != '01-01-91':
        c.drawAlignedString(560, d, LSCDATE)

    total(result)

    logic(result)


def GroupByProduct(result, d):
    fonts(7)
    c.drawString(10, d, result['PLANTNAME'])


def itemcodes(result, d):
    fonts(7)
    # c.drawString(10, d, "PLANTNAME : " + str(result['PLANTNAME']))


def total(result):
    global CompanyQuentityTotal
    global CompanyAmountTotal


def logic(result):
    divisioncode.append(result['PLANTNAME'])
    warehouse.append(result['COSTCENTERNAME'])


def dlocvalue(d):
    d = d - 20
    return d


def warehousename(result, d):
    c.drawString(10, d, result['COSTCENTERNAME'])


def newpage():
    global d
    d = 730
    return d


def companyclean():
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = 0
    CompanyAmountTotal = 0

def newrequest():
    global divisioncode
    global pageno
    global warehouse
    divisioncode=[]
    pageno=0
    warehouse=[]


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    if len(divisioncode) == 1:
        if len(warehouse) == 1:
            if d > 14:
                header(stdt, etdt, divisioncode)
                d = dvalue()
                fonts(7)
                warehousename(result, d)
                d = dvalue()
                data(result, d)


    elif divisioncode[-1] == divisioncode[-2]:
        if warehouse[-2] == warehouse[-1]:

            data(result, d)
        elif warehouse[-2] != warehouse[-1]:
            warehousename(result, d)
            d = dvalue()
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        d = dvalue()
        fonts(7)
        companyclean()
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue()
        if warehouse[-2] == warehouse[-1]:
            data(result, d)
        elif warehouse[-2] != warehouse[-1]:
            warehousename(result, d)
            d = dvalue()
            data(result, d)
