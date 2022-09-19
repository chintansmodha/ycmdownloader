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
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, str(result['ADDRESS']))
    if result['PAN'] != None:
        pan = str(result['PAN'])
    c.drawCentredString(300, 770, "GSTIN:"+" "+str(result['GSTIN']) +"  "+"STATE CODE:"+" "+  str(result['STATECODE'])+" "+pan)
    c.drawString(250, 750, str("Delivery Challan"))
    c.drawString(10, 720, str("Buyer/Party:"))
    c.drawString(10, 710, str(result['PARTY']))

    if result['ADDRESSLINE1'] != None:
        c.drawString(10, 700, str(result['ADDRESSLINE1']))
    if result['ADDRESSLINE2'] != None:
        c.drawString(10, 690, str(result['ADDRESSLINE2']))
    if result['ADDRESSLINE3'] != None:
        c.drawString(10, 680, str(result['ADDRESSLINE3']))

    c.drawString(450, 730, str("Challan No:"))
    c.drawString(500, 730, str(result['CHALLANNO']))

    c.drawString(450, 720, str("Challan Dt:"))
    c.drawString(500, 720, str(result['CHALLANDATE']))

    c.drawString(450, 710, str("LR No:"))
    c.drawString(480, 710, str(result['LRNO']))

    c.drawString(10, 650, str("Consignee:"))
    c.drawString(10, 640, str(result['PARTYNAME']))

    if result['ADDRESS1'] != None:
        c.drawString(10, 630, str(result['ADDRESS1']))
    if result['ADDRESS2'] != None:
        c.drawString(10, 620, str(result['ADDRESS2']))
    if result['ADDRESS3'] != None:
        c.drawString(10, 610, str(result['ADDRESS3']))
    if result['ADDRESS4'] != None:
        c.drawString(10, 600, str(result['ADDRESS4']))
    if result['ADDRESS5'] != None:
        c.drawString(10, 590, str(result['ADDRESS5']))
    # c.drawString(10,580, str(result['']))

    c.drawString(350, 600, str("Boxes:"))
    c.drawString(380, 600, str(result['BOXES']))

    c.drawString(500, 600, str("Nett Wt.:"))
    c.drawString(540, 600, str(result['QUANTITY']))



    p=page()
    c.drawString(780,530,"Page No."+str(p))
    c.line(0, 590, 870, 590)
    c.line(0, 570, 870, 570)
    # c.line(0, 520, 870, 520)
    # c.line(0, 500, 870, 500)
    #Upperline in header
    c.drawString(10, 580, "No.")
    c.drawString(40, 580, "Lot No.")
    c.drawString(110, 580, "Item name")
    c.drawString(220, 580, "HSN Cd")
    c.drawString(320, 580, "Desp.Ord.No.")
    c.drawString(430, 580, "Boxes")
    c.drawString(495, 580, "Cops")
    c.drawString(560, 580, "Weight")

def data(stdt,etdt,result,d):

    global no
    no=no+1
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(no))
    c.drawAlignedString(65, d, str(result['LOTNO']))
    if result['HSNCD']!=None:
        c.drawAlignedString(250, d, result['HSNCD'])
    c.drawAlignedString(455, d, str(result['BOXES']))
    c.drawAlignedString(515, d, str(result['COPS']))
    c.drawAlignedString(575, d, str(result['QUANTITY']))
    if len(str(result['ITEM']))>25:
        lines = textwrap.wrap(str(result['ITEM']), 25, break_long_words=False)
        for i in lines:
            c.drawString(110, d, str(i))
            d = dvalue(stdt, etdt, result, divisioncode)
    else:
        c.drawString(110, d, str(result['ITEM']))
    total(result)

def LowerLineData(result,d):
    # Lowerline in data
    fonts(7)
    # c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))
    # c.drawString(65, d, result['MRNNO'])
    # c.drawString(110, d, result['ITEM'])
    # c.drawAlignedString(540, d, str(("%.3f" % float(result['RATE']))))
    # c.drawAlignedString(610, d, str(("%.3f" % float(result['QUANTITY']))))
    # c.drawAlignedString(690, d, str(("%.2f" % float(result['BASICVALUE']))))
    # c.drawString(720, d, result['PRODUCTGLACCOUNT'])
    # itemtotal(result)

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
    global BoxesTotal
    global WeightTotal
    global CopsTotal
    BoxesTotal = BoxesTotal + float("%.3f" % float(result['BOXES']))
    WeightTotal = WeightTotal + float("%.3f" % float(result['QUANTITY']))
    CopsTotal = CopsTotal + (float("%.3f" % float(result['COPS'])))

def printtotal(d):
    global BoxesTotal
    global WeightTotal
    global CopsTotal
    c.drawAlignedString(450, d-20, str(("%.3f" % float(BoxesTotal))))
    c.drawAlignedString(510, d-20, str(("%.3f" % float(CopsTotal))))
    c.drawAlignedString(575, d-20, str(("%.3f" % float(WeightTotal))))
    BoxesTotal = 0
    WeightTotal = 0
    CopsTotal = 0
    c.drawString(320, d-20, "TOTAL:")

    c.line(0, d-10, 870, d-10)
    c.line(0, d-30, 870, d-30)



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
            data(stdt,etdt,result, d)
                # d = dvalue(stdt, etdt,result, divisioncode)
                # LowerLineData(result, d)
                # d = dvalue(stdt, etdt,result, divisioncode)
                # GST(result, d)



    elif challanno[-1] == challanno[-2]:
        data(stdt,etdt,result, d)


    elif challanno[-1] != challanno[-2]:
        printtotal(d)
        d = dvalue(stdt, etdt, result, divisioncode)
        signature(d)
        companyclean()
        no = 0
        c.showPage()
        d=newpage()
        header(stdt, etdt, result, divisioncode)
        data(stdt,etdt,result, d)
