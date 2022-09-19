import textwrap

# from reportlab.lib.pagesizes import landscape, A4
# from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib.pagesizes import landscape, A2
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
from datetime import date


pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
# c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
# c.setPageSize(landscape(A3))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A2)))
c.setPageSize(landscape(A2))
d = 990
ca=0
companyname=[]
divisioncode=[]
departmentname=[]
boxno=[]
product=[]
agent=[]
palletnamelist=[]
newpalletnamelist=[]
customer=[]
itemcount=[]
CompanyQuentityTotal=0
CompanyAmountTotal=0
pageno=0
totalquantity=0
totalprice=0
totalagentquantity=0
totalagentprice=0

lsshadename=''

depttotalcops=0
depttotalgrosswt=0
depttotalterawt=0
depttotalnetwt=0
depttotalpallet=0
deptpallettotal=0

totalgrosswt=0
totalterawt=0
totalnetwt=0

totaldepartmentquentity=0
totaldepartmentagent=0
totaldepartmentprice=0
totalbox=0
totalcops=0
totalcompanyquantity=0
totalcompanyprice=0

totaldisplaypointer=0

nextpallet=0
pallet1=0
pallet2=0
pallet3=0
pallet4=0
pallet5=0
pallet6=0
pallet7=0
pallet8=0
pallettotallist=[]

pflag1=0
pflag2=0
pflag3=0
pflag4=0
pflag5=0
pflag6=0
pflag7=0
pflag8=0

rowhorizantalpallettotal=0
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

def dvalue20():
    global d
    d=d-20
    return d
# def checkend():
#     global d
#     if d > 40:
#         d = d - 10
#         return d
#     else:
#         d = newpage()
#         c.showPage()
#         header(stdt, etdt, divisioncode[:-1])
#         return d

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    # d = 480
    d = 990
    return d

def newrequest():
    global divisioncode
    global pageno
    global product
    global rowhorizantalpallettotal
    global companyname
    global boxno
    global palletnamelist
    # global warehouse
    divisioncode=[]
    boxno=[]
    product=[]
    companyname=[]
    # palletnamelist=[]
    pageno=0
    global d
    d=990
    rowhorizantalpallettotal=0
    # warehouse=[]
    product=0

def logic(result):
    departmentname.append(result['DEPARTMENT'])
    companyname.append(result['COMPNAME'])
    boxno.append(result['BOXNO'])
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

def palletlist(result):
    palletnamelist.append(result['PALLETNAME'])
    # print("pallet added in the list ")

def printdepartment(result,d):
    c.drawString(10, d, result['DEPARTMENT'])

def header(stdt,etdt,divisioncode):
    global d
    global ca
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # c.drawString(10, 1170, "Page type: A2 ")
    c.drawCentredString(300, 1100, departmentname[-1])
    fonts(9)
    c.drawCentredString(300  , 1090-8    , "Challan  Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    # p=page()
    # c.drawString(530,790-8,"Page No."+str(p))
    # c.line(0, 770, 600, 770)  this line is now drawn from the textsize funstion
    # c.line(0, 500, 600, 500)  this line is now drawn from the textsize function
    #Upperline in header
    c.drawString(10, 1060, "Box No.")
    c.drawString(90, 1060, "Date")
    c.drawString(145, 1060, "Lot No")
    c.drawString(210, 1060, "Item")
    c.drawString(210, 1060-10, "Shade")
    c.drawString(420, 1060, "Cops")
    c.drawString(450, 1060, "Gross Wt")
    c.drawString(500, 1060, "Tera. Wt")
    c.drawString(540, 1060, "Net. Wt")
    printpalletlist()
    # d=ca-15
    # c.drawString(590, d, "d= "+str(d))

def printpalletlist ():
    global ca
    global nextpallet
    global totaldisplaypointer
    counter=0
    nextpallet=10
    pointer=570
    lessercounter=0
    lesser=0
    while counter!= len(palletnamelist):
        palletname = palletnamelist[counter]
        # print("palletname: "+str(palletname))
        ca = 1060
        # lesser = ca
        if len(str(palletname)) > 10:
            lines = textwrap.wrap(str(palletname), 10, break_long_words=False)
            for i in lines:
                c.drawString(pointer+nextpallet, ca, str(i))
                ca = ca - 12
        else:
            c.drawString(pointer + nextpallet, ca, str(palletname))
        # c.drawAlignedString(pointer+nextpallet+50,d,str(pointer+nextpallet+50))
        counter=counter+1
        nextpallet=nextpallet+70
    c.drawString(pointer + nextpallet+20, 1060, "Total")
    totaldisplaypointer=pointer + nextpallet+50
    p = page()
    c.drawString(totaldisplaypointer, 1060 - 8, "Page No." + str(p))
    c.line(0, 1070, totaldisplaypointer+50, 1070)
    c.line(0, 1000, totaldisplaypointer+50, 1000)

def textsize(c,result,stdt,etdt):
    global d
    fonts(9)
    logic(result)

    if d<40:
        d = newpage()
        # c.setPageSize(landscape(A3))
        c.setPageSize(landscape(A2))
        c.showPage()
        header(stdt, etdt, divisioncode)

    if len(departmentname) == 1:
        header(stdt,etdt,divisioncode)
        # print("boxno : "+str(result['BOXNO']))
        printdetail(result)

        # d=dvalue()
    elif departmentname[-1]==departmentname[-2]:
        printdetail(result)
    elif departmentname[-1]!=departmentname[-2]:
        c.drawAlignedString(totaldisplaypointer, d, str(("%.0f" % float(rowhorizantalpallettotal))))
        d=dvalue()
        printpallettotal()
        printdepertmenttotal()
        # d=480
        # c.setPageSize(landscape(A3))
        c.setPageSize(landscape(A2))
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode)
        printdetail(result)

