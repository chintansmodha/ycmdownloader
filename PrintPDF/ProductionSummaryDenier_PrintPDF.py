import textwrap
from dateutil.relativedelta import relativedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfgen import canvas
from datetime import date
import  pandas as pd
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf", pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))

d = 750
i = 1
f = 580
g = 0
p = 0
pageno = 0

divisioncode = []
Department = []
Itemname = []
wrap_text = []
netwt = 0
total = 0

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

def header(stdt, etdt, divisioncode):
    startdate = str(stdt)
    enddate = str(etdt)
    h_date = pd.period_range(startdate,enddate,
              freq='M').strftime("%Y-%m %b").tolist()
    # print(h_date)
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Department Wise Production From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 1200, 775)
    c.line(0, 755, 1200, 755)
    # Upperline in header
    c.drawString(10, 760, "Department")
    c.drawString(250, 760, "Denier")
    s = 555
    i = 0
    while i < len(h_date):
        c.drawString(s, 760, str(h_date[i]))
        s = s + 100
        i = i + 1
    c.drawString(s , 760, "Total")



def data(stdt, etdt, result, d):
    global f
    global g
    f = 580
    # c.drawString(10, d, str(result['DEPARTMENT']))
    startdate = str(stdt)
    enddate = str(etdt)
    h_date = pd.period_range(startdate, enddate,
                           freq='M').strftime("%Y-%m").tolist()
    fonts(7)
    i = 0
    while i < len(h_date) :
        p = "'"+result['DATES']+"'"
        q = "'"+h_date[i]+" '"
        # print('p', p)
        # print('q', q)
        if p == q:
            c.drawAlignedString(f, d, str(result['NETWT']))
            Total(result)
        else:
            f = f + 100
        i = i + 1
    # f = 555
    g = f


def logic(result):
    global divisioncode
    global Department
    global Itemname
    divisioncode.append(result['COMPNAME'])
    Department.append(result['DEPARTMENT'])
    Itemname.append(result['PRODUCT'])

def newpage():
    global d
    d = 750
    return d

def newrequest():
    global divisioncode
    global Department
    global Itemname
    global pageno
    divisioncode = []
    Department = []
    Itemname = []
    pageno = 0

def Total(result):
    global netwt
    netwt = netwt + float(result['NETWT'])

def TotalClean():
    global netwt
    netwt = 0

def TotalTotals(result):
    global total
    total = total + float(result['NETWT'])

def TotalTottalsClean():
    global total
    total = 0

