import textwrap

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
#from SalesRegister import SalesRegister_View as salesview

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf")
c.setPageSize(landscape(A4))
d = 630

# d = 730
divisioncode = []
itemcode = []
invoiceno=[]
plantname=[]
plantaddress=[]

docremark=[]
invoicenocounter=[]
invoicenocheck=[]
partyname=[]
itemname=[]
docremark=[]
CompanyAmountTotal = 0
itemcounter=0
pageno = 0


def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def total(result):
    global Totalquantity
    try:
        Totalquantity=Totalquantity +(float("%.3f"% float(result['QUANTITY'])))
    except:
        pass

def dvalue():
    global d
    d = d - 20
    return d
def dvalue10():
    global d
    d = d - 10
    return d
def dlocvalue(d):
    d = d - 20
    return d
def newpage():
    global d
    d = 510
    return d

def companyclean():
    global CompanyQuentityTotal
    global CompanyAmountTotal
    CompanyQuentityTotal = 0
    CompanyAmountTotal = 0

def newrequest():
    global divisioncode
    global plantaddress
    global docremark
    global itemcode
    global invoiceno
    divisioncode=[]
    itemcode=[]
    invoiceno=[]
    plantaddress=[]
    docremark=[]


def logic(result):
    invoiceno.append(result['CHALLANNO'])
    divisioncode.append(result['DIVISION'])
    plantaddress.append(result['COMPANYADDRESS'])

def textsize(x, result):
    global d
    global itemcounter
    # d = dvalue()
    logic(result)
    if len(divisioncode) == 1:
        if len(invoiceno) == 1:
            # if d > 14:
            # header("stdt", "etdt", plantname)
            header("stdt"," etdt", divisioncode,result)
            # d=dvalue()
            itemcounter=itemcounter+1
            data(result)
            adddocremark(result)
    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1]==invoiceno[-2]:
            d=dvalue()
            itemcounter=itemcounter+1
            data(result)
            adddocremark(result)
        else:
            printdocremark()
            c.showPage()
            header("stdt", " etdt", divisioncode,result)
            d=630
            # d = dvalue()
            itemcounter=1
            data(result)
    elif divisioncode[-1]!=divisioncode[-2]:
        c.showPage()
        # d = 630
        clearadddocremark()
        header("stdt", " etdt", divisioncode,result)
        # d=dvalue()
        d=630
        itemcounter=1
        data(result)
    total(result)


def header(stdt, etdt, plantname,result):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(430, 560, divisioncode[-1]+" "+plantname[-1])
    c.drawCentredString(300, 800, plantname[-1])

    fonts(9)
    # c.drawCentredString(430, 550, "Sales Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
    #     etdt.strftime('%d-%m-%Y')))
    c.drawCentredString(300, 785, plantaddress[-1])
    c.drawCentredString(300, 770,  "GSTIN : "+str(result['COMPANYGST']))
    c.drawCentredString(300, 750, "Retunable Gate Pass" )

    c.drawString(10,740,"Gate Keeper")
    c.drawString(430,740,"No     : " +str(result['CHALLANNO']))
    c.drawString(430,725,"Date  : " +str(result['CHALLANDATE']))
    c.drawString(10,710,"Please allow the following goods out of the factory premises.")
    c.drawString(10, 690, "Party : "+str(result['PARTY']))
    c.drawString(430, 690, "GSTIN : "+str(result['CUSTOMERGST']))
    partyaddress = result['PARTYRADDRESS']
    ca=680
    # ca = ca - 24
    if len(str(partyaddress)) > 100:
        lines = textwrap.wrap(str(partyaddress), 100, break_long_words=False)
        for i in lines:
            c.drawString(10, ca, str(i))
            ca = ca - 12
    else:
        c.drawString(10, 575, result['PARTYRADDRESS'])

    p = page()
    c.drawString(530, 780, "Page No." + str(p))
    c.line(0, 660, 850, 660)
    c.line(0, 640, 850, 640)


    c.drawString(10,650 , "Sr. No.")
    c.drawString(40, 650, "Item Name")
    c.drawString(340, 650, "Unit")
    c.drawString(370, 650, "HSN Code")
    c.drawString(430, 650, "Quantity")
    c.drawString(500, 650, "Item Remark")

def data(result):
    fonts(9)
    try:
        c.drawString(10, d,str(itemcounter))

        itemname = result['ITEMNAME']
        ca = d
        # ca = ca - 24
        if len(str(itemname)) > 70:
            lines = textwrap.wrap(str(itemname), 70, break_long_words=False)
            for i in lines:
                c.drawString(40, ca, str(i))
                ca = ca - 12
        else:
            c.drawString(40, d, result['ITEMNAME'])

        c.drawString(340, d, result['ITEMUNIT'])
        c.drawString(370, d, result['HSNNO'])
        c.drawString(430, d, result['ITEMQTY'])
        c.drawString(500, d, result['ITEMREMARK'])
        # c.drawString(120, d, result['HSNNO'])

        total(result)
    except:
        pass


def printdocremark():
    global d

    doccounter=0
    d=dvalue()
    c.line(0, d, 850, d)
    # d=dvalue()
    c.drawString(10, d-10, "Document Remarks")
    d=dvalue()
    # c.drawString(10, d, docremark[doccounter])
    while len(docremark)<=doccounter:
        doccounter = doccounter + 1
        c.drawString(10, d, docremark[doccounter])
        d=dvalue()
    c.line(0, d, 850, d)
    c.drawString(60, d-50, "Prepared By")
    c.drawString(250, d-50,"Stores InCharge " )
    c.drawString(430, d-50,"Receiver's Signature" )

def adddocremark(result):
    docremark.append(result['DOCREMARK'])
    # docremark.append(result['ITEMNAME'])

def clearadddocremark():
    docremark=[]


