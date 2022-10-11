from glob import glob
from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from Global_Files import Connection_String as con

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))
d = 740

divisioncode=[]
costcenter=[]
item=[]
challantype=[]

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
    fonts(16)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(600, 820, divisioncode[-1])
    
    fonts(14)
    c.drawCentredString(600, 800, "Excise Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))

    p=page()
    c.drawString(1080,800,"Page No."+str(p))
    c.line(0, 790, 1200, 790)
    c.line(0, 750, 1200, 750)
    fonts(8)
    c.drawString(10, 765, "Inv.No.")
    c.drawString(60, 765, "ChallanNo.")
    c.drawString(140, 765, "Inv.Date")
    c.drawString(210, 765, "QTY")
    c.drawString(270, 765, "Party Name")
    c.drawString(400, 765, "GST No.")
    c.drawString(470, 765, "Rate")
    c.drawString(540, 765, "Assessbl")
    c.drawString(630, 765, "Freight")
    c.drawString(700, 765, "Insaurance")
    c.drawString(770, 765, "Oth.Chrgs.")
    c.drawString(840, 765, "IGST")
    c.drawString(880, 765, "CGST")
    c.drawString(930, 765, "UTGST")
    c.drawString(980, 765, "Total GST")
    c.drawString(1040, 765, "Inv Amt")
    c.drawString(1080, 765, "Tax Value")
    c.drawString(1130, 765, "TCS Amt")
  

def data(result,d):
    fonts(8)
    # Upperline in data
    c.drawString(10, d, str(result['INVNO']))
    c.drawString(60, d, str(result['CHALLANNO']))
    c.drawString(140, d, str(result['INVDATE'].strftime('%d-%m-%Y')))
    c.drawString(210, d, str(result['QTY']))
    c.drawString(270, d, str(result['PARTY']))
    c.drawString(400, d, str(result['GSTNO']))
    c.drawString(470, d, str(result['RATE']))
    c.drawString(540, d, str(result['ASSAMT']))
    c.drawString(630, d, str(result['FRT']))
    c.drawString(700, d, str(result['INS']))
    c.drawString(770, d, str(result['OTHCH']))
    c.drawString(840, d, str(result['IGST']))
    c.drawString(880, d, str(result['CGST']))
    c.drawString(930, d, str(result['UTGST']))
    c.drawString(980, d, str(result['GST']))
    c.drawString(1040, d, str(result['INVAMT']))
    c.drawString(1080, d, str(result['TCS']))
    c.drawString(1130, d, str(result['TCS']))
    total(result)
    # c.drawString(65, d, result['costcenter'])
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
    
    global Qty
    global Assessbl
    global Freight
    global Insaurance
    global OtherCharges
    global Igst
    global Cgst
    global UTgst
    global TotalGST
    global InvAmt
    global TaxValue
    global TCSAmt
    if result['QTY']!=None:
        Qty=Qty+(float("%.2f"%float(result['QTY'])))     
    elif result['ASSAMT']!=None:
        Assessbl=Assessbl+(float("%.3f"%float(result['ASSAMT'])))     
    elif result['FRT']!=None:
        Freight=Freight+(float("%.3f"%float(result['FRT'])))    
    elif result['INS']!=None:
        Insaurance=Insaurance+(float("%.2f"%float(result['INS'])))
    elif result['OTHCH']!=None:
        OtherCharges=OtherCharges+(float("%.2f"%float(result['OTHCH'])))
    elif result['IGST']!=None:
        Igst=Igst+(float("%.2f"%float(result['IGST'])))
    elif result['CGST']!=None:
        Cgst=Cgst+(float("%.2f"%float(result['CGST'])))
    elif result['UTGST']!=None:
        UTgst=UTgst+(float("%.2f"%float(result['UTGST'])))
    elif result['GST']!=None:
        TotalGST=TotalGST+(float("%.2f"%float(result['GST'])))
    elif result['INVAMT']!=None:
        InvAmt=InvAmt+(float("%.2f"%float(result['INVAMT'])))
    elif result['TCS']!=None:
        TCSAmt=TCSAmt+(float("%.2f"%float(result['TCS'])))
    
def totalprint(d):
    global Qty
    global Assessbl
    global Freight
    global Insaurance
    global OtherCharges
    global Igst
    global Cgst
    global UTgst
    global TotalGST
    global InvAmt
    global TaxValue
    global TCSAmt

    c.drawString(10,d,"Chintan")
    c.drawString(210,d,str(Qty))
    c.drawString(540,d,str(Assessbl))
    c.drawString(630,d,str(Freight))
    c.drawString(700,d,str(Insaurance))
    c.drawString(770,d,str(OtherCharges))
    c.drawString(840,d,str(Igst))
    c.drawString(880,d,str(Cgst))
    c.drawString(930,d,str(UTgst))
    c.drawString(980,d,str(TotalGST))
    c.drawString(1040,d,str(InvAmt))
    c.drawString(1130,d,str(TCSAmt))
    
    
    
    # TaxValue=TaxValue+(float("%.2f"%float(result['TCAMT'])))
    

    # global CompanyQuentityTotal
    # global CompanyAmountTotal
    # CompanyQuentityTotal = CompanyQuentityTotal + (float("%.3f" % float(result['QUANTITY'])))
    # CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['BILLAMOUNT'])))

# def itemtotal(result):
#     global ItemAmountTotal
#     ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))

def GSTTotal(result):
    global ChargesTotal
    ChargesTotal = ChargesTotal + (float("%.2f" % float(result['PRODUCTCHARGEAMOUNT'])))

def logic(result):
    divisioncode.append(result['COMPANY'])
    costcenter.append(result['COST'])
    challantype.append(result['CHALT'])

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    
    global d
    d = 740
  
    return d

def newrequest():
    global divisioncode
    global pageno
    global costcenter
    divisioncode=[]
    pageno=0
    costcenter=[]


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

    pageno =0
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

def textsize(result, d, stdt, etdt):
    d=dvalue()
    logic(result)
    if len(divisioncode) == 1:
        if len(costcenter) == 1:
                header(stdt,etdt,divisioncode)
                c.drawString(10,d,costcenter[-1])
                d = dvalue()
                c.drawString(10,d,challantype[-1])
                d = dvalue()
                data(result, d)
                

    elif divisioncode[-1] == divisioncode[-2]:
        if costcenter[-1] == costcenter[-2]:
            if challantype[-1] == challantype[-2]:
                data(result, d)
            elif challantype[-1] != challantype[-2]:
                c.drawString(10, d, str(challantype[-1]))
                d = dvalue()
                data(result, d)
                

        elif costcenter[-1] != costcenter[-2]:
            c.drawString(10, d, str(costcenter[-1]))
            d = dvalue()
            if challantype[-1] == challantype[-2]:
                data(result,d)
             
            elif challantype[-1] != challantype[-2]:
                c.drawString(10, d, str(challantype[-1]))
                d = dvalue()
                data(result, d)
                

    elif divisioncode[-1] != divisioncode[-2]:
            fonts(7)
            c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            d=dvalue()
            totalprint(d)
            c.setPageSize(landscape(A3))
            c.showPage()

            header(stdt, etdt, divisioncode)
            d=newpage()
            d=dvalue()
            if costcenter[-1] == costcenter[-2]:
                if challantype[-1] == challantype[-2]:
                    pass
                    
                elif challantype[-1] != challantype[-2]:
                    LowerLineData(result, d)
                    d = dvalue()
                    

            elif costcenter[-1] != costcenter[-2]:
                data(result, d)
                d = dvalue()
                if challantype[-1] == challantype[-2]:
                    pass
                elif challantype[-1] != challantype[-2]:
                    LowerLineData(result, d)
                    d = dvalue()