def printdetail(result):
    global d
    global totalbox
    global rowhorizantalpallettotal
    global lsshadename
    try:

        if len(boxno)==1:
            lsshadename=result['SHADENAME']
            c.drawString(10, d, result['BOXNO'])
            c.drawString(90, d, result['ENTRYDATE'].strftime('%d-%m-%Y'))
            c.drawString(145, d, result['LOTNO'])
            c.drawString(210, d, result['PRODUCT'])
            #c.drawString(210, d - 10, result['SHADENAME'])

            c.drawAlignedString(440, d, str(("%.0f" % float(result['COPS']))))
            c.drawAlignedString(470, d, str(("%.3f" % float(result['GROSSWT']))))
            c.drawAlignedString(515, d, str(("%.3f" % float(result['TAREWT']))))
            c.drawAlignedString(565, d, str(("%.3f" % float(result['NETWT']))))
            totalbox = totalbox + 1
            # printpalletdetails(d, result)
            # itemname = result['PRODUCT']
            # ia = d
            # sa = d
            # if len(str(itemname)) > 15:
            #     lines = textwrap.wrap(str(itemname), 15, break_long_words=False)
            #     for i in lines:
            #         c.drawString(180, ia, str(i))
            #         # c.drawString(60 + printing, 505, palletnamelist[counter])
            #         ia = ia - 10
            # shadename = result['SHADENAME']
            # # sa = d
            # if len(str(shadename)) > 15:
            #     lines = textwrap.wrap(str(shadename), 15, break_long_words=False)
            #     for i in lines:
            #         c.drawString(330, sa, str(i))
            #         # c.drawString(60 + printing, 505, palletnamelist[counter])
            #         sa = sa - 10
            #     # d = dvalue()
            total(result)

            printpalletdetails(result)
            # d=dvalue20()
            # d = dvalue()
            # c.drawString(210, d , result['SHADENAME'])
            # d = dvalue()

        elif boxno[-1] != boxno[-2]:
            lsshadename = result['SHADENAME']
            # c.drawString(totaldisplaypointer-100,d,"box chang")
            if departmentname[-1]==departmentname[-2]:
                c.drawAlignedString(totaldisplaypointer, d, str(("%.0f" % float(rowhorizantalpallettotal))))
                # d=dvalue()
                # c.drawString(210, d-10 , result['SHADENAME'])
                # d=d-10
            rowhorizantalpallettotal=0
            d=dvalue()
            c.drawString(10, d, result['BOXNO'])
            c.drawString(90, d, result['ENTRYDATE'].strftime('%d-%m-%Y'))
            # c.drawString(80, d, result['ENTRYDATE'])
            c.drawString(145, d, result['LOTNO'])
            c.drawString(210, d, result['PRODUCT'])
            # c.drawString(210, d-10, result['SHADENAME'])
            c.drawAlignedString(440, d, str(("%.0f" % float(result['COPS']))))
            c.drawAlignedString(470, d, str(("%.3f" % float(result['GROSSWT']))))
            c.drawAlignedString(515, d, str(("%.3f" % float(result['TAREWT']))))
            c.drawAlignedString(565, d, str(("%.3f" % float(result['NETWT']))))
            totalbox = totalbox + 1
            printpalletdetails( result)
            # d = dvalue20()

            # c.drawString(210, d, result['SHADENAME'])

            # itemname = result['PRODUCT']
            # ia = d
            # sa = d
            # if len(str(itemname)) > 15:
            #     lines = textwrap.wrap(str(itemname), 15, break_long_words=False)
            #     for i in lines:
            #         c.drawString(180, ia, str(i))
            #         # c.drawString(60 + printing, 505, palletnamelist[counter])
            #         ia = ia - 10
            # shadename = result['SHADENAME']
            # # sa = d
            # if len(str(shadename)) > 15:
            #     lines = textwrap.wrap(str(shadename), 15, break_long_words=False)
            #     for i in lines:
            #         c.drawString(330, sa, str(i))
            #         # c.drawString(60 + printing, 505, palletnamelist[counter])
            #         sa = sa - 10
            #     d = dvalue()
            total(result)
        else:
            pass
            printpalletdetails( result)
            # d=dvalue()
    except:
        print("problem in the print detail function : ")


