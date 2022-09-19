from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 740

divisioncode = []
BankName = []
pageno = 0
totalcramt = 0
totaldramt = 0
Comptotalcramt = 0
Comptotaldramt = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d -7
    return d
def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780,"Accounts Summary From "+ str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')) )
    # c.drawCentredString(300, 760, "For The Period of " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 745, 600, 745)
    c.drawString(10, 760, "Account")
    c.drawString(395, 760, "Debit Amount")
    c.drawString(525, 760, "Credit Amount")


def data(result, d):
    fonts(8)
    c.drawString(10, d, result['ACCNAME'])   #.strftime('%d-%m-%Y'))
    # c.drawString(150, d, result['DrAmt'])
    # c.drawString(250, d, result['CrAmt'])
    if (float(result['DRAMT']))!= 0:
        c.drawAlignedString(440, d, str(locale.currency(float(result['DRAMT']), grouping=True))[1:])
    if (float(result['CRAMT'])) != 0:
        c.drawAlignedString(570, d, str(locale.currency(float(result['CRAMT']), grouping=True))[1:])

    # if result['CHEQUENUMBER']!=None:
    #     c.drawString(100, d, result['CHEQUENUMBER'])
    # c.drawString(155, d, result['VCHNO'])
    # c.drawString(200, d, result['PARTYNAME'])
    # c.drawAlignedString(455, d, str(("%.3f" % float(result['PAYMENTAMT']))))
    # c.drawAlignedString(510, d, str(("%.3f" % float(result['RECEIPTAMT']))))








def total(result):
    global totalcramt
    global totaldramt
    totalcramt = totalcramt +  float(result['CRAMT'])
    totaldramt = totaldramt +  float(result['DRAMT'])

def CompanyTotal(result):
    global Comptotalcramt
    global Comptotaldramt
    Comptotalcramt = Comptotalcramt + float(result['CRAMT'])
    Comptotaldramt = Comptotaldramt + float(result['DRAMT'])

def SetTDrmtCrmtZero():
    global totaldramt
    global totalcramt
    totalcramt = 0
    totaldramt = 0

def SetCompTDrmtCrmtZero():
    global Comptotalcramt
    global Comptotaldramt
    Comptotalcramt = 0
    Comptotaldramt = 0

def logic(result):
    divisioncode.append(result['BUSINESSUNITNAME'])
    BankName.append(result['BANKNAME'])

def dlocvalue(d):
    d = d - 10
    return d

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global divisioncode
    global BankName
    global pageno
    divisioncode = []
    BankName = []
    pageno = 0


def textsize(c, result, d, stdt, etdt):
    # global OpeningBalance
    global totalcramt
    global totaldramt
    global Comptotalcramt
    global Comptotaldramt
    d = dvalue()
    logic(result)
    # SetTDrmtCrmtZero()

    if len(divisioncode) == 1:
        # total(result)
        header(stdt, etdt, divisioncode)
        SetTDrmtCrmtZero()
        SetCompTDrmtCrmtZero()
        # fonts(8)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(10, d, BankName[-1])
        fonts(8)
        d = dvalue()
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
        CompanyTotal(result)
        # if str(result['VCHDATE']) != '1980-01-01':
        #     data(result, d)
        #     c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))



    elif divisioncode[-1] == divisioncode[-2]:
        if BankName[-1] == BankName[-2]:

            # total(result)
            CompanyTotal(result)
            data(result,d)
            total(result)
        elif BankName[-1] != BankName[-2]:
            # fonts(8)

            # c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
            # c.drawAlignedString(575, d, str("%.3f" % float(OpeningBalance)))
            # companyclean()
            c.setFillColorRGB(0.0, 0.0, 0.0)
            c.setFont('Helvetica-Bold', 8)

            c.drawString(150, d,"BANK TOTAL : ")
            if (float(totaldramt))!= 0:
                c.drawAlignedString(440, d, str(locale.currency(float(totaldramt), grouping=True))[1:])
            if (float(totalcramt)) != 0:
                c.drawAlignedString(570, d, str(locale.currency(float(totalcramt), grouping=True))[1:])

            c.showPage()
            header(stdt, etdt, divisioncode)
            d = newpage()
            # d = dvalue()
            SetTDrmtCrmtZero()
            # fonts(8)
            d = dvalue()
            c.setFont('Helvetica-Bold', 8)
            c.drawString(10, d, BankName[-1])
            fonts(8)
            d = dvalue()
            d = dvalue()
            # print(BankName[-1], d)
            # total(result)
            data(result, d)
            total(result)
            CompanyTotal(result)
        # c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))

    elif divisioncode[-1] != divisioncode[-2]:
        # fonts(8)

        # c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
        # c.drawAlignedString(575, d, str("%.3f" % float(OpeningBalance)))
        # companyclean()
        c.setFillColorRGB(0, 0, 0)
        c.setFont('Helvetica-Bold',8)

        c.drawString(150, d, "BANK TOTAL : ")
        if (float(totaldramt))!= 0:
            c.drawAlignedString(440, d, str(locale.currency(float(totaldramt), grouping=True))[1:])
        if (float(totalcramt)) != 0:
            c.drawAlignedString(570, d, str(locale.currency(float(totalcramt), grouping=True))[1:])
        d = dvalue()
        d = dvalue()
        c.drawString(150, d,"Company TOTAL : ")
        if (float(Comptotaldramt))!= 0:
            c.drawAlignedString(440, d, str(locale.currency(float(Comptotaldramt), grouping=True))[1:])
        if (float(Comptotalcramt)) != 0:
            c.drawAlignedString(570, d, str(locale.currency(float(Comptotalcramt), grouping=True))[1:])
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue()
        SetTDrmtCrmtZero()
        SetCompTDrmtCrmtZero()
        c.setFont('Helvetica-Bold', 8)
        c.drawString(10, d, BankName[-1])
        fonts(8)
        d = dvalue()
        d = dvalue()
        # total(result)
        data(result,d)
        total(result)
        CompanyTotal(result)
        # openingbalance(result)
        # fonts(7)
        # c.drawString(10, 715, divisionglcode[-1])
        #
        # if float(result['OPBAL']) > 0:
        #     c.drawString(10, d, "Opening Balance")
        #     c.drawAlignedString(510, d, str(("%.3f" % float(result['RECEIPTAMT']))))
        #     c.drawAlignedString(575, d, str("%.3f" % OpeningBalance))
        # total(result)
        # d = dvalue()
        # # data(result, d)
        # if str(result['VCHDATE']) != '1980-01-01':
        #     data(result, d)
        #     c.drawAlignedString(575, d, str(("%.3f" % float(OpeningBalance))))