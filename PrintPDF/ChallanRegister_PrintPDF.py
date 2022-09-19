from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
from datetime import date


pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
# c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
# c.setPageSize(landscape(A4))
d = 730
divisioncode=[]
departmentname=[]
product=[]
agent=[]
customer=[]
itemcount=[]
CompanyQuentityTotal=0
CompanyAmountTotal=0
pageno=0
totalquantity=0
totalprice=0
totalagentquantity=0
totalagentprice=0

totaldepartmentquentity=0
totaldepartmentagent=0
totaldepartmentprice=0
totalbox=0
totalcops=0
totalcompanyquantity=0
totalcompanyprice=0

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



def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    # d = 480
    d = 730
    return d

def newrequest():
    global divisioncode
    global pageno
    global product
    # global warehouse
    divisioncode=[]
    pageno=0
    global d
    d=480
    # warehouse=[]
    product=0

def logic(result):
    divisioncode.append(result['DEPTNAME'])
    departmentname.append(result['DEPTNAME'])
    agent.append(result['AGENT'])
    customer.append(result['CUSTOMER'])
    # print(customer)
    try:
        product.append(result['PRODUCT'])
    except:
        pass

# def total(result):
#     global totalbox
#     global totalcops
#     global totalquantity
#     global totalagentquantity
#     global totaldepartmentquentity
#     temp =0
#     temp=totalquantity
#     totalquantity=totalquantity+ (float("%.3f" % float(result['QUANTITY'])))
#     # totalcops=totalbox+ (float("%.3f" % float(result['COPS'])))
#     # totalbox=totalbox+ (float("%.3f" % float(result['BOXES'])))
#     print("temp : "+str(temp))
#     print("total : "+str(totalquantity))

def printdepartment(result,d):
    c.drawString(10, d, result['DEPTNAME'])

def printsubdetail(result):
    d=dvalue()
    c.drawCentredString(300, d, '05 Doc Name')
    d=dvalue()
    c.drawString(10, d, "Agent              : "+str(result['AGENT']))
    d=dvalue()
    c.drawString(10, d, "Customer        : "+str(result['CUSTOMER']))
    d=dvalue()
    c.drawString(10, d, "Chal. Desc      : 06 Doc Name")

def printdetail(result,d):
    fonts(8)
    # d=dvalue()
    global totalquantity
    global totalagentquantity
    global totaldepartmentquentity
    c.drawString(10, d, result['CHALLANNUMBER'])
    c.drawString(70, d, result['CHALLANDATE'].strftime('%d-%m-%Y'))
    c.drawString(120, d, result['PRODUCT'])
    c.drawString(390, d, "0000000")
    c.drawString(440, d, result['SHADECODE'])
    c.drawString(490, d, "0")
    c.drawString(520, d, "0")
    c.drawAlignedString(570, d, str(("%.3f" % float(result['QUANTITY']))))
    print("totalquantity from printdetails before   : " + str(totalquantity))
    print("quantity from printdetails               : " +str(float("%.3f" % float(result['QUANTITY']))))

    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalagentquantity = totalagentquantity + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentquentity = totaldepartmentquentity + (float("%.3f" % float(result['QUANTITY'])))
    print("totalquantity from printdetails after    : " + str(totalquantity))

def printcustomertotal(d):
    d=dvalue()
    # c.line(380, d+8, 590, d+8)
    global totalquantity
    print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(450, d, "Party Total :")
    c.drawString(490, d, "0")  # Boxes
    c.drawString(520, d, "0")  # Cops for this 2 value sir will tell to use then have to use field to display
    c.drawAlignedString(570, d, str(("%.3f" % float(totalquantity))))
    # d=dvalue()

    totalquantity=0

def printagenttotal(d):
    d=dvalue()
    global totalagentquantity
    print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(450, d, "Agent Total :")
    c.drawString(490, d, "0")  # Boxes
    c.drawString(520, d, "0")  # Cops for this 2 value sir will tell to use then have to use field to display
    # c.drawString(560, d, "Net Wt ")
    c.drawAlignedString(570, d, str(("%.3f" % float(totalagentquantity))))
    # d=dvalue()

    totalagentquantity=0

