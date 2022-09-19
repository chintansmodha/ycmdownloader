import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal
pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))

c = canvas.Canvas("1.pdf")
d = 745

divisioncode = []
account = []
subaccount = []
AccountSubAcc = []
pageno = 0
date=[]
openingbalance = 0
CRAmountTotal = 0
DRAmountTotal = 0
ClosingBalance = 0
# string1 = ''
# DocumentType = []
def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue():
    global d
    d = d - 5
    return d

def dincrease():
    global d
    d = d + 10

def header(stdt, etdt, divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(8)
    c.drawCentredString(300, 780,"Adhoc Ledger From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))

    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 750, 600, 750)
    # Upperline in header
    c.drawString(10, 760, "Party")
    c.drawString(220, 760, "PAN")
    c.drawString(310, 760, "Op.Balance")
    c.drawString(390, 760, "Dr.Amount")
    c.drawString(465, 760, "Cr.Amount")
    c.drawString(540, 760, "Cl.Balance")


def data(result, d ,LCNarration, LCAddress):
    fonts(7)
    if float(float(result['OPBAL']) + float(result['DRAMOUNT']) + float(result['CRAMOUNT'])) != 0:
        c.drawString(10, d, result['SUBACCOUNT'])
        c.drawString(215, d, result['PAN'])
        if float(result['OPBAL']) != 0:
            if float(result['OPBAL']) < 0:
                c.drawAlignedString(335, d, str('{0:1.2f}'.format(-float(result['OPBAL']))) + ' CR')
            if float(result['OPBAL']) > 0:
                c.drawAlignedString(335, d, result['OPBAL'] + ' DR')
        else:
            c.drawAlignedString(335, d, result['OPBAL'])
        c.drawAlignedString(420, d, result['DRAMOUNT'])
        c.drawAlignedString(495, d, result['CRAMOUNT'])
        if float(result['CLBAL']) != 0:
            if float(result['CLBAL']) < 0:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(-float(result['CLBAL']))) + ' CR')
            if float(result['CLBAL']) > 0:
                c.drawAlignedString(570, d, result['CLBAL'] + ' DR')
        else:
            c.drawAlignedString(570, d, result['CLBAL'])
        # ************************** NARRATION *********************************************
        # if LCNarration == ['1']:
        #     if (result['HDRREMARKS']) != '':
        #         d = dvalue()
        #         d = dvalue()
        #         c.drawString(52, d, result['HDRREMARKS'])
        #         d = dvalue()
        #         d = dvalue()

        #****************************** ADDRESS ********************************************
        # result['ADDRESS1'], result['ADDRESS2'], result['CITY'], result['DISTRICT'], break_long_words=False
        if LCAddress != ['0']:
            c.setFillColor('_CMYK_black')#_CMYK_black
            str1  = ''
            string = str1.join(result['ADDRESS'])
            res = sum(not chr.isspace() for chr in string)
            if res != 0:
                d = dvalue()
                d = dvalue()
                # c.drawString(10, d, string)
                wrap_text = textwrap.wrap(string, width=70)
                # print(len(wrap_text))
                if len(wrap_text) != 2:
                    c.drawString(10, d, wrap_text[0])
                else:
                    if len(wrap_text) == 3:
                        c.drawString(10, d, wrap_text[0])
                        d = dvalue()
                        d = dvalue()
                        c.drawString(10, d, wrap_text[1])
                        d = dvalue()
                        d = dvalue()
                        c.drawString(10, d, wrap_text[2])
                    else:
                        c.drawString(10, d, wrap_text[0])
                        d = dvalue()
                        d = dvalue()
                        c.drawString(10, d, wrap_text[1])
                # if len(string) >= 75:
                #     wrap_text = textwrap.wrap(string, width=75)
                #     c.drawString(10, d, wrap_text[0])
                #     d = dvalue()
                #     d = dvalue()
                #     c.drawString(10, d,wrap_text[1])
                # elif len(string) < 4:
                #     d = dincrease()
                #     d = dincrease()
                # else:
                #     c.drawString(10, d, string)

            # if str(result['ADDRESS1A']) != '':
            #     d = dvalue()
            #     d = dvalue()
            #     if str (result['ADDRESS1B']) or str (result['ADDRESS1C']) != '':
            #         string  = str(result['ADDRESS1A'] + ' ' + result['ADDRESS1B'] + ' ' + result['ADDRESS1C'])
            #         if len(string) >= 75:
            #             wrap_text = textwrap.wrap(string, width=75)
            #         # print(string)
            #             c.drawString(10, d, wrap_text[0])
            #             d = dvalue()
            #             d = dvalue()
            #             c.drawString(10, d,wrap_text[1])
            #         else:
            #             c.drawString(10, d, string)
            #     else:
            #         string = str(result['ADDRESS1A'])
            #         if len(string) >= 75:
            #             wrap_text = textwrap.wrap(string, width=75)
            #             # print(string)
            #             c.drawString(10, d, wrap_text[0])
            #             d = dvalue()
            #             d = dvalue()
            #             c.drawString(10, d, wrap_text[1])
            #         else:
            #             c.drawString(10, d, string)
            # if str(result['ADDRESS2A']) != '':
            #     d = dvalue()
            #     d = dvalue()
            #     if str (result['ADDRESS2B']) or str (result['ADDRESS2C']) != '':
            #         c.drawString(10, d, str(result['ADDRESS2A'] + ' ' + result['ADDRESS2B'] + ' ' + result['ADDRESS2C']))
            #         # c.drawString(10, d, textwrap.wrap(result['ADDRESS2A'] + ' ' + result['ADDRESS2B'] + ' ' + result['ADDRESS2C'], 12))
            #     else:
            #         c.drawString(10, d, result['ADDRESS2A'])
            # elif str(result['ADDRESS2B']) != '':
            #     d = dvalue()
            #     d = dvalue()
            #     if str(result['ADDRESS2C']) != '':
            #         c.drawString(10, d, str(result['ADDRESS2B'] + ' ' + result['ADDRESS2C']))
            #         # c.drawString(10, d, textwrap.wrap(result['ADDRESS2B'] + ' ' + result['ADDRESS2C'],12))
            #     else:
            #         c.drawString(10, d, result['ADDRESS2B'])
            # if str(result['CITY']) !='':
            #     d = dvalue()
            #     d = dvalue()
            #     if str(result['CITY']) == str(result['DISTRICT']) :
            #         c.drawString(10, d, "City & Dist- " + result['CITY'])
            #     else:
            #         c.drawString(10, d, "City- " + result['CITY'])
            # if str(result['DISTRICT']) != ' ':
            #     if str(result['CITY']) != str(result['DISTRICT']):
            #         d = dvalue()
            #         d = dvalue()
            #         c.drawString(10, d, "Dist- " + result['DISTRICT'])
    else:
        d = dincrease()
    c.setFillColor('black')
    #***********************            *******************************************


