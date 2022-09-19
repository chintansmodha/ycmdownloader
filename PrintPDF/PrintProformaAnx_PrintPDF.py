import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")
d = 440
Yordno = 760
i = 0
pageno = 0

divisioncode = []
invoiceno = []
orderno = []
lotno = []
itemname = []
itemtype = []
hsncode = []
payment = []
Remark = []
countryofOrigin = []
grosswt = 0
netwt = 0
packages = 0

def page():
    global pageno
    pageno = pageno + 1
    return pageno


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)

def dvalue():
    global d
    d = d - 5
    return d

def dvalueincrese():
    global d
    d = d + 10
    return d

def updatedvalue():
    global d
    d = 190
    return d

def yordnovalue():
    global Yordno
    Yordno = Yordno - 8
    return Yordno

def wrap(string, type, width, x, y):
    global i
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        y = y - 8
        e = e + 1
        i = i + 1
    return s

def header(divisioncode, result,Yordno):
    c.setTitle('Annexure - 1')
    boldfonts(10)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(290, 790, 'ANNEXURE - 1')
    boldfonts(7)
    c.drawCentredString(290, 778, 'INFORMATION ABOUT VARIFIED GROSS MASS (VGM) OF CONTAINER')
    c.drawCentredString(290, 778, '___________________________________________________________')
    c.drawString(45, 765, 'Master Exp No. :   ' + str(result['MASTEREXPNO']) )
    c.drawString(400, 765, 'GST - Invoice No. :   ' + str(result['GSTINVOICENO']))
    #Horizontal line
    c.line(35, 800, 560, 800)# Upper line
    c.line(35, 761, 560, 761)#1
    c.line(35, 731, 560, 731)#2
    c.line(35, 701, 560, 701)#3
    c.line(35, 671, 560, 671)#4
    c.line(35, 641, 560, 641)#5
    c.line(35, 611, 560, 611)#6
    c.line(35, 581, 560, 581)#7
    c.line(35, 541, 560, 541)#8
    c.line(35, 441, 560, 441)#9
    c.line(35, 321, 560, 321)#10
    c.line(35, 291, 560, 291)#11
    c.line(35, 261, 560, 261)#12
    c.line(35, 231, 560, 231)#13
    c.line(35, 201, 560, 201)#14
    c.line(35, 60, 560, 60)# Lower Line

    #Vertical Line
    c.line(35, 800, 35, 60)
    c.line(60, 761, 60, 61)#sr No
    c.line(261, 761, 261, 61)#Mid ************
    c.line(560, 800, 560, 60)
    #Refrence Box
    c.drawAlignedString(55, 750, '1')  #1
    c.drawAlignedString(55, 720, '2')  # 2
    c.drawAlignedString(55, 690, '3')  # 3
    c.drawAlignedString(55, 660, '4')  # 4
    c.drawAlignedString(55, 630, '5')  # 5
    c.drawAlignedString(55, 600, '6')  # 6
    c.drawAlignedString(55, 570, '7')  # 7
    c.drawAlignedString(55, 530, '8')  # 8
    c.drawAlignedString(55, 430, '9')  # 9
    c.drawAlignedString(55, 310, '10')  # 10
    c.drawAlignedString(55, 280, '11')  # 11
    c.drawAlignedString(55, 250, '12')  # 12
    c.drawAlignedString(55, 220, '13')  # 13
    # c.drawAlignedString(55, 190, '14')  # 14
    fonts(7)
    c.drawString(65, 750, 'NAME OF THE SHIPPER')  # 1
    c.drawString(65, 720, 'SIPPER IEC NO.')  # 2
    # c.drawString(65, 690, '3')  # 3
    str1 = 'NAME OF THE DESIGNATION OF OFFICIAL OF THE SHIPPER AUTHORISED TO SIGN DOCUMENTS '
    wrap(str1,c.drawString,40, 65, 690)
    # c.drawString(65, 660, '4')  # 4
    str2 = '24 X 7 CONTACT DETAILS OF AUTHORISED OFFICIAL OF SHIPPER'
    wrap(str2, c.drawString, 40, 65, 660)
    c.drawString(65, 630, 'CONTAINER NO. ')  # 5
    c.drawString(65, 600, 'CONTAINER SIZE (TEU/FEU/OTHER)')  # 6
    # c.drawString(65, 570, '7')  # 7
    str3 = 'MAXIMUM PERMISSIBLE WEIGHT OF CONTAINER AS PER THE CSC PLATE'
    wrap(str3, c.drawString, 40, 65, 570)
    # c.drawString(65, 530, '8')  # 8
    str4 = 'WEIGHTBRIDGE REGISTRATION NO. AND ADDRESS OF WEIGHTBRIDGE '
    wrap(str4, c.drawString, 40, 65, 530)
    # c.drawString(65, 430, '9')  # 9
    str5 = 'VERIFIED GROSS MASS OF CONTAINER (METHOD-I) / METHOD-2)'
    wrap(str5, c.drawString, 40, 65, 430)
    c.drawString(65, 310, 'DATE AND TIME OF WEIGHING')  # 10
    c.drawString(65, 280, 'WEIGHING SLIP NO.')  # 11
    c.drawString(65, 250, 'TYPE (NORMAL / REEFER / HAZARDOUS / OTHERS)')  # 12
    c.drawString(65, 220, 'IF HAZARDOUS UN NO. IMDG CLASS.')  # 13
    # c.drawString(65, 190, '14')  # 14

    #Reference Box Data
    c.drawString(265, 750, divisioncode[-1])
    if result['SHIPERIECNO'] != None:
        c.drawString(265, 720, str(result['SHIPERIECNO']))
    c.drawString(265, 690, str(result['EXOFFICENAME']))
    c.drawString(265, 645, str(result['EXOFFICENAME']))
    c.drawString(265, 630, str(result['CONTNO']))
    c.drawString(265, 600, str(result['CONTSIZE']))
    # c.drawString(265, 1, str(result['']))
    # c.drawString(265, 1, str(result['']))
    if result['WEIGHPARTYNAME'] != None:
        c.drawString(265, 530, str(result['REGNO']))
        c.drawString(265, 520, str(result['WEIGHPARTYNAME']))#name
        wrap(str(result['WEIGHPARTYNAMEADD']), c.drawString, 45, 265, 510)#add
        # c.drawString(265, 1, str(result['WEIGHPARTYNAMEADD']))#Add
    c.drawCentredString(440, 430, '(METHOD - 1)')
    c.drawString(265, 410, 'Container Tare Weight ')
    if result['CONTWT'] != None:
        c.drawAlignedString(545, 410, str(result['CONTWT']))
    c.drawString(265, 395, 'Total Cargo Gr. Weight ')
    if result['CARGOWT'] != None:
        c.drawAlignedString(545, 395, str(result['CARGOWT']))
    if result['DATEOFWEIGH'] != None:
        c.drawString(265, 310, str(result['DATEOFWEIGH']))
    # c.drawString(265, 1, str(result['']))
    if result['TYPEOFCARGO'] != None:
        c.drawString(265, 250, str(result['TYPEOFCARGO']))

    c.drawString(365, 191, divisioncode[-1])
    c.drawString(365 , 140, 'AUTHORISED SIGNATORY')

