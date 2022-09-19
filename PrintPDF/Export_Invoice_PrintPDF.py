import textwrap

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
# c = canvas.Canvas("1.pdf")
c = canvas.Canvas("1.pdf", pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 495
divisioncode = []
party = []
product = []
CompanyQuentityTotal = 0
CompanyAmountTotal = 0
totalivoiceqty = 0
totalchalllanqty = 0
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


def GroupByProduct(result, d):
    fonts(7)
    c.drawString(10, d, result['PLANTNAME'])


def itemcodes(result, d):
    fonts(7)
    c.drawString(10, d, "PLANTNAME : " + str(result['PLANTNAME']))


def logic(result):
    divisioncode.append(result['COMPANY'])
    party.append(result['PARTY'])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 495
    return d


def supplier(result):
    # c.drawString(10, d, str(result['SUPPLIER']))
    pass


def companyclean():
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = 0
    CompanyAmountTotal = 0


def newrequest():
    global divisioncode
    global pageno
    global suppliername
    divisioncode = []
    pageno = 0
    suppliername = []


def textsize(c, result, d, stdt, etdt):
    # d = dvalue()
    logic(result)
    if d < 40:
        d = newpage()

        c.showPage()
        header(stdt, etdt, divisioncode)
        d = dvalue()
    if len(divisioncode) == 1:
        # data(result, d)
        # d=dvalue()
        header(stdt, etdt, divisioncode)
        data(result, d)
    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)
    elif divisioncode[-1] != divisioncode[-2]:
        # d = newpage()
        d=495
        c.showPage()
        header(stdt, etdt, divisioncode)
        data(result, d)


