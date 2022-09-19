import textwrap

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
from datetime import date

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
# d = 730
d=560
divisioncode=[]
challanno=[]
pageno=0
def page():
    global pageno
    pageno = pageno + 1
    return pageno
def fonts(size):
    global c
    c.setFont("MyOwnArial", size)
def dvalue():
    global d
    d=d-10
    return d
def newpage():
    global d
    d = 510
    # d = 730
    return d
def newrequest():
    global divisioncode
    global pageno
    global product
    global departmentname
    global agent
    global broker
    global challanno
    global customer
    global product
    # global warehouse
    divisioncode=[]
    departmentname=[]
    agent=[]
    challanno=[]
    brokergroup=[]
    customer=[]
    product=[]
    # print(customer)

    pageno=0
    global d
    d=510
    # warehouse=[]
    product=0

def logic(result):
    divisioncode.append(result['COMPANYNAME'])
    challanno.append(result['CHALLANNUMBER'])

def header(result):
    c.drawCentredString(360, 540, result['COMPANYNAME'])
    c.drawCentredString(360, 520, "address plant  here Beekaylon Synthetics PTV. LTD.")
    c.drawString(30, 465, "M/S : " + str(result['CUSTOMER']))
    c.drawString(30, 455, "Address : " + str(result['ADDRESS']))
    c.drawString(310, 475, "Challan No. : " + str(result['CHALLANNUMBER']))
    c.drawString(310, 465, "LR No.      : " + str(result['LRNO']))
    c.drawString(310, 455, "Des. From   : ")
    c.drawString(310, 445, "Lot No.     : ")
    c.drawString(310, 435, "Quality.    : " + str(result['PRODUCT']))
    c.drawString(310, 425, "Net Wt.     : ")
    c.drawString(310, 415, "Shade No/ Shade : " + str(result['SHADECODE']))
    c.drawString(550, 475, "Date : " + str(result['CHALLANDATE']))
    c.drawString(550, 465, "Date : " + str(result['LRDATE']))
    c.drawString(550, 455, "To : ")
    c.drawString(550, 445, "Twist : ")
    c.drawString(550, 425, "Boxes : ")
    c.drawString(580, 377, "Ref. " + str(result['REFERANCECODE']))

def textsize(c, result, d):
    fonts(7)
    logic(result)

    if d< 40:
        d = newpage()
        c.showPage()
        header(result)

    c.drawString(280, 569, "Subject to Silvassa Jurisdiction.")
    if len(challanno) == 1:
        # header(stdt, etdt, divisioncode, lslotno, LSRegistertype)
        fonts(7)
        c.drawString(280, 569, "Subject to Silvassa Jurisdiction.")
        header(result)
    #     printbrokergroup(result)
    #     if LSRegistertype == '0':
    #         printbroker(result)
    #     else:
    #         printbroker(result)
    #         printparty(result)
    #     printcompanyname(result)
    #     printproduct(result)
    #     printdetailh(stdt, etdt,result, lslotno,LSRegistertype)
    # elif departmentname[-1] == departmentname[-2]:
    #     if brokergroup[-1] != brokergroup[-2]:
    #         printitemtotal(d)
    #         # printpartytotal(d)
    #         # printbrokertotal(d)
    #         # printbrokergrouptotal(d)
    #         # printbrokergroup(result)
    #         if LSRegistertype == '0':
    #             printbrokertotal(d)
    #             printbrokergrouptotal(d)
    #             printbrokergroup(result)
    #             printbroker(result)
    #         else:
    #             printpartytotal(d)
    #             printbrokergroup(result)
    #             printbroker(result)
    #             printparty(result)
    #         printcompanyname(result)
    #         printproduct(result)
    #         printdetailh(stdt, etdt,result, lslotno,LSRegistertype)
    #         # print('Invoice number : - ' + str(result['INVOICENO']) + ' Product : -  ' + str(result['PRODUCT']))
    #     else:
    #         if broker[-1] != broker[-2]:
    #             printitemtotal(d)
    #             # printbrokertotal(d)
    #             if LSRegistertype == '0':
    #                 printbrokertotal(d)
    #                 printbroker(result)
    #             else:
    #                 printpartytotal(d)
    #                 printbrokergroup(result)
    #                 printparty(result)
    #             printproduct(result)
    #             printdetailh(stdt, etdt,result, lslotno,LSRegistertype)
    #
    #         else:
    #             printdetail(stdt, etdt,result, d, lslotno,LSRegistertype)
    # elif departmentname[-1] != departmentname[-2]:
    #     printitemtotal(d)
    #     # printcustomertotal(d)
    #     # printcompanytotal(d)
    #     if LSRegistertype=='0':
    #         printbrokertotal(d)
    #     else:
    #         printpartytotal(d)
    #     printcompanytotal(d)
    #     # printdepartmenttotal(d)
    #     d = dvalue()
    #     c.showPage()
    #     d = newpage()
    #     header(stdt, etdt, divisioncode, lslotno, LSRegistertype)
    #     printdepartment(result, d)
    #     # if agent[-1]!=agent[-2]:
    #     if broker[-1] != broker[-2]:
    #         # printitemtotal(d)
    #         if LSRegistertype == '0':
    #             printbroker(result)
    #         else:
    #             printparty(result)
    #         printsubdetail(result)
    #         d = dvalue()
    #         printdetail(stdt, etdt,result, d, lslotno,LSRegistertype)
    #         # printtotal(d)
    #     else:
    #         d = dvalue()
    #         printdetail(stdt, etdt,result, d, lslotno,LSRegistertype)
    # if product[-1] != product[-2]:
    #     printitemtotal(d)
    # dvaluex(stdt, etdt, result, divisioncode, LSRegistertype)
    print("after textsize")