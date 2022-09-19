from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from Global_Files import Connection_String as con
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 480

divisioncode=[]
finno=[]
item=[]
id=[]

CompanyQuentityTotal=0
CompanyAmountTotal=0
ItemAmountTotal=0
ChargesTotal=0
pageno=0

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

def dvaluegst():
    global d
    d = d + 10
    return d

def header(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(400, 550, divisioncode[-1])
    #Excel


    fonts(9)
    c.drawCentredString(400, 530, "Purchase Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))

    p=page()
    c.drawString(780,530,"Page No."+str(p))
    c.line(0, 520, 850, 520)
    c.line(0, 480, 850, 480)
    #Upperline in header



    c.drawString(10, 505, "FINDATE")
    c.drawString(65, 505, "FINNO")
    c.drawString(110, 505, "BILLDATE")
    c.drawString(160, 505, "BILLNO")
    c.drawString(530, 505, "SUPPLIER")
    c.drawString(720, 505, "BILL AMOUNT")
    #LowerLine in header
    c.drawString(65, 490, "MRNNO")
    c.drawString(10, 490, "MRNDATE")
    c.drawString(110, 490, "ITEM")
    c.drawString(530, 490, "RATE")
    c.drawString(580, 490, "QUANTITY")
    c.drawString(640, 490, "BRK AMOUNT")
    c.drawString(720, 490, "PRODUCT ACCOUNT")

def data(result,d):
    fonts(7)
    # Upperline in data
    c.drawString(10, d, str(result['FINDATE'].strftime('%d-%m-%Y')))
    c.drawString(65, d, result['FINNO'])
    c.drawString(110, d, str(result['BILLDATE'].strftime('%d-%m-%Y')))
    c.drawString(160, d, result['BILLNO'])
    c.drawString(530, d, result['SUPPLIER'])
    c.drawAlignedString(750, d, str(("%.2f" % float(result['BILLAMOUNT']))))

def LowerLineData(result,d):
    # Lowerline in data
    fonts(7)
    c.drawString(10, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))
    c.drawString(65, d, result['MRNNO'])
    c.drawString(110, d, result['ITEM'])
    c.drawAlignedString(540, d, str(("%.3f" % float(result['RATE']))))
    c.drawAlignedString(610, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(690, d, str(("%.2f" % float(result['BASICVALUE']))))
    # c.drawString(720, d, result['PRODUCTGLACCOUNT'])
    itemtotal(result)

def GST(result, d):
    print(result['ID'])
    sql = "Select           ITAX.LONGDESCRIPTION AS PRODUCTCHARGENAME" \
          ", INDTAXDETAIL.VALUE AS PRODUCTCHARGERATE" \
          ", INDTAXDETAIL.CALCULATEDVALUE AS PRODUCTCHARGEAMOUNT" \
          " From    MRNDETAIL" \
          " JOIN    INDTAXDETAIL            ON      MRNDETAIL.ABSUNIQUEID = INDTAXDETAIL.ABSUNIQUEID" \
          " AND     INDTAXDETAIL.TAXCATEGORYCODE <> 'OTH'" \
          " AND     INDTAXDETAIL.CALCULATEDVALUE <> 0" \
          " Join ITAX ON INDTAXDETAIL.ITAXCODE = ITAX.CODE " \
          " Where MRNDETAIL.ABSUNIQUEID = '"+str(result['ID'])+"' " \
          " Order by SEQUENCENO "
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    resultset = con.db.fetch_both(stmt)
    while resultset != False:
        fonts(7)
        c.drawString(400, d, resultset['PRODUCTCHARGENAME'])
        c.drawAlignedString(540, d, str(("%.3f" % float(resultset['PRODUCTCHARGERATE']))))
        c.drawAlignedString(690, d, str(("%.2f" % float(resultset['PRODUCTCHARGEAMOUNT']))))
        GSTTotal(resultset)
        resultset = con.db.fetch_both(stmt)
        d = dvalue()


def total(result):
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = CompanyQuentityTotal + (float("%.3f" % float(result['QUANTITY'])))
    CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['BILLAMOUNT'])))

def itemtotal(result):
    global ItemAmountTotal
    ItemAmountTotal = ItemAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))

def GSTTotal(result):
    global ChargesTotal
    ChargesTotal = ChargesTotal + (float("%.2f" % float(result['PRODUCTCHARGEAMOUNT'])))

def logic(result):
    divisioncode.append(result['DIVCODE'])
    finno.append(result['FINNO'])
    item.append(result['ITEM'])
    id.append(result['ID'])

def dlocvalue(d):
    d=d-20
    return d

def newpage():
    global d
    d = 480
    return d

def newrequest():
    global divisioncode
    global pageno
    global finno
    divisioncode=[]
    pageno=0
    finno=[]


def companyclean():
    global CompanyQuentityTotal
    global CompanyAmountTotal
    global ItemAmountTotal
    global ChargesTotal
    CompanyQuentityTotal = 0
    CompanyAmountTotal = 0
    ItemAmountTotal=0
    ChargesTotal=0

def textsize(c, result, d, stdt, etdt):
    d=dvalue()
    logic(result)
    if len(divisioncode) == 1:
        if len(finno) == 1:
                header(stdt,etdt,divisioncode)
                data(result, d)
                d = dvalue()
                LowerLineData(result, d)
                d = dvalue()
                GST(result, d)
                total(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if finno[-1] == finno[-2]:
            if id[-1] == id[-2]:
                d=dvaluegst()
            elif id[-1] != id[-2]:
                LowerLineData(result, d)
                d = dvalue()
                GST(result, d)

        elif finno[-1] != finno[-2]:
            data(result, d)
            d = dvalue()
            total(result)
            if id[-1] == id[-2]:
                d=dvaluegst()
            elif id[-1] != id[-2]:
                LowerLineData(result, d)
                d = dvalue()
                GST(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
            fonts(7)
            c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            c.drawString(490, d, "Basic Value Total : "+str("%.2f" % float(ItemAmountTotal)))
            c.drawAlignedString(750, d, str("%.2f" % float(CompanyAmountTotal)))
            d=dvalue()
            c.drawString(490, d, "Charges Total : "+str("%.2f" % float(ChargesTotal)))
            companyclean()
            c.setPageSize(landscape(A4))
            c.showPage()

            header(stdt, etdt, divisioncode)
            d=newpage()
            d=dvalue()
            if finno[-1] == finno[-2]:
                if id[-1] == id[-2]:
                    d=dvaluegst()
                    GST(result, d)
                elif id[-1] != id[-2]:
                    LowerLineData(result, d)
                    d = dvalue()
                    GST(result, d)

            elif finno[-1] != finno[-2]:
                data(result, d)
                d = dvalue()
                total(result)
                if id[-1] == id[-2]:
                    GST(result, d)
                elif id[-1] != id[-2]:
                    LowerLineData(result, d)
                    d = dvalue()
                    GST(result, d)