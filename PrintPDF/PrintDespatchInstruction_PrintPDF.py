from reportlab.lib.pagesizes import portrait,A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import textwrap
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(portrait(A5)))
c.setPageSize(portrait(A5))
d = 560
no=0
divisioncode=[]
challanno=[]
remark=[]
authuser=[]
pageno=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt, etdt,result,divisioncode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,result,divisioncode)
        return d

def dvaluegst():
    global d
    d = d - 10
    return d

def header(stdt,etdt,result,divisioncode):
    d=670
    global pan
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    fonts(12)
    c.drawString(220, 780, str("Despatch Instruction Memo"))
    c.line(220, 775, 368, 775)
    fonts(9)
    c.drawString(10, 750, str("Despatch No:"))
    c.drawString(65, 750, str(result['DESPATCHNO']))
    c.drawString(200, 750, str("Despatch Date:"))
    c.drawString(265, 750, str(result['DESPATCHDATE']))
    c.drawString(400, 750, str("Despatch:"))
    if result['DESPTO'] != None:
        c.drawString(440, 750, str(result['DESPTO']))

    c.line(0, 745, 800, 745)
    c.drawString(10, 730, str("Broker:"))
    f=730
    if len(str(result['BROKER'])) > 25:

        lines = textwrap.wrap(str(result['BROKER']), 25, break_long_words=False)
        for i in lines:
            c.drawString(40, f, str(i))
            f = f-10
    else:
        c.drawString(40, f , str(result['BROKER']))
        f=f-10
    c.drawString(200, 730, str("Broker E-Mail:"))
    if result['BROKEREMAIL'] != None:
        c.drawString(260, 730, str(result['BROKEREMAIL']))
    c.drawString(10, 700, str("Name Of Buyer"))
    c.line(10,695,70,695)
    c.drawString(10, 685 , str(result['BUYERNAME']))
    if len(str(result['BUYERADDRESS1'])) > 45:

        lines = textwrap.wrap(str(result['BUYERADDRESS1']), 45, break_long_words=False)
        for i in lines:
            c.drawString(10, d, str(i))
            d = d-10
    else:
        c.drawString(10, d, str(result['BUYERADDRESS1']))
        d=d-10

    if len(str(result['BUYERADDRESS2'])) > 45:
        lines = textwrap.wrap(str(result['BUYERADDRESS2']), 45, break_long_words=False)
        for i in lines:
            c.drawString(10, d, str(i))
            d = d - 10
    else:
        c.drawString(10, d, str(result['BUYERADDRESS2']))
        d = d - 10

    if len(str(result['BUYERADDRESS3'])) > 45:
        lines = textwrap.wrap(str(result['BUYERADDRESS3']), 45, break_long_words=False)
        for i in lines:
            c.drawString(10, d, str(i))
            d = d-10
    else:
        c.drawString(10, d, str(result['BUYERADDRESS3']))
        d = d - 10

    if len(str(result['BUYERADDRESS4'])) > 45:
        lines = textwrap.wrap(str(result['BUYERADDRESS4']), 45, break_long_words=False)
        for i in lines:
            c.drawString(10, d, str(i))
            d = d-10
    else:
        c.drawString(10, d, str(result['BUYERADDRESS4']))
        d = d - 10

    if len(str(result['BUYERADDRESS5'])) > 45:
        lines = textwrap.wrap(str(result['BUYERADDRESS5']), 45, break_long_words=False)
        for i in lines:
            c.drawString(10, d, str(i))
            d = d-10
    else:
        c.drawString(10, d, str(result['BUYERADDRESS5']))
        d = d - 10
    c.drawString(10, 625, str("Postal Code:"))
    c.drawString(65, 625, str(result['BUYERPOSTALCODE']))
    c.drawString(10,605,str("GST No:"))
    c.drawString(55,605,str(result['BUYERGSTNO']))
    c.drawString(150, 605, str("PAN No:"))
    c.drawString(190, 605, str(result['BUYERPANNO']))

    c.drawString(300, 700, str("Name Of Consignee"))
    c.line(300, 695, 380, 695)
    c.drawString(300, 685, str(result['CONSIGNEENAME']))
    z=670
    if len(str(result['CONADDRESS1'])) > 45:
        lines = textwrap.wrap(str(result['CONADDRESS1']), 25, break_long_words=False)
        for i in lines:
            c.drawString(300, z, str(i))
            z = z-10
    else:
        c.drawString(300, z, str(result['CONADDRESS1']))
        z = z - 10

    if len(str(result['CONADDRESS2'])) > 45:
        lines = textwrap.wrap(str(result['CONADDRESS2']), 25, break_long_words=False)
        for i in lines:
            c.drawString(300, z, str(i))
            z = z-10
    else:
        c.drawString(300, z, str(result['CONADDRESS2']))
        z = z - 10

    if len(str(result['CONADDRESS3'])) > 45:
        lines = textwrap.wrap(str(result['CONADDRESS3']), 25, break_long_words=False)
        for i in lines:
            c.drawString(300, z, str(i))
            z = z-10
    else:
        c.drawString(300, z, str(result['CONADDRESS3']))
        z = z - 10

    if len(str(result['CONADDRESS4'])) > 45:
        lines = textwrap.wrap(str(result['CONADDRESS4']), 25, break_long_words=False)
        for i in lines:
            c.drawString(300, z, str(i))
            z = z-10
    else:
        c.drawString(300, z, str(result['CONADDRESS4']))
        z = z - 10

    if len(str(result['CONADDRESS5'])) > 45:
        lines = textwrap.wrap(str(result['CONADDRESS5']), 25, break_long_words=False)
        for i in lines:
            c.drawString(300, z, str(i))
            z = z-10
    else:
        c.drawString(300, d, str(result['CONADDRESS5']))
        z = z - 10
    c.drawString(300, 625, str("Postal Code:"))
    c.drawString(365, 625, str(result['CONPOSTALCODE']))
    c.drawString(300, 605, str("GST No:"))
    # c.drawString(335, 615, str(result['CONGSTNO']))
    c.drawString(440, 605, str("PAN No:"))
    # c.drawString(480, 615, str(result['CONPANNO']))
    p=page()
    c.drawString(780,530,"Page No."+str(p))
    #Upperline in header
    c.drawString(10, 570, "No.")
    c.drawString(40, 570, "Item")
    c.drawString(160, 570, "Shade")
    c.drawString(350, 570, "Lot No.")
    c.drawString(410, 570, "Qnty Kgs.")
    c.drawString(500, 570, "Rate")
    c.drawString(560 ,570, "RD")
    c.line(0, 580, 870, 580)
    c.line(0, 560, 870, 560)

