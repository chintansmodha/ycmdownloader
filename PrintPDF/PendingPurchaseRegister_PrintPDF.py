from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
# c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
# c.setPageSize(landscape(A4))
d = 730
divisioncode=[]
product=[]
CompanyQuentityTotal=0
CompanyAmountTotal=0
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

def header(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, "Pending Purchase Order List Register ")
    p=page()
    c.drawString(530,780,"Page No."+str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 730, 600, 730)
    #Upperline in header
    c.drawString(10, 755, "PRODUCTNAME")
    c.drawString(10, 745, "PONO")
    c.drawString(70, 745, "DATE")
    c.drawString(120, 745, "Supplier")
    c.drawString(460, 755, "Purchase Order")
    c.drawString(460, 745, "QUANTITY")
    c.drawString(530, 755, "PENDING ")
    c.drawString(530, 745, "QUANTITY")

    #LowerLine in header
    c.drawString(390, 745, "QUALITYNAME")
    c.drawString(740, 755, "POQUANTITY")




def data(result,d):
    fonts(7)
    total(result)
    logic(result)

    # fonts(7)
    # # Upperline in data
    # c.drawString(10, d, str(result['FINDATE'].strftime('%d-%m-%Y')))

    # c.drawString(110, d, str(result['BILLDATE'].strftime('%d-%m-%Y')))
    # c.drawAlignedString(470, d, result['BILLNO'])
    # c.drawString(500, d, result['SUPPLIER'])
    c.drawString(410, d, result['QUALITYNAME'])
    d = dvalue()
    # # Lowerline in data
    c.drawString(10, d, result['PONO'])
    c.drawString(70, d, str(result['PODATE'].strftime('%d-%m-%Y')))
    c.drawString(120, d, result['SUPPLIER'])
    # c.drawString(320, d, result['QUALITYNAME'])
    c.drawAlignedString(466, d, str(("%.3f" % float(result['POQUANTITY']))))
    c.drawAlignedString(536, d, str(("%.3f" % float(result['PENDINGQUANTITY']))))
    # c.drawAlignedString(740, d, str(("%.2f" % float(result['BASICVALUE']))))


    total(result)

    logic(result)

def GroupByProduct(result,d):
    fonts(7)
    c.drawString(10, d, result['PRODUCTNAME'])

def productname(result, d):
    fonts(7)
    print("productname before pdf : "+str(result['PRODUCTNAME']))
    c.drawString(10, d, "PRODUCTNAME : " + str(result['PRODUCTNAME']))

def total(result):
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = CompanyQuentityTotal + (float("%.3f" % float(result['POQUANTITY'])))
    CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['PENDINGQUANTITY'])))

def logic(result):
    divisioncode.append(result['DIVISIONNAME'])

def dlocvalue(d):
    d=d-20
    return d

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
    global product
    divisioncode=[]
    pageno=0
    product=[]


def textsize(c, result, d, stdt, etdt):
    d=dvalue()
    divisioncode.append(result['DIVISIONNAME'])
    product.append(result['PRODUCTNAME'])
    if len(divisioncode) == 1:
        if len(product)==1:
            if d > 14:
                header(stdt,etdt,divisioncode)
                #itemcodes(result, d)
                data(result, d)
                GroupByProduct(result,d)


    elif divisioncode[-1] == divisioncode[-2]:
        if product[-1]==product[-2]:
            data(result,d)
        elif product[-1]!=product[-2]:
            GroupByProduct(result, d)
            data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
            d=dvalue()
            fonts(7)
            c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            c.drawAlignedString(460, d, str("%.3f" % float(CompanyQuentityTotal)))
            c.drawAlignedString(536, d, str("%.2f" % float(CompanyAmountTotal)))
            companyclean()
            # c.setPageSize(landscape(A4))
            c.showPage()

            header(stdt, etdt, divisioncode)
            d=newpage()
            d=dvalue()
            if product[-1] == product[-2]:
                data(result, d)
            elif product[-1] != product[-2]:
                GroupByProduct(result, d)
                data(result, d)