def logic(result):
    global divisioncode
    global account
    # global subaccount
    # global AccountSubAcc
    divisioncode.append(result['BUSINESSUNIT'])
    account.append(result['GLACCOUNT'])
    # subaccount.append(result['SUBACCOUNT'])

def newpage():
    global d
    d = 745
    return d

def newrequest():
    global divisioncode
    global pageno
    global account
    divisioncode = []
    pageno = 0
    account = []

def CompanyAmtTotal(result):
    global openingbalance
    global CRAmountTotal
    global DRAmountTotal
    global ClosingBalance
    openingbalance = openingbalance + float(result['OPBAL'])
    DRAmountTotal = DRAmountTotal + float(result['DRAMOUNT'])
    CRAmountTotal = CRAmountTotal + float(result['CRAMOUNT'])
    ClosingBalance = ClosingBalance + float(result['CLBAL'])

def CompanyAmtClean():
    global openingbalance
    global CRAmountTotal
    global DRAmountTotal
    global ClosingBalance
    openingbalance = 0
    DRAmountTotal =  0
    CRAmountTotal =  0
    ClosingBalance =  0

def textsize(c, result, d, stdt, etdt, LCEject, LCNarration, LCAddress ):
    d = dvalue()
    logic(result)
    # CompanyAmtClean()

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        CompanyAmtClean()
        # if float(result['OPBAL']) and float(result['DRAMOUNT']) and float(result['CRAMOUNT']) != 0:
        c.setFont('Helvetica-Bold', 7)
        c.drawString(10, d, account[-1])
        d = dvalue()
        d = dvalue()
        data(result,d,LCNarration, LCAddress)
        CompanyAmtTotal(result)


    elif divisioncode[-1] == divisioncode[-2]:
        if account[-1] == account[-2]:
            data(result,d,LCNarration, LCAddress)
            CompanyAmtTotal(result)

        else:
            c.setFont('Helvetica-Bold', 7)
            c.drawString(230, d, "Totals :")
            if float(openingbalance) != 0:
                if float(openingbalance) < 0:
                    c.drawAlignedString(335, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
                else:
                    c.drawAlignedString(335, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
            else:
                c.drawAlignedString(335, d, str('{0:1.2f}'.format(openingbalance)))
            c.drawAlignedString(420, d, str('{0:1.2f}'.format(DRAmountTotal)))
            c.drawAlignedString(495, d, str('{0:1.2f}'.format(CRAmountTotal)))
            if float(ClosingBalance) != 0:
                if float(ClosingBalance) < 0:
                    c.drawAlignedString(570, d, str('{0:1.2f}'.format(-ClosingBalance)) + ' CR')
                else:
                    c.drawAlignedString(570, d, str('{0:1.2f}'.format(ClosingBalance)) + ' DR')
            else:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(ClosingBalance)))
            CompanyAmtClean()
            d = dvalue()
            d = dvalue()
            # if LCEject == ['1']:
            #     c.showPage()
            #     d = newpage()
            #     header(stdt, etdt, divisioncode)
            #     d = dvalue()
            #     c.setFont('Helvetica-Bold', 7)
            c.drawString(10, d, account[-1])
            d = dvalue()
            d = dvalue()
            data(result,d,LCNarration, LCAddress)
            CompanyAmtTotal(result)

    elif divisioncode[-1] != divisioncode[-2]:
        c.setFont('Helvetica-Bold', 7)
        c.drawString(230, d, "Totals :")
        if float(openingbalance) != 0:
            if float(openingbalance) < 0:
                c.drawAlignedString(335, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
            else:
                c.drawAlignedString(335, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
        else:
            c.drawAlignedString(335, d, str('{0:1.2f}'.format(openingbalance)))
        c.drawAlignedString(420, d, str('{0:1.2f}'.format(DRAmountTotal)))
        c.drawAlignedString(495, d, str('{0:1.2f}'.format(CRAmountTotal)))
        if float(ClosingBalance) != 0:
            if float(ClosingBalance) < 0:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(-ClosingBalance)) + ' CR')
            else:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(ClosingBalance)) + ' DR')
        else:
            c.drawAlignedString(570, d, str('{0:1.2f}'.format(ClosingBalance)))
        CompanyAmtClean()
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode)
        d = dvalue()
        c.setFont('Helvetica-Bold', 7)
        c.drawString(10, d, account[-1])
        d = dvalue()
        d = dvalue()
        data(result,d,LCNarration, LCAddress)
        CompanyAmtTotal(result)