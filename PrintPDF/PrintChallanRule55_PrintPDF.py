from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import textwrap

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 560
no=0
divisioncode=[]
party=[]
item=[]
challanno=[]
remark=[]

BoxesTotal=0
CopsTotal=0
WeightTotal=0
pageno=0
pan=''

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt, etdt,result, divisioncode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,result, divisioncode[:-1])
        return d

def dvaluegst():
    global d
    d = d + 10
    return d

def header(stdt,etdt,result,divisioncode):
    global pan
    fonts(9)
    c.setFillColorRGB(0, 0, 0)
    # Box For Whole page
    c.line(20, 820, 580, 820)#first horizontal line
    c.line(20,780,580,780)#second horizontal line
    c.line(380,820,380,780)#third vertical line
    c.line(380, 800, 580, 800)  # third horizontal line
    c.line(20,820,20,20)#first vertical line
    c.line(580, 820, 580, 20)#last horizontal line
    c.line(20,20,580,20)#last vertical line
    #(left,up,right,down)
    c.line(20, 220, 580, 220)
    c.drawString(30, 210, "Transporter Name")
    c.drawString(30, 200, "Consignment Note/LR No.")
    c.drawString(30, 190, "Date")
    c.drawString(30, 180, "Vehicle No.")
    c.drawString(30, 170, "Driver Name")
    c.drawString(30, 160, "Receiver Signature")
    c.drawString(30, 150, "Licence No.")
    c.drawString(150, 210, ":")
    c.drawString(150, 200, ":")
    c.drawString(150, 190, ":")
    c.drawString(150, 180, ":")
    c.drawString(150, 170, ":")
    c.drawString(150, 160, ":")
    c.drawString(150, 150, ":")
    c.line(280, 140, 280, 80)
    c.line(20, 140, 580, 140)
    c.line(20,80,580,80)
    c.line(20,35,580,35)
    c.drawString(160,210,str(result['TRANSPORTERNAME1']))
    c.drawString(160,200,str(result['LRNO']))
    if result['LRDATE']!=None:
        c.drawString(160, 190, str(result['LRDATE']))
    c.drawString(160,180,str(result['VEHICLENO']))
    c.drawString(160, 170, str(result['TRUCKDRIVER']))
    c.drawString(160, 150, str(result['TRUCKDRIVERLICENCENO']))
    c.drawString(30,25,"The above document to be generated in triplicate:")
    c.drawString(30,70,"Principal Place of Business of the Supplying State:")
    c.drawString(280, 70, divisioncode[-1])
    if len(str(result['ADDRESS']))>60:
        lines = textwrap.wrap(str(result['ADDRESS']), 60, break_long_words=False)
        d=60
        for i in lines:
            c.drawString(280, d , str(i))
            d=d-10
    else:
        c.drawString(280, 60, str(result['ADDRESS']))
    c.drawString(280, 40, "GSTIN :"+str(result['GSTIN']))
    c.drawString(350, 130, "For "+divisioncode[-1])
    c.drawString(400, 85, "Authorised Signatory")
    c.drawString(30,810,"Challan Issued Under Rule 55")
    c.drawString(390, 810, "ORIGINAL FOR CONSIGNEE")
    c.drawString(390, 790, "DUPLICATE FOR TRANSPORTER ")

def challandata(result):
    c.line(20, 700, 580, 700)  # fourth horizontal line
    c.line(80, 780, 80, 700)  # logo vertical line
    c.line(20, 610, 580, 610)
    c.line(20, 560, 580, 560)

    c.drawString(90, 770, "Supplying Co. Name")
    c.drawString(90, 760, "Supplier full address with State")
    c.drawString(90, 740, "State Code")
    c.drawString(90, 730, "Pin Code")
    c.drawString(90, 720, "Supplier's GSTIN")
    c.drawString(90, 710, "Supplier's PAN")
    c.drawString(380, 730, "Delivery Challan No.")
    c.drawString(380, 720, "Delivery Challan Date")
    c.drawString(220, 770, ":")
    c.drawString(230,770,divisioncode[-1])
    # c.drawString(230,760,str(result['ADDRESS']))
    if len(str(result['ADDRESS']))>60:
        lines = textwrap.wrap(str(result['ADDRESS']), 60, break_long_words=False)
        d=760
        for i in lines:
            c.drawString(230, d , str(i))
            d=d-10
    else:
        c.drawString(230, 760, str(result['ADDRESS']))
    c.drawString(230,740,str(result['STATECODE']))
    c.drawString(230, 730, str(result['PINCODE']))
    c.drawString(230, 720, str(result['GSTIN']))
    c.drawString(230,710,str(result['PAN']))
    c.drawString(480, 730, str(result['CHALLANNO']))
    c.drawString(480, 720, str(result['CHALLANDATE']))
    c.drawString(220, 760, ":")
    c.drawString(220, 740, ":")
    c.drawString(220, 730, ":")
    c.drawString(220, 720, ":")
    c.drawString(220, 710, ":")
    c.drawString(470, 730, ":")
    c.drawString(470, 720, ":")
    c.drawCentredString(300, 690, "Details Of Consignee")
    c.drawString(30, 680, "Name")
    c.drawString(30, 670, "Address")
    c.drawString(30, 660, "State")
    c.drawString(30, 650, "State Code")
    c.drawString(30, 640, "PIN")
    c.drawString(30, 630, "GSTIN/Unique ID")
    c.drawString(30, 620, "PAN")
    c.drawString(120, 680, ":")
    c.drawString(120, 670, ":")
    c.drawString(120, 660, ":")
    c.drawString(120, 650, ":")
    c.drawString(120, 640, ":")
    c.drawString(120, 630, ":")
    c.drawString(120, 620, ":")
    if len(str(result['PARTYNAME'])) > 70:
        c.drawString(130,680,textwrap.wrap(str(result['PARTYNAME']), 70, break_long_words=False)[0])
    else:
        c.drawString(130,680,str(result['PARTYNAME']))
    c.drawString(130, 670, str(result['ADDRESS1']))
    # c.drawString(130, 660, str(result['PARTYNAME']))
    c.drawString(130,650,str(result['PARTYSTATECODE']))
    c.drawString(130, 640, str(result['POSTALCODE']))
    c.drawString(130,630,str(result['PARTYGSTINNUMBER']))
    # c.drawString(130, 620, str(result['PARTYNAME']))



    fonts(12)
    c.drawCentredString(300, 595, "Material sent for Weight Purpose as per Rule 138(14)(N)")
    fonts(9)
    c.line(20, 585, 580, 585)
    c.drawString(30, 575, "Sr.#")
    c.drawString(60, 575, "Description of Goods")
    c.drawString(300, 575, "HSN")
    c.drawString(400, 575, "Quantity")
    c.drawString(400, 565,"Kg.Approx")
    c.drawString(480, 575, "Rate")
    c.drawString(530, 575, "Total (Rs.)")

