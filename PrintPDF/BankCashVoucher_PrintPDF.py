from msilib.schema import Font
from operator import rshift
from reportlab.lib.pagesizes import  A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
# from GetDataFromDB import PurchaseMoreThanAmount_GetDataFromDB
from Global_Files import AmmountINWords as amw
pdfmetrics.registerFont(TTFont("MyOwnArial", "arial.ttf"))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
c = canvas.Canvas("1.pdf",pagesize=((A4)))
c.setPageSize((A4))
d = 670
amount=[]
remark=[]
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


def dvalue(divisioncode,result):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize((A4))
        c.showPage()
        header(divisioncode,result)
        return d


def header(divisioncode,result):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 820, str(divisioncode[-1]))
    fonts(9)
    c.drawCentredString(300, 800,"HO : "+ result['HOADDRESS'])
    if result['COMPANYCODE']!='P06     ' and result['COMPANYCODE']!='P07     ':
        c.drawCentredString(300, 780,"FACT : "+ result['COMPANYADDRESS'])
    if result['DOCTYPE']=='BP ':
        c.drawCentredString(300, 760, 'Bank Payment')
    if result['DOCTYPE']=='BR ':
        c.drawCentredString(300, 760, 'Bank Receipt')
    if result['DOCTYPE']=='CP ':
        c.drawCentredString(300, 760, 'Cash Payment')
    if result['DOCTYPE']=='CR ':
        c.drawCentredString(300, 760, 'Cash Receipt')
    
    c.drawString(10,750,result['PARTY'])
    c.drawString(10,740,str(result['BANKADDRESS'])[:80])
    c.drawString(10,730,str(result['BANKADDRESS'])[80:])
    if result['BANKADDRESS1']:
        c.drawString(10,730,result['BANKADDRESS1'])

    c.drawString(450,750,'Voucher No    :')
    c.drawString(520,750,result['VCHNO'])
    c.drawString(450,740,'Voucher Dt     :')
    c.drawString(520,740,str(result['VCHDATE']))
    c.drawString(450,730,'Cheque No     :')
    c.drawString(520,730,result['CHQNO'])
    c.drawString(450,720,'Voucher Amt  : ')
    c.drawString(520,720,result['AMOUNT'])

    c.drawString(10,700,'Bank : ')
    c.drawString(40,700,result['BANKNAME'])
    c.line(0, 690, 600, 690)
    c.line(0, 670, 600, 670)
    # # Upperline in header

    c.drawString(10, 680, "Account Name")
    c.drawString(320, 680, "Bill No.")
    c.drawString(400, 680, "Bill Date")
    c.drawString(480, 680, "Debit")
    c.drawString(560, 680, "Credit")
    

def data(result, d):
    fonts(7)
    c.drawString(10, d, "("+result["GLTYPE"]+") "+result['BANKLINE'])
    d = d-10
    c.drawString(20, d, result["PARTY"])
    if result['BILLNO']!=None:
        c.drawString(320,d,result['BILLNO'])
    if result['BILLDATE']!=None:
        c.drawString(400,d,str(result['BILLDATE']))

    if result['CREDIT']!=0:
        c.drawAlignedString(575, d, result["CREDIT"])
    if result['DEBIT']!=0:
        c.drawAlignedString(500, d, result["DEBIT"])


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
    remark.append(result["REMARKS"])
    orderno.append(result["VCHNO"])
    divisioncode.append(result["DIVCODE"])
    amount.append(result['AMOUNT'])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 670
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
    global CompanyAmountTotal
    CompanyAmountTotal = 0


def textsize(c, result, d):
    logic(result)
    d = dvalue(divisioncode,result)
    
    # d = dvalue(stdt, etdt, divisioncode)
    # logic(result)
    if len(orderno) == 1:
        header(divisioncode,result)
        data(result, d)

    elif orderno[-1] == orderno[-2]:
        data(result, d)
        
    elif orderno[-1] != orderno[-2]:
        d=d-20
        c.drawString(10,d,"Remark :")
        c.drawString(50,d,remark[-2])
        d=d-10
        c.line(0, d, 600, d)
        c.drawString(10,d-10,amw.inwords(amount[-2]))
        d=d-20
        c.line(0, d, 600, d)
        c.drawString(10,d-50,'Prepared By')
        c.drawString(200,d-50,'Checked By')
        c.drawString(400,d-50,'Authorised Signature')
        c.drawString(500,d-50,"Receiver's Signature")
        boldfonts(9)
        # c.drawString(400, d, " Total : ")
    #     c.drawAlignedString(570, d, str("%.2f" % float(CompanyAmountTotal)))
        companyclean()
        c.setPageSize((A4))
        c.showPage()
        fonts(7)
        header(divisioncode,result)
        d = newpage()
        d = dvalue(divisioncode,result)
        data(result, d)
