from reportlab.lib.pagesizes import landscape, A4,A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import textwrap

#####################################################
# Author : Tejas Goswami
# Date : July-2021
#
#####################################################
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c=canvas.Canvas("1.pdf")
c = canvas.Canvas("1.pdf",pagesize=(landscape(A5)))
c.setPageSize(landscape(A5))
printleft=200
printright=200
limit=110
d = 200
x = 200
totalnoofchallan=0
challancounter=0

no=0
divisioncode=[]
party=[]
item=[]
challanno=[]
ShadeCode=[]
Lotno=[]
boxno=[]
remark=[]
unit=''
BoxesTotal=0
Grosswt=0
Tarewt=0
Netwt=0
Copswt=0
BoxCounter=0
totalmainGrosswt=0
totalmainNetwt=0
totalmainTarewt=0
totalmainCopswt=0
pageno=1
pan=''

def page():
    global pageno
    pageno = pageno + 1
    return pageno
def fonts(size):
    global c
    c.setFont("MyOwnArial", size)
def dvalue():
    global d
    if d > 20:
        d = d - 10
    return d
def xvalue():
    global x
    if x > 20:
        x = x - 10
    return x
# def dvalue(result, divisioncode):
#     global d
#     if d > 20:
#         d = d - 10
#         return d
#     else:
#         d = newpage()
#         c.showPage()
#         header(result, divisioncode[:-1])
#         return d
def dvaluegst():
    global d
    d = d + 10
    return d
def header(result):
    global unit
    fonts(15)
    c.drawCentredString(305, 385, result['COMPANYNAME'])
    fonts(8)
    c.drawCentredString(300, 370, result['PLANTADDRESS'])
    fonts(9)
    c.drawString(55, 340, str(result['CUSTOMER']))
    customeraddress=result['CUSTOMERADDRESS']
    ca=326
    if len(str(customeraddress))>40:
        lines = textwrap.wrap(str(customeraddress), 40, break_long_words=False)
        for i in lines:
            c.drawString(25, ca, str(i))
            ca=ca-12

    c.drawString(25, ca-12, "CONSIGNEE : " + str(result['CONSIGNEE']))
    consigeeaddress = result['CONSIGNEEADDRESS']
    ca = ca-24
    if len(str(consigeeaddress)) > 30:
        lines = textwrap.wrap(str(consigeeaddress), 30, break_long_words=False)
        for i in lines:
            c.drawString(25, ca, str(i))
            ca = ca - 12
    # c.drawString(30, 328, "M/S : " + str(result['CUSTOMER']))
    c.drawString(265, 340, "Challan No." )
    c.drawString(340, 340, ": " + str(result['CHALLANNUMBER']))
    c.drawString(265, 328, "LR No.")
    c.drawString(340, 328, ": " + str(result['LRNO']))
    c.drawString(265, 316, "Desp. From " )
    c.drawString(340, 316, ": " +str(result['DESPFROM']))
    c.drawString(265, 304, "Lot No.")
    # c.drawString(340, 304, ": " +str(result['LOTNO']))
    c.drawString(265, 292, "Quality." )
    # product=result['PRODUCT']+""+result['PRODUCT']
    product=result['PRODUCT']
    pa = 292
    if len(str(product)) > 40:
        # ca=316
        c.drawString(340, pa, ": " )
        lines = textwrap.wrap(str(product), 40, break_long_words=False)
        for i in lines:
            c.drawString(345, pa,str(i))
            pa = pa - 12
    else:
        c.drawString(340, 292, ": " + str(result['PRODUCT']))
    # c.drawString(310, 425, "Net Wt.     : ")  this value is printed at the end after the total of net wt
    # c.drawString(380, 268, ": " + str(result['WEIGHTUNIT']))
    unit=result['WEIGHTUNIT']
    c.drawString(265, 256, "Shade No/ Shade" )

    shadecode=result['SHADECODE']
    sa = 256
    if len(str(shadecode)) > 50:
        c.drawString(340, sa, ": " )
        lines = textwrap.wrap(str(shadecode), 50, break_long_words=False)
        for i in lines:
            # c.drawString(345, sa, str(i))
            sa = sa - 12
    else:
        # c.drawString(340, 256, ": " + str(result['SHADECODE']))
        pass

    # c.drawString(265, 244, "extra line" )
    # c.drawString(340, 244, ": " + str(result['SHADECODE']))
    #
    c.drawString(440, 340, "Date")
    c.drawString(480, 340, ": " + str(result['CHALLANDATE']))
    c.drawString(440, 328, "LR Date" )
    c.drawString(480, 328, ": " + str(result['LRDATE']))
    c.drawString(440, 316, "Desp. To")
    c.drawString(480, 316, ": "+str(result['DESPTO']))
    c.drawString(440, 304, "Twist")
    c.drawString(480, 304, ": "+str(result['TWIST']))
    # # c.drawString(550, 425, "Boxes : ") this value is printed at the end after the total of boxes

    c.drawString(440, 229, "Ref." )
    c.drawString(480, 229, ": " + str(result['REFERANCECODE']))
    printgst_invoice(40,result)
