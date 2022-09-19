import textwrap
from reportlab.lib.pagesizes import landscape, A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A5)))
c.setPageSize(landscape(A5))

d = 0

divisioncode = []
CompanyAddress = []
Agent = []
Party = []
partyAddress = []
ChallanNo = []
ChallanDt = []
LrNo = []
LrDt = []
Product = []
Quantity = []
Box = []
LotNo = []
OrdRef = []
pageno = 0
totalQuantity = 0
totalBox = 0
totalCops = 0
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

def dlocalvalue():
    global d
    d = d - 10
    return d
def dslocal():
    global d
    d = d - 30
    return d

def dvalueincrease():
    global d
    d = d + 10
    return d

def header(divisioncode, CompanyAddress):
    global d
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 395, divisioncode[-1])
    fonts(8)
    c.drawCentredString(300, 382, CompanyAddress[-1])
    fonts(8)
    c.drawCentredString(300, 370, "Despatch Advice")

    #Upper header
    fonts(7)
    c.drawString(10, 350, "Party: " + Party[-1])
    str1 = ''
    string = str1.join(partyAddress[-1])
    wrap_text = textwrap.wrap(string, width=100)
    e = 0
    y = 340
    while e < len(wrap_text):
        c.drawString(30, y, wrap_text[e])
        y = y - 10
        e = e + 1

    c.drawString(10, y-10, "Challan No: " + ChallanNo[-1])
    c.drawString(10, y-30, "L.R.NO.: " + LrNo[-1])
    c.drawString(10, y-50, "Quality: " + Product[-1])

    # Side Header
    c.drawString(450, y-10 , "Challan Date: "+ ChallanDt[-1])
    c.drawString(450, y - 30, "L.R. Date: " + LrDt[-1])
    c.line(0, y - 55, 600, y-55)
    c.drawString(10, y-70, "Shade")
    c.drawString(200, y-70, "LotNo.")
    c.drawString(400, y-70, "Quantity")
    c.drawString(480, y-70, "Boxes")
    c.drawString(560, y-70, "Cops")
    c.line(0, y-75, 600, y-75)
    d = d + y - 85


def data(result, d):
    fonts(7)
    c.drawString(10, d, str(result['SHADENAME']))
    c.drawString(200, d, str(result['LOTNO']))
    c.drawAlignedString(410, d, str(result['QUANTITY']))
    c.drawAlignedString(495, d, str(result['BOXES']))
    c.drawAlignedString(575, d, str(result['COPS']))
    Total(result)

def logic(result):
    global divisioncode, Party, partyAddress, ChallanNo, ChallanDt
    global CompanyAddress, LrNo, LrDt, Product, Agent, OrdRef
    divisioncode.append(result['COMPANYNAME'])
    CompanyAddress.append(result['COMPADDRESS'])
    Party.append(result['PARTYNAME'])
    partyAddress.append(result['PARTYADDRESS'])
    ChallanNo.append(result['CHALLANNO'])
    ChallanDt.append(result['CHALLANDATE'])
    LrNo.append(result['LRNO'])
    LrDt.append(result['LRDT'])
    Product.append(result['PRODUCT'])
    Agent.append(result['AGENT'])
    OrdRef.append(result['ORDREF'])


def newpage():
    global d
    d = 0
    return d

def newrequest():
    global divisioncode, Party, partyAddress, ChallanNo, ChallanDt
    global pageno
    global CompanyAddress, LrNo, LrDt, Product, Agent, OrdRef
    divisioncode = []
    CompanyAddress = []
    Party = []
    partyAddress = []
    ChallanNo = []
    ChallanDt = []
    LrNo = []
    LrDt = []
    Product = []
    Agent = []
    OrdRef = []
    pageno = 0

def Total(result):
    global totalQuantity, totalBox, totalCops
    totalQuantity = totalQuantity + float(result['QUANTITY'])
    totalBox = totalBox + int(result['BOXES'])
    totalCops = totalCops + int(result['COPS'])

