import textwrap
from reportlab.lib.pagesizes import landscape, A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A5)))
c.setPageSize(landscape(A5))

d = 235
i = 1

divisioncode = []
CompanyAddress = []
Itemname = []
GrnNo = []
Remark = []
pageno = 0
date=[]
itemtotal = 0
departmenttotal = 0
grandtotal = 0
# DocumentType = []
def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 5
    return d

def dvalueincrease():
    global d
    d = d + 10
    return d

def serialNo():
    global i
    i = i + 1
    return i

def header(result, divisioncode, CompanyAddress):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 400, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 385, CompanyAddress[-1])
    c.drawCentredString(300, 372, "Goods Receipt Note " )
    c.drawString(10, 350, "Supplier ")
    c.drawString(10, 330, "Address: ")
    c.drawString(10, 310, "Chal No: ")
    c.drawString(10, 290, "Bill No: ")
    c.drawString(10, 270, "L.R No: ")
    c.drawString(450, 350, "Grn No: ")
    c.drawString(450, 330, "Grn Dt: ")
    c.drawString(450, 310, "Chal Dt: ")
    c.drawString(450, 290, "Bill Dt: ")
    c.drawString(450, 270, "L.R Dt: ")

    c.line(0, 260, 600, 260)
    c.line(0, 240, 600, 240)
    # Upperline in header
    c.drawString(10,  245, "Sr. ")
    c.drawString(30,  245, "Item Name")
    c.drawString(170, 245, "Lot No.")
    c.drawString(250, 245, "Tariff Code")
    c.drawString(350, 245, "unit")
    c.drawString(430, 245, "P.O. No")
    c.drawString(500, 245, "P.O. Dt")
    c.drawString(555, 245, "Quantity")


def data(result, d, i):
    fonts(7)
    c.drawString(10, d, str(i))
    str1 = ''
    string = str1.join(result['PRODUCTNAME'])
    res = sum(not chr.isspace() for chr in string)
    wrap_text = textwrap.wrap(string, width=30)
    # print(len(wrap_text))
    e = 0
    while e < len(wrap_text):
        c.drawString(30, d, wrap_text[e])
        d = dvalue()
        d = dvalue()
        e = e + 1
    f = 0
    while f < len(wrap_text):
        d = dvalueincrease()
        f = f + 1
    # if len(wrap_text) == 1:
    #     c.drawString(30, d, wrap_text[0])
    #     # print(wrap_text[0])
    # else:
    #     if len(wrap_text) == 3:
    #         c.drawString(30, d, wrap_text[0])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[1])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[2])
    #         d = dvalueincrease()
    #         d = dvalueincrease()
    #     if len(wrap_text) == 4:
    #         c.drawString(30, d, wrap_text[0])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[1])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[2])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[3 ])
    #         d = dvalueincrease()
    #         d = dvalueincrease()
    #         d = dvalueincrease()
    #     if len(wrap_text) == 5:
    #         c.drawString(30, d, wrap_text[0])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[1])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[2])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[3 ])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[4])
    #         d = dvalueincrease()
    #         d = dvalueincrease()
    #         d = dvalueincrease()
    #         d = dvalueincrease()
    #     if len(wrap_text) == 2:
    #         c.drawString(30, d, wrap_text[0])
    #         d = dvalue()
    #         d = dvalue()
    #         c.drawString(30, d, wrap_text[1])
    #         d = dvalueincrease()
    # c.drawString(30, d, result['PRODUCTNAME'])
    c.drawString(172, d, result['LOTNO'])
    c.drawString(254, d, result['TARIFFCODE'])
    c.drawString(350, d, result['UNITS'])
    c.drawString(430, d, result['PONO'])
    c.drawString(500, d, result['PODT'])
    c.drawAlignedString(575, d, result['QUANTITY'])
    g = 0
    while g < len(wrap_text)-1:
        d = dvalue()
        d = dvalue()
        g = g + 1
    # if len(wrap_text) > 1:
    #     d = dvalue()
    #     d = dvalue()
    #     if len(wrap_text) == 3:
    #         d = dvalue()
    #         d = dvalue()
    #     elif len(wrap_text) == 4:
    #         d = dvalue()
    #         d = dvalue()
    #     elif len(wrap_text) == 5:
    #         d = dvalue()
    #         d = dvalue()

    i = serialNo()

