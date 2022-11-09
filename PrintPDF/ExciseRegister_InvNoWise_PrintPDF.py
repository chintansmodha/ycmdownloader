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

def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(landscape(A3))
        c.showPage()
        header(stdt, etdt, divisioncode)
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
    fonts(10)
    c.drawString(20, 765, "Inv.No.")
    c.drawString(100, 765, "ChallanNo.")
    c.drawString(180, 765, "Inv.Date")
    c.drawString(270, 765, "QTY")
    # c.drawString(270, 765, "Party Name")
    # c.drawString(400, 765, "GST No.")
    c.drawString(350, 765, "Rate")
    c.drawString(420, 765, "Assessbl")
    c.drawString(510, 765, "Freight")
    c.drawString(580, 765, "Insaurance")
    c.drawString(650, 765, "Oth.Chrgs.")
    c.drawString(720, 765, "IGST")
    c.drawString(760, 765, "CGST")
    c.drawString(810, 765, "UTGST")
    c.drawString(860, 765, "Total GST")
    c.drawString(920, 765, "Inv Amt")
    # c.drawString(1080, 765, "Tax Value")
    c.drawString(1010, 765, "TCS Amt")
  

def data(result,d):
    fonts(10)
    # Upperline in data
    if result['INVNO']!=None:
        c.drawString(10, d, str(result['INVNO']))
    if result['CHALLANNO']!=None:
        c.drawString(100, d, str(result['CHALLANNO']))
    if result['INVDATE']!=None:
        c.drawString(180, d, str(result['INVDATE'].strftime('%d-%m-%Y')))
    if result['QTY']!=None:
        c.drawAlignedString(280, d, str(result['QTY']))
    # if result['PARTY']!=None:
    #     c.drawAlignedString(270, d, str(result['PARTY'])[:25])
    # if result['GSTNO']!=None:
    #     c.drawAlignedString(400, d, str(result['GSTNO']))
    if result['RATE']!=None:
        c.drawAlignedString(360, d, str(result['RATE']))
    if result['ASSAMT']!=None:
        c.drawAlignedString(440, d, str(result['ASSAMT']))
    if result['FRT']!=None:
        c.drawAlignedString(530, d, str(result['FRT']))
    if result['INS']!=None:
        c.drawAlignedString(600, d, str(result['INS']))
    if result['OTHCH']!=None:
        c.drawAlignedString(670, d, str(result['OTHCH']))
    if result['IGST']!=None:
        c.drawAlignedString(740, d, str(result['IGST']))
    if result['CGST']!=None:
        c.drawAlignedString(780, d, str(result['CGST']))
    if result['UTGST']!=None:
        c.drawAlignedString(830, d, str(result['UTGST']))
    if result['GST']!=None:
        c.drawAlignedString(880, d, str(result['GST']))
    if result['INVAMT']!=None:
        c.drawAlignedString(940, d, str(result['INVAMT']))
    
    c.drawAlignedString(980, d, " ")
    if result['TCS']!=None:
        c.drawAlignedString(1030, d, str(result['TCS']))
        
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
    if result['ASSAMT']!=None:
        Assessbl=Assessbl+(float("%.3f"%float(result['ASSAMT'])))     
    if result['FRT']!=None:
        Freight=Freight+(float("%.3f"%float(result['FRT'])))    
    if result['INS']!=None:
        Insaurance=Insaurance+(float("%.2f"%float(result['INS'])))
    if result['OTHCH']!=None:
        OtherCharges=OtherCharges+(float("%.2f"%float(result['OTHCH'])))
    if result['IGST']!=None:
        Igst=Igst+(float("%.2f"%float(result['IGST'])))
    if result['CGST']!=None:
        Cgst=Cgst+(float("%.2f"%float(result['CGST'])))
    if result['UTGST']!=None:
        UTgst=UTgst+(float("%.2f"%float(result['UTGST'])))
    if result['GST']!=None:
        TotalGST=TotalGST+(float("%.2f"%float(result['GST'])))
    if result['INVAMT']!=None:
        InvAmt=InvAmt+(float("%.2f"%float(result['INVAMT'])))
    if result['TCS']!=None:
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

    
    c.drawAlignedString(230,d,str(round(Qty,3)))
    c.drawAlignedString(560,d,str(Assessbl))
    c.drawAlignedString(650,d,str(Freight))
    c.drawAlignedString(720,d,str(Insaurance))
    c.drawAlignedString(790,d,str(OtherCharges))
    c.drawAlignedString(860,d,str(Igst))
    c.drawAlignedString(900,d,str(Cgst))
    c.drawAlignedString(950,d,str(UTgst))
    c.drawAlignedString(1000,d,str(TotalGST))
    c.drawAlignedString(1060,d,str(InvAmt))
    c.drawAlignedString(1150,d,str(TCSAmt))
    
    
    
    # TaxValue=TaxValue+(float("%.2f"%float(result['TCAMT'])))
    

    # global CompanyQuentityTotal
    # global CompanyAmountTotal
    # CompanyQuentityTotal = CompanyQuentityTotal + (float("%.3f" % float(result['QUANTITY'])))
    # CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['BILLAMOUNT'])))

# def itemtotal(result):
#     global ItemAmountTotal
#     ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))


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
    global challantype
    divisioncode=[]
    pageno=0
    costcenter=[]
    challantype=[]


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
    global TotalGST
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
    d=dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        if len(costcenter) == 1:
                header(stdt,etdt,divisioncode)
                c.drawString(10,d,costcenter[-1])
                d = dvalue(stdt, etdt, divisioncode)
                c.drawString(10,d,challantype[-1])
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
                

    elif divisioncode[-1] == divisioncode[-2]:
        if costcenter[-1] == costcenter[-2]:
            if challantype[-1] == challantype[-2]:
                data(result, d)
            elif challantype[-1] != challantype[-2]:
                c.drawString(10, d, str(challantype[-1]))
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
                

        elif costcenter[-1] != costcenter[-2]:
            c.drawString(10, d, str(costcenter[-1]))
            d = dvalue(stdt, etdt, divisioncode)
            if challantype[-1] == challantype[-2]:
                data(result,d)
             
            elif challantype[-1] != challantype[-2]:
                c.drawString(10, d, str(challantype[-1]))
                d = dvalue(stdt, etdt, divisioncode)
                data(result, d)
                

    elif divisioncode[-1] != divisioncode[-2]:
            fonts(7)
            c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            d=dvalue(stdt, etdt, divisioncode)
            totalprint(d)
            c.setPageSize(landscape(A3))
            c.showPage()

            header(stdt, etdt, divisioncode)
            d=newpage()
            d=dvalue(stdt, etdt, divisioncode)
            data(result,d)
           