import textwrap
from reportlab.lib.pagesizes import landscape, A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")

d = 520
i = 1

divisioncode = []
CompanyAddress = []
CompGstNo = []
Costcenter = []
Party = []
partyAddress = []
PGstNo = []
PoNo = []
PoDt = []
shippname = []
shippAddress = []
Delivery = []
Payment = []
Remarks = []
pageno = 0
TotalAmt = 0
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

def SerialNo():
    global i
    i = i + 1
    return i

def SetSerialNo():
    global i
    i = 1
    return i

def header(divisioncode):
    global d
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(8)
    c.drawCentredString(300, 785, CompanyAddress[-1])
    boldfonts(8)
    c.drawCentredString(300, 770, "Purchase Order ")

    #Upper header
    fonts(7)
    c.drawString(10, 750, "To,")
    c.drawString(30, 740, "Party: " + Party[-1])
    str1 = ''
    string = str1.join(partyAddress[-1])
    wrap_text = textwrap.wrap(string, width=60)
    e = 0
    y = 730
    while e < len(wrap_text):
        c.drawString(30, y, wrap_text[e])
        y = y - 10
        e = e + 1

    c.drawString(10, 670, "GST No. : " + PGstNo[-1])

    #Right Header
    c.drawString(350, 740, "P.O. No.: " + PoNo[-1])
    c.drawString(450, 740, "P.O. Dt.: " + PoDt[-1])
    boldfonts(7)
    c.drawString(350, 720, "BILLING/BUYER ADDRESS:")
    fonts(7)
    c.drawString(350, 710, divisioncode[-1])
    str1 = ''
    string = str1.join(CompanyAddress[-1])
    wrap_text = textwrap.wrap(string, width=60)
    e = 0
    y = 700
    while e < len(wrap_text):
        c.drawString(350, y, wrap_text[e])
        y = y - 10
        e = e + 1

    c.drawString(350, 660, "GST No.: " + CompGstNo[-1])
    boldfonts(7)
    c.drawString(350, 640, "SHIPPING ADDRESS")
    fonts(7)
    c.drawString(350, 630, shippname[-1])
    str1 = ''
    string = str1.join(shippAddress[-1])
    wrap_text = textwrap.wrap(string, width=60)
    e = 0
    y = 620
    while e < len(wrap_text):
        c.drawString(350, y, wrap_text[e])
        y = y - 10
        e = e + 1

    c.line(0,550, 600, 550)
    c.line(0, 530, 600, 530)
    c.drawString(10, 535, "Sr")
    c.drawString(30, 535, "Item Name")
    c.drawString(180, 535, "HSN N0.")
    c.drawString(230, 535, "GST")
    c.drawString(290, 535, "Quantity")
    c.drawString(350, 535, "Gross Rate")
    c.drawString(395, 535, "Unit")
    c.drawString(420, 535, "Dis %/Amt")
    c.drawString(490, 535, "Rate")
    c.drawString(560, 535, "Amount")


def data(result, d, i):
    fonts(7)
    c.drawString(10, d, str(i))
    str1 = ''
    string = str1.join(result['ITEMNAME'])
    wrap_text = textwrap.wrap(string, width=30)
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
    # c.drawString(30, d, result['ITEMNAME'])
    c.drawAlignedString(205, d, str(result['HSNNO']))
    if result['GST'] != None:
        c.drawString(231, d, str(result['GST']))
    else:
        c.drawString(231, d, str(result['GSTTAXTEMP']))
    c.drawAlignedString(307, d, str(result['QUANTITY']))
    #calculate for gross rate
    # grossrate = 0
    # if str(result['GROSSVAL']) != None:
    #     grossrate = (float(result['GROSSVAL'])/ float(result['QUANTITY']))
    # else:
    #     grossrate = (float(result['GROSSRATE']))
    # c.drawAlignedString(370, d, str('{0:1.3f}'.format(grossrate)))
    c.drawAlignedString(370, d, str(result['GROSSRATE']))
    c.drawString(396, d, str(result['UNIT']))
    c.drawAlignedString(430, d, str(result['DISPERAMT']))
    c.drawAlignedString(500, d, str(result['RATE']))
    if result['AMOUNT2'] != None:
        c.drawAlignedString(577, d, str(result['AMOUNT2']))
    else:
        c.drawAlignedString(577, d, str(result['AMOUNT']))

    g = 0
    while g < len(wrap_text) - 1:
        d = dvalue()
        d = dvalue()
        g = g + 1

    i = SerialNo()
    Total(result)


def logic(result):
    global divisioncode, Party, partyAddress, PoNo, PoDt, CompGstNo
    global CompanyAddress, PGstNo, shippname, shippAddress, Costcenter
    global Delivery, Payment, Remarks
    divisioncode.append(result['COMPNAME'])
    CompanyAddress.append(result['COMPADDRESS'])
    Party.append(result['PARTYNAME'])
    partyAddress.append(result['PARTYADDRESS'])
    PoNo.append(result['PONO'])
    PoDt.append((result['PODT']).strftime('%d-%m-%Y'))
    PGstNo.append(result['PGSTNO'])
    shippname.append(result['SHIPPNAME'])
    shippAddress.append(result['SHIPPADDRESS'])
    Costcenter.append(result['COSTCENTER'])
    Delivery.append((result['DELIVERY']))
    Payment.append(result['PAYMENT'])
    Remarks.append(result['REMARKS'])
    CompGstNo.append(str(result['COMPGSTNO']))



