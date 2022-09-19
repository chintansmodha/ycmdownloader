from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_currency
#from SalesRegister import SalesRegister_View as salesview

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf", pagesize=(landscape(A4)))
c.setPageSize(landscape(A4))
d = 500

# d = 730
divisioncode = []
itemcode = []
taxdetail = []
taxamount=[]
invoiceno=[]
plantname=[]
row=500
col=500
invoicenocounter=[]
invoicenocheck=[]
partyname=[]
invoicedate=[]
itemname=[]
rate=[]

InvoiceAmountTotal=0
GrossAmountTotal=0
Bills=0
BasicAmount=0
netweight=0
TaxAmount=0
Totalquantity=0
ChargesummaryTotalquantity=0
TotalBoxes=0
Planttotalinvoiceamount=0
Planttotalquantity=0
TOTALInvoiceTAXAmount=0

ItemAmountTotal = 0
CompanyAmountTotal = 0
pageno = 0


def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def header(stdt, etdt, plantname):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(430, 560, divisioncode[-1]+" "+plantname[-1])
    c.drawCentredString(430, 560, plantname[-1])

    fonts(9)
    c.drawCentredString(430, 550, "Sales Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))

    p = page()
    c.drawString(770, 550, "Page No." + str(p))
    c.line(0, 540, 850, 540)
    c.line(0, 510, 850, 510)

    c.drawString(10, 530, "Inv. No.")
    c.drawString(60, 530, "Inv. Date")
    c.drawString(110, 530, "Party")
    c.drawString(430, 530, "Broker")
    # c.drawString(700, 530, "Gross Amount")
    c.drawString(770, 515, "Inv Amount")
    # c.drawString(320, 530, "ITEM")

    c.drawString(10, 515, "LR. No.")
    c.drawString(60, 515, "LR. Date.")
    c.drawString(110, 515, "Item / Charge ")
    c.drawString(550, 515, "Boxes ")
    c.drawString(600, 515, "Quantity ")
    c.drawString(660, 515, "Rate ")
    c.drawString(700, 515, "Brk. Amount ")

def header1(stdt, etdt, plantname):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(430, 560, plantname[-1])

    fonts(9)
    c.drawCentredString(430, 550, "Charge Summary Report From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))

    p = page()
    c.drawString(770, 550, "Page No." + str(p))
    c.line(0, 540, 850, 540)
    # c.line(0, 510, 850, 510)


def data(result, d):
    fonts(9)
    try:
        c.drawString(10, d, result['INVOICENO'])
        c.drawString(60, d, str(result['INVDATE'].strftime('%d-%m-%Y')))
        c.drawString(110, d, result['BUYER'])
        c.drawAlignedString(810, d,  str(format_currency("%.2f" % float( result['INVOICEAMOUNT']),'',locale='en_IN'))) # Invoice Amount

        if result['BROKER'] != None:
            c.drawString(430, d, result['BROKER'])

        d=dvalue10()

        if result['LRNO'] != None:
            c.drawString(10, d, result['LRNO'])
        if result['LRDATE'] != None:
            c.drawString(60, d, str(result['LRDATE'].strftime('%d-%m-%Y')))
        c.drawString(110, d, result['PRODUCT']+ ' '+result['QUALITY'])
        c.drawString(565, d, "0 ")                                              # Boxes
        c.drawAlignedString(625, d, str(("%.3f" % float(result['QUANTITY']))))      # Quanitity
        c.drawAlignedString(680, d, str(format_currency("%.2f" % float( result['RATE']),'',locale='en_IN')))          # Rate
        try:
            rate=float(result['RATE'])
            quantity=float(result['QUANTITY'])
            sumtotal=rate*quantity
            c.drawAlignedString(740, d,str(format_currency("%.2f" % float(sumtotal), '', locale='en_IN')))
        except:
            pass

        # salesview.getproducttaxdetail(result)

        total(result)
    except:
        pass
        # print("problem in the data function : ")
    # logic(result)

def taxdetailscharges(result,d):
    d=dvalue10()
    global TOTALInvoiceTAXAmount
    fonts(10)
    # c.drawString(210, d, "d value :  "+ str(d))
    c.drawString(200, d , result['TAXDETAILS']+": ")
    try:
        TOTALInvoiceTAXAmount = TOTALInvoiceTAXAmount + (float("%.3f" % float(result['TAXAMOUNT'])))
        # print(InvoiceAmountTotal)
    except:
        print("exception tax details charges from ")
    c.drawAlignedString(630, d , str(format_currency("%.2f" % float(result['TAXAMOUNT']), '', locale='en_IN')))  # tax Amount
    # c.drawString(40, d,  "d : "+str(d))

def taxdetails(c,result,d):
    d=dvalue()
    fonts(8)
    # d=335
    # c.drawString(210, d, "d value :  "+ str(d))
    c.drawString(110, d, result['ITAXNAME']+": ")
    try:
        c.drawAlignedString(680, d, str(("%.2f" % float(result['TAXRATE']))))  # taxRate
    except:
        c.drawAlignedString(680, d, str(("%.2f" % float(00.00))))
    try:
        c.drawAlignedString(740, d , str(format_currency("%.2f" % float(result['TAXAMOUNT']), '', locale='en_IN')))  # tax Amount
    except:
        c.drawAlignedString(740, d, str(("%.2f" % float(00.00))))

def producttaxdetails(c,result,d):
    d=dvalue10()
    fonts(8)

    c.drawString(110, d, result['ITAXNAME']+": ")
    try:
        c.drawAlignedString(680, d, str(("%.2f" % float(result['TAXRATE']))))  # taxRate
    except:
        c.drawAlignedString(680, d, str(("%.2f" % float(00.00))))
    try:
        c.drawAlignedString(740, d , str(format_currency("%.2f" % float(result['TAXAMOUNT']), '', locale='en_IN')))  # tax Amount
    except:
        c.drawAlignedString(740, d, str(("%.2f" % float(00.00))))



def invoicetaxdetails(c,result,d):
    d=dvalue10()
    fonts(8)

    c.drawString(110, d, result['ITAXNAME']+": ")
    try:
        c.drawAlignedString(680, d, str(("%.2f" % float(result['TAXRATE']))))  # taxRate
    except:
        c.drawAlignedString(680, d, str(("%.2f" % float(00.00))))
    try:
        c.drawAlignedString(740, d , str(format_currency("%.2f" % float(result['CALCULATEDVALUERCC']), '', locale='en_IN')))  # tax Amount
    except:
        c.drawAlignedString(740, d, str(("%.2f" % float(00.00))))

def itemdetail( result,d):
    fonts(9)
    try:
        c.drawString(110, d, result['PRODUCT'] + ' ' + result['QUALITY'])
        c.drawString(565, d, "0 ")  # Boxes
        c.drawAlignedString(625, d, str(("%.3f" % float(result['QUANTITY']))))  # Quanitity
        c.drawAlignedString(680, d, str(format_currency("%.2f" % float(result['RATE']), '', locale='en_IN')))  # Rate
        rate = float(result['RATE'])
        quantity = float(result['QUANTITY'])
        sumtotal = rate * quantity
        c.drawAlignedString(740, d, str(format_currency("%.2f" % float(sumtotal), '', locale='en_IN')))
        # c.drawAlignedString(740, d, str(format_currency("%.2f" % float(result['GROSSAMOUNT']), 'INR', locale='en_IN')))  # Gross Amount
    except:
        print("problem in itemdetail functino ")
    # d+40

def printtotal():
    c.drawString(565, d, str("%2.f" % float(TotalBoxes)))  # Boxes
    c.drawAlignedString(625, d, str(("%.3f" % float(Totalquantity))))  # Quanitity
    c.drawAlignedString(740, d, str(format_currency("%.2f" % float(InvoiceAmountTotal), '', locale='en_IN')))
def itemcodes(result, d):
    fonts(8)
    # c.drawString(10, d, "ITEMCODE : " + str(result['ITEMCODE']))
    c.drawString(10, d, "ITEMCODE : " + str('test item code '))


def total(result):
    global InvoiceAmountTotal
    global GrossAmountTotal
    global BrkAmountTotal

    global ItemAmountTotal
    global CompanyAmountTotal
    global BasicAmount
    global TotalBoxes

    global Planttotalquantity
    global Planttotalinvoiceamount

    global Totalquantity

    try:
        InvoiceAmountTotal = InvoiceAmountTotal + (float("%.3f" % float(result['INVOICEAMOUNT'])))
    except:
        pass
    try:
        TotalBoxes = TotalBoxes + (float("%.3f" % float(result['Boxes'])))
    except:
        pass

    try:
        Totalquantity=Totalquantity +(float("%.3f"% float(result['QUANTITY'])))
    except:
        pass
    # GrossAmountTotal = GrossAmountTotal + (float("%.2f" % float(result['GROSSAMOUNT'])))
    # BrkAmountTotal = BrkAmountTotal + (float("%.3f" % float(result['GROSSAMOUNT'])))
    try:
        BasicAmount = BasicAmount + (float("%.3f" % float(result['BASICAMOUNT'])))
    except:
        print("An exception occurred in total")

    Planttotalinvoiceamount=InvoiceAmountTotal
    Planttotalquantity=TotalBoxes

    # CompanyAmountTotal = CompanyAmountTotal + (float("%.2f" % float(result['BASICVALUE'])))
def planttotal():
    global Planttotalquantity
    global Planttotalinvoiceamount
    # c.drawString(550, d, "0 ")  # Boxes
    c.drawString(110,d,"Total : ")
    c.drawAlignedString(625, d, str(("%.3f" % float(Planttotalquantity))))  # Total at the end of the plant Quanitity
    c.drawAlignedString(810, d, str(format_currency("%.2f" % float(Planttotalinvoiceamount), '', locale='en_IN')))  # Total of Invoice Amount at the end of plant
    Planttotalinvoiceamount=0
    Planttotalquantity=0
    print("plant total called")



def totalitemsummary(result):
    global InvoiceAmountTotal
    global GrossAmountTotal
    global Bills

    global ItemAmountTotal
    global CompanyAmountTotal
    global BasicAmount
    global netweight
    global TaxAmount
    global Totalquantity
    global ChargesummaryTotalquantity
    print("quantity from totalitemsummary function : " + str(result['QUANTITY']))
    try:
        InvoiceAmountTotal = InvoiceAmountTotal + (float("%.3f" % float(result['INVOICEAMOUNT'])))
        print(InvoiceAmountTotal)
    except:
        print("")
    try:
        GrossAmountTotal = GrossAmountTotal + (float("%.2f" % float(result['GROSSAMOUNT'])))
        print(GrossAmountTotal)
    except:
        print("")
    try:
        Bills = Bills + int(result['BILLS'])
        print(Bills)
    except:
        print("")
    try:
        BasicAmount = BasicAmount + (float("%.3f" % float(result['BASICAMOUNT'])))
        print(BasicAmount)
    except:
        print("An exception occurred in total")
    try:
        TaxAmount = TaxAmount + (float("%.2f" % float(result['TAXAMOUNT'])))
        print(TaxAmount)
    except:
        print("")
    try:
        netweight = netweight + (float("%.2f" % float(result['NETWEIGHT'])))
        print(TaxAmount)
    except:
        print("")
    try:
        ChargesummaryTotalquantity = ChargesummaryTotalquantity + (float("%.3f" % float(result['QUANTITY'])))
        print("Quantity : item chargers")
        print(Totalquantity)
    except:
        print("not able to get Quantity : item chargers ")
    try:
        InvoiceAmountTotal = InvoiceAmountTotal + BasicAmount+GrossAmountTotal
        print(InvoiceAmountTotal)
    except:
        print("")




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
    d = 480
    return d


def itemcodeclean():
    #global ItemQuentityTotal
    global ItemAmountTotal
    # ItemQuentityTotal = 0
    ItemAmountTotal = 0


def companyclean():
    global CompanyQuentityTotal
    global CompanyAmountTotal

    CompanyQuentityTotal = 0
    CompanyAmountTotal = 0

def newrequest():
    global divisioncode
    divisioncode=[]
    global invoiceno
    invoiceno=[]
    global itemcode
    itemcode=[]
def printproducttaxdetail(c, result, d ):
    d=dvalue()


def textsize(c, result, d, stdt, etdt):
    d = dvalue()
    partyname.append(result['BUYER'])
    invoiceno.append(result['INVOICENO'])
    divisioncode.append(result['DIVI'])
    plantname.append(result['PLANT'])
    itemname.append(result['PRODUCT'])
    rate.append(result['RATE'])
    if len(divisioncode) == 1:
        if len(invoiceno) == 1:
            # if d > 14:
            header(stdt, etdt, plantname)
                # header(stdt, etdt, divisioncode)
            data(result, d)
    elif divisioncode[-1] == divisioncode[-2]:
        if plantname[-1]!=plantname[-2]:
            planttotal()
        if invoiceno[-1]==invoiceno[-2] and partyname[-1]==partyname[-2]:
            itemdetail(result, d)
            # d = dvalue10()
        else:
            data(result,d)
            # planttotal()
    elif divisioncode[-1]!=divisioncode[-2]:
        planttotal()

    total(result)

def header2(stdt, etdt, divisioncode):
    fonts(15)
    # print('from header  2 ')
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(430, 560, divisioncode[-1])
    fonts(9)
    c.drawCentredString(430, 550, "Sales item Summary Report From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')))
    c.drawCentredString(420, 600, "Sales Item Summary")
    c.line(0, 540, 850, 540)
    p = page()

    d=dvalue()
    c.drawString(10, 525, "Item")
    c.drawString(360, 525, "Quantity")
    c.drawString(430, 525, "Avg. Rate")
    c.drawString(510, 525, "Basic Amt.")
    # c.drawString(700, 530, "Gross Amount")
    # c.drawString(770, d, "Excise Amt.")
    c.drawString(600, 525, "Gross Amt.")
    c.drawString(650, 525, "Comm Rt")
    c.drawString(720, 525, "Boxes")
    c.drawString(770, 525, "Bills")
    c.line(0, 520, 850, 520)

def textsize1(c, result, d, stdt, etdt):
    divisioncode.append(result['DIVI'])
    itemcode.append('item code')
    plantname.append(result['PLANT'])
    print("quantity : "+str(result['QUANTITY']))
    if len(divisioncode) == 1:
        if d > 14:
            # header1(stdt, etdt, divisioncode)
            header1(stdt, etdt, plantname)
            totalitemsummary(result)
            taxdetailscharges(result,d)
    elif divisioncode[-1] == divisioncode[-2]:
        totalitemsummary(result)
        taxdetailscharges(result, d)
    elif divisioncode[-1] != divisioncode[-2]:
        totalitemsummary(result)
        taxdetailscharges(result, d)
        c.showPage()
        d = newpage()

def textsize2(c, result, d, stdt, etdt):
    # d = dvalue()
    divisioncode.append(result['DIVI'])
    plantname.append(result['PLANT'])
    itemcode.append('item code')
    if len(divisioncode) == 1:
        if len(itemcode) == 1:
            if d > 14:
                header2(stdt, etdt, plantname)
                # d = dvalue()
                data2(result, d)
        # DATA
        elif itemcode[-1] == itemcode[-2]:
            # d=dvalue10()
            data2(result, d)
        else:
            # d = dvalue10()
            fonts(8)
            c.drawString(110, d, str(itemcode[-2]) + " TOTAL : ")
            # c.drawAlignedString(225, d, str("%.3f" % float(ItemQuentityTotal)))
            # c.drawAlignedString(300, d, str("%.2f" % float(ItemAmountTotal)))
            itemcodeclean()
            d = dvalue10()
            data2(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        if len(itemcode) == 1:
            if d > 14:
                d = dvalue10()
                data2(result, d)

        elif itemcode[-1] == itemcode[-2]:
            data2(result, d)
        else:
            # d = dvalue10()
            fonts(8)
            c.drawString(110, d, str(itemcode[-2]) + " TOTAL : ")
            # c.drawAlignedString(225, d, str("%.3f" % float(ItemQuentityTotal)))
            # c.drawAlignedString(300, d, str("%.2f" % float(ItemAmountTotal)))
            itemcodeclean()

            # d = dvalue10()

            # d = dvalue10()
            data2(result, d)

    elif divisioncode[-1] != divisioncode[-2]:

        if len(itemcode) == 1:

            if d > 14:

                d = dvalue10()
                data2(result, d)

        elif itemcode[-1] == itemcode[-2]:
            data2(result, d)

        else:
            # d = dvalue10()
            fonts(8)
            c.drawString(110, d, str(itemcode[-2]) + " TOTAL : ")
            # c.drawAlignedString(225, d, str("%.3f" % float(ItemQuentityTotal)))
            # c.drawAlignedString(300, d, str("%.2f" % float(ItemAmountTotal)))
            itemcodeclean()
            d = dlocvalue(d)

            fonts(8)
            c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            c.drawAlignedString(225, d, str("%.3f" % float(CompanyQuentityTotal)))
            c.drawAlignedString(300, d, str("%.2f" % float(CompanyAmountTotal)))

            companyclean()

            c.showPage()

            header1(stdt, etdt, divisioncode)
            d = newpage()
            # d = dvalue()

            data2(result, d)

def data1(result,d):
    fonts(8)
    c.drawString(10, d, "Total Invoice : ")
    c.drawString(540, d, str(result['BILLS']))
    c.drawString(10, d-10, "Net Weight : ")
    c.drawString(540, d-10, result['NETWEIGHT'])
    # c.drawString(30, d, "GROSS AMOUNT : ")
    # c.drawString(540, d, result['NETWEIGHT'])
    #

def data2(result, d):
    fonts(8)
    # d=dvalue10()
    c.drawString(10, d, result['PRODUCT']+' '+result['QUALITY'])                                     # Product
    c.drawAlignedString(380, d, str("%.3f" % float(result['QUANTITY'])))      # Quanitity
    # c.drawAlignedString(625, d, str(("%.0f" % float(result['QUANTITY']))))
    bacis=float(result['BASICAMOUNT'])
    qty=float(result['QUANTITY'])
    rate=bacis/qty
    # print(rate)
    c.drawAlignedString(460, d, str(format_currency("%.2f" % float(rate), '', locale='en_IN')))          # Rate
    c.drawAlignedString(540, d, str(format_currency("%.2f" % float(result['BASICAMOUNT']), '', locale='en_IN')))
    # c.drawString(110, d, result['RATE'])
    # c.drawAlignedString(810, d,  str(("%.2f" % float(result['INVOICEAMOUNT']))))  # Invoice Amount
    # x= dvalue()
    # c.drawString(320, 530, "ITEM")
    # c.drawAlignedString(320, x, str(("%.2f" % float(result['GROSSAMOUNT']))))  # Gross Amount
    # c.drawString(550, d, "0 ")                                              # Boxes
    c.drawString(730, d, "0")
    c.drawString(780, d, str(("%.0f" % float(result['BILLS']))))
    total(result)

    # logic(result)

def checkcount(resultcounter):
    invoiceno.append(str(resultcounter['INVOICENO']))
    global test
    try:
        print('invoice check ' + str(resultcounter['TOTALITEM']))
        invoicenocounter.append(resultcounter['TOTALITEM'])
        invoicenocheck.append(resultcounter['INVOICENO'])
        print('invoice  added ' + str(resultcounter['INVOICENO']))
    except:
        pass