def printdepartmenttotal(d):
    d=dvalue()
    global totaldepartmentquentity
    print("totalquantity from printtotal "+str(totaldepartmentquentity))
    c.drawAlignedString(450, d, "Dept Total :")
    c.drawString(490, d, "0") # Boxes
    c.drawString(520, d, "0") # Cops for this 2 value sir will tell to use then have to use field to display
    # c.drawString(560, d, "Net Wt ")
    c.drawAlignedString(570, d, str(("%.3f" % float(totaldepartmentquentity))))
    # d=dvalue()

    totaldepartmentquentity=0

def header(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300  , 780, "Challan  Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    #Upperline in header
    c.drawString(10, 758, "Chal No.")
    c.drawString(70, 758, "Date")
    c.drawString(120, 758, "Item")
    c.drawString(390, 758, "Lot No")
    c.drawString(440, 758, "Shade")
    c.drawString(480, 758, "Boxes")
    c.drawString(520, 758, "Cops")
    c.drawString(560, 758, "Net Wt")
    print("from header end ")

def textsize(c,result,d,stdt,etdt):
    fonts(9)
    logic(result)
    if len(departmentname) == 1:
        header(stdt,etdt,divisioncode)
        printdepartment(result, d)
        printsubdetail(result)
        d = dvalue()
        printdetail(result,d)
    elif departmentname[-1]==departmentname[-2]:
        if agent[-1]!=agent[-2]:
            printdetail(result,d)
            printcustomertotal(d)
            printagenttotal(d)
            printsubdetail(result)
        else:
            printdetail(result,d)
    elif departmentname[-1]!=departmentname[-2]:
        printcustomertotal(d)
        printagenttotal(d)
        printdepartmenttotal(d)
        d = dvalue()

        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode)
        printdepartment(result, d)
        if agent[-1]!=agent[-2]:
            printsubdetail(result)
            d = dvalue()
            printdetail(result, d)
            # printtotal(d)
        else:
            d = dvalue()
            printdetail(result, d)


            # printtotal(d)
    # else:
    #     printtotal(dvalue())

#########################################################################
#               Code for the Challan Register start                     #
#########################################################################

