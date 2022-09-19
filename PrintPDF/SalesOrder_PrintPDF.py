from msilib.schema import Font
from operator import rshift
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
# from GetDataFromDB import PurchaseMoreThanAmount_GetDataFromDB

pdfmetrics.registerFont(TTFont("MyOwnArial", "arial.ttf"))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 430

divisioncode = []
orderno = []
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
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.line(20, 580, 820, 580)
    c.line(20, 20, 820, 20)

    c.line(20, 580, 20, 20)
    c.line(820, 580, 820, 20)
    
    boldfonts(9)
    c.drawString(30, 570, "COMPANY NAME:")
    c.drawString(120, 570, result['COMPANY'])
    c.drawString(30, 560, "DIVISION:")
    c.drawString(120, 560, result['DIVCODE'])
    c.drawString(30, 550, "TEMPLATE:")
    c.drawString(120, 550, result['TEMP'])
    c.drawString(30, 540, "DOCUMENT TYPE:")
    c.drawString(120, 540, result['DOCTYPE'])
    c.drawString(30, 530, "ORDER NO:")
    if result['ORDNO'] != None:
        c.drawString(120, 530, result['ORDNO'])
    c.drawString(190, 530, "ORDER DATE:")
    if result['ORDDT'] != None:
        c.drawString(270, 530, str(result['ORDDT'].strftime('%d-%m-%Y')))
    c.drawString(30, 520, "CUSTOMER NAME & ADDRESS WITH CODE:")
    c.drawString(270, 520, str(result['CUSTOMER'])[:60])
    c.drawString(30, 510, str(result['CUSTOMER'])[60:])
    c.drawString(30, 500, "CONSIGNEE/ SHIPTO NAME & ADDRESS WITH CODE:")
    c.drawString(270, 500, str(result['CONSIGNEE'])[:60])
    c.drawString(30, 490, str(result['CONSIGNEE'])[60:])
    c.drawString(30, 480, "BROKER NAME WITH CODE:")
    if result['BROKER'] != None:
        c.drawString(220, 480, result['BROKER'])
    c.drawString(30, 470, "DISPATCH TO:")
    if result['DESPATCHTO'] != None:
        c.drawString(130,470,result['DESPATCHTO'])
    c.drawString(250, 470, "TYPE OF INVOICE:")
    if result['INVTYPE'] == 0:
        c.drawString(350,470,"Domestic")
    elif result['INVTYPE'] == 2:
        c.drawString(350,470,"Export")
    elif result['INVTYPE'] == 3:
        c.drawString(350,470,"Deemed Export")
    elif result['INVTYPE'] == 4:
        c.drawString(350,470,"Jobwork")
    elif result['INVTYPE'] == 5:
        c.drawString(350,470,"SEZ")
    elif result['INVTYPE'] == 6:
        c.drawString(350,470,"Merchant")
    elif result['INVTYPE'] == 7:
        c.drawString(350,470,"None")


# 0=Domestic;2=Export;3=Deemed Export;4=Jobwork;5=SEZ;6=Merchant Export;7=None;
    c.line(20, 467, 820, 467)
    c.line(20, 440, 820, 440)

    
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
    orderno.append(result["ORDNO"])
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
    global orderno
    divisioncode = []
    pageno = 0
    orderno = []


def companyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0


def textsize(c, result, d, stdt, etdt):
    logic(result)
    d = dvalue(stdt, etdt, divisioncode,result)
    # d = dvalue(stdt, etdt, divisioncode)
    # logic(result)
    if len(orderno) == 1:
        header(stdt, etdt, divisioncode,result)
        data(result, d)

    elif orderno[-1] == orderno[-2]:
        data(result, d)

    elif orderno[-1] != orderno[-2]:
        boldfonts(9)
        # c.drawString(400, d, " Total : ")
    #     c.drawAlignedString(570, d, str("%.2f" % float(CompanyAmountTotal)))
        companyclean()
        c.setPageSize(landscape(A4))
        c.showPage()
        fonts(7)
        header(stdt, etdt, divisioncode,result)
        d = newpage()
        d = dvalue(stdt, etdt, divisioncode,result)
        data(result, d)