def header(stdt, etdt, divisioncode):
    global d
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(450, 550, divisioncode[-1])
    fonts(9)
    c.drawCentredString(450, 540,
                        "Shipment details Order-wise From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(780, 540, "Page No." + str(p))
    c.line(0, 530, 860, 530)
    c.line(0, 505, 860, 505)
    # Upperline in header
    c.drawString(10, 520, "Order No")
    c.drawString(70, 520, "Order")
    c.drawString(70, 510, " Date")
    c.drawString(110, 520, "Commit")
    c.drawString(120, 510, "Days")
    c.drawString(150, 520, "Buyer Name")
    c.drawString(375, 520, "Exp")
    c.drawString(365, 510, "Invoice No.")
    c.drawString(422, 520, "Invoice")
    c.drawString(422, 510, "  Date")
    c.drawString(480, 520, "Commitme")
    c.drawString(480, 510, "nt Date")
    c.drawString(535, 520, "Delivery")
    c.drawString(535, 510, "  Days")
    c.drawString(580, 520, "Order")
    c.drawString(580, 510, "  Qty")
    c.drawString(620, 520, "Invoice")
    c.drawString(620, 510, "  Qty")
    c.drawString(660, 520, "Contract No")
    c.drawString(720, 520, "Contract")
    c.drawString(720, 510, "   Date")
    c.drawString(760, 520, " Commitment ")
    c.drawString(760, 510, "Date - Contract")

    # , SO03.CODE as ORDERNUMBER
    # , SO03.ORDERDATE as ORDERDATE
    # , SPL03.SALESORDERCODE
    # AS
    # SALESORDERLINECODE
    # , '' as commtdays
    # , BusinessPartner.LEGALNAME1
    # AS
    # BuyerNAME
    # , '' as EXPINVNO
    # , '' as COMMITMENTDATE
    # , '' as DELVDAYS
    # , SPL03.USERPRIMARYQUANTITY as ORDERQUNITIY
    # , PLI.PRIMARYQTY as INVOICEQUANTITY
    # , SO02.CODE as CONTACTNO
    # , SO02.ORDERDATE as CONTACTDATE
    # , '' as COMMITMENTDATECONTRACT


def data(result, d):
    fonts(7)
    c.drawString(10, d, result['ORDNO_03'])
    c.drawString(65, d, str(result['ORDDT_03']))
    c.drawString(120, d, str(result['COMMITEDDAYS']))
    c.drawString(150, d, result['PARTY'])
    c.drawString(365, d, result['INVOICENO'])
    c.drawString(420, d, str(result['INVOICEDATE']))
    c.drawString(480, d, str(result['COMMITEMENTDATE']))
    c.drawString(540, d, str(result['DELAYDAYS']))
    c.drawString(580, d, result['ORDQTY'])
    c.drawString(620, d, result['CHALQTY'])
    c.drawString(660, d, result['CONTNO_02'])
    c.drawString(720, d, str(result['CONTDT_02']))
    c.drawString(780, d, str(result['COMMITEMENTDATE']))
    # print("from pdf data  file")


#     if len(divisioncode) == 1:

# def textsize(c, result, d, stdt, etdt):
#     d = dvalue()
#     logic(result)
#     if d < 40:
#         d = newpage()
#         c.showPage()
#         header(stdt, etdt, divisioncode)
#
#     if len(divisioncode) == 1:
#         if len(suppliername) == 1:
#             if d > 14:
#                 header(stdt, etdt, divisioncode)
#                 d = dvalue()
#                 fonts(7)
#                 supplier(result)
#                 d = dvalue()
#                 data(result, d)
#
#     elif divisioncode[-1] == divisioncode[-2]:
#         if suppliername[-2] == suppliername[-1]:
#             data(result, d)
#         elif suppliername[-2] != suppliername[-1]:
#             fonts(7)
#             supplier(result)
#             d = dvalue()
#             data(result, d)
#
#     elif divisioncode[-1] != divisioncode[-2]:
#         d = dvalue()
#         fonts(7)
#         companyclean()
#         c.showPage()
#
#         header(stdt, etdt, divisioncode)
#         d = newpage()
#         d = dvalue()
#         fonts(7)
#         if suppliername[-2] == suppliername[-1]:
#             data(result, d)
#         elif suppliername[-2] != suppliername[-1]:
#             supplier(result)
#             d = dvalue()
#             data(result, d)

def textsize2(c, result, d, stdt, etdt):
    logic(result)
    # LSRegistertyp = LSRegistertype
    # printdetail(result,d)
    if d < 40:
        d = newpage()
        c.showPage()
        header2(stdt, etdt, result, divisioncode)

    if len(divisioncode) == 1:
        header2(stdt, etdt, divisioncode)
        d=dvalue()
        printpartyname(result, d)
        fonts(7)
        # printdetails(result)
    elif divisioncode[-1] == divisioncode[-2]:
        if party[-1] != party[-2]:
            printtotal()
            d=dvalue()
            printpartyname(result, d)
        else:
            printdetails(result,d)
    elif divisioncode[-1] != divisioncode[-2]:
        printtotal()
        d = dvalue()
        d = dvalue()
        c.showPage()
        d = newpage()
        header2(stdt, etdt, divisioncode)
        printpartyname(result, d)
        # if agent[-1]!=agent[-2]:

    print("after textsize")

def header2(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(450, 550, divisioncode[-1])
    fonts(9)
    c.drawCentredString(450, 540,
                        "Shipment details Order-wise From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(780, 540, "Page No." + str(p))
    c.line(0, 530, 860, 530)
    c.line(0, 505, 860, 505)
    # Upperline in header
    c.drawString(10, 520, "Order No")
    c.drawString(70, 520, "Order")
    c.drawString(70, 510, " Date")
    c.drawString(110, 520, "Commit")
    c.drawString(120, 510, "Days")
    # c.drawString(10, 520, "Order No")
    # c.drawString(50, 520, "Order Date")
    # c.drawString(100, 520, "Comt Days")
    c.drawString(150, 520, "Item")
    c.drawString(280, 520, "Shade")
    c.drawString(375, 520, "Exp")
    c.drawString(365, 510, "Invoice No.")
    c.drawString(422, 520, "Invoice")
    c.drawString(422, 510, "  Date")
    c.drawString(480, 520, "Commitme")
    c.drawString(480, 510, "nt Date")
    c.drawString(535, 520, "Delivery")
    c.drawString(535, 510, "  Days")
    c.drawString(580, 520, "Order")
    c.drawString(580, 510, "  Qty")
    c.drawString(620, 520, "Invoice")
    c.drawString(620, 510, "  Qty")
    c.drawString(660, 520, "Contract No")
    c.drawString(720, 520, "Contract")
    c.drawString(720, 510, "   Date")
    c.drawString(760, 520, " Commitment ")
    c.drawString(760, 510, "Date - Contract")
    # c.drawString(250, 520, "Exp Invoice No.")
    # c.drawString(350, 520, "Invoice Date")
    # c.drawString(460, 520, "Commit")
    # c.drawString(460, 510, "ment Date")
    # c.drawString(500, 520, "  Delivery")
    # c.drawString(500, 510, "    Days")
    # c.drawString(540, 520, "  Order")
    # c.drawString(540, 510, " Quantity")
    # c.drawString(590, 520, " Invoice")
    # c.drawString(590, 510, "Quantity")
    # c.drawString(630, 520, "Contract No")
    # c.drawString(680, 520, "Contract")
    # c.drawString(680, 510, "   Date")
    # c.drawString(750, 520, " Commitment ")
    # c.drawString(750, 510, "Date - Contract")

def printpartyname(result, d):
    c.drawString(10, d, result['PARTY'])
    d = dvalue()
    printdetails(result,d)

def printdetails(result,d):
    fonts(7)
    d=dvalue()
    c.drawString(10, d, result['ORDNO_03'])
    c.drawString(65, d, str(result['ORDDT_03']))
    c.drawString(120, d, str(result['COMMITEDDAYS']))
    # c.drawString(10, d, result['ORDNO_03'])
    # c.drawString(50, d, str(result['ORDDT_03']))
    # c.drawString(100, d, str(result['COMMITEDDAYS']))
    c.drawString(280, d, result['SHADE'])
    # c.drawString(430, d, result['INVOICENO'])
    # c.drawString(480, d, str(result['INVOICEDATE']))
    # c.drawString(520, d, str(result['COMMITEDDAYS']))
    # c.drawString(550, d, str(result['DELAYDAYS']))
    # c.drawString(580, d, result['CHALQTY'])
    # c.drawString(620, d, result['ORDQTY'])
    # c.drawString(660, d, result['CONTNO_02'])
    # c.drawString(710, d, str(result['CONTDT_02']))
    # c.drawString(750, d, str(result['COMMITEMENTDATE']))

    c.drawString(365, d, result['INVOICENO'])
    c.drawString(420, d, str(result['INVOICEDATE']))
    c.drawString(480, d, str(result['COMMITEMENTDATE']))

    c.drawString(540, d, str(result['DELAYDAYS']))
    # c.drawString(580, d, result['ORDQTY'])
    # c.drawString(620, d, result['CHALQTY'])
    c.drawAlignedString(590, d, str(("%.3f" % float(result['ORDQTY']))))
    c.drawAlignedString(630, d, str(("%.3f" % float(result['CHALQTY']))))
    c.drawString(660, d, result['CONTNO_02'])
    c.drawString(720, d, str(result['CONTDT_02']))
    c.drawString(780, d, str(result['COMMITEMENTDATE']))

    itemname = result['ITEM']
    # sa = d
    if len(str(itemname)) > 30:
        lines = textwrap.wrap(str(itemname), 30, break_long_words=False)
        for i in lines:
            c.drawString(150, d, str(i))
            d = d - 10
    else:
        c.drawString(150, d, result['ITEM'])
        # c.drawString(340, 256, ": " + str(result['SHADECODE']))
    total(result)

def total(result):
    global totalivoiceqty
    global totalchalllanqty
    totalivoiceqty = totalivoiceqty + float("%.3f" % float(result['ORDQTY']))
    totalchalllanqty = totalchalllanqty + float("%.3f" % float(result['CHALQTY']))

def printtotal():
    global totalivoiceqty
    global totalchalllanqty
    c.drawString(460,d,"Buyer Total :  ")
    c.drawAlignedString(590, d, str(("%.3f" % float(totalivoiceqty))))
    c.drawAlignedString(630, d, str(("%.3f" % float(totalchalllanqty))))
    totalivoiceqty = 0
    totalchalllanqty = 0


def textsize3(c, result, d, stdt, etdt):
    logic(result)
    if d < 40:
        d = newpage()
        c.showPage()
        header3(stdt, etdt, result, divisioncode)
    if len(divisioncode) == 1:
        header3(stdt, etdt, divisioncode)
        d=dvalue()
        printitemname(result, d)
        fonts(7)
    elif divisioncode[-1] == divisioncode[-2]:
        if party[-1] != party[-2]:
            printtotal()
            d=dvalue()
            printitemname(result, d)
        else:
            printdetails3(result,d)
    elif divisioncode[-1] != divisioncode[-2]:
        printtotal()
        d = dvalue()
        d = dvalue()
        c.showPage()
        d = newpage()
        header3(stdt, etdt, divisioncode)
        printitemname(result, d)
    print("after textsize")

def header3(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(450, 550, divisioncode[-1])
    fonts(9)
    c.drawCentredString(450, 540,
                        "Shipment details Order-wise From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(780, 540, "Page No." + str(p))
    c.line(0, 530, 860, 530)
    c.line(0, 505, 860, 505)
    # Upperline in header
    # c.drawString(10, 520, "Order No")
    # c.drawString(50, 520, "Order Date")
    # c.drawString(100, 520, "Comt Days")
    c.drawString(10, 520, "Order No")
    c.drawString(70, 520, "Order")
    c.drawString(70, 510, " Date")
    c.drawString(110, 520, "Commit")
    c.drawString(120, 510, "Days")
    c.drawString(150, 520, "Buyer Name")
    c.drawString(280, 520, "Shade")
    c.drawString(375, 520, "Exp")
    c.drawString(365, 510, "Invoice No.")
    c.drawString(422, 520, "Invoice")
    c.drawString(422, 510, "  Date")
    c.drawString(480, 520, "Commitme")
    c.drawString(480, 510, "nt Date")
    c.drawString(535, 520, "Delivery")
    c.drawString(535, 510, "  Days")
    c.drawString(580, 520, "Order")
    c.drawString(580, 510, "  Qty")
    c.drawString(620, 520, "Invoice")
    c.drawString(620, 510, "  Qty")
    c.drawString(660, 520, "Contract No")
    c.drawString(720, 520, "Contract")
    c.drawString(720, 510, "   Date")
    c.drawString(760, 520, " Commitment ")
    c.drawString(760, 510, "Date - Contract")
    # c.drawString(250, 520, "Exp Invoice No.")
    # c.drawString(350, 520, "Invoice Date")
    # c.drawString(460, 520, "Commit")
    # c.drawString(460, 510, "ment Date")
    # c.drawString(500, 520, "  Delivery")
    # c.drawString(500, 510, "    Days")
    # c.drawString(540, 520, "  Order")
    # c.drawString(540, 510, " Quantity")
    # c.drawString(590, 520, " Invoice")
    # c.drawString(590, 510, "Quantity")
    # c.drawString(630, 520, "Contract No")
    # c.drawString(680, 520, "Contract")
    # c.drawString(680, 510, "   Date")
    # c.drawString(750, 520, " Commitment ")
    # c.drawString(750, 510, "Date - Contract")

def printitemname(result, d):
    c.drawString(10, d, result['ITEM'])
    d = dvalue()
    printdetails3(result,d)

def printdetails3(result,d):
    fonts(7)
    d = dvalue()
    # c.drawString(10, d, result['ORDNO_03'])
    # c.drawString(50, d, str(result['ORDDT_03']))
    # c.drawString(100, d, str(result['COMMITEDDAYS']))
    c.drawString(10, d, result['ORDNO_03'])
    c.drawString(65, d, str(result['ORDDT_03']))
    c.drawString(120, d, str(result['COMMITEDDAYS']))
    c.drawString(280, d, result['SHADE'])
    c.drawString(365, d, result['INVOICENO'])
    c.drawString(420, d, str(result['INVOICEDATE']))
    c.drawString(480, d, str(result['COMMITEMENTDATE']))

    c.drawString(540, d, str(result['DELAYDAYS']))
    # c.drawString(580, d, result['ORDQTY'])
    # c.drawString(620, d, result['CHALQTY'])
    c.drawAlignedString(590, d, str(("%.3f" % float(result['ORDQTY']))))
    c.drawAlignedString(630, d, str(("%.3f" % float(result['CHALQTY']))))
    c.drawString(660, d, result['CONTNO_02'])
    c.drawString(720, d, str(result['CONTDT_02']))
    c.drawString(780, d, str(result['COMMITEMENTDATE']))
    # c.drawString(430, d, result['INVOICENO'])
    # c.drawString(480, d, str(result['INVOICEDATE']))
    # c.drawString(520, d, "Commit")
    # c.drawString(550, d, str(result['DELAYDAYS']))
    # c.drawString(580, d, result['CHALQTY'])
    # c.drawString(620, d, result['ORDQTY'])
    # c.drawString(660, d, result['CONTNO_02'])
    # c.drawString(710, d, str(result['CONTDT_02']))
    # c.drawString(750, d, str(result['COMMITEMENTDATE']))
    partyname = result['PARTY']
    # sa = d
    if len(str(partyname)) > 30:
        lines = textwrap.wrap(str(partyname), 30, break_long_words=False)
        for i in lines:
            c.drawString(150, d, str(i))
            d = d - 10
    else:
        c.drawString(150, d, result['PARTY'])
        # c.drawString(340, 256, ": " + str(result['SHADECODE']))
    total(result)