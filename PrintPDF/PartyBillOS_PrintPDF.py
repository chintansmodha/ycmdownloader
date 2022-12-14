from msilib.schema import Font
from operator import rshift
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
# from GetDataFromDB import PurchaseMoreThanAmount_GetDataFromDB

pdfmetrics.registerFont(TTFont("MyOwnArial", "arial.ttf"))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
c = canvas.Canvas("1.pdf",A4)
d = 430

divisioncode = []
party = []
ItemQuantityTotal = 0
CompanyAmountTotal = 0
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


def dvalue(stdt, etdt, divisioncode,result):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(landscape(A4))
        c.showPage()
        header(stdt, etdt, divisioncode,result)
        return d


def header(stdt, etdt, divisioncode,result):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(400, 550, divisioncode[-1])
    #Excel


    fonts(9)
    # c.drawCentredString(400, 530, "Purchase Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))

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
    
    boldfonts(7)
    
    c.drawString(25, 460, "ITEM TYPE")#
    c.drawString(100, 460, "ITEM")#
    
    c.drawString(500, 460, "QNTY")#
    c.drawString(550, 460, "GST")#

    c.drawString(25, 450, "CONT.NO.")
    c.drawString(80, 450, "SHADE NO.")
    c.drawString(140, 450, "LOT NO.")

    
    c.drawString(200, 450, "CONT RATE")
    c.drawString(260, 450, "INITIAL COMMA.%")
    
    c.drawString(330, 450, "NET RATE")
    c.drawString(380, 450, "BAL COMMA.%")
    c.drawString(440, 450, "DHARA RATE")
    c.drawString(500, 450, "BILL RATE")
    
    c.drawString(550, 450, "REQUESTED DUE DATE")
    c.drawString(650, 450, "PO REF. NO.")
    c.drawString(750, 450, "REMARK")
    fonts(7)


def data(result, d):
    fonts(7)
    c.drawString(25, d, result["ITEMTYP"])
    c.drawString(80, d, result["ITEM"])
    if result["ORDQTY"] != None:
        c.drawString(500, d, result["ORDQTY"])
    if result["GST"] != None:
        c.drawString(550, d, result["GST"])
    # c.drawAlignedString(570, d, str(("%.2f" % float(result["BILLAMOUNT"]))))
    d = d - 10
    c.drawAlignedString(270,d,result['INITIALCOMM'])
    c.drawAlignedString(350,d,result['NETRATE'])
    c.drawAlignedString(400,d,result['BALCOMM'])
    c.drawAlignedString(460,d,result['DHARARATE'])
    c.drawString(550,d,str(result['REQDUEDATE'].strftime('%d-%m-%Y')))
    c.drawAlignedString(520,d,result['BILLRAT'])
    if result["REMARK"] != None:
        c.drawString(750,d,result['REMARK'])
    if result["CONTRACTRATE"] != None:
        c.drawAlignedString(220,d,result["CONTRACTRATE"])
    if result["CONTNO"] != None:
        c.drawAlignedString(65,d,result["CONTNO"])
    c.drawAlignedString(100,d,result["SHADE"])
    # if result["CONTRACTRATE"] != None:

    # c.drawString(10, d, result["ADDRESS"])
    # total(result)


def total(result):
    global CompanyAmountTotal
    global ItemQuantityTotal
    CompanyAmountTotal = CompanyAmountTotal + (
        float("%.2f" % float(result["BILLAMOUNT"]))
    )
    ItemQuantityTotal = ItemQuantityTotal + (
        float("%.2f" % float(result["BILLAMOUNT"]))
    )


def logic(result):
    party.append(result["PARTY"])
    divisioncode.append(result["COMPANY"])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 430
    return d


def newrequest():
    global divisioncode
    global pageno
    global party
    divisioncode = []
    pageno = 0
    party = []


def companyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0


def textsize(c, result, d, stdt, etdt):
    logic(result)
    d = dvalue(stdt, etdt, divisioncode,result)
    # d = dvalue(stdt, etdt, divisioncode)
    # logic(result)
    if len(divisioncode)==1:
        if len(party) == 1:
            header(stdt, etdt, divisioncode,result)
    #         data(result, d)

    # elif divisioncode[-1] == divisioncode[-2]:
    #     if party[-1] == party[-2]:
    #         data(result, d)

    #     elif party[-1] != party[-2]:
    #         boldfonts(9)
    #         c.drawString(400, d, " Total : ")
    # #     c.drawAlignedString(570, d, str("%.2f" % float(CompanyAmountTotal)))
    # elif divisioncode[-1] != divisioncode[-2]:
    #     companyclean()
    #     c.setPageSize(landscape(A4))
    #     c.showPage()
    #     fonts(7)
    #     header(stdt, etdt, divisioncode,result)
    #     d = newpage()
    #     d = dvalue(stdt, etdt, divisioncode,result)
    #     data(result, d)