def signature(d):
    c.drawCentredString(510, 30, "Authorised Signatory")
def logic(result):
    # divisioncode.append(result['UNIT'])
    divisioncode.append(result['COMPANYNAME'])
    challanno.append(result['CHALLANNUMBER'])
    ShadeCode.append(result['SHADECODE'])
    Lotno.append(result['LOTNO'])
    # boxno.append(result['BOXNO'])
def dlocvalue(d):
    d=d-20
    return d
# def newpage(c,result):
def newpage():
    global d
    d = 330
    # border(c,c,result)
    return d
def newrequest():
    global divisioncode
    global pageno
    global challanno
    global no
    global boxno
    global ShadeCode
    global Lotno
    global printleft
    global printright
    global x
    global limit
    global d
    no=0
    printleft = 200
    printright = 200
    limit = 110
    d = 200
    x = 210
    divisioncode=[]
    pageno=1
    challanno=[]
    boxno=[]
    ShadeCode=[]
    Lotno=[]
def companyclean():
    global BoxesTotal
    global WeightTotal
    BoxesTotal = 0
    WeightTotal = 0

def textsize(c,result):
    fonts(9)
    logic(result)
    global printleft
    global printright
    global limit
    global d
    global x
    global totalnoofchallan
    global challancounter
    global pageno
    totalnoofchallan=result['TOTALNOOFCHALLAN']
    challancounter = challancounter + 1
    if len(challanno) == 1:
        # print(challanno)
        border(c,result)
        header(result)
        if d <= printleft and d >= limit:
            fonts(9)
            c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
            d=dvalue()
            printdetail1(result, d)
        else:
            x= xvalue()
            printdetail2(result,x)
    elif challanno[-1]== challanno[-2]:
        if d <= printleft and d >= limit:
            if len(ShadeCode) == 1:
                pass
            elif ShadeCode[-1] != ShadeCode[-2]:
                c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
            if len(Lotno)==1:
                pass
            elif Lotno[-1]!=Lotno[-2]:
                printtotal1(d)
                d=dvalue()
                c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
                d=dvalue()
            printdetail1(result, d)
        else:
            x=xvalue()
            try:
                if len(ShadeCode) == 1:
                    pass
                elif ShadeCode[-1] != ShadeCode[-2]:
                    c.drawString(30, x, result['SHADECODE'] + '  ' + result['LOTNO'])
            except:
                pass
            if x<=printleft and x>=limit:
                printdetail2(result, x)
            else:
                c.drawString(520, 355, "Page no : " + str(pageno))
                p = page()
                c.drawString(467, 87, "Continued  on Page No. "+str(p))
                c.showPage()
                # p = page()
                fonts(9)
                c.drawString(520, 355, "Page no : " + str(p))
                border(c, result)
                header(result)
                d=200
                x=210
                # printleft = 200
                # printright = 200
                printdetail1(result, d)
    elif challanno[-1]!= challanno[-2]:
        # global pageno
        pageno=0
        # if challancounter == totalnoofchallan:
        printtotalmain()
        # else:
        if d <= printleft and d >= limit:
            printtotal1(d)
        else:
            printtotal2(x)



        c.showPage()
        p = page()
        fonts(9)
        printleft = 200
        printright = 200
        limit = 110

        # c.drawString(520, 355, "Page no : " +str(p))
        border(c,result)
        header(result)
        d = 200
        x = 200

        if d <= printleft and d >= limit:
            c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
            d=dvalue()
            printdetail1(result, d)
        else:
            c.drawString(27, x, result['SHADECODE'] + '  ' + result['LOTNO'])
            x=xvalue()
            printdetail2(result, x)

    # print(challancounter)
    # print(totalnoofchallan)

    # print("out textsize")

