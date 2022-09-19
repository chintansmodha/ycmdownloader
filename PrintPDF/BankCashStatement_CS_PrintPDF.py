from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 747

divisioncode = []
CompanyName = []
# BankName = []
pageno = 0
totalcramt = 0
totaldramt = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 7
    return d
def header(stdt, etdt, CompanyName):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, CompanyName[-1])
    # division = str(divisioncode[-1])
    # if(division[31]=='P'):
    #     division=division[31:]
    # else:
    #     division=division[32:]
    fonts(9)
    c.drawCentredString(300, 780, "Consolidated Accounts Summary From "+ str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')) )
    # c.drawCentredString(300, 760, "For The Period of " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    c.drawString(10, 760, "Account")
    c.drawString(360, 760, "Debit Amount")
    c.drawString(510, 760, "Credit Amount")


def data(result, d):
    fonts(8)
    c.drawString(10, d, result['ACCNAME'])   #.strftime('%d-%m-%Y'))
    # c.drawString(150, d, result['DrAmt'])
    # c.drawString(250, d, result['CrAmt'])
    if (float(result['DRAMT']))!= 0:
        c.drawAlignedString(400, d, str(locale.currency(float(result['DRAMT']), grouping=True))[1:])
    if (float(result['CRAMT'])) != 0:
        c.drawAlignedString(560, d, str(locale.currency(float(result['CRAMT']), grouping=True))[1:])

    # if result['CHEQUENUMBER']!=None:
    #     c.drawString(100, d, result['CHEQUENUMBER'])
    # c.drawString(155, d, result['VCHNO'])
    # c.drawString(200, d, result['PARTYNAME'])
    # c.drawAlignedString(455, d, str(("%.3f" % float(result['PAYMENTAMT']))))
    # c.drawAlignedString(510, d, str(("%.3f" % float(result['RECEIPTAMT']))))








def total(result):
    global totalcramt
    global totaldramt
    if (float(result['CRAMT']))!= 0:
        totalcramt = totalcramt +  float(result['CRAMT'])
    if (float(result['DRAMT'])) != 0:
        totaldramt = totaldramt +  float(result['DRAMT'])

def SetTDrmtCrmtZero():
    global totaldramt
    global totalcramt
    totalcramt = 0
    totaldramt = 0

def logic(result):
    # divisioncode.append(result['BUSINESSUNITNAME'])
    # division = str(divisioncode[-1])

    Company = ("Beekaylon Group Of Companies ")
    CompanyName.append(Company)
    # BankName.append(result['BANKNAME'])
    # print(CompanyName)

def dlocvalue(d):
    d = d - 10
    return d

def newpage():
    global d
    d = 747
    return d

def newrequest():
    global divisioncode
    global CompanyName
    global pageno
    divisioncode = []
    CompanyName = []
    pageno = 0


def textsize(c, result, d, stdt, etdt):
    # global OpeningBalance
    global totalcramt
    global totaldramt
    d = dvalue()
    logic(result)
    # SetTDrmtCrmtZero()

    if len(CompanyName) == 1:
        # total(result)
        header(stdt, etdt, CompanyName)
        SetTDrmtCrmtZero()
        fonts(8)
        # c.drawString(250, d, BankName[-1])
        d = dvalue()
        # openingbalance(result)
        # fonts(7)
        # c.drawString(10, 715, divisionglcode[-1] )
        #
        # if float(result['OPBAL']) > 0:
        #     c.drawString(10, d, "Opening Balance" )
        #     c.drawAlignedString(510, d, str(("%.3f" % float(result['RECEIPTAMT']))))
        #     c.drawAlignedString(575, d, str("%.3f" % OpeningBalance))
        # d=dvalue()
        # total(result)
        data(result, d)
        total(result)
        # if str(result['VCHDATE']) != '1980-01-01':
        #     data(result, d)
        #     c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))



    elif CompanyName[-1] == CompanyName[-2]:
        # if BankName[-1] == BankName[-2]:

        # total(result)
        data(result,d)
        total(result)
        # elif BankName[-1] != BankName[-2]:
        #     fonts(9)
        #
        #     # c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
        #     # c.drawAlignedString(575, d, str("%.3f" % float(OpeningBalance)))
        #     # companyclean()
        #     c.setFillColorRGB(0, 0, 0)
        #     c.drawString(10, d, BankName[-2] + " " + "BANK TOTAL : ")
        #     c.drawAlignedString(400, d, str(locale.currency(float(totaldramt), grouping=True))[1:])
        #     c.drawAlignedString(550, d, str(locale.currency(float(totalcramt), grouping=True))[1:])
        #
        #
        #     # header(stdt, etdt, divisioncode)
        #     # d = newpage()
        #     d = dvalue()
        #     d = dvalue()
        #     SetTDrmtCrmtZero()
        #     fonts(7)
        #     d = dvalue()
        #     c.drawString(250, d, BankName[-1])
        #     d = dvalue()
        #     # total(result)
        #     data(result, d)
        #     total(result)
        # c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))

    # elif CompanyName[-1] != CompanyName[-2]:
    #     fonts(9)
    #
    #     # c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
    #     # c.drawAlignedString(575, d, str("%.3f" % float(OpeningBalance)))
    #     # companyclean()
    #     c.setFillColorRGB(0, 0, 0)
    #     c.drawString(10, d, " TOTAL : ")
    #     c.drawAlignedString(400, d, str(locale.currency(float(totaldramt), grouping=True))[1:])
    #     c.drawAlignedString(560, d, str(locale.currency(float(totalcramt), grouping=True))[1:])
    #     c.showPage()
    #
    #     header(stdt, etdt, CompanyName)
    #     d = newpage()
    #     d = dvalue()
    #     SetTDrmtCrmtZero()
    #     fonts(7)
    #     # c.drawString(250, d, BankName[-1])
    #     d = dvalue()
    #     # total(result)
    #     data(result,d)
    #     total(result)
    #     # openingbalance(result)
    #     # fonts(7)
    #     # c.drawString(10, 715, divisionglcode[-1])
    #     #
    #     # if float(result['OPBAL']) > 0:
    #     #     c.drawString(10, d, "Opening Balance")
    #     #     c.drawAlignedString(510, d, str(("%.3f" % float(result['RECEIPTAMT']))))
    #     #     c.drawAlignedString(575, d, str("%.3f" % OpeningBalance))
    #     # total(result)
    #     # d = dvalue()
    #     # # data(result, d)
    #     # if str(result['VCHDATE']) != '1980-01-01':
    #     #     data(result, d)
    #     #     c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))