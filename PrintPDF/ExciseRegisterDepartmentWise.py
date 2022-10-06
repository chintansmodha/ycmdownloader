from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from Global_Files import Connection_String as con

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))
d = 680

divisioncode=[]
finno=[]
item=[]
id=[]

pageno=0
Qty=0
Assessbl=0
Freight=0
Insaurance=0
OtherCharges=0
Igst=0
Cgst=0
UTgst=0
TotalGST=0
InvAmt=0
TaxValue=0
TCSAmt=0

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
    c.drawCentredString(400, 780, divisioncode[-1])
    
    fonts(9)
    c.drawCentredString(400, 530, "Excise Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))

    p=page()
    c.drawString(780,530,"Page No."+str(p))
    c.line(0, 520, 850, 520)
    c.line(0, 480, 850, 480)
 
    c.drawString(10, 520, "Inv.No.")
    c.drawString(70, 520, "ChallanNo.")
    c.drawString(70, 510, "Inv.Date")
    c.drawString(110, 520, "QTY")
    c.drawString(120, 510, "Party Name")
    c.drawString(150, 520, "GST No.")
    c.drawString(375, 520, "Rate")
    c.drawString(365, 510, "Assessbl")
    c.drawString(422, 520, "Freight")
    c.drawString(422, 510, "  Insaurance")
    c.drawString(480, 520, "Othr Charges")
    c.drawString(480, 510, "IGST")
    c.drawString(535, 520, "CGST")
    c.drawString(535, 510, "UTGST")
    c.drawString(580, 520, "Total GST")
    c.drawString(580, 510, "Inv Amt")
    c.drawString(620, 520, "Tax Value")
    c.drawString(620, 510, "TCS Amt")
  

def data(result,d):
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(result['INVNO']))
    # c.drawString(65, d, result['FINNO'])
    # c.drawString(110, d, str(result['BILLDATE'].strftime('%d-%m-%Y')))
    # c.drawString(160, d, result['BILLNO'])
    # c.drawString(530, d, result['SUPPLIER'])
    # c.drawAlignedString(750, d, str(("%.2f" % float(result['BILLAMOUNT']))))

def LowerLineData(result,d):
    # Lowerline in data
    fonts(7)
    # c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))
    # c.drawString(65, d, result['MRNNO'])
    # c.drawString(110, d, result['ITEM'])
    # c.drawAlignedString(540, d, str(("%.3f" % float(result['RATE']))))
    # c.drawAlignedString(610, d, str(("%.3f" % float(result['QUANTITY']))))
    # c.drawAlignedString(690, d, str(("%.2f" % float(result['BASICVALUE']))))
    # # c.drawString(720, d, result['PRODUCTGLACCOUNT'])
    # itemtotal(result)


def total(result):
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = CompanyQuentityTotal + (float("%.3f" % float(result['QUANTITY'])))
    CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['BILLAMOUNT'])))

def itemtotal(result):
    global ItemAmountTotal
    ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))

def GSTTotal(result):
    global ChargesTotal
    ChargesTotal = ChargesTotal + (float("%.2f" % float(result['PRODUCTCHARGEAMOUNT'])))

def logic(result):
    divisioncode.append(result['COMPANY'])
    finno.append(result['COST'])
    # item.append(result['ITEM'])
    id.append(result['CHALT'])

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    d = 680
    return d

def newrequest():
    global divisioncode
    global pageno
    global finno
    divisioncode=[]
    pageno=0
    finno=[]


def companyclean():

    global pageno
    global Qty
    global Assessbl
    global Freight
    global Insaurance
    global  OtherCharges
    global Igst
    global Cgst
    global UTgst
    global  TotalGST
    global InvAmt
    global TaxValue
    global TCSAmt

    pageno=0
    Qty=0
    Assessbl=0
    Freight=0
    Insaurance=0
    OtherCharges=0
    Igst=0
    Cgst=0
    UTgst=0
    TotalGST=0
    InvAmt=0
    TaxValue=0
    TCSAmt=0

def textsize(c, result, d, stdt, etdt):
    d=dvalue()
    logic(result)
    if len(divisioncode) == 1:
        if len(finno) == 1:
                header(stdt,etdt,divisioncode)
                data(result, d)
                d = dvalue()
                LowerLineData(result, d)
                d = dvalue()
                # total(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if finno[-1] == finno[-2]:
            if id[-1] == id[-2]:
                pass
            elif id[-1] != id[-2]:
                LowerLineData(result, d)
                d = dvalue()
                

        elif finno[-1] != finno[-2]:
            data(result, d)
            d = dvalue()
            # total(result)
            if id[-1] == id[-2]:
                pass
            elif id[-1] != id[-2]:
                LowerLineData(result, d)
                d = dvalue()
                

    elif divisioncode[-1] != divisioncode[-2]:
            fonts(7)
            c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            # c.drawString(490, d, "Basic Value Total : "+str("%.2f" % float(ItemAmountTotal)))
            # c.drawAlignedString(750, d, str("%.2f" % float(CompanyAmountTotal)))
            # d=dvalue()
            # c.drawString(490, d, "Charges Total : "+str("%.2f" % float(ChargesTotal)))
            companyclean()
            c.setPageSize(landscape(A3))
            c.showPage()

            header(stdt, etdt, divisioncode)
            d=newpage()
            d=dvalue()
            if finno[-1] == finno[-2]:
                if id[-1] == id[-2]:
                    pass
                    
                elif id[-1] != id[-2]:
                    LowerLineData(result, d)
                    d = dvalue()
                    

            elif finno[-1] != finno[-2]:
                data(result, d)
                d = dvalue()
                # total(result)
                if id[-1] == id[-2]:
                    pass
                elif id[-1] != id[-2]:
                    LowerLineData(result, d)
                    d = dvalue()