def textsize(c, result, d, stdt, etdt,monthwisetotal,Date):
    d = dvalue()
    logic(result)
    global g, p, wrap_text

    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        fonts(7)
        c.drawString(10, d, Department[-1])
        # *************************** WRAP ITEM NAME*****************************
        str1 = ''
        string = str1.join(Itemname[-1])
        wrap_text = textwrap.wrap(string, width=70)
        k = 0
        while k < len(wrap_text):
            c.drawString(250, d, wrap_text[k])
            d = dvalue()
            d = dvalue()
            k = k + 1
        l = 0
        while l < len(wrap_text):
            d = dvalueincrese()
            l = l + 1
        # ***************************************************************************
        # c.drawString(250, d, Itemname[-1])
        data(stdt,etdt,result,d)
        TotalTotals(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if Department[-1] == Department[-2]:
            if Itemname[-1] == Itemname[-2]:
                d = dvalueincrese()
                data(stdt, etdt, result, d)
                TotalTotals(result)

            else:
                d = dvalueincrese()
                c.drawAlignedString(g + 90, d, str('{0:1.3f}'.format(netwt)))
                # ****************** Wrap end *********************************
                m = 0
                while m < len(wrap_text) - 1:
                    d = dvalue()
                    d = dvalue()
                    m = m + 1
                # **********************************************************
                d = dvalue()
                d = dvalue()
                TotalClean()
                # *************************** WRAP ITEM NAME*****************************
                str1 = ''
                string = str1.join(Itemname[-1])
                wrap_text = textwrap.wrap(string, width=70)
                k = 0
                while k < len(wrap_text):
                    c.drawString(250, d, wrap_text[k])
                    d = dvalue()
                    d = dvalue()
                    k = k + 1
                l = 0
                while l < len(wrap_text):
                    d = dvalueincrese()
                    l = l + 1
                # ***************************************************************************
                # c.drawString(250, d, Itemname[-1])
                data(stdt, etdt, result, d)
                TotalTotals(result)

        else:
            d = dvalueincrese()
            c.drawAlignedString(g + 90, d, str('{0:1.3f}'.format(netwt)))
            # ****************** Wrap end *********************************
            m = 0
            while m < len(wrap_text) - 1:
                d = dvalue()
                d = dvalue()
                m = m + 1
            # **********************************************************
            d = dvalue()
            d = dvalue()
            TotalClean()
            c.drawString(10, d, Department[-1])
            # *************************** WRAP ITEM NAME*****************************
            str1 = ''
            string = str1.join(Itemname[-1])
            wrap_text = textwrap.wrap(string, width=70)
            k = 0
            while k < len(wrap_text):
                c.drawString(250, d, wrap_text[k])
                d = dvalue()
                d = dvalue()
                k = k + 1
            l = 0
            while l < len(wrap_text):
                d = dvalueincrese()
                l = l + 1
            # ***************************************************************************
            # c.drawString(250, d, Itemname[-1])
            data(stdt, etdt, result, d)
            TotalTotals(result)



    elif divisioncode[-1] != divisioncode[-2]:
        d = dvalueincrese()
        c.drawAlignedString(g + 90, d, str('{0:1.3f}'.format(netwt)))
        # ****************** Wrap end *********************************
        m = 0
        while m < len(wrap_text) - 1:
            d = dvalue()
            d = dvalue()
            m = m + 1
        # **********************************************************
        TotalClean()
        d = dvalue()
        d = dvalue()
        boldfonts(7)
        c.drawString(250, d, "Total :")
        h = 580
        startdate = str(stdt)
        enddate = str(etdt)
        h_date = pd.period_range(startdate, enddate,
                               freq='M').strftime("%Y-%m").tolist()
        i = 0
        while i < len(h_date):
            r = "'" + Date[p] + "'"
            s = "'" + h_date[i] + " '"
            # print('p', p)
            # print('q', q)
            if r == s:
                c.drawAlignedString(h, d, str(monthwisetotal[p]))
                h = h + 100
                p = p + 1
            else:
                h = h + 100
            i = i + 1

        c.drawAlignedString(h -10, d, str('{0:1.3f}'.format(total)))
        TotalTottalsClean()

        c.setPageSize(landscape(A3))
        c.showPage()
        d = newpage()
        d = dvalue()
        header(stdt, etdt, divisioncode)
        fonts(7)
        c.drawString(10, d, Department[-1])
        # *************************** WRAP ITEM NAME*****************************
        str1 = ''
        string = str1.join(Itemname[-1])
        wrap_text = textwrap.wrap(string, width=70)
        k = 0
        while k < len(wrap_text):
            c.drawString(250, d, wrap_text[k])
            d = dvalue()
            d = dvalue()
            k = k + 1
        l = 0
        while l < len(wrap_text):
            d = dvalueincrese()
            l = l + 1
        # ***************************************************************************
        # c.drawString(250, d, Itemname[-1])
        data(stdt, etdt, result, d)
        TotalTotals(result)


#*************************************** NODEPT DENIER ***********************************************

def header_Nodept(stdt, etdt, divisioncode):
    startdate = str(stdt)
    enddate = str(etdt)
    h_date = pd.period_range(startdate,enddate,
              freq='M').strftime("%Y-%m %b").tolist()
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    fonts(9)
    c.drawString(10, 800, str((date.today()).strftime('%d %b %Y')))
    c.drawCentredString(300, 780, "Without Department Wise Production From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(
        etdt.strftime('%d-%m-%Y')) )
    # c.drawString(10, 780, "Document Type: ")
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 775, 1200, 775)
    c.line(0, 755, 1200, 755)
    # Upperline in header
    c.drawString(10, 760, "Denier")
    s = 265
    i = 0
    while i < len(h_date):
        c.drawString(s, 760, str(h_date[i]))
        s = s + 100
        i = i + 1
    c.drawString(s , 760, "Total")



def data_Nodept(stdt, etdt, result, d):
    global f
    global g
    f = 290
    startdate = str(stdt)
    enddate = str(etdt)
    h_date = pd.period_range(startdate, enddate,
                           freq='M').strftime("%Y-%m").tolist()
    fonts(7)
    i = 0
    while i < len(h_date) :
        p = "'"+result['DATES']+"'"
        q = "'"+h_date[i]+" '"
        # print('p', p)
        # print('q', q)
        if p == q:
            c.drawAlignedString(f, d, str(result['NETWT']))
            Total(result)
        else:
            f = f + 100
        i = i + 1
    # f = 555
    g = f


