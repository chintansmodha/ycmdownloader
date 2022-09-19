from reportlab.lib.pagesizes import portrait, A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from datetime import datetime
import textwrap

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(portrait(A3)))
c.setPageSize(portrait(A3))
d = 730
divisioncode=[]
requisitionno=[]
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
        header(stdt, etdt,d,result,divisioncode[:-1])
        return d

def header(stdt,etdt,d,result,divisioncode):
    fonts(9)
    c.setFillColorRGB(0, 0, 0)
    format = '%d-%m-%Y %I:%M %p'
    datestring = datetime.now(tz=None)
    date = datetime.strftime(datestring, format)
    c.drawString(10, 800, date)
    boldfonts(12)
    c.drawCentredString(300, 800, str("STORES REQUISITION"))
    c.drawCentredString(300,780,divisioncode[-1])
    fonts(9)
    c.drawString(10,760,str("REQUISITION NO:"))
    c.drawString(100,760,str(result['REQUISITIONNO']))
    c.drawString(400, 760, str("REQUISITION DATE:"))
    c.drawString(500, 760, str(result['REQUISITIONDATE']))
    c.line(0, 750, 870, 750)
    c.line(0, 730, 870, 730)
    boldfonts(9)
    c.drawString(10, 740, str("SR NO."))
    c.drawString(50, 740, str("ITEM"))
    c.drawString(400, 740, str("UNIT"))
    c.drawString(500, 740, str("QUANTITY"))

def data(stdt,etdt,result,d):
    global no
    no = no + 1
    fonts(9)
    c.drawString(10, d, str(no))
    c.drawString(50, d, str(result['ITEM']))
    c.drawString(400, d, str(result['UNIT']))
    c.drawString(510, d, str(("%.3f" % float(result['QUANTITY']))))
    total(result)

def total(result):
    global QuantityTotal
    QuantityTotal=QuantityTotal+float("%.3f" % float(result['QUANTITY']))

def printtotal(d):
    global QuantityTotal
    boldfonts(9)
    c.drawString(510, d, str(("%.3f" % float(QuantityTotal))))
    QuantityTotal = 0
    boldfonts(7)
    c.drawString(400, d, "TOTAL:")
    fonts(7)

def signature(d):
    boldfonts(9)
    d = d-40
    c.drawCentredString(50, d-100, "Dept. Incharge")
    c.drawCentredString(480, d-100, "Receiver's Signature")

def newpage():
    global d
    d = 730
    return d

def logic(result):
    divisioncode.append(result['DEPARTMENTNAME'])
    requisitionno.append(result['REQUISITIONNO'])

def newrequest():
    global divisioncode
    global requisitionno
    global no
    global pageno
    global d
    divisioncode = []
    requisitionno = []
    pageno = 0
    no = 0
    d = 730

def textsize(c, result, d, stdt, etdt):
    global no
    d = dvalue(stdt, etdt,result, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        header(stdt, etdt, d, result, divisioncode)
        data(stdt, etdt, result, d)
    elif divisioncode[-2] == divisioncode[-1]:
        if requisitionno[-1] == requisitionno[-2]:
            data(stdt, etdt, result, d)
        elif requisitionno[-1] != requisitionno[-2]:
            printtotal(d)
            d = dvalue(stdt, etdt, result, divisioncode)
            signature(d)
            c.showPage()
            d = newpage()
            no = 0
            header(stdt, etdt, d,result, divisioncode)
            d = dvalue(stdt, etdt, result, divisioncode)
            data(stdt, etdt, result, d)
    elif divisioncode[-2] != divisioncode[-1]:
        printtotal(d)
        d = dvalue(stdt, etdt, result, divisioncode)
        signature(d)
        no = 0
        c.showPage()
        d = newpage()
        header(stdt, etdt, d,result, divisioncode)
        d = dvalue(stdt, etdt, result, divisioncode)
        data(stdt, etdt, result, d)