def printpalletdetails(result):
    global d
    global pallet1
    global pallet2
    global pallet3
    global pallet4
    global pallet5
    global pallet6
    global pallet7
    global pallet8
    # global totalbox
    global nextpallet
    global pflag1
    global pflag2
    global pflag3
    global pflag4
    global pflag5
    global pflag6
    global pflag7
    global pflag8
    global totaldisplaypointer
    global rowhorizantalpallettotal
    hp1=0

    nextpallet = 10
    pointer = 550
    fonts(8)
    # d=dvalue()
    # checkpalletlist(result)
    # global totalquantity
    # global totalagentquantity
    # global totaldepartmentquentity
    # c.drawString(10, d, result['BOXNO'])
    # # c.drawString(70, d, result['CHALLANDATE'].strftime('%d-%m-%Y'))
    # c.drawString(80, d, "12/12/2222")
    # c.drawString(130, d, result['LOTNO'])
    # c.drawString(400, d, str(("%.0f" % float(result['COPS']))))
    # c.drawString(430, d, str(("%.3f" % float(result['GROSSWT']))))
    # c.drawString(470, d, str(("%.3f" % float(result['TAREWT']))))
    # c.drawString(510, d, str(("%.3f" % float(result['NETWT']))))
    # totalbox=totalbox+1
    try:

        if palletnamelist[0]== result['PLTNAME']:
            c.drawAlignedString(630, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet1 = pallet1 + (float("%.0f" % float(result['PLTQTY'])))
            hp1=hp1+(float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal=rowhorizantalpallettotal+hp1
            pflag1=1
        if palletnamelist[1]== result['PLTNAME']:
            c.drawString(700, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet2 = pallet2 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag2=1
        if palletnamelist[2]== result['PLTNAME']:
            c.drawString(770, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet3 = pallet3 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag3=1
        if palletnamelist[3]== result['PLTNAME']:
            c.drawString(840, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet4 = pallet4 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag4=1
        if palletnamelist[4]== result['PLTNAME']:
            c.drawString(910, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet5 = pallet5 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag5=1
        if palletnamelist[5]== result['PLTNAME']:
            c.drawString(980, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet6 = pallet6 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag6=1
        if palletnamelist[6]== result['PLTNAME']:
            c.drawString(1050, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet7 = pallet7 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag7=1
        if palletnamelist[7] == result['PLTNAME']:
            c.drawString(1110, d, str(("%.0f" % float(result['PLTQTY']))))
            pallet8 = pallet8 + (float("%.0f" % float(result['PLTQTY'])))
            hp1 = hp1 + (float("%.0f" % float(result['PLTQTY'])))
            rowhorizantalpallettotal = rowhorizantalpallettotal + hp1
            pflag8 = 1

    except:
        pass


    # itemname = result['PRODUCT']
    # ia = d
    # sa=d
    # if len(str(itemname)) > 15:
    #     lines = textwrap.wrap(str(itemname), 15, break_long_words=False)
    #     for i in lines:
    #         c.drawString(180, ia, str(i))
    #         # c.drawString(60 + printing, 505, palletnamelist[counter])
    #         ia = ia - 10
    # shadename = result['SHADENAME']
    # # sa = d
    # if len(str(shadename)) > 15:
    #         lines = textwrap.wrap(str(shadename), 15, break_long_words=False)
    #         for i in lines:
    #             c.drawString(330, sa, str(i))
    #             # c.drawString(60 + printing, 505, palletnamelist[counter])
    #             sa = sa - 10
    #         d=dvalue()
    # total(result)

def total(result):
    global totalcops
    global totalgrosswt
    global totalterawt
    global totalnetwt
    global totalpallet  #  for the hotizental total at the last of the line
    global pallettotal
    global depttotalcops
    global depttotalgrosswt
    global depttotalterawt
    global depttotalnetwt
    global depttotalpallet
    global deptpallettotal
    depttotalcops = depttotalcops + (float("%.0f" % float(result['COPS'])))
    depttotalgrosswt = depttotalgrosswt + (float("%.3f" % float(result['GROSSWT'])))
    depttotalterawt = depttotalterawt + (float("%.3f" % float(result['TAREWT'])))
    depttotalnetwt = depttotalnetwt + (float("%.3f" % float(result['NETWT'])))

def printpallettotal():
    ca = 760
    counter =0
    nextpallet=10
    pointer = 550
    horizantalpallettotal=0
    global pflag1
    global pflag2
    global pflag3
    global pflag4
    global pflag5
    global pflag6
    global pflag7
    global pflag8
    global d
    # global lsshadename
    d = dvalue()
    if pflag1==1:
        # c.drawString(pointer+nextpallet, d, str(("%.0f" % float(pallet1))))
        c.drawString(620, d, str(("%.0f" % float(pallet1))))
        horizantalpallettotal=horizantalpallettotal+pallet1
    nextpallet = nextpallet + 70
    if pflag2==1:
        c.drawString(695, d, str(("%.0f" % float(pallet2))))
        horizantalpallettotal = horizantalpallettotal + pallet2
    nextpallet = nextpallet + 70
    if pflag3==1:
        c.drawString(760, d, str(("%.0f" % float(pallet3))))
        horizantalpallettotal = horizantalpallettotal + pallet3
    nextpallet = nextpallet + 70
    if pflag4==1:
        c.drawString(835, d, str(("%.0f" % float(pallet4))))
        horizantalpallettotal = horizantalpallettotal + pallet4
    nextpallet = nextpallet + 70
    if pflag5==1:
        c.drawString(910, d, str(("%.0f" % float(pallet5))))
        horizantalpallettotal = horizantalpallettotal + pallet5
    nextpallet = nextpallet + 70
    if pflag6==1:
        c.drawString(975, d, str(("%.0f" % float(pallet6))))
        horizantalpallettotal = horizantalpallettotal + pallet6
    nextpallet = nextpallet + 70
    if pflag7==1:
        c.drawString(1050, d, str(("%.0f" % float(pallet7))))
        horizantalpallettotal = horizantalpallettotal + pallet7
    nextpallet = nextpallet + 70
    if pflag8==1:
        c.drawString(1110, d, str(("%.0f" % float(pallet8))))
        horizantalpallettotal = horizantalpallettotal + pallet8
    nextpallet = nextpallet + 70

    c.drawAlignedString(totaldisplaypointer, d, str(("%.0f" % float(horizantalpallettotal))))



def printdepertmenttotal():
    global d
    global totalbox
    global depttotalcops
    global depttotalgrosswt
    global depttotalterawt
    global depttotalnetwt
    global pallet1
    global pallet2
    global pallet3
    global pallet4
    global pallet5
    global pallet6
    global pallet7
    global pallet8
    # d=dvalue()
    c.drawString(10, d, "Dept Wise Total : ")
    # str(("%.0f" % float(result['PLTQTY']))))
    c.drawString(100, d, str(totalbox))
    c.drawAlignedString(440, d, str(("%.0f" % float(depttotalcops))))
    c.drawAlignedString(470, d, str(("%.3f" % float(depttotalgrosswt))))
    c.drawAlignedString(515, d, str(("%.3f" % float(depttotalterawt))))
    c.drawAlignedString(565, d, str(("%.3f" % float(depttotalnetwt))))

    totalbox=0
    depttotalcops=0
    depttotalgrosswt=0
    depttotalterawt=0
    depttotalnetwt=0
    pallet1=0
    pallet2=0
    pallet3=0
    pallet4=0
    pallet5=0
    pallet6=0
    pallet7=0
    pallet8=0
    rowhorizantalpallettotal=0

def printasttotal():
    c.drawAlignedString(totaldisplaypointer, d, str(("%.0f" % float(rowhorizantalpallettotal))))













