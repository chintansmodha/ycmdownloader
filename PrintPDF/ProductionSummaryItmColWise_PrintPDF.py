import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A3
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=landscape(A3))
c.setPageSize(landscape(A3))
d = 770
q = 0
t = 0
b = 200
j = 0
l = 0
r = 0
pageno = 0

divisioncode = []
Itemname = []
ShadeName = []
ShadeCode =  []
LotNo = []
wrap_text = []
Qualitys = []
Quaty = []
d_total = []
total = []
Netwt = 0
CompTotal = 0

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

def dvalueincrease():
    global d
    d = d + 10
    return d

def header(stdt, etdt):
    fonts(15)
    # c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    fonts(12)
    c.drawCentredString(300, 780, "Item Col Wise Production Summary From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    fonts(9)
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    # c.line(0, 775, 1200, 775)
    # c.line(0, 755, 1200, 755)
    # # Upperline in header
    # # Item Saprate by Quality Label
    # c.drawString(10, 760, "Item")

def header_h(d):
    fonts(9)
    c.line(0, d, 1200, d)
    d = dvalue()
    d = dvalue()
    d = dvalue()
    d = dvalue()
    c.line(0, d, 1200, d)
    # Upperline in header
    # Item Saprate by Quality Label
    d = dvalueincrease()
    d = dvalue()
    c.drawString(10, d, "Item")
    d = dvalue()
    d = dvalue()
    d = dvalue()
    d = dvalueincrease()
    d =  dvalue()


def data(result, x, d):
    fonts(7)
    c.drawAlignedString(x, d, str(result['NETWT']))
    Total(result)


def logic(result):
    global divisioncode
    global Itemname
    global Qualitys
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])
    Qualitys.append(result['QUALTY'])

def newpage():
    global d
    d = 770
    return d

def newrequest():
    global divisioncode
    global Itemname
    global Qualitys
    global pageno
    divisioncode = []
    Itemname = []
    Qualitys = []
    pageno = 0

def Total(result):
    global Netwt
    global CompTotal
    Netwt = Netwt + float(result['NETWT'])
    CompTotal = CompTotal + float(result['NETWT'])

def TotalClean():
    global Netwt
    Netwt = 0

def CompClean():
    global CompTotal
    CompTotal = 0


