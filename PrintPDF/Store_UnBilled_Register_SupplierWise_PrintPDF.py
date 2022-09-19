from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
# c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
# c.setPageSize(landscape(A4))
d = 730
divisioncode = []
product = []
CompanyQuentityTotal = 0
CompanyAmountTotal = 0
pageno = 0
suppliername = []


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
    c.drawCentredString(300, 780,
                        "Supplier Wise UnBilled Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 777, 600, 777)
    c.line(0, 750, 600, 750)
    # Upperline in header
    c.drawString(10, 765, "Supplier Name")
    c.drawString(10, 755, "Grn No.")
    c.drawString(100, 755, "Grn Date")
    # c.drawString(120, 755, "Supplier")
    c.drawString(420, 755, "Challan No.")
    c.drawString(520, 755, "Challan Date")
    # c.drawString(480, 745, "PENDING QUANTITY")
    print("from pdf header  file")


def data(result, d):
    fonts(7)
    c.drawString(10, d, result['MRNPREFIX'] + "-" + result['MRNCODE'])
    c.drawString(100, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))

    if len(str(result['CHALNO'])) > 0:
        c.drawString(430, d, result['CHALNO'])

    LSCDATE = str(result['CHALDATE'].strftime('%d-%m-%y'))
    if LSCDATE != '01-01-91':
        c.drawAlignedString(560, d, LSCDATE)

    total(result)
    print("from pdf data  file")


def GroupByProduct(result, d):
    fonts(7)
    c.drawString(10, d, result['PLANTNAME'])


def itemcodes(result, d):
    fonts(7)
    c.drawString(10, d, "PLANTNAME : " + str(result['PLANTNAME']))


def total(result):
    global CompanyQuentityTotal
    global CompanyAmountTotal


def logic(result):
    divisioncode.append(result['PLANTNAME'])
    suppliername.append(result['SUPPLIER'])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 730
    return d


def supplier(result):
    c.drawString(10, d, str(result['SUPPLIER']))


def companyclean():
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = 0
    CompanyAmountTotal = 0

def newrequest():
    global divisioncode
    global pageno
    global suppliername
    divisioncode=[]
    pageno=0
    suppliername=[]

def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    logic(result)
    if len(divisioncode) == 1:
        if len(suppliername) == 1:
            if d > 14:
                header(stdt, etdt, divisioncode)
                d = dvalue()
                fonts(7)
                supplier(result)
                d = dvalue()
                data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if suppliername[-2] == suppliername[-1]:
            data(result, d)
        elif suppliername[-2] != suppliername[-1]:
            fonts(7)
            supplier(result)
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
        fonts(7)
        if suppliername[-2] == suppliername[-1]:
            data(result, d)
        elif suppliername[-2] != suppliername[-1]:
            supplier(result)
            d = dvalue()
            data(result, d)