def header1(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300  , 780, "Challan  Register Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    #Upperline in header
    c.drawString(10, 758, "Item")
    c.drawString(480, 758, "Boxes")
    c.drawString(520, 758, "Cops")
    c.drawString(560, 758, "Net Wt")

def printdetail1(result,d):
    fonts(8)
    # d=dvalue()
    global totalquantity
    global totalbox
    global totalcops

    c.drawString(10, d, result['PRODUCT'])
    c.drawString(490, d, "0")
    c.drawString(520, d, "0")
    c.drawAlignedString(570, d, str(("%.3f" % float(result['QUANTITY']))))
    print("totalquantity from printdetails before   : " + str(totalquantity))
    print("quantity from printdetails               : " +str(float("%.3f" % float(result['QUANTITY']))))
    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    # totalbox = totalbox + (float("%.3f" % float(result['QUANTITY'])))
    # totalcops = totalcops + (float("%.3f" % float(result['QUANTITY'])))

def printregistersummarytotal(d):
    d=dvalue()
    # c.line(380, d+8, 590, d+8)
    global totalquantity
    print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(450, d, " Total :")
    c.drawString(490, d, "0") # Boxes
    c.drawString(520, d, "0") # Cops for this 2 value sir will tell to use then have to use field to display
    c.drawAlignedString(570, d, str(("%.3f" % float(totalquantity))))
    # d=dvalue()

    totalquantity=0

def textsize1(c,result,d,stdt,etdt):
    fonts(9)
    logic(result)
    if len(departmentname) == 1:
        header1(stdt,etdt,divisioncode)
        d = dvalue()
        printdetail1(result,d)
    elif departmentname[-1]==departmentname[-2]:
        # d = dvalue()
        printdetail1(result,d)
    elif departmentname[-1]!=departmentname[-2]:
        c.showPage()
        d = newpage()
        header1(stdt, etdt, divisioncode)
        printdetail1(result, d)

#########################################################################
#       Code for the Agent Party Item-wise Register start               #
#########################################################################
def textsize2(c,result,d,stdt,etdt):
    fonts(9)
    logic(result)
    itemcount.append(result['ITEMCOUNT'])
    if len(departmentname) == 1:
        header2(stdt,etdt,divisioncode)
        # printdepartment(result, d)
        printsubdetail2(result)
        d = dvalue()
        printdetail2(result,d)
    elif departmentname[-1]==departmentname[-2]:
        if agent[-1]!=agent[-2]:
            printdetail2(result,d)
            # printcustomertotal(d)
            # printagenttotal(d)
            printtotal2(d)
            printsubdetail2(result)
        else:
            printdetail2(result,d)
    elif departmentname[-1]!=departmentname[-2]:
        # printcustomertotal(d)
        # printagenttotal(d)
        printtotal2(d)
        printdepartmenttotal2(d)
        d = dvalue()

        c.showPage()
        d=newpage()
        header2(stdt, etdt, divisioncode)
        printdepartment(result, d)
        if agent[-1]!=agent[-2]:
            printsubdetail2(result)
            d = dvalue()
            printdetail2(result, d)
            # printtotal2(d,result)

        else:
            d = dvalue()
            printdetail2(result, d)
        # c.showPage()

def header2(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")

    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, d1)
    c.drawCentredString(300  , 780, "Sales Agent-Party-Itemwise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    #Upperline in header
    c.drawString(60, 758, "Item")
    c.drawString(460, 758, "Quanitity")
    c.drawString(540, 758, "Item Amount")

def printsubdetail2(result):
    d=dvalue()
    # c.drawCentredString(300, d, '05 Doc Name')
    # d=dvalue()
    c.drawString(10, d,result['AGENT'])
    d=dvalue()
    c.drawString(30, d, result['CUSTOMER'])
    # d=dvalue()
    # c.drawString(10, d, "Chal. Desc      : 06 Doc Name")

def printdetail2(result,d):
    fonts(8)
    # d=dvalue()
    global totalquantity
    global totalprice
    global totaldepartmentquentity
    global totaldepartmentagent
    global totaldepartmentprice
    c.drawString(60, d, result['PRODUCT'])
    c.drawAlignedString(480, d, str(("%.3f" % float(result['QUANTITY']))))
    print("totalquantity from printdetails before   : " + str(totalquantity))
    print("quantity from printdetails               : " +str(float("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(580, d, str(format_currency("%.2f" % float(result['INVOICEAMOUNT']), '', locale='en_IN')))
    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalprice = totalprice + (float("%.2f" % float(result['INVOICEAMOUNT'])))
    totaldepartmentquentity = totaldepartmentquentity + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentagent = totaldepartmentagent + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentprice = totaldepartmentprice + (float("%.3f" % float(result['INVOICEAMOUNT'])))
    print("totalquantity from printdetails after    : " + str(totalquantity))

def printtotal2(d):
    temp =int (itemcount[0])
    # if (itemcount!=1):
    printcustomertotal2(d)
    printagenttotal2(d)

def printcustomertotal2(d):
    d=dvalue()
    # c.line(380, d+8, 590, d+8)
    global totalquantity
    global totalprice
    print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(450, d, "Party Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))

    # totalquantity=0

def printagenttotal2(d):
    d=dvalue()
    global totalquantity
    global totalprice
    print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(450, d, "Agent Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))

    totalquantity=0
    totalprice=0

def printdepartmenttotal2(d):
    d=dvalue()
    global totaldepartmentquentity
    global totaldepartmentagent
    global totaldepartmentprice
    print("totalquantity from printtotal "+str(totaldepartmentquentity))

    # d=dvalue()
    c.drawAlignedString(450, d, "Dept Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totaldepartmentquentity))))
    c.drawAlignedString(580, d, str(("%.2f" % float(totaldepartmentprice))))

    totaldepartmentquentity=0
    totaldepartmentprice=0

#########################################################################
#       Code for the Party Agent Item-wise Register start               #
#########################################################################
def textsize3(c,result,d,stdt,etdt):
    fonts(9)
    logic(result)
    itemcount.append(result['ITEMCOUNT'])
    if len(departmentname) == 1:
        header3(stdt,etdt,divisioncode)
        # printdepartment(result, d)
        printsubdetail3(result)
        d = dvalue()
        printdetail3(result,d)
    elif departmentname[-1]==departmentname[-2]:
        if agent[-1]!=agent[-2]:
            printdetail3(result,d)
            # printcustomertotal(d)
            # printagenttotal(d)
            printtotal3(d)
            printsubdetail3(result)
        else:
            printdetail3(result,d)
    elif departmentname[-1]!=departmentname[-2]:
        # printcustomertotal(d)
        # printagenttotal(d)
        printtotal3(d)
        printdepartmenttotal3(d)
        d = dvalue()

        c.showPage()
        d=newpage()
        header3(stdt, etdt, divisioncode)
        printdepartment(result, d)
        if agent[-1]!=agent[-2]:
            printsubdetail3(result)
            d = dvalue()
            printdetail3(result, d)
            # printtotal2(d,result)

        else:
            d = dvalue()
            printdetail3(result, d)
        # c.showPage()

def header3(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")

    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, d1)
    c.drawCentredString(300  , 780, "Sales Party-Agent-Itemwise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    #Upperline in header
    c.drawString(60, 758, "Item")
    c.drawString(460, 758, "Quanitity")
    c.drawString(540, 758, "Item Amount")

def printsubdetail3(result):
    d=dvalue()
    # c.drawCentredString(300, d, '05 Doc Name')
    # d=dvalue()
    c.drawString(10, d,result['CUSTOMER'])
    d=dvalue()
    c.drawString(30, d, result['AGENT'])
    # d=dvalue()
    # c.drawString(10, d, "Chal. Desc      : 06 Doc Name")

def printdetail3(result,d):
    fonts(8)
    # d=dvalue()
    global totalquantity
    global totalprice
    global totaldepartmentquentity
    global totaldepartmentagent
    global totaldepartmentprice

    c.drawString(60, d, result['PRODUCT'])
    c.drawAlignedString(480, d, str(("%.3f" % float(result['QUANTITY']))))
    print("totalquantity from printdetails before   : " + str(totalquantity))
    print("quantity from printdetails               : " +str(float("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(580, d, str(format_currency("%.2f" % float(result['INVOICEAMOUNT']), '', locale='en_IN')))

    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalprice = totalprice + (float("%.2f" % float(result['INVOICEAMOUNT'])))
    totaldepartmentquentity = totaldepartmentquentity + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentagent = totaldepartmentagent + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentprice = totaldepartmentprice + (float("%.3f" % float(result['INVOICEAMOUNT'])))
    print("totalquantity from printdetails after    : " + str(totalquantity))

def printtotal3(d):
    temp =int (itemcount[0])
    # if (itemcount!=1):
    printcustomertotal3(d)
    printagenttotal3(d)

def printcustomertotal3(d):
    d=dvalue()
    # c.line(380, d+8, 590, d+8)
    global totalquantity
    global totalprice
    print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(450, d, "Party Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))

    # totalquantity=0

def printagenttotal3(d):
    d=dvalue()
    global totalquantity
    global totalprice
    print("totalquantity from printtotal "+str(totalagentquantity))
    c.drawAlignedString(450, d, "Agent Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))

    totalquantity=0
    totalprice=0

def printdepartmenttotal3(d):
    d=dvalue()
    global totaldepartmentquentity
    global totaldepartmentagent
    global totaldepartmentprice
    print("totalquantity from printtotal "+str(totaldepartmentquentity))

    # d=dvalue()
    c.drawAlignedString(450, d, "Dept Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totaldepartmentquentity))))
    c.drawAlignedString(580, d, str(("%.2f" % float(totaldepartmentprice))))

    totaldepartmentquentity=0
    totaldepartmentprice=0

#########################################################################
#       Code for the Item Agent Party-wise Register start               #
#########################################################################
def textsize4(c,result,e,stdt,etdt):
    fonts(9)
    logic(result)
    global d
    if len(departmentname)==1:
        # product.append(result['PRODUCT'])
        header4(stdt,etdt,divisioncode)
        c.drawString(10, d, result['PRODUCT'])
        printagentdetail4(result)
        printcustomerdetail4(result)
        maketotal(result)
    elif departmentname[-1]== departmentname[-2]:
        if product[-1]==product[-2]:
            if agent[-1]==agent[-2]:
                if customer[-1]==customer[-2]:
                    maketotal(result)
                else:
                    printcustomertotal4(d)
            # else:
            #     printagenttotal4(d)
        else:
            printtotal4(d)
            maketotal(result)
            d=dvalue()
            c.drawString(10, d, result['PRODUCT'])
            printagentdetail4(result)
            printcustomerdetail4(result)

    elif departmentname[-1]!=departmentname[-2]:
        printtotal4(d)
        printdepartmenttotal4(d)
        c.showPage()
        d=newpage()
        header4(stdt,etdt,divisioncode)
        if product[-1] == product[-2]:
            if agent[-1] == agent[-2]:
                if customer[-1] == customer[-2]:
                    maketotal(result)
                else:
                    printcustomertotal4(d)
            # else:
            #     printagenttotal4(d)
        else:
            d = dvalue()
            c.drawString(10, d, result['PRODUCT'])
            printagentdetail4(result)
            printcustomerdetail4(result)
            maketotal(result)

# def textsize4(c,result,d,stdt,etdt):
#     fonts(9)
#     logic(result)
#     itemcount.append(result['ITEMCOUNT'])
#     if len(departmentname) == 1:
#         header4(stdt,etdt,divisioncode)
#         # printdepartment(result, d)
#         # printsubdetail4(result)
#         printitemdetail4(result)
#         printagentdetail4(result)
#         d = dvalue()
#         product.append(result['PRODUCT'])
#         printdetail4(result,d)
#     elif departmentname[-1]==departmentname[-2]:
#         if product[-1]!= product[-2]:
#         # if agent[-1]!=agent[-2]:
#             printitemdetail4(result)
#             printagentdetail4(result)
#             printcustomerdetail4(result)
#             printdetail4(result,d)
#         # make a function get total to make a total of the quntity and invoice and add where needed
#             # printcustomertotal(d)
#             # printagenttotal(d)
#             printtotal4(d)
#             # printsubdetail4(result)
#         else:
#             # printagentdetail4(result)
#             printdetail4(result,d)
#     elif departmentname[-1]!=departmentname[-2]:
#         # printcustomertotal(d)
#         # printagenttotal(d)
#         printtotal4(d)
#         printdepartmenttotal4(d)
#         d = dvalue()
#
#         c.showPage()
#         d=newpage()
#         header4(stdt, etdt, divisioncode)
#         printdepartment(result, d)
#         if product[-1]!= product[-2]:
#         # if agent[-1]!=agent[-2]:
#         #     printsubdetail4(result)
#             printitemdetail4(result)
#             printagentdetail4(result)
#             d = dvalue()
#             printdetail4(result, d)
#             # printtotal2(d,result)
#         else:
#             d = dvalue()
#             printdetail4(result, d)
#         # c.showPage()
def maketotal(result):
    global totalquantity
    global totalprice
    global totalagentquantity
    global totalagentprice
    global totaldepartmentquentity
    global totaldepartmentagent
    global totaldepartmentprice
    global totalcompanyprice
    global totalcompanyquantity

    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalprice = totalprice + (float("%.2f" % float(result['INVOICEAMOUNT'])))
    totalagentquantity = totalagentquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalagentprice = totalagentprice + (float("%.2f" % float(result['INVOICEAMOUNT'])))
    totaldepartmentquentity = totaldepartmentquentity + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentagent = totaldepartmentagent + (float("%.3f" % float(result['QUANTITY'])))
    totaldepartmentprice = totaldepartmentprice + (float("%.3f" % float(result['INVOICEAMOUNT'])))
    totalcompanyquantity = totalcompanyquantity + (float("%.3f" % float(result['QUANTITY'])))
    totalcompanyprice = totalcompanyprice + (float("%.3f" % float(result['INVOICEAMOUNT'])))
    # d=dvalue()
    # c.drawAlignedString(450, d, "from make total :"+str(totalquantity))
    # d = dvalue()
    # c.drawAlignedString(450, d, "from make total agent :" + str(totalagentquantity))
    # d = dvalue()
    # c.drawAlignedString(450, d, "from make total agent :" + str(totalagentprice))

def header4(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")

    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, d1)
    c.drawCentredString(300  , 780, "Sales Item Agent-Party-Wise Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    #Upperline in header
    c.drawString(60, 758, "Item")
    c.drawString(460, 758, "Quanitity")
    c.drawString(540, 758, "Item Amount")

def printitemdetail4(result):
    if len(product)==1:

       fonts(8)
       d=dvalue()
       c.drawString(10, d, result['PRODUCT'])
       printagentdetail4(result)
       printcustomerdetail4(result)
    elif product[-1]!=product[-2]:
        d = dvalue()
        c.drawAlignedString(450, d, "elif print item details :")
        printagenttotal4(d)
        printcustomertotal(d)
        # printdetail4(result)
        c.drawString(10, d,result['PRODUCT'])
        # printagentdetail4(result)
        # printcustomerdetail4(result)
        # printdetail4(result)
    else:
       d = dvalue()
       c.drawAlignedString(450, d, "elif print item details :")
       # printdetail4(result)


# def printsubdetail4(result):
def printagentdetail4(result):
    d=dvalue()
    c.drawString(30, d, str(result['AGENT']))

def printcustomerdetail4(result):
    d=dvalue()
    qty=result['QUANTITY']
    invamt=result['INVOICEAMOUNT']
    c.drawString(50, d, str(result['CUSTOMER']))
    # c.drawAlignedString(480, d, str(("%.3f" % float(qty))))
    # c.drawAlignedString(580, d, str(format_currency("%.2f" % float(invamt), '', locale='en_IN')))



def printtotal4(d):
    # global totalquantity
    # global totalprice
    # print("totalquantity from printtotal " + str(totalquantity))
    # c.drawAlignedString(450, d, "Party Total :")
    # c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    # c.drawAlignedString(580, d, str(format_currency("%.2f" % float(totalprice), '', locale='en_IN')))
    global totalquantity
    global totalprice
    printcustomertotal4(d)
    # printagenttotal4(d)
    totalquantity = 0
    totalprice = 0



def printcustomertotal4(d):
    d=dvalue()
    # c.line(380, d+8, 590, d+8)
    global totalquantity
    global totalprice
    print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(450, d, "Item Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    # c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))
    c.drawAlignedString(580, d, str(format_currency("%.2f" % float(totalprice), '', locale='en_IN')))

    totalquantity=0
    totalprice=0

def printagenttotal4(d):
    d=dvalue()
    global totalagentquantity
    global totalagentprice
    print("totalquantity from printtotal "+str(totalquantity))
    c.drawAlignedString(450, d, "Agent Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalagentquantity))))
    # c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))
    c.drawAlignedString(580, d, str(format_currency("%.2f" % float(totalagentprice), '', locale='en_IN')))
    #c.drawAlignedString(480, d, str(("%.3f" % float(totalquantity))))
    #c.drawAlignedString(580, d, str(("%.2f" % float(totalprice))))
    totalagentquantity=0
    totalagentprice=0


def printdepartmenttotal4(d):
    d=dvalue()
    global totaldepartmentquentity
    global totaldepartmentagent
    global totaldepartmentprice
    print("totalquantity from printtotal "+str(totaldepartmentquentity))

    # d=dvalue()
    c.drawAlignedString(450, d, "Dept Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totaldepartmentquentity))))
    c.drawAlignedString(580, d, str(format_currency("%.2f" % float(totaldepartmentprice), '', locale='en_IN')))

    totaldepartmentquentity=0
    totaldepartmentprice=0

def printcompanytotal4(d):
    d=dvalue()
    global totalcompanyquantity
    global totalcompanyprice
    c.drawAlignedString(450, d, "Company Total :")
    c.drawAlignedString(480, d, str(("%.3f" % float(totalcompanyquantity))))
    c.drawAlignedString(580, d, str(format_currency("%.2f" % float(totalcompanyprice), '', locale='en_IN')))

    totalcompanyprice = 0
    totalcompanyquantity = 0

#################################################################################
#               Code for the Transporter fright / service wise  Register start                     #
#################################################################################

def header5(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300  , 780, "Transportwise Freight / Service Tax  From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 750, 600, 750)
    #Upperline in header
    c.drawString(10, 758, "Transpoter")
    c.drawString(380, 758, "Quanitiy")
    c.drawString(450, 758, "Feright")
    c.drawString(510, 758, "Service Tax")

def textsize5(c,result,d,stdt,etdt):
    fonts(9)
    logic(result)
    if len(departmentname) == 1:
        header5(stdt,etdt,divisioncode)
        d = dvalue()
        printdetail5(result,d)
    elif departmentname[-1]==departmentname[-2]:
        # d = dvalue()
        printdetail5(result,d)
    elif departmentname[-1]!=departmentname[-2]:
        c.showPage()
        d = newpage()
        header5(stdt, etdt, divisioncode)
        printdetail5(result, d)

def printdetail5(result,d):
    fonts(8)
    # d=dvalue()
    global totalquantity
    global totalbox
    global totalcops

    c.drawString(10, d, result['PRODUCT'])
    c.drawString(490, d, "0")
    c.drawString(520, d, "0")
    c.drawAlignedString(570, d, str(("%.3f" % float(result['QUANTITY']))))
    print("totalquantity from printdetails before   : " + str(totalquantity))
    print("quantity from printdetails               : " +str(float("%.3f" % float(result['QUANTITY']))))
    totalquantity = totalquantity + (float("%.3f" % float(result['QUANTITY'])))
    # totalbox = totalbox + (float("%.3f" % float(result['QUANTITY'])))
    # totalcops = totalcops + (float("%.3f" % float(result['QUANTITY'])))