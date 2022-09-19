from datetime import datetime

from reportlab.lib.pagesizes import portrait, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from FormLoad import PrintYarnChallan_FormLoad as PYCFL
import textwrap

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(portrait(A3)))
c.setPageSize(portrait(A3))
d=680
no=0
divisioncode=[]
costcenter=[]
challanno=[]
pageno=0
GrossTotal=0
BoxesTotal=0
CopsTotal=0

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

def dvalue(stdt, etdt,result, divisioncode):
    global d
    if d > 20:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt,result, divisioncode)
        return d

def header(stdt,etdt,result,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(300, 780,"Departmentwise Despatch Report From " + str(PYCFL.stdate) + " To " + str(PYCFL.etdate))
    format = '%d-%m-%Y %I:%M %p'
    datestring=datetime.now(tz=None)
    date=datetime.strftime(datestring, format)
    c.drawString(10,770,date)
    c.drawString(10,750,str("COST CENTER:"))
    if result['COSTCENTERNAME']!=None:
        c.drawString(100,750,str(result['COSTCENTERNAME']))

    c.drawString(300, 750, str("CHALLAN NO:"))
    if result['CHALLANNUMBER'] != None:
        c.drawString(370, 750, str(result['CHALLANNUMBER']))

    c.drawString(300, 740, str("DESPATCH:"))
    if result['DESPATCH'] != None:
        c.drawString(370, 740, str(result['DESPATCH']))

    c.drawString(10,740,str("LR NO:"))
    if result['LRNO']!=None:
        c.drawString(100,740,str(result['LRNO']))

    c.drawString(10, 730, str("CUSTOMER:"))
    if result['CUSTOMER'] != None:
        c.drawString(100, 730, str(result['CUSTOMER']))

    c.drawString(300, 730, str("PRODUCT:"))
    z = 730
    if len(str(result['PRODUCT'])) > 25:
        lines = textwrap.wrap(str(result['PRODUCT']), 25, break_long_words=False)
        for i in lines:
            c.drawString(370, z, str(i))
            z=z-10
    else:
        c.drawString(370, z, str(result['PRODUCT']))
        z = z - 10

    p = page()
    c.drawString(780, 530, "Page No." + str(p))
    c.line(0, 710, 900, 710)
    c.line(0, 680, 900, 680)

    c.drawString(10, 700, "NO.")
    c.drawString(30,700,str("CONTAINER"))
    c.drawString(30, 690, str("ELEMENT NO."))
    c.drawString(110, 700, str("GROSS WT."))
    c.drawString(180, 700, str("TARE WT."))
    c.drawString(240, 700, str("NETT WT."))
    c.drawString(300, 700, str("COPS"))
    c.drawString(345, 700, str("BATCH"))
    c.drawString(390, 700, str("SHADECODE_NAME"))
    c.drawString(490, 700, str("TWIST"))
    c.drawString(490, 690, str("CODE"))
    c.drawString(530, 700, str("WINDER&"))
    c.drawString(530, 690, str("PACKSIZE"))

def data(stdt, etdt, result, d):
    global no
    no = no + 1
    fonts(7)
    c.drawString(10, d, str(no))
    c.drawString(490, d, str(result['TWISTCODE']))
    c.drawString(530, d, str(result['WINDCODEANDPACKSIZE']))
    c.drawString(30,d,str(result['CONTAINERELEMENTNO']))
    c.drawString(135,d,str(("%.3f" % float(result['GROSSWT']))))
    c.drawString(200, d, str(("%.3f" % float(result['TAREWT']))))
    c.drawString(260, d, str(("%.3f" % float(result['NETWT']))))
    c.drawString(320, d, str(("%.0f" % float(result['COPS']))))
    c.drawString(345, d, str(result['LOTNO']))
    if len(str(result['SHADECODE'])) > 25:

        lines = textwrap.wrap(str(result['SHADECODE']), 25, break_long_words=False)
        for i in lines:
            c.drawString(390, d, str(i))
            d = d-10
    else:
        c.drawString(390, d , str(result['SHADECODE']))
        d=d-10
    # c.drawString(400, d, str(result['SHADECODE']))


def total(result):
    global GrossTotal
    global BoxesTotal
    global CopsTotal
    GrossTotal=GrossTotal+float("%.3f" % float(result['NETWT']))
    BoxesTotal=BoxesTotal+float("%.3f" % float(result['BOXESCOUNT']))
    CopsTotal=CopsTotal+float("%.3f" % float(result['COPS']))
    print(GrossTotal)
    print(BoxesTotal)

def printtotal(d):
    global GrossTotal
    global BoxesTotal
    global CopsTotal
    boldfonts(7)
    c.drawString(10, d, "NET WEIGHT:")
    c.drawString(135,d,str(("%.3f" % float(GrossTotal))))
    c.drawString(200,d,"BOXES:")
    c.drawString(230, d, str(("%.3f" % float(BoxesTotal))))
    c.drawString(300,d,"COPS:")
    c.drawString(330, d, str(("%.3f" % float(CopsTotal))))
    print(GrossTotal)
    print(BoxesTotal)
    GrossTotal=0
    BoxesTotal=0
    CopsTotal=0

def logic(result):
    divisioncode.append(result['COMPANYNAME'])
    costcenter.append(result['COSTCENTERNAME'])
    challanno.append(result['CHALLANNUMBER'])

def newpage():
    global d
    d = 670
    return d

def newrequest():
    global divisioncode
    global pageno
    global costcenter
    global no
    divisioncode = []
    costcenter=[]
    pageno=0
    no=0

def companyclean():
    global GrossTotal
    global BoxesTotal
    global CopsTotal
    GrossTotal=0
    BoxesTotal=0
    CopsTotal=0

def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt,etdt,result,divisioncode)
    logic(result)
    global no
    if len(divisioncode) == 1:
        header(stdt,etdt,result,divisioncode)
        fonts(7)
        data(stdt,etdt,result, d)
        total(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if challanno[-1] == challanno[-2]:
            data(stdt, etdt, result, d)
            total(result)
        elif challanno[-1] != challanno[-2]:
            no=0
            printtotal(d)
            c.showPage()
            header(stdt, etdt, result, divisioncode)
            d = newpage()
            data(stdt, etdt, result, d)
            total(result)

    elif divisioncode[-1] != divisioncode[-2]:
        fonts(7)
        printtotal(d)
        companyclean()
        no = 0
        c.showPage()
        header(stdt,etdt,result,divisioncode)
        d = newpage()
        # d=dvalue(stdt,etdt,result,divisioncode)
        data(stdt, etdt, result, d)
        total(result)