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

debit=0
credit=0
clbal=0
partydebit=0
partycredit=0
partyclbal=0
divisioncode = []
party=[]
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



    c.drawString(10, 505, "VCHDATE")
    c.drawString(80, 505, "VCHNO")
    c.drawString(150, 505, "INV. NO.")
    c.drawString(230, 505, "INV. DT.")
    c.drawString(310, 505, "TYPE")
    c.drawString(390, 505, "CHQ. NO.")
    c.drawString(470, 505, "BANK")
    c.drawString(610, 505, "Debit Amt")
    c.drawString(690, 505, "Credit Amt")
    c.drawString(770, 505, "Closing Bal.")
    

def data(result, d):
    fonts(7)
    c.drawString(10, d, result['VCHDATE'])
    c.drawString(80, d, result['VCHNO'])
    if result['INVNO'] != None:
        c.drawString(150, d, result['INVNO'])
    if result['INVOICEDATE'] != None:
        c.drawString(230, d, str(result['INVOICEDATE']))
    c.drawString(310, d, result['DOCTYPE'])
    c.drawString(390, d, result['CHQNO'])
    c.drawString(470, d, result['BANK'])
    c.drawAlignedString(640, d, str(result['DRAMOUNT']))
    c.drawAlignedString(730, d, str(result['CRAMOUNT']))
    c.drawAlignedString(800, d, str(result['CLBAL']))
    total(result)

def total(result):
    global credit
    global debit
    global opbal
    global clbal
    global partycredit
    global partydebit
    global partyclbal
    # opbal = opbal + float(("%.3f" % float(result['OPBAL']))) 
    credit = credit + float(("%.3f" % float(result['CRAMOUNT']))) 
    debit = debit + float(("%.3f" % float(result['DRAMOUNT']))) 
    clbal = clbal + float(("%.3f" % float(result['CLBAL']))) 
    partycredit = partycredit + float(("%.3f" % float(result['CRAMOUNT']))) 
    partydebit = partydebit + float(("%.3f" % float(result['DRAMOUNT']))) 
    partyclbal = partyclbal + float(("%.3f" % float(result['CLBAL'])))

def printTotal(d):
    global debit
    global credit
    global clbal

    c.drawString(10, d, "TOTAL")
    c.drawAlignedString(640, d, str(round(debit,2)))
    c.drawAlignedString(730, d, str(round(credit,2)))
    c.drawAlignedString(800, d, str(round(clbal,2)))

    

def printPartyTotal(d):
    global partydebit
    global partycredit
    global partyclbal

    c.drawString(350, d, "TOTAL")
    c.drawAlignedString(640, d, str(round(partydebit,2)))
    c.drawAlignedString(730, d, str(round(partycredit,2)))
    c.drawAlignedString(800, d, str(round(partyclbal,2)))

    partydebit=0
    partycredit=0
    partyclbal=0

def logic(result):
    party.append(result['PARTY'])
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
        boldfonts(9)
        c.drawString(10, d, result['PARTY'])
        fonts(7)
        d = dvalue(divisioncode,result,reportName,startdate,enddate)
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if party[-1] == party[-2]:
            data(result, d)
        if party[-1] != party[-2]:
            boldfonts(7)
            printPartyTotal(d)
            boldfonts(9)
            d = dvalue(divisioncode,result,reportName,startdate,enddate)
            c.drawString(10, d, result['PARTY'])
            fonts(7)
            d = dvalue(divisioncode,result,reportName,startdate,enddate)
            data(result, d)
        
    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(7)
        c.line(0, d, 850, d)
        printTotal(d-10)
        c.line(0, d-20, 850, d-20)
        companyclean()
        c.setPageSize(landscape(A4))
        c.showPage()
        fonts(7)
        header(divisioncode,result,reportName,startdate,enddate)
        d = newpage()
        d = dvalue(divisioncode,result,reportName,startdate,enddate)
        c.drawString(10, d, result['PARTY'])
        d = dvalue(divisioncode,result,reportName,startdate,enddate)
        data(result, d)