def dataheader(result):
    fonts(9)
    c.drawString(50, 350, result['SUPPLIER'])
    c.drawString(50, 330, result['ADDRESS'])
    c.drawString(50, 310, result['CHALNO'])
    c.drawString(50, 290, result['BILLNO'])
    c.drawString(50, 270, result['LRNO'])
    c.drawString(485, 330, result['GRNDATE'])
    c.drawString(485, 310, result['CHALDT'])
    c.drawString(485, 290, result['BILLDT'])
    c.drawString(485, 270, result['LRDT'])

def logic(result):
    global divisioncode
    global CompanyAddress
    global GrnNo
    global Remark
    divisioncode.append(result['COMPNAME'])
    CompanyAddress.append(result['COMPADDRESS'])
    GrnNo.append(result['GRNNUMBER'])
    if result['REMARK'] != None:
        try:
            Remark.append(result['REMARK'])
        except:
            pass


def newpage():
    global d
    d = 235
    return d

def newserialNo():
    global i
    i = 1
    return i

def newrequest():
    global divisioncode
    # global pageno
    global GrnNo
    global CompanyAddress
    global Remark
    divisioncode = []
    CompanyAddress = []
    pageno = 0
    GrnNo = []
    Remark = []

def textsize(c, result, d, i):
    d = dvalue()
    logic(result)

    if len(divisioncode) == 1:
        header(result, divisioncode, CompanyAddress)
        c.drawString(485, 350, GrnNo[-1])
        dataheader(result)
        data(result, d, i)

    elif divisioncode[-1] == divisioncode[-2]:
        if GrnNo[-1] == GrnNo[-2]:
            data(result, d, i)

        else:
            c.line(0, d+5, 600, d+5)
            str1 = ''
            string = str1.join(Remark[-2])
            res = sum(not chr.isspace() for chr in string)
            if res != 0:
                d = dvalue()
                c.drawString(10, d, "Remarks: ")
            c.drawString(45, d, Remark[-2])
            # print(Remark[-2])
            c.drawString(10, 10, "Store")
            c.drawString(200, 10, "Inspected By")
            c.drawString(360, 10, "Store Incharge")
            c.drawString(510, 10, "Authorised By")
            # RemarkClean()
            c.setPageSize(landscape(A5))
            c.showPage()
            d = newpage()
            i = newserialNo()
            header(result, divisioncode, CompanyAddress)
            fonts(9)
            d = dvalue()
            c.drawString(485, 350, GrnNo[-1])
            dataheader(result)
            data(result, d, i)


    # elif divisioncode[-1] != divisioncode[-2]:
    #     c.line(0, d + 5, 600, d + 5)
    #     str1 = ''
    #     string = str1.join(Remark)
    #     res = sum(not chr.isspace() for chr in string)
    #     if res != 0:
    #         d = dvalue()
    #         c.drawString(10, d, "Remarks")
    #         c.drawString(45, d, Remark[-1])
    #     c.drawString(10, 10, "Store")
    #     c.drawString(200, 10, "Inspected By")
    #     c.drawString(360, 10, "Store Incharge")
    #     c.drawString(510, 10, "Authorised By")
    #     c.setPageSize(landscape(A5))
    #     c.showPage()
    #     d = newpage()
    #     i = newserialNo()
    #     header(result, divisioncode, CompanyAddress)
    #     fonts(9)
    #     d = dvalue()
    #     c.drawString(485, 350, GrnNo[-1])
    #     dataheader(result)
    #     data(result, d, i)