def textsize(c, result, d, stdt, etdt, TOTALS, quality_total):
    d = dvalue()
    logic(result)
    global q, wrap_text, Quaty, t, b
    global  d_total, total, j, l, r
    # str('{0:1.3f}'.format(

    if len(divisioncode) == 1:
        TotalClean()
        CompClean()
        Quaty = []
        total = []
        d_total = []
        q = t = l = j = r = 0
        b = 200
        Quaty.append(Qualitys[-1])
        header(stdt, etdt)
        header_h(d)
        t = d = dvalueincrease()
        if Qualitys[-1] == '':
            c.drawString(b, t, "Others")
        else:
            c.drawString(b, t, Qualitys[-1])
        # c.drawString(b, t, Qualitys[-1])
        d = dvalue()
        d = dvalue()
        d = dvalue()
        c.drawCentredString(300, d, divisioncode[-1])
        d = dvalue()
        d = dvalue()
        d = dvalue()
        fonts(7)
        # ********************** WRAP PRODUCT ****************************************
        str1 = ''
        string = str1.join(Itemname[-1])
        wrap_text = textwrap.wrap(string, width=35)
        e = 0
        while e < len(wrap_text):
            c.drawString(11, d, wrap_text[e])
            d = dvalue()
            d = dvalue()
            e = e + 1
        f = 0
        while f < len(wrap_text):
            d = dvalueincrease()
            f = f + 1
        # c.drawString(11, d, str(result['PRODUCT']))
        # *****************************************************************************
        data(result, b + 15 , d)
        j = j + 1


    elif divisioncode[-1] == divisioncode[-2]:
        if Itemname[-1] == Itemname[-2]:
            if Qualitys[-1] != Qualitys[-2]:
                d = dvalueincrease()
                h = 215
                i = 0
                itr = 0#check Quality is written or not on header(between line)
                while i < len(Quaty):
                    if "'" + Qualitys[-1] + "'" == "'" + Quaty[i] + "'":
                        data(result, h, d)
                        itr = itr + 1
                    i = i + 1
                    h = h + 100
                if itr == 0:
                    b = b + 100
                    Quaty.append(Qualitys[-1])
                    fonts(9)
                    if Qualitys[-1] == '':
                        c.drawString(b, t, "Others")
                    else:
                        c.drawString(b, t, Qualitys[-1])
                # c.drawString(b, t, Qualitys[-1])
                    data(result, b + 15 , d)
                    j = j + 1
                fonts(7)

        else:
            # ******************* Wrap End *********************************
            d = dvalueincrease()
            total.append(Netwt)
            d_total.append(d)
            TotalClean()
            g = 0
            while g < len(wrap_text):
                d = dvalue()
                d = dvalue()
                g = g + 1
            # #***************************************************************
            # ********************** WRAP PRODUCT ****************************************
            str1 = ''
            string = str1.join(Itemname[-1])
            wrap_text = textwrap.wrap(string, width=35)
            e = 0
            while e < len(wrap_text):
                c.drawString(11, d, wrap_text[e])
                d = dvalue()
                d = dvalue()
                e = e + 1
            f = 0
            while f < len(wrap_text):
                d = dvalueincrease()
                f = f + 1
            # c.drawString(11, d, str(result['PRODUCT']))
            # *****************************************************************************
            h = 215
            i = 0
            itr = 0
            while i < len(Quaty):
                if "'" + Qualitys[-1] + "'" == "'" + Quaty[i] + "'":
                    data(result, h, d)
                    itr = itr + 1
                i = i + 1
                h = h + 100
            if itr == 0:
                b = b + 100
                Quaty.append(Qualitys[-1])
                fonts(9)
                if Qualitys[-1] == '':
                    c.drawString(b, t, "Others")
                else:
                    c.drawString(b, t, Qualitys[-1])
                # c.drawString(b, t, Qualitys[-1])
                data(result, b + 15, d)
                j = j + 1
                fonts(7)

    elif divisioncode[-1] != divisioncode[-2]:
        # ******************* Wrap End *********************************
        d = dvalueincrease()
        total.append(Netwt)
        d_total.append(d)
        TotalClean()
        g = 0
        while g < len(wrap_text):
            d = dvalue()
            d = dvalue()
            g = g + 1
        # #***************************************************************
        n = 215
        boldfonts(8)
        c.drawString(20, d, "Dept Total: ")
        p1 = p = r
        r1 = 0
        while l < j:
            if "'"+quality_total[p]+"'" == "'"+Quaty[r1]+"'":
                c.drawAlignedString(n, d, str(TOTALS[p]))
                l = l + 1
                r1 = r1 + 1
                p = p1
                r = r + 1
                n = n + 100
                # b1 = b1 + 100
            else:
                p = p + 1
        c.drawAlignedString(n, d, str('{0:1.3f}'.format(CompTotal)))
        CompClean()
        # d = dvalueincrease()
        # d_total.append(d)
        # total.append(Netwt)
        d = dvalue()
        d = dvalue()
        d = dvalue()
        fonts(9)
        b = b + 100
        c.drawString(b, t, "Total")
        e = 0
        while e < len(d_total):
            fonts(7)
            c.drawAlignedString(b+15, int(d_total[e]), str('{0:1.3f}'.format(total[e])))
            e = e + 1
        fonts(9)
        d = dvalue()
        d = dvalue()
        Quaty = []
        TotalClean()
        total = []
        d_total = []
        c.setPageSize(landscape(A3))
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt,etdt)
        Quaty.append(Qualitys[-1])
        header_h(d)
        t = d = dvalueincrease()
        b = 200
        if Qualitys[-1] == '':
            c.drawString(b, t, "Others")
        else:
            c.drawString(b, t, Qualitys[-1])
        d = dvalue()
        d = dvalue()
        d = dvalue()
        c.drawCentredString(300, d, divisioncode[-1])
        d = dvalue()
        d = dvalue()
        d = dvalue()
        fonts(7)
        # ********************** WRAP PRODUCT ****************************************
        str1 = ''
        string = str1.join(Itemname[-1])
        wrap_text = textwrap.wrap(string, width=35)
        e = 0
        while e < len(wrap_text):
            c.drawString(11, d, wrap_text[e])
            d = dvalue()
            d = dvalue()
            e = e + 1
        f = 0
        while f < len(wrap_text):
            d = dvalueincrease()
            f = f + 1
        # c.drawString(11, d, str(result['PRODUCT']))
        # *****************************************************************************
        data(result, b + 15 , d)
        j = j + 1