def border(c, result):
    # print("from border")
    c.setFillColorRGB(0, 0, 0)
    # Box For Whole page
    fonts(7)
    c.line(20, 410, 580, 410)  # first horizontal line
    c.drawString(260, 402, "Subject to Silvassa Jurisdiction.")
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.line(20, 410, 20, 20)  # first vertical line
    c.line(580, 410, 580, 20)  # right vertical border  line
    fonts(12)
    c.drawCentredString(310, 355, "DELIVERY CHALLAN")
    # c.drawString(545,355,"Page no : "+page())
    c.line(20, 350, 580, 350)  # second horizontal line
    fonts(8)
    c.line(260, 238, 260, 350)  # center vertical line  short line for address and header deatils  |
    c.drawString(25, 340, "Buyer : ")
    c.drawString(25, 229, "PLEASE RECEIVE THE FOLLOWING GOODS IN ORDER & CONDITION AS PER YOUR ORDER NO.")
    c.line(20, 238, 580, 238)  # third horizontal line
    c.line(20, 225, 580, 225)  # fourth horizontal line
    c.line(20, 100, 580, 100)
    c.drawString(50, 215, "Box No.")
    c.line(105, 210, 105, 225)
    c.drawString(115, 215, "Cops")
    c.line(140, 210, 140, 225)
    c.drawString(150, 215, "Gross Wt.")
    c.line(195, 210, 195, 225)
    c.drawString(200, 215, "Tare Wt.")
    c.line(238, 210, 238, 225)
    c.drawString(255, 215, "Net Wt.")
    c.line(290, 225, 290, 83)
    c.drawString(315, 215, "Box No.")
    c.line(370, 210, 370, 225)
    c.drawString(380, 215, "Cops")
    c.line(405, 210, 405, 225)
    c.drawString(415, 215, "Gross Wt.")
    c.line(455, 210, 455, 225)
    c.drawString(465, 215, "Tare Wt.")
    c.line(510, 210, 510, 225)
    c.drawString(520, 215, "Net Wt.")
    c.line(20, 210, 580, 210)  # fifth horizontal line
    c.drawString(25,90,"CAUTION : - Please do not mix this lot(Goods) with any other lot. Any")
    c.drawString(25,80,"complaint regarding the quality and weight of yern must be made within")
    note = "seven days after receipt of the goods. The complaint received thereafter will not entertained. Our responsibility regarding the Quality of yarn ceases once the goods are convertedinto cloth."
    if len(str(note)) > 95:
        t = 70
        lines = textwrap.wrap(str(note), 95, break_long_words=False)
        for i in lines:
            c.drawString(25, t, str(i))
            t = t - 10
    c.drawAlignedString(367, 87, "Total")
    c.line(290, 83, 580, 83)  # horizantal line after total
    signature(90)
    c.line(20, 20, 580, 20)  # last vertical line

def printgst_invoice(d,result):
    c.drawString(25, 30, "GOODS CLEARED UNDER GST INVOICE No. " + str(result['PLANTINVOICENO'])+" Dated "+str(result['PLANTINVOICEDATE']))

def printdetail1(result, d):
    c.drawAlignedString(100, d, result['BOXNO'])
    c.drawAlignedString(134, d, str(("%.0f" % float(result['COPS']))))
    c.drawAlignedString(175, d, str(("%.3f" % float(result['GROSSWT']))))
    c.drawAlignedString(217, d, str(("%.3f" % float(result['TAREWT']))))
    c.drawAlignedString(270, d, str(("%.3f" % float(result['NETWT']))))
    total(result)