def data(result, d):
    fonts(7)


def logic(result):
    global divisioncode, lotno
    global invoiceno, Remark, itemtype, orderno
    global itemname, hsncode, payment, countryofOrigin
    divisioncode.append(result['SHIPER'])
    invoiceno.append(result['INVOICENO'])

def newpage():
    global d
    d = 440
    return d

def newrequest():
    global divisioncode, lotno
    global invoiceno, Remark, itemtype
    global itemname, hsncode, payment, countryofOrigin
    global pageno, Yordno
    divisioncode = []
    pageno = 0
    Yordno = 760
    invoiceno = []
    itemname = []
    hsncode = []
    payment = []
    Remark = []
    itemtype = []
    countryofOrigin = []
    lotno = []

def TotalWT(result):
    global grosswt, netwt, packages

def TotalClean():
    global grosswt
    global netwt
    global packages
    grosswt = 0
    netwt = 0
    packages = 0

def textsize(c, result):
    d = dvalue()
    logic(result)
    global i, Yordno
    #'{0:1.3f}'.format(

    if len(divisioncode) == 1:
        header(divisioncode, result,Yordno)
        # c.drawString(155, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result,d)

    elif divisioncode[-1] == divisioncode[-2]:
        if invoiceno[-1] == invoiceno[-2]:
            data(result, d)

        elif invoiceno[-1] != invoiceno[-2]:
            c.showPage()
            d = newpage()
            header(divisioncode, result, Yordno)
            # c.drawString(155, d, itemtype[-1])
            d = dvalue()
            d = dvalue()
            data(result, d)
    elif divisioncode[-1] != divisioncode[-2]:
        c.showPage()
        d = newpage()
        header(divisioncode, result, Yordno)
        # c.drawString(155, d, itemtype[-1])
        d = dvalue()
        d = dvalue()
        data(result, d)