def data(stdt,etdt,result,d):
    global no
    no=no+1
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(no))
    c.drawString(370, d, str(result['LOTNO']))
    c.drawRightString(445, d, str(result['QUANTITY']))
    c.drawString(160, d, str(result['SHADECODE']))
    if result['RATE']!=None:
        c.drawRightString(520, d, str(("%.2f" % float(result['RATE']))))
    if result['RD'] != None:
        c.drawRightString(575, d, str(("%.2f" % float(result['RD']))))

    if len(str(result['ITEM'])) > 25:
        lines = textwrap.wrap(str(result['ITEM']), 25, break_long_words=False)
        for i in lines:
            c.drawString(40, d, str(i))
            d = dvalue(stdt, etdt, result, divisioncode)
    else:
        c.drawString(40, d, str(result['ITEM']))
    # c.drawString(40 ,d, str(result['ITEMREMARKS']))

def remarks(result,d):
    d = d - 40
    c.drawString(10,d,str(result(['REMARKS'])))

def signature(stdt,etdt,result,d):
    c.line(0, d, 800, d)
    d = d-10

    c.drawString(10, d, "Remarks:")
    if remark[-1]!=None:
        c.drawString(40, d, str(remark[-1]))
    # c.drawString(55,d,str(result['REMARKS']))
    c.drawCentredString(480, d - 50, "Authorised Signatory")
    if authuser[-1] != None:
        d = d - 10
        c.drawCentredString(500, d - 50, str(authuser[-1]))

def logic(result):
    divisioncode.append(result['COMPANY'])
    challanno.append(result['DESPATCHNO'])
    authuser.append(result['AUTHUSER'])
    remark.append(result['REMARKS'])

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
    global authuser
    global no
    no=0
    divisioncode=[]
    pageno=0
    challanno=[]
    authuser=[]
    remark=[]

def companyclean():
    global BoxesTotal
    global WeightTotal
    BoxesTotal = 0
    WeightTotal = 0

def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt, etdt,result,divisioncode)
    logic(result)
    global no
    if len(challanno) == 1:
            header(stdt,etdt,result,divisioncode)
            data(stdt,etdt,result, d)

    elif challanno[-1] == challanno[-2]:
        data(stdt,etdt,result, d)

    elif challanno[-1] != challanno[-2]:
        # d = dvalue(stdt, etdt, result,divisioncode)
        signature(stdt,etdt,result,d)
        companyclean()
        no = 0
        c.showPage()
        d=newpage()
        header(stdt, etdt, result,divisioncode)
        data(stdt,etdt,result, d)