def printdetail2(result, x):
    c.drawAlignedString(367, x, result['BOXNO'])
    c.drawAlignedString(400, x, str(("%.0f" % float(result['COPS']))))
    c.drawAlignedString(435, x, str(("%.3f" % float(result['GROSSWT']))))
    c.drawAlignedString(487, x, str(("%.3f" % float(result['TAREWT']))))
    c.drawAlignedString(545, x, str(("%.3f" % float(result['NETWT']))))
    total(result)

def printlasttotal(d):
    if d <= printleft and d >= limit:
        printtotal1(d)
    else:
        printtotal2(x)

def printtotalmain():
    global totalmainGrosswt
    global totalmainNetwt
    global totalmainTarewt
    global totalmainCopswt
    global BoxCounter
    global unit
    c.drawString(385, 87, str(("%.0f" % float(totalmainCopswt))))
    c.drawAlignedString(435, 87, str(("%.3f" % float(totalmainGrosswt))))
    c.drawAlignedString(486, 87, str(("%.3f" % float(totalmainTarewt))))
    c.drawAlignedString(545, 87, str(("%.3f" % float(totalmainNetwt))))
    fonts(9)
    c.drawString(265, 268, "Net Wt.")

    c.drawString(340, 268, ": " + str(("%.3f" % float(totalmainNetwt))))
    c.drawString(380, 268, "   " + unit)
    c.drawString(440, 268, "Boxes")
    c.drawString(480, 268, ": " + str(BoxCounter))

    totalmainGrosswt=0
    totalmainNetwt=0
    totalmainTarewt=0
    totalmainCopswt=0
    BoxCounter=0

def total(result):
    global Grosswt
    global Netwt
    global Tarewt
    global Copswt
    global totalmainGrosswt
    global totalmainNetwt
    global totalmainTarewt
    global totalmainCopswt
    global BoxCounter
    Grosswt = Grosswt + float("%.3f" % float(result['GROSSWT']))
    Tarewt = Tarewt + float("%.3f" % float(result['TAREWT']))
    Netwt = Netwt + float("%.3f" % float(result['NETWT']))
    Copswt = Copswt + float("%.3f" % float(result['COPS']))

    totalmainTarewt=totalmainTarewt+float("%.3f" % float(result['TAREWT']))
    totalmainGrosswt=totalmainGrosswt+float("%.3f" % float(result['GROSSWT']))
    totalmainNetwt=totalmainNetwt+float("%.3f" % float(result['NETWT']))
    totalmainCopswt=totalmainCopswt+float("%.3f" % float(result['COPS']))
    BoxCounter=BoxCounter+1

def printtotal1(d):
    global Grosswt
    global Netwt
    global Tarewt
    global Copswt
    c.drawAlignedString(134, d, str(("%.0f" %float(Copswt))))
    c.drawAlignedString(175, d, str(("%.3f" % float(Grosswt))))
    c.drawAlignedString(217, d, str(("%.3f" % float(Tarewt))))
    c.drawAlignedString(270, d, str(("%.3f" % float(Netwt))))
    Grosswt = 0
    Tarewt = 0
    Netwt = 0
    Copswt=0
def printtotal2(x):
    global Grosswt
    global Netwt
    global Tarewt
    global Copswt
    x=xvalue()
    c.drawAlignedString(400, x, str(("%.0f" % float(Copswt))))
    c.drawAlignedString(435, x, str(("%.3f" % float(Grosswt))))
    c.drawAlignedString(487, x, str(("%.3f" % float(Tarewt))))
    c.drawAlignedString(545, x, str(("%.3f" % float(Netwt))))
    Grosswt = 0
    Tarewt = 0
    Netwt = 0
    Copswt=0







