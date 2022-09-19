from reportlab.lib.pagesizes import portrait, A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import textwrap

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(portrait(A3)))
c.setPageSize(portrait(A3))
d = 620
divisioncode=[]
gatepassno=[]
remarks=[]
no=0
pageno=0
QuantityTotal=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

def dvalue(stdt, etdt,result, divisioncode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,d,result, divisioncode[:-1])
        return d

def header(stdt,etdt,d,result,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780, str(result['COMPANYADDRESS']))
    boldfonts(9)
    c.drawCentredString(300, 760, str("PALLETE GATE PASS"))
    fonts(9)
    c.drawString(10, 730, str("Supplier's Name:"))
    c.drawString(80, 730, str(result['SUPPLIER']))
    c.drawString(10, 720, str("Supplier's Address:"))
    f=720
    if len(str(result['SUP_ADDR1'])) > 45:
        lines = textwrap.wrap(str(result['SUP_ADDR1']), 25, break_long_words=False)
        for i in lines:
            c.drawString(90, f, str(i))
            f=f-10
    else:
        c.drawString(90, f, str(result['SUP_ADDR1']))
        f=f-10

    if len(str(result['SUP_ADDR2'])) > 45:
        lines = textwrap.wrap(str(result['SUP_ADDR2']), 25, break_long_words=False)
        for i in lines:
            c.drawString(10, f, str(i))
            f=f-10
    else:
        c.drawString(10, f, str(result['SUP_ADDR2']))
        f=f-10

    if len(str(result['SUP_ADDR3'])) > 45:
        lines = textwrap.wrap(str(result['SUP_ADDR3']), 25, break_long_words=False)
        for i in lines:
            c.drawString(10, f, str(i))
            f=f-10
    else:
        c.drawString(10, f, str(result['SUP_ADDR3']))
        f=f-10

    if len(str(result['SUP_ADDR4'])) > 45:
        lines = textwrap.wrap(str(result['SUP_ADDR4']), 25, break_long_words=False)
        for i in lines:
            c.drawString(10, f, str(i))
            f=f-10
    else:
        c.drawString(10, f, str(result['SUP_ADDR4']))
        f=f-10

    if len(str(result['SUP_ADDR5'])) > 45:
        lines = textwrap.wrap(str(result['SUP_ADDR5']), 25, break_long_words=False)
        for i in lines:
            c.drawString(10, f, str(i))
            f=f-10
    else:
        c.drawString(10, f, str(result['SUP_ADDR5']))
        f=f-10

    c.drawString(10, 680, str("Supplier's Postal Code:"))
    c.drawString(105, 680, str(result['SUP_POSTALCODE']))
    c.drawString(400, 730, str("G.P No.:"))
    c.drawString(450,730,str(result['GATEPASSNO']))
    c.drawString(400, 720, str("G.P Date.:"))
    c.drawString(450, 720, str(result['GATEPASSDATE']))
    c.drawString(400, 710, str("Template Name:"))
    c.drawString(470, 710, str(result['TEMPLATENAME']))
    c.drawString(400, 700, str("Vehicle No.:"))
    if result['VEHICLENO']!=None:
        c.drawString(450, 700, str(result['VEHICLENO']))
    c.drawString(400, 690, str("LR No.:"))
    if result['LRNO'] != None:
        c.drawString(450, 690, str(result['LRNO']))
    c.line(0,670,1000,670)
    c.drawString(10,660,str("Please Receive The Following Material In Good Order and Condition."))
    c.line(0, 650, 1000, 650)
    c.line(0, 630, 1000, 630)
    c.drawString(10,640,str("Sr No."))
    c.drawString(50, 640, str("Pallete Type"))
    c.drawString(400, 640, str("Quantity"))
    c.drawString(500, 640, str("HSN Code."))

def data(stdt,etdt,result,d):
    # d=620
    d=dvalue(stdt,etdt,result,divisioncode)
    global no
    no = no + 1
    fonts(7)
    c.drawString(10, d, str(no))
    c.drawString(50,d,str(result['PRODUCT']))
    c.drawString(410, d, str(result['QUANTITY']))
    c.drawString(510, d, str(result['HSNCODE']))
    total(result)

def total(result):
    global QuantityTotal
    QuantityTotal=QuantityTotal+float("%.3f" % float(result['QUANTITY']))

def printtotal(d):
    # d = 620
    global QuantityTotal
    c.drawString(410, d - 20, str(("%.3f" % float(QuantityTotal))))
    QuantityTotal=0
    c.drawString(380, d - 20, "TOTAL:")

def signature(d,z):
    # d=610
    d = d-40
    c.drawString(10,d,str("Remarks:"))
    if remarks[z]!=None:
        c.drawString(50, d, str(remarks[z]))
    c.drawCentredString(480, d-40, "For " + divisioncode[-1])
    c.drawCentredString(50, d - 100, "Receiver Signature")
    c.drawCentredString(200, d - 100, "Prepared By")
    c.drawCentredString(480, d-100, "Authorised Signatory")

def newpage():
    global d
    d = 620
    return d

def logic(result):
    divisioncode.append(result['COMPANYNAME'])
    gatepassno.append(result['GATEPASSNO'])
    remarks.append(result['REMARKS'])

def newrequest():
    global divisioncode
    global gatepassno
    global no
    global pageno
    global d
    pageno=0
    no = 0
    divisioncode=[]
    gatepassno=[]
    d=620

def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt, etdt,result, divisioncode)
    logic(result)
    global no
    if len(gatepassno) == 1:
        header(stdt,etdt,d,result,divisioncode)
        data(stdt, etdt, result, d)
    elif gatepassno[-1] == gatepassno[-2]:
        data(stdt,etdt,result, d)
    elif gatepassno[-1] != gatepassno[-2]:
        printtotal(d)
        d = dvalue(stdt, etdt, result, divisioncode)
        signature(d,-2)
        no = 0
        c.showPage()
        d=newpage()
        header(stdt, etdt, d, result, divisioncode)
        data(stdt,etdt,result, d)