def newpage():
    global d
    d = 520
    return d

def newrequest():
    global divisioncode, Party, partyAddress, PoNo, PoDt,CompGstNo
    global pageno
    global CompanyAddress,PGstNo, shippname, shippAddress,Costcenter
    divisioncode = []
    CompanyAddress = []
    Costcenter = []
    Party = []
    partyAddress = []
    PGstNo = []
    PoNo = []
    PoDt = []
    shippname = []
    shippAddress = []
    CompGstNo = []
    pageno = 0

def Footer(d):
    d = dslocal()
    c.drawString(10, d, "Order By")
    c.drawString(300, d, "Approved By")
    c.drawString(470, d, "Authorised Signatory")

def Total(result):
    global TotalAmt
    if result['AMOUNT2'] != None:
        TotalAmt = TotalAmt + float(result['AMOUNT2'])
    else:
        TotalAmt = TotalAmt + float(result['AMOUNT'])

def TotalClean():
    global TotalAmt
    TotalAmt = 0

def TotalPrit(d, i):
    d = dvalue()
    c.drawString(450, d, "Total Amount")
    c.drawAlignedString(580, d, str('{0:1.3f}'.format(TotalAmt)))
    TotalClean()
    i = SetSerialNo()

def textsize(c, result):
    global d
    logic(result)

    if len(divisioncode) == 1:
        header(divisioncode)
        data(result, d, i)

    elif divisioncode[-1] == divisioncode[-2]:
            if Party[-1] == Party[-2]:
                if PoNo[-1] == PoNo[-2]:
                    if Costcenter[-1] == Costcenter[-2]:
                        d = dvalue()
                        data(result, d, i)

                    elif Costcenter[-1] != Costcenter[-2]:
                        d = dvalue()
                        c.drawString(30, d, "Costcenter: " + Costcenter[-2])
                        d = dvalue()
                        d = dvalue()
                        data(result, d, i)

                elif PoNo[-1] != PoNo[-2]:
                    d = dvalue()
                    c.drawString(30, d, "Costcenter: " + Costcenter[-2])
                    d = dvalue()
                    d = dvalue()
                    c.line(0, d, 600, d)
                    d = dvalue()
                    TotalPrit(d,i)
                    d = dlocalvalue()
                    c.drawString(10, d, "Delivery: " + '        ' + Delivery[-2])
                    d = dvalue()
                    d = dvalue()
                    c.drawString(10, d, "Payment: " +  '        ' + Payment[-2])
                    d = dslocal()
                    c.drawString(10, d, Remarks[-2])
                    d = dlocalvalue()
                    c.drawString(10, d, "Note: Please Kindly Confirm Receipt Of This Order")
                    d = dvalue()
                    c.drawString(400, d, "For " + ' '  + divisioncode[-2])
                    d = dvalue()
                    Footer(d)
                    c.showPage()
                    d = newpage()
                    header(divisioncode)
                    data(result, d, i)

            elif Party[-1] != Party[-2]:
                d = dvalue()
                c.drawString(30, d, "Costcenter: " + Costcenter[-2])
                d = dvalue()
                d = dvalue()
                c.line(0, d, 600, d)
                d = dvalue()
                TotalPrit(d,i)
                d = dlocalvalue()
                c.drawString(10, d, "Delivery: " + '        ' + Delivery[-2])
                d = dvalue()
                d = dvalue()
                c.drawString(10, d, "Payment: " + '        ' + Payment[-2])
                d = dslocal()
                c.drawString(10, d, Remarks[-2])
                d = dlocalvalue()
                c.drawString(10, d, "Note: Please Kindly Confirm Receipt Of This Order")
                d = dvalue()
                c.drawString(400, d, "For " + ' ' + divisioncode[-2])
                d = dvalue()
                Footer(d)
                c.showPage()
                d = newpage()
                header(divisioncode)
                data(result, d, i)


    elif divisioncode[-1] != divisioncode[-2]:
        d = dvalue()
        c.drawString(30, d, "Costcenter: " + Costcenter[-2])
        d = dvalue()
        d = dvalue()
        c.line(0, d, 600, d)
        d = dvalue()
        TotalPrit(d,i)
        d = dlocalvalue()
        c.drawString(10, d, "Delivery: " + '        ' + Delivery[-2])
        d = dvalue()
        d = dvalue()
        c.drawString(10, d, "Payment: " + '        ' + Payment[-2])
        d = dslocal()
        c.drawString(10, d, Remarks[-2])
        d = dlocalvalue()
        c.drawString(10, d, "Note: Please Kindly Confirm Receipt Of This Order")
        d = dvalue()
        c.drawString(400, d, "For " + ' ' + divisioncode[-2])
        d = dvalue()
        Footer(d)
        c.showPage()
        d = newpage()
        header(divisioncode)
        data(result, d, i)

