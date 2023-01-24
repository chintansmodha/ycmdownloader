from reportlab.lib.pagesizes import  A4,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
# from GetDataFromDB import PurchaseMoreThanAmount_GetDataFromDB
from Global_Files import AmmountINWords as amw
pdfmetrics.registerFont(TTFont("MyOwnArial", "arial.ttf"))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 490

opbal=0
debit=0
credit=0
clbal=0
divisioncode = []
pageno = 0


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


def dvalue(divisioncode,result,reportName,startdate,enddate):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(landscape(A4))
        c.showPage()
        header(divisioncode,result,reportName,startdate,enddate)
        return d


def header(divisioncode,result,reportName,startdate,enddate):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(400, 550, str(divisioncode[-1]))
    fonts(9)
    c.drawCentredString(400, 530, reportName+"- From "+startdate+" To "+enddate)

    p=page()
    c.drawString(780,530,"Page No."+str(p))
    c.line(0, 520, 850, 520)
    c.line(0, 500, 850, 500)
    #Upperline in header



    c.drawString(10, 505, "FINDATE")
    c.drawString(65, 505, "FINNO")
    c.drawString(110, 505, "BILLDATE")
    c.drawString(160, 505, "BILLNO")
    c.drawString(530, 505, "SUPPLIER")
    c.drawString(720, 505, "BILL AMOUNT")
    

def data(result, d):
    fonts(7)
    c.drawString(10, d, result['VCHDATE'])
    c.drawString(60, d, result['VCHNO'])
    if result['INVNO'] != None:
        c.drawString(110, d, result['INVNO'])
    if result['INVOICEDATE'] != None:
        c.drawString(170, d, str(result['INVOICEDATE']))
    c.drawString(230, d, result['DOCTYPE'])
    c.drawString(290, d, result['CHQNO'])
    c.drawString(350, d, result['BANK'])
    c.drawAlignedString(420, d, str(result['DRAMOUNT']))
    c.drawAlignedString(490, d, str(result['CRAMOUNT']))
    c.drawAlignedString(560, d, str(result['CLBAL']))
    total(result)

def total(result):
    global credit
    global debit
    global opbal
    global clbal
    opbal = opbal + float(("%.3f" % float(result['OPBAL']))) 
    credit = credit + float(("%.3f" % float(result['CRAMOUNT']))) 
    debit = debit + float(("%.3f" % float(result['DRAMOUNT']))) 
    clbal = clbal + float(("%.3f" % float(result['CLBAL']))) 

def printTotal(d):
    global credit
    global debit
    global opbal
    global clbal
    c.drawString(10, d, "TOTAL")
    c.drawAlignedString(350, d, str(round(opbal,2)))
    c.drawAlignedString(420, d, str(round(debit,2)))
    c.drawAlignedString(490, d, str(round(credit,2)))
    c.drawAlignedString(560, d, str(round(clbal,2)))

def logic(result):
    divisioncode.append(result["DIVCODE"])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 490
    return d


def newrequest():
    global divisioncode
    global pageno
    global orderno
    global amount
    global remark
    remark=[]
    amount=[]
    divisioncode = []
    pageno = 0
    orderno = []


def companyclean():
    global credit
    global debit
    global opbal
    global clbal
    credit =0
    debit=0
    opbal=0
    clbal=0


def textsize(c, result, d,reportName,startdate,enddate):
    logic(result)
    d = dvalue(divisioncode,result,reportName,startdate,enddate)
    if len(divisioncode) == 1:
        header(divisioncode,result,reportName,startdate,enddate)
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)
        
    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.line(0, d, 600, d)
        printTotal(d-10)
        c.line(0, d-20, 600, d-20)
        companyclean()
        c.setPageSize(landscape(A4))
        c.showPage()
        fonts(7)
        header(divisioncode,result,reportName,startdate,enddate)
        d = newpage()
        d = dvalue(divisioncode,result,reportName,startdate,enddate)
        data(result, d)