def textsize_Nodept(c, result, d, stdt, etdt, monthwisetotal, Date):
    d = dvalue()
    logic(result)
    global g, p, wrap_text

    if len(divisioncode) == 1:
        header_Nodept(stdt, etdt, divisioncode)
        fonts(7)
        #*************************** WRAP ITEM NAME*****************************
        str1 = ''
        string = str1.join(Itemname[-1])
        wrap_text = textwrap.wrap(string, width=60)
        k = 0
        while k < len(wrap_text):
            c.drawString(10, d, wrap_text[k])
            d = dvalue()
            d = dvalue()
            k = k + 1
        l = 0
        while l < len(wrap_text):
            d = dvalueincrese()
            l = l + 1
        #***************************************************************************
        # c.drawString(10, d, Itemname[-1])
        data_Nodept(stdt, etdt, result, d)
        TotalTotals(result)

    elif divisioncode[-1] == divisioncode[-2]:
        if Itemname[-1] == Itemname[-2]:
            d = dvalueincrese()
            data_Nodept(stdt, etdt, result, d)
            TotalTotals(result)

        else:
            d = dvalueincrese()
            c.drawAlignedString(g + 90, d, str('{0:1.3f}'.format(netwt)))
            # ****************** Wrap end *********************************
            m = 0
            while m < len(wrap_text) - 1:
                d = dvalue()
                d = dvalue()
                m = m + 1
            # **********************************************************
            d = dvalue()
            d = dvalue()
            TotalClean()
            # *************************** WRAP ITEM NAME*****************************
            str1 = ''
            string = str1.join(Itemname[-1])
            wrap_text = textwrap.wrap(string, width=60)
            k = 0
            while k < len(wrap_text):
                c.drawString(10, d, wrap_text[k])
                d = dvalue()
                d = dvalue()
                k = k + 1
            l = 0
            while l < len(wrap_text):
                d = dvalueincrese()
                l = l + 1
            # c.drawString(10, d, Itemname[-1])
            # ****************************************************************************
            data_Nodept(stdt, etdt, result, d)
            TotalTotals(result)


    elif divisioncode[-1] != divisioncode[-2]:
        d = dvalueincrese()
        c.drawAlignedString(g + 90, d, str('{0:1.3f}'.format(netwt)))
        #************************** Wrap End ************************************
        m = 0
        while m < len(wrap_text) - 1:
            d = dvalue()
            d = dvalue()
            m = m + 1
        # ***********************************************************************
        TotalClean()
        d = dvalue()
        d = dvalue()
        boldfonts(7)
        c.drawString(10, d, "Total :")
        h = 290
        startdate = str(stdt)
        enddate = str(etdt)
        h_date = pd.period_range(startdate, enddate,
                               freq='M').strftime("%Y-%m").tolist()
        i = 0
        while i < len(h_date):
            r = "'" + Date[p] + "'"
            s = "'" + h_date[i] + " '"
            # print('p', p)
            # print('q', q)
            if r == s:
                c.drawAlignedString(h, d, str(monthwisetotal[p]))
                h = h + 100
                p = p + 1
            else:
                h = h + 100
            i = i + 1

        c.drawAlignedString(h - 10, d, str('{0:1.3f}'.format(total)))
        TotalTottalsClean()

        c.setPageSize(landscape(A3))
        c.showPage()
        d = newpage()
        d = dvalue()
        header_Nodept(stdt, etdt, divisioncode)
        fonts(7)
        #*************************** WRAP ITEM NAME*****************************
        str1 = ''
        string = str1.join(Itemname[-1])
        wrap_text = textwrap.wrap(string, width=60)
        k = 0
        while k < len(wrap_text):
            c.drawString(10, d, wrap_text[k])
            d = dvalue()
            d = dvalue()
            k = k + 1
        l = 0
        while l < len(wrap_text):
            d = dvalueincrese()
            l = l + 1
        # **********************************************************************
        # c.drawString(10, d, Itemname[-1])
        data_Nodept(stdt, etdt, result, d)
        TotalTotals(result)