def TotalClean():
    global totalQuantity, totalBox, totalCops
    totalQuantity = 0
    totalBox = 0
    totalCops = 0

def TotalPrit(d):
    c.drawAlignedString(410, d, str('{0:1.3f}'.format(totalQuantity)))
    c.drawAlignedString(495, d, str(totalBox))
    c.drawAlignedString(575, d, str(totalCops))
    TotalClean()

def textsize(c, result):
    global d
    logic(result)

    if len(divisioncode) == 1:
        header(divisioncode, CompanyAddress)
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if Party[-1] == Party[-2]:
            if ChallanNo[-1] == ChallanNo[-2]:
                if Product[-1] == Product[-2]:
                    d = dvalue()
                    data(result, d)

                else:#Product change
                    c.line(0, d, 600, d)
                    d = dvalue()
                    d = dvalue()
                    c.drawString(200, d, "Total: ")
                    TotalPrit(d)
                    d = dvalue()
                    c.line(0, d, 600, d)
                    d = dvalue()
                    d = dvalue()
                    c.drawString(10, d, "Agent         :" + "       " + Agent[-2])
                    d = dlocalvalue()
                    d = dvalue()
                    c.drawString(10, d, "Order Ref  :" + "        " + OrdRef[-2])
                    c.drawString(400, d, "For " + divisioncode[-2])
                    d = dslocal()
                    c.drawString(400, d, "Authorised Signatory")
                    c.setPageSize(landscape(A5))
                    c.showPage()
                    d = newpage()
                    header(divisioncode, CompanyAddress)
                    data(result, d)

            else:# ChallaNO change
                c.line(0, d, 600, d)
                d = dvalue()
                d = dvalue()
                c.drawString(200, d , "Total: ")
                TotalPrit(d)
                d = dvalue()
                c.line(0, d, 600, d)
                d = dvalue()
                d = dvalue()
                c.drawString(10, d, "Agent         :" + "       " + Agent[-2])
                d = dlocalvalue()
                d = dvalue()
                c.drawString(10, d, "Order Ref  :" + "        " + OrdRef[-2])
                c.drawString(400, d, "For " + divisioncode[-2])
                d = dslocal()
                c.drawString(400, d, "Authorised Signatory")
                c.setPageSize(landscape(A5))
                c.showPage()
                d = newpage()
                header(divisioncode, CompanyAddress)
                data(result, d)

        else: #Party Change
            c.line(0, d, 600, d)
            d = dvalue()
            d = dvalue()
            c.drawString(200, d, "Total: ")
            TotalPrit(d)
            d = dvalue()
            c.line(0, d, 600, d)
            d = dvalue()
            d = dvalue()
            c.drawString(10, d, "Agent         :" + "       " + Agent[-2])
            d = dlocalvalue()
            d = dvalue()
            c.drawString(10, d, "Order Ref  :" + "        " + OrdRef[-2])
            c.drawString(400, d, "For " + divisioncode[-2])
            d = dslocal()
            c.drawString(400, d, "Authorised Signatory")
            c.setPageSize(landscape(A5))
            c.showPage()
            d = newpage()
            header(divisioncode, CompanyAddress)
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        c.line(0, d, 600, d)
        d = dvalue()
        d = dvalue()
        c.drawString(200, d, "Total: ")
        TotalPrit(d)
        d = dvalue()
        c.line(0, d, 600, d)
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, "Agent         :" + "       " + Agent[-2])
        d = dlocalvalue()
        d = dvalue()
        c.drawString(10, d, "Order Ref  :" + "        " + OrdRef[-2])
        c.drawString(400, d, "For " + divisioncode[-2])
        d = dslocal()
        c.drawString(400, d, "Authorised Signatory")
        c.setPageSize(landscape(A5))
        c.showPage()
        d = newpage()
        header(divisioncode, CompanyAddress)
        data(result, d)