def data(stdt,etdt,result,d):
    global no
    no = no + 1
    c.drawString(40, d, str(no))
    if result['HSNCD']!=None:
        c.drawString(300, d, result['HSNCD'])
    c.drawString(400, d, str(result['QUANTITY']))
    if len(str(result['ITEM']))>45:
        lines = textwrap.wrap(str(result['ITEM']), 45, break_long_words=False)
        for i in lines:
            c.drawString(60, d, str(i))
            d = dvalue(stdt, etdt, result, divisioncode)
    else:
        c.drawString(60, d, str(result['ITEM']))

    total(result)



def remarks(result,d):
    d = d - 40
    c.drawString(10,d,str(result(['REMARKS'])))

def signature(d):
    d = d-40
    if remark[-1]!=None:
        c.drawString(10, d, str(remark[-1]))
    c.drawCentredString(480, d, "For " + divisioncode[-1])
    c.drawCentredString(480, d-20, "Authorised Signatory")

def GST(result, d):
    fonts(7)
    # c.drawString(400, d, result['PRODUCTCHARGENAME'])
    # c.drawAlignedString(540, d, str(("%.3f" % float(result['PRODUCTCHARGERATE']))))
    # c.drawAlignedString(690, d, str(("%.2f" % float(result['PRODUCTCHARGEAMOUNT']))))
    # GSTTotal(result)

def total(result):
    global WeightTotal
    WeightTotal = WeightTotal + float("%.3f" % float(result['QUANTITY']))


def printtotal(stdt,etdt,result,d):
    fonts(9)
    c.line(20, d, 580, d)
    global WeightTotal
    d=dvalue(stdt,etdt,result,divisioncode)
    c.drawString(400, d, str(("%.3f" % float(WeightTotal))))
    WeightTotal = 0
    c.drawString(300, d, "TOTAL:")
    d = dvalue(stdt, etdt, result, divisioncode)
    c.line(20, d, 580, d)
    d = dvalue(stdt, etdt, result, divisioncode)
    c.drawString(30, d,"Total Challan  Value in Rs.  (In Figures) : ")
    d = dvalue(stdt, etdt, result, divisioncode)
    c.drawString(30, d, "Total Challan  Value in Rs. (In Words) : ")
    d = dvalue(stdt, etdt, result, divisioncode)
    if remark[-1] != None:
        c.drawString(30, d, str(remark[-1]))

def logic(result):
    divisioncode.append(result['UNIT'])
    challanno.append(result['CHALLANNO'])
    remark.append(result['REMARKS'])

    # item.append(result['ITEM'])
    # id.append(result['ID'])

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    d = 550
    return d

def newrequest():
    global divisioncode
    global pageno
    global challanno
    global no
    no=0
    divisioncode=[]
    pageno=0
    challanno=[]


def companyclean():
    global BoxesTotal
    global WeightTotal
    BoxesTotal = 0
    WeightTotal = 0

def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt, etdt,result, divisioncode)
    logic(result)
    global no
    if len(challanno) == 1:
            header(stdt,etdt,result,divisioncode)
            challandata(result)
            data(stdt,etdt,result,d)
                # d = dvalue(stdt, etdt,result, divisioncode)
                # LowerLineData(result, d)
                # d = dvalue(stdt, etdt,result, divisioncode)
                # GST(result, d)



    elif challanno[-1] == challanno[-2]:
        data(stdt,etdt,result, d)


    elif challanno[-1] != challanno[-2]:
        #challandata()
        printtotal(stdt,etdt,result,d)
        #d = dvalue(stdt, etdt, result, divisioncode)
        #signature(d)
        # companyclean()
        no = 0
        c.showPage()
        d=newpage()
        header(stdt, etdt, result, divisioncode)
        data(stdt,etdt,result, d)
        challandata(result)
