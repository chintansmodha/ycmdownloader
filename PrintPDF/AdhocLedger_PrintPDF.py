from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from textwrap import wrap
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

def dvalueIn():
    global d
    d = d + 5
    return d

def header(stdt, etdt, divisioncode, LMMergeCompany, LMMergeSubAcc ):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(8)
    if LMMergeCompany == ['true']:
        c.drawCentredString(300, 780,"Adhoc Ledger with Merge Company Report From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                            etdt.strftime('%d-%m-%Y')))
    else:
        if LMMergeSubAcc == ['true']:
            c.drawCentredString(300, 780, "Adhoc Ledger Without Subaccount From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                etdt.strftime('%d-%m-%Y')))
        else:
            c.drawCentredString(300, 780,"Adhoc Ledger From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
                                etdt.strftime('%d-%m-%Y')))

    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 600, 775)
    c.line(0, 750, 600, 750)
    # Upperline in header
    c.drawString(10, 760, "Vch. Date")
    c.drawString(52, 760, "TXN")
    c.drawString(80, 760, "Vch.No.")
    c.drawString(160, 760, "Chq.No.")
    # if LMMergeCompany == ['true']:
    #     c.drawString(230, 760, "Ref. No.")
    # else:
    c.drawString(230, 760, "Doc.No.")
    c.drawString(362, 760, "Debit Amt.")
    c.drawString(450, 760, "Credit Amt.")
    c.drawString(540, 760, "Cum Amt.")
    # c.drawString(545, 760, "Status")


def data(result, d ,LCNarration, LMMergeCompany):
    fonts(7)
    if str(result['VCHDATE']) != '1900-01-01':
        c.drawString(10, d, result['VCHDATE'].strftime('%d-%m-%Y'))
        c.drawString(55, d, result['TXNTYPE'])
        c.drawString(75, d, result['VCHNO'])
        c.drawString(165, d, result['CHQNO'])
        c.drawString(230, d, result['DOCNO'])
        if float(result['DRAMOUNT']) != 0:
            c.drawAlignedString(390, d, result['DRAMOUNT'])
        if float(result['CRAMOUNT']) != 0:
            c.drawAlignedString(480, d, result['CRAMOUNT'])
        #************ CUM Amt *****************************************
        if openingbalance != 0:
            if openingbalance < 0:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(-openingbalance))+ ' CR')
            else:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance))+ ' DR')
        else:
            c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)))
        #************************** NARRATION *********************************************
        if LCNarration == ['1']:
            if (result['HDRREMARKS']) != '':
                d = dvalue()
                d = dvalue()
                c.drawString(52, d, result['HDRREMARKS'])
                d = dvalue()
                # d = dvalue()

def total(result):
    global openingbalance
    if str(result['VCHDATE']) != '1900-01-01':
        openingbalance = openingbalance + float(result['DRAMOUNT']) - float(result['CRAMOUNT'])

def OpeningBalance(result):
    global openingbalance
    global CRAmountTotal
    global DRAmountTotal
    # if str(result['VCHDATE']) != '1900-01-01':
    openingbalance = float(result['OPBAL'])
    if float(result['OPBAL']) < 0:
        CRAmountTotal = -float(result['OPBAL'])
    if float(result['OPBAL']) > 0:
        DRAmountTotal = float(result['OPBAL'])

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

def CompanyAmtclean():
    global openingbalance
    global CRAmountTotal
    global DRAmountTotal
    openingbalance = 0
    CRAmountTotal = 0
    DRAmountTotal = 0

def CompanyAmttotal(result):
    global CRAmountTotal
    global DRAmountTotal
    CRAmountTotal = CRAmountTotal + float(result['CRAMOUNT'])
    DRAmountTotal = DRAmountTotal + float(result['DRAMOUNT'])