# from reportlab.lib.pagesizes import landscape, A4,A5
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas
# import textwrap
#
# #####################################################
# # Author : Tejas Goswami
# # Date : July-2021
# #
# #####################################################
# pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
# c=canvas.Canvas("1.pdf")
# c = canvas.Canvas("1.pdf",pagesize=(landscape(A5)))
# c.setPageSize(landscape(A5))
# printleft=200
# printright=200
# limit=110
# d = 200
# x = 200
# totalnoofchallan=0
# challancounter=0
#
# no=0
# divisioncode=[]
# party=[]
# item=[]
# challanno=[]
# ShadeCode=[]
# Lotno=[]
# boxno=[]
# remark=[]
# unit=''
# BoxesTotal=0
# Grosswt=0
# Tarewt=0
# Netwt=0
# Copswt=0
# BoxCounter=0
# totalmainGrosswt=0
# totalmainNetwt=0
# totalmainTarewt=0
# totalmainCopswt=0
# pageno=1
# pan=''
#
# def page():
#     global pageno
#     pageno = pageno + 1
#     return pageno
# def fonts(size):
#     global c
#     c.setFont("MyOwnArial", size)
# def dvalue():
#     global d
#     if d > 20:
#         d = d - 10
#     return d
# def xvalue():
#     global x
#     if x > 20:
#         x = x - 10
#     return x
# # def dvalue(result, divisioncode):
# #     global d
# #     if d > 20:
# #         d = d - 10
# #         return d
# #     else:
# #         d = newpage()
# #         c.showPage()
# #         header(result, divisioncode[:-1])
# #         return d
# def dvaluegst():
#     global d
#     d = d + 10
#     return d
# def header(result):
#     global unit
#     fonts(15)
#     c.drawCentredString(305, 385, result['COMPANYNAME'])
#     fonts(8)
#     c.drawCentredString(300, 370, result['PLANTADDRESS'])
#     fonts(9)
#     c.drawString(25, 328, "M/S : " + str(result['CUSTOMER']))
#     customeraddress=result['CUSTOMERADDRESS']
#     ca=316
#     if len(str(customeraddress))>40:
#         lines = textwrap.wrap(str(customeraddress), 40, break_long_words=False)
#         for i in lines:
#             c.drawString(25, ca, str(i))
#             ca=ca-12
#
#     c.drawString(25, ca-12, "CONSIGNEE : " + str(result['CONSIGNEE']))
#     consigeeaddress = result['CONSIGNEEADDRESS']
#     ca = ca-24
#     if len(str(consigeeaddress)) > 30:
#         lines = textwrap.wrap(str(consigeeaddress), 30, break_long_words=False)
#         for i in lines:
#             c.drawString(25, ca, str(i))
#             ca = ca - 12
#     # c.drawString(30, 328, "M/S : " + str(result['CUSTOMER']))
#     c.drawString(265, 340, "Challan No." )
#     c.drawString(340, 340, ": " + str(result['CHALLANNUMBER']))
#     c.drawString(265, 328, "LR No.")
#     c.drawString(340, 328, ": " + str(result['LRNO']))
#     c.drawString(265, 316, "Desp. From " )
#     c.drawString(340, 316, ": " +str(result['DESPFROM']))
#     c.drawString(265, 304, "Lot No.")
#     # c.drawString(340, 304, ": " +str(result['LOTNO']))
#     c.drawString(265, 292, "Quality." )
#     # product=result['PRODUCT']+""+result['PRODUCT']
#     product=result['PRODUCT']
#     pa = 292
#     if len(str(product)) > 40:
#         # ca=316
#         c.drawString(340, pa, ": " )
#         lines = textwrap.wrap(str(product), 40, break_long_words=False)
#         for i in lines:
#             c.drawString(345, pa,str(i))
#             pa = pa - 12
#     else:
#         c.drawString(340, 292, ": " + str(result['PRODUCT']))
#     # c.drawString(310, 425, "Net Wt.     : ")  this value is printed at the end after the total of net wt
#     # c.drawString(380, 268, ": " + str(result['WEIGHTUNIT']))
#     unit=result['WEIGHTUNIT']
#     c.drawString(265, 256, "Shade No/ Shade" )
#
#     shadecode=result['SHADECODE']
#     sa = 256
#     if len(str(shadecode)) > 50:
#         c.drawString(340, sa, ": " )
#         lines = textwrap.wrap(str(shadecode), 50, break_long_words=False)
#         for i in lines:
#             # c.drawString(345, sa, str(i))
#             sa = sa - 12
#     else:
#         # c.drawString(340, 256, ": " + str(result['SHADECODE']))
#         pass
#
#     # c.drawString(265, 244, "extra line" )
#     # c.drawString(340, 244, ": " + str(result['SHADECODE']))
#     #
#     c.drawString(440, 340, "Date")
#     c.drawString(480, 340, ": " + str(result['CHALLANDATE']))
#     c.drawString(440, 328, "LR Date" )
#     c.drawString(480, 328, ": " + str(result['LRDATE']))
#     c.drawString(440, 316, "Desp. To")
#     c.drawString(480, 316, ": "+str(result['DESPTO']))
#     c.drawString(440, 304, "Twist")
#     c.drawString(480, 304, ": "+str(result['TWIST']))
#     # # c.drawString(550, 425, "Boxes : ") this value is printed at the end after the total of boxes
#
#     c.drawString(440, 229, "Ref." )
#     c.drawString(480, 229, ": " + str(result['REFERANCECODE']))
#     printgst_invoice(40,result)
# def signature(d):
#     c.drawCentredString(510, 30, "Authorised Signatory")
# def logic(result):
#     # divisioncode.append(result['UNIT'])
#     divisioncode.append(result['COMPANYNAME'])
#     challanno.append(result['CHALLANNUMBER'])
#     ShadeCode.append(result['SHADECODE'])
#     Lotno.append(result['LOTNO'])
#     # boxno.append(result['BOXNO'])
# def dlocvalue(d):
#     d=d-20
#     return d
# # def newpage(c,result):
# def newpage():
#     global d
#     d = 330
#     # border(c,c,result)
#     return d
# def newrequest():
#     global divisioncode
#     global pageno
#     global challanno
#     global no
#     global boxno
#     global ShadeCode
#     global Lotno
#     global printleft
#     global printright
#     global x
#     global limit
#     global d
#     no=0
#     printleft = 200
#     printright = 200
#     limit = 110
#     d = 200
#     x = 210
#     divisioncode=[]
#     pageno=1
#     challanno=[]
#     boxno=[]
#     ShadeCode=[]
#     Lotno=[]
# def companyclean():
#     global BoxesTotal
#     global WeightTotal
#     BoxesTotal = 0
#     WeightTotal = 0
#
# def textsize(c,result):
#     fonts(9)
#     logic(result)
#     global printleft
#     global printright
#     global limit
#     global d
#     global x
#     global totalnoofchallan
#     global challancounter
#     global pageno
#     totalnoofchallan=result['TOTALNOOFCHALLAN']
#     challancounter = challancounter + 1
#     if len(challanno) == 1:
#         print(challanno)
#         border(c,result)
#         header(result)
#         if d <= printleft and d >= limit:
#             fonts(9)
#             c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
#             d=dvalue()
#             printdetail1(result, d)
#         else:
#             x= xvalue()
#             printdetail2(result,x)
#     elif challanno[-1]== challanno[-2]:
#         if d <= printleft and d >= limit:
#             if len(ShadeCode) == 1:
#                 pass
#             elif ShadeCode[-1] != ShadeCode[-2]:
#                 c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
#             if len(Lotno)==1:
#                 pass
#             elif Lotno[-1]!=Lotno[-2]:
#                 printtotal1(d)
#                 d=dvalue()
#                 c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
#                 d=dvalue()
#             printdetail1(result, d)
#         else:
#             x=xvalue()
#             try:
#                 if len(ShadeCode) == 1:
#                     pass
#                 elif ShadeCode[-1] != ShadeCode[-2]:
#                     c.drawString(30, x, result['SHADECODE'] + '  ' + result['LOTNO'])
#             except:
#                 pass
#             if x<=printleft and x>=limit:
#                 printdetail2(result, x)
#             else:
#                 c.drawString(520, 355, "Page no : " + str(pageno))
#                 p = page()
#                 c.drawString(467, 87, "Continued  on Page No. "+str(p))
#                 c.showPage()
#                 # p = page()
#                 fonts(9)
#                 c.drawString(520, 355, "Page no : " + str(p))
#                 border(c, result)
#                 header(result)
#                 d=200
#                 x=210
#                 # printleft = 200
#                 # printright = 200
#                 printdetail1(result, d)
#     elif challanno[-1]!= challanno[-2]:
#         # global pageno
#         pageno=0
#         # if challancounter == totalnoofchallan:
#         printtotalmain()
#         # else:
#         if d <= printleft and d >= limit:
#             printtotal1(d)
#         else:
#             printtotal2(x)
#
#
#
#         c.showPage()
#         p = page()
#         fonts(9)
#         printleft = 200
#         printright = 200
#         limit = 110
#
#         # c.drawString(520, 355, "Page no : " +str(p))
#         border(c,result)
#         header(result)
#         d = 200
#         x = 200
#
#         if d <= printleft and d >= limit:
#             c.drawString(27, d, result['SHADECODE'] + '  ' + result['LOTNO'])
#             d=dvalue()
#             printdetail1(result, d)
#         else:
#             c.drawString(27, x, result['SHADECODE'] + '  ' + result['LOTNO'])
#             x=xvalue()
#             printdetail2(result, x)
#
#     # print(challancounter)
#     # print(totalnoofchallan)
#
#     # print("out textsize")
#
# def border(c, result):
#     # print("from border")
#     c.setFillColorRGB(0, 0, 0)
#     # Box For Whole page
#     fonts(7)
#     c.line(20, 410, 580, 410)  # first horizontal line
#     c.drawString(260, 402, "Subject to Silvassa Jurisdiction.")
#     fonts(15)
#     c.setFillColorRGB(0, 0, 0)
#     c.line(20, 410, 20, 20)  # first vertical line
#     c.line(580, 410, 580, 20)  # right vertical border  line
#     fonts(12)
#     c.drawCentredString(310, 355, "DELIVERY CHALLAN")
#     # c.drawString(545,355,"Page no : "+page())
#     c.line(20, 350, 580, 350)  # second horizontal line
#     fonts(8)
#     c.line(260, 238, 260, 350)  # center vertical line  short line for address and header deatils  |
#     c.drawString(25, 340, "To,")
#     c.drawString(25, 229, "PLEASE RECEIVE THE FOLLOWING GOODS IN ORDER & CONDITION AS PER YOUR ORDER NO.")
#     c.line(20, 238, 580, 238)  # third horizontal line
#     c.line(20, 225, 580, 225)  # fourth horizontal line
#     c.line(20, 100, 580, 100)
#     c.drawString(50, 215, "Box No.")
#     c.line(105, 225, 105, 100)
#     c.drawString(115, 215, "Cops")
#     c.line(140, 225, 140, 100)
#     c.drawString(150, 215, "Gross Wt.")
#     c.line(195, 225, 195, 100)
#     c.drawString(200, 215, "Tare Wt.")
#     c.line(238, 225, 238, 100)
#     c.drawString(255, 215, "Net Wt.")
#     c.line(290, 225, 290, 83)
#     c.drawString(315, 215, "Box No.")
#     c.line(370, 225, 370, 83)
#     c.drawString(380, 215, "Cops")
#     c.line(405, 225, 405, 83)
#     c.drawString(415, 215, "Gross Wt.")
#     c.line(455, 225, 455, 83)
#     c.drawString(465, 215, "Tare Wt.")
#     c.line(510, 225, 510, 83)
#     c.drawString(520, 215, "Net Wt.")
#     c.line(20, 210, 580, 210)  # fifth horizontal line
#     c.drawString(25,90,"CAUTION : - Please do not mix this lot(Goods) with any other lot. Any")
#     c.drawString(25,80,"complaint regarding the quality and weight of yern must be made within")
#     note = "seven days after receipt of the goods. The complaint received thereafter will not entertained. Our responsibility regarding the Quality of yarn ceases once the goods are convertedinto cloth."
#     if len(str(note)) > 95:
#         t = 70
#         lines = textwrap.wrap(str(note), 95, break_long_words=False)
#         for i in lines:
#             c.drawString(25, t, str(i))
#             t = t - 10
#     c.drawAlignedString(367, 87, "Total")
#     c.line(290, 83, 580, 83)  # horizantal line after total
#     signature(90)
#     c.line(20, 20, 580, 20)  # last vertical line
#
# def printgst_invoice(d,result):
#     c.drawString(25, 30, "GOODS CLEARED UNDER GST INVOICE No. " + str(result['PLANTINVOICENO'])+" Dated "+str(result['PLANTINVOICEDATE']))
#
# def printdetail1(result, d):
#     c.drawAlignedString(100, d, result['BOXNO'])
#     c.drawAlignedString(134, d, str(("%.0f" % float(result['COPS']))))
#     c.drawAlignedString(175, d, str(("%.3f" % float(result['GROSSWT']))))
#     c.drawAlignedString(217, d, str(("%.3f" % float(result['TAREWT']))))
#     c.drawAlignedString(270, d, str(("%.3f" % float(result['NETWT']))))
#     total(result)
# def printdetail2(result, x):
#     c.drawAlignedString(367, x, result['BOXNO'])
#     c.drawAlignedString(400, x, str(("%.0f" % float(result['COPS']))))
#     c.drawAlignedString(435, x, str(("%.3f" % float(result['GROSSWT']))))
#     c.drawAlignedString(487, x, str(("%.3f" % float(result['TAREWT']))))
#     c.drawAlignedString(545, x, str(("%.3f" % float(result['NETWT']))))
#     total(result)
#
# def printlasttotal(d):
#     if d <= printleft and d >= limit:
#         printtotal1(d)
#     else:
#         printtotal2(x)
#
# def printtotalmain():
#     global totalmainGrosswt
#     global totalmainNetwt
#     global totalmainTarewt
#     global totalmainCopswt
#     global BoxCounter
#     global unit
#     c.drawString(385, 87, str(("%.0f" % float(totalmainCopswt))))
#     c.drawAlignedString(435, 87, str(("%.2f" % float(totalmainGrosswt))))
#     c.drawAlignedString(486, 87, str(("%.3f" % float(totalmainTarewt))))
#     c.drawAlignedString(545, 87, str(("%.3f" % float(totalmainNetwt))))
#     fonts(9)
#     c.drawString(265, 268, "Net Wt.")
#
#     c.drawString(340, 268, ": " + str(("%.3f" % float(totalmainNetwt))))
#     c.drawString(380, 268, "   " + unit)
#     c.drawString(440, 268, "Boxes")
#     c.drawString(480, 268, ": " + str(BoxCounter))
#
#     totalmainGrosswt=0
#     totalmainNetwt=0
#     totalmainTarewt=0
#     totalmainCopswt=0
#     BoxCounter=0
#
# def total(result):
#     global Grosswt
#     global Netwt
#     global Tarewt
#     global Copswt
#     global totalmainGrosswt
#     global totalmainNetwt
#     global totalmainTarewt
#     global totalmainCopswt
#     global BoxCounter
#     Grosswt = Grosswt + float("%.2f" % float(result['GROSSWT']))
#     Tarewt = Tarewt + float("%.2f" % float(result['TAREWT']))
#     Netwt = Netwt + float("%.2f" % float(result['NETWT']))
#     Copswt = Copswt + float("%.2f" % float(result['COPS']))
#     totalmainTarewt=totalmainTarewt+float("%.3f" % float(result['TAREWT']))
#     totalmainGrosswt=totalmainGrosswt+float("%.3f" % float(result['GROSSWT']))
#     totalmainNetwt=totalmainNetwt+float("%.3f" % float(result['NETWT']))
#     totalmainCopswt=totalmainCopswt+float("%.3f" % float(result['COPS']))
#     BoxCounter=BoxCounter+1
#
# def printtotal1(d):
#     global Grosswt
#     global Netwt
#     global Tarewt
#     global Copswt
#     c.drawAlignedString(125, d, str(("%.0f" %float(Copswt))))
#     c.drawAlignedString(175, d, str(("%.3f" % float(Grosswt))))
#     c.drawAlignedString(217, d, str(("%.3f" % float(Tarewt))))
#     c.drawAlignedString(270, d, str(("%.3f" % float(Netwt))))
#     Grosswt = 0
#     Tarewt = 0
#     Netwt = 0
#     Copswt=0
# def printtotal2(x):
#     global Grosswt
#     global Netwt
#     global Tarewt
#     global Copswt
#     x=xvalue()
#     c.drawAlignedString(392, x, str(("%.0f" % float(Copswt))))
#     c.drawAlignedString(435, x, str(("%.3f" % float(Grosswt))))
#     c.drawAlignedString(487, x, str(("%.2f" % float(Tarewt))))
#     c.drawAlignedString(545, x, str(("%.3f" % float(Netwt))))
#     Grosswt = 0
#     Tarewt = 0
#     Netwt = 0
#     Copswt=0
#
#
#
#
#
