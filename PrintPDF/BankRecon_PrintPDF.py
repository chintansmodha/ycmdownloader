from reportlab.lib.pagesizes import  A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from Global_Files import AmmountINWords as amw
pdfmetrics.registerFont(TTFont("MyOwnArial", "arial.ttf"))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
c = canvas.Canvas("1.pdf",pagesize=((A4)))
c.setPageSize((A4))
d = 740
divisioncode = []
pageno = 0
totalamount=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt,etdt,divisioncode,result):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize((A4))
        c.showPage()
        header(divisioncode,result,stdt,etdt)
        return d

def header(divisioncode,result,stdt,etdt):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 820, str(divisioncode[-1]))
    c.drawCentredString(300, 800, str(result['BANKNAME']))
    c.drawCentredString(300, 780, "Bank Reconciliation Statement From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    fonts(9)

    c.drawString(10,760,"VCH DATE")
    c.drawString(100,760,"VCH NO.")
    c.drawString(180,760,"PARTY")
    c.drawString(320,760,"CHQ NO.")
    c.drawString(420,760,"CHQ DATE")
    c.drawString(520,760, "AMOUNT RECO.")
    c.line(0, 775, 600, 775)
    c.line(0, 750, 600, 750)

def data(result, d):
    fonts(8)
    d = d-10
    # c.drawString(20, d, result["PARTY"])
    if result['VCHDATE']!=None:
        c.drawString(10,d,str(result['VCHDATE']))
    if result['VCHNO']!=None:
        c.drawString(100,d, str(result['VCHNO']))
    if result['PARTY']!=None:
        c.drawString(180,d,str(result['PARTY']))
    if result['CHQNO']!=None:
        c.drawString(320,d,str(result['CHQNO']))
    if str(result['CHQDATE'])!='1999-01-01':
        c.drawString(420,d,str(result['CHQDATE']))
    if result['AMOUNT']!=None:
        c.drawString(520,d,str(result['AMOUNT']))
    total(result)
    



def total(result):
    global totalamount
    totalamount = totalamount + (float("%.2f" % float(result["AMOUNT"])))
def totalprint(d):
    c.drawAlignedString(560,d,str(totalamount))

def logic(result):
    divisioncode.append(result["DIVCODE"])

def dlocvalue(d):
    d = d - 20
    return d

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode
    global pageno
    global totalamount
    divisioncode = []
    pageno = 0
    totalamount=0
    
def companyclean():
    global totalamount
    totalamount = 0

def textsize(c, result, d, stdt, etdt):
    logic(result)
    d = dvalue(stdt,etdt,divisioncode,result)
    if len(divisioncode) == 1:
        header(divisioncode,result,stdt,etdt)
        data(result, d)
    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)              

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(8)
        c.drawString(10, d, str(" Total Receipts : "))
        totalprint(d)
        c.setPageSize(A4)
        c.showPage()
        header(divisioncode,result,stdt,etdt)
        d=newpage()
        d=dvalue(stdt, etdt, divisioncode,result)
        data(result,d)
           