def textsize(c, result, d, stdt, etdt, LCEject, LCNarration, LMMergeCompany, LMMergeSubAcc ):
    d = dvalue()
    logic(result)
    # CompanyAmtclean()

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode, LMMergeCompany , LMMergeSubAcc)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(10, d, account[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        CompanyAmtclean()
        OpeningBalance(result)
        # ******************Opening Balance Check and Print *******************
        c.drawString(10, d, "Opening Balance As On " + stdt.strftime("%d %b %Y"))
        if float(openingbalance) != 0:
            if float(openingbalance) < 0:
                c.drawAlignedString(480, d, str('{0:1.2f}'.format(-openingbalance)))  # --- CRAmt
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
            else:
                c.drawAlignedString(390, d, str('{0:1.2f}'.format(openingbalance)))  #--DRAmt
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
        else:
            if LMMergeCompany != ['true']:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)))
        #   ***********Data Printing***************************
        if str(result['VCHDATE']) != '1900-01-01':
            d = dvalue()
            d = dvalue()
        total(result)
        data(result,d,LCNarration, LMMergeCompany)
        CompanyAmttotal(result)
        # print('Dr :', DRAmountTotal)
        # print('Cr :',CRAmountTotal)


    elif divisioncode[-1] == divisioncode[-2]:
        fonts(7)
        if account[-1] == account[-2]:
            total(result)
            data(result,d,LCNarration, LMMergeCompany)
            CompanyAmttotal(result)
        else:
            #*************** total print Before AcccountName Change ******************
            # d = dvalue()
            #***************** LINE START **************************
            if LMMergeCompany == ['true']:
                d = dvalueIn()
                c.line(340, d, 500, d)
                d = dvalue()
                d = dvalue()
                c.setFont('Helvetica-Bold', 7)
                c.drawAlignedString(480, d, str('{0:1.2f}'.format(CRAmountTotal)))
                c.drawAlignedString(390, d, str('{0:1.2f}'.format(DRAmountTotal)))
            else:
                c.setFont('Helvetica-Bold', 7)
                c.drawString(270, d, 'Totals :')
            #*************************************************
                if float(CRAmountTotal) != 0:
                    c.drawAlignedString(480, d, str('{0:1.2f}'.format(CRAmountTotal)))
                if float(DRAmountTotal) != 0:
                    c.drawAlignedString(390, d, str('{0:1.2f}'.format(DRAmountTotal)))
                if float(openingbalance) != 0:
                    if float(openingbalance) > 0:
                        c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
                    else:
                        c.drawAlignedString(570, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
                else:
                    c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)))
            #******************** LINE END *************************
            if LMMergeCompany == ['true']:
                d = dvalue()
                c.line(340, d, 500, d)
            #****************************************************
            CompanyAmtclean()
            #************************               **************************
            d = dvalue()
            d = dvalue()
            if LCEject == ['1']:
                c.showPage()
                d = newpage()
                header(stdt, etdt, divisioncode, LMMergeCompany, LMMergeSubAcc )
                d = dvalue()
                c.setFont('Helvetica-Bold', 7)
            c.drawString(10, d, account[-1])
            d = dvalue()
            d = dvalue()
            fonts(7)
            # ******************Opening Balance Check and Print *******************
            OpeningBalance(result)
            c.drawString(10, d, "Opening Balance As On " + stdt.strftime("%d %b %Y"))
            if float(openingbalance) != 0:
                if float(openingbalance) < 0:
                    c.drawAlignedString(480, d, str('{0:1.2f}'.format(-openingbalance)))  # --- CRAmt
                    c.drawAlignedString(570, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
                else:
                    c.drawAlignedString(390, d, str('{0:1.2f}'.format(openingbalance)))  # --DRAmt
                    c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
            else:
                if LMMergeCompany != ['true']:
                    c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)))
            # ***********Data Printing***************************
            if str(result['VCHDATE']) != '1900-01-01':
                d = dvalue()
                d = dvalue()
            total(result)
            data(result,d,LCNarration, LMMergeCompany)
            CompanyAmttotal(result)


    elif divisioncode[-1] != divisioncode[-2]:
        # *************** total print Before Company Change ******************
        c.setFont('Helvetica-Bold', 7)
        # d = dvalue()
        c.drawString(270, d, 'Totals :')
        if float(CRAmountTotal) != 0:
            c.drawAlignedString(480, d, str('{0:1.2f}'.format(CRAmountTotal)))
        if float(DRAmountTotal) != 0:
            c.drawAlignedString(390, d, str('{0:1.2f}'.format(DRAmountTotal)))
        if float(openingbalance) != 0:
            if float(openingbalance) > 0:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
            else:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
        else:
            c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)))
        CompanyAmtclean()
        # ************************               **************************
        c.showPage()
        d = newpage()
        header(stdt, etdt, divisioncode, LMMergeCompany, LMMergeSubAcc )
        d = dvalue()
        c.setFont('Helvetica-Bold', 7)
        c.drawString(10, d, account[-1])
        d = dvalue()
        d = dvalue()
        fonts(7)
        # ******************Opening Balance Check and Print *******************
        OpeningBalance(result)
        c.drawString(10, d, "Opening Balance As On " + stdt.strftime("%d %b %Y"))
        if float(openingbalance) != 0:
            if float(openingbalance) < 0:
                c.drawAlignedString(480, d, str('{0:1.2f}'.format(-openingbalance)))  # --- CRAmt
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(-openingbalance)) + ' CR')
            else:
                c.drawAlignedString(390, d, str('{0:1.2f}'.format(openingbalance)))  # --DRAmt
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)) + ' DR')
        else:
            if LMMergeCompany != ['true']:
                c.drawAlignedString(570, d, str('{0:1.2f}'.format(openingbalance)))
        # ***********Data Printing***************************
        if str(result['VCHDATE']) != '1900-01-01':
            d = dvalue()
            d = dvalue()
        total(result)
        data(result,d,LCNarration, LMMergeCompany)
        CompanyAmttotal(result)