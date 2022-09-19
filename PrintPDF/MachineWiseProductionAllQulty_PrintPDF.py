import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, portrait, A4, A1, A2, A0, A5,A3,A6, A7
from reportlab.pdfgen import canvas
from datetime import date
from babel.numbers import format_number , format_currency , format_decimal
from Global_Files import Connection_String as con

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialItalic', 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBoldItalic', 'arialbi.ttf'))

c = canvas.Canvas("1.pdf")
c.setPageSize(portrait(A4))

d = 505
check = 0
pageno = 0
pageSize = 0
Xaxis = 0
Yaxis = 0

divisioncode = []
Machine = []
Itemname = []
QualityHeader = []
X_axis = 0

rowtotal = 0
prev_d = 0
current_d = 0

departmentTotal = []
departmentTotaltotal = 0

item_breakupline_count = 0


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

def dvalue(stdt,etdt,result, divisioncode):
    global d
    if d > 20:
        d = d - 5
        return d
    else:
        PrintRowTotal()
        d = newpage()
        c.setPageSize(portrait(A4))
        c.showPage()
        page()
        headerSql(stdt, etdt, divisioncode)
        headerRef(stdt, etdt, divisioncode)
        return d

def dvalueincrese():
    global d
    if d > 30 and d < 745:
        d = d + 10
    else:
        pass
    return d

def wrap(string, type, width, x, y, result, stdt, etdt):
    global prev_d, current_d, item_breakupline_count
    prev_d = y
    wrap_text = textwrap.wrap(string, width=width, break_long_words=False)
    e = 0
    item_breakupline_count = 0
    s = ''
    while e < len(wrap_text):
        s = type(x, y, wrap_text[e])
        e = e + 1
        item_breakupline_count += 1
        if e < len(wrap_text):
            y = dvalue(stdt,etdt,result, divisioncode)
            y = dvalue(stdt,etdt,result, divisioncode)
    current_d = y


def headerRef(stdt, etdt, divisioncode):
    global pageSize, Xaxis, Yaxis, d
    # print(len(LSDay))
    if len(QualityHeader) <=2:
        # print('3')
        c.setPageSize(portrait(A4))
        pageSize = 4
        Xaxis = 596 #596
        Yaxis = 800 #842
        d = Yaxis - 45
    elif len(QualityHeader)> 2 and len(QualityHeader)<=5:
        # print('3-6')
        c.setPageSize(portrait(A3))
        pageSize = 3
        Xaxis = 842 #842
        Yaxis = 1140 #1192
        d = Yaxis - 45
    elif len(QualityHeader)> 5 and len(QualityHeader)<=11:
        # print('6-9')
        c.setPageSize(portrait(A2))
        pageSize = 2
        Xaxis = 1192 #1192
        Yaxis = 1620 # 1684
        d = Yaxis - 45
    elif len(QualityHeader)> 11 and len(QualityHeader)<=20:
        # print('9-12')
        c.setPageSize(portrait(A1))
        pageSize = 1
        Xaxis = 1684 #1684
        Yaxis = 2310 #2384
        d = Yaxis - 45
    elif len(QualityHeader)> 20:
        # print('12-15')
        c.setPageSize(portrait(A0))
        pageSize = 0
        Xaxis = 2384 #2384
        Yaxis = 3290 #3372
        d = Yaxis - 45

    header(stdt, etdt, divisioncode)
    return d


def headerSql(stdt, etdt, divisioncode):
    productiondate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    currentDepartment = divisioncode[-1]
    global QualityHeader
    QualityHeader = []

    sql = "Select           Distinct COALESCE(COSTCENTER.LONGDESCRIPTION, Case When BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE is Null " \
          "Then 'Plant Not Entered' Else 'Department Not Entered' End ) As Department " \
          ", Coalesce(Qlty.SHORTDESCRIPTION, 'QultyNameNotEntered') as Quality " \
          "From BKLELEMENTS " \
          "Left Join QUALITYLEVEL Qlty                    On      BKLELEMENTS.LOTITEMTYPECODE = Qlty.ITEMTYPECODE " \
          "And     BKLELEMENTS.QUALITYLEVELCODE = Qlty.CODE " \
          "Left Join LOGICALWAREHOUSE                     On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join COSTCENTER                           On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Join    ELEMENTS                               On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where   ELEMENTS.ENTRYDATE Between "+productiondate+" and "+enddate+"  And     BKLELEMENTS.ACTUALNETWT  > 0 " \
          "And     COALESCE(COSTCENTER.LONGDESCRIPTION, Case When BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE is Null " \
          "Then 'Plant Not Entered' Else 'Department Not Entered' End ) = '"+currentDepartment+"' Order By Department, Quality "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        QualityHeader.append(result['QUALITY'])
        result = con.db.fetch_both(stmt)
    QualityHeader = list(set(QualityHeader))

def header(stdt, etdt, divisioncode):
    global QualityHeader, X_axis, pageno, Xaxis, Yaxis
    c.setTitle('MachineWiseProductionAllQualities')
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(Xaxis/2, Yaxis, divisioncode[-1])
    fonts(9)
    c.drawString(30, Yaxis-15, str((date.today()).strftime('%d/%m/%Y')))
    c.drawCentredString(Xaxis/2, Yaxis-15, "Machine Wise Production Summary From " + str(stdt.strftime(' %d  %B  %Y')) +
                        " To " + str(etdt.strftime(' %d  %B  %Y')))
    # c.drawCentredString(300, 780, "Stock In Hand (Item Shade Lot - Wise) As On  " + str(stdt.strftime(' %d  %B  %Y')))
    # c.drawString(10, 780, "Document Type: ")
    c.drawString(Xaxis-100, Yaxis-15, "Page No." + str(pageno))
    # c.setDash(2,3)
    c.line(0, Yaxis - 20, Xaxis, Yaxis - 20)
    c.line(0, Yaxis - 40, Xaxis, Yaxis - 40)
    # Upperline in header
    c.drawString(30, Yaxis-35, 'Machine')
    c.drawString(100, Yaxis-35, 'Item Description')
    X_axis = 350
    i = 0
    while i < len(QualityHeader):
        c.drawString(X_axis, Yaxis-35, str(QualityHeader[i]))
        X_axis += 80
        i += 1
    c.drawString(X_axis+20, Yaxis-35, 'Total')


def data(result, stdt, etdt, divisioncode):
    fonts(7)
    global QualityHeader, check, prev_d, current_d, d,departmentTotal
    if len(Machine) == 1:
        X = 350
        i = 0
        d = dvalue(stdt, etdt, result, divisioncode)
        c.drawString(31, d, str(result['MACHINE']))
        wrap(str(result['ITEM']),c.drawString,40,101,d,result,stdt,etdt)
        if current_d != prev_d:
            d = prev_d
        # c.drawString(101, d, str(result['ITEM']))
        while i != len(QualityHeader):
            if str(result['QUALITY']).strip() == str(QualityHeader[i]).strip():
                c.drawAlignedString(X + int(len(result['QUALITY'])), d , str(result['QUANTITY']))
                departmentTotal.append(float(result['QUANTITY']))
            else:
                departmentTotal.append(float(0))
            i += 1
            X += 80
    else:
        X = 350
        i = 0
        if Machine[-1] == Machine[-2]:
            if Itemname[-1] == Itemname[-2]:
                while i != len(QualityHeader):
                    if str(result['QUALITY']).strip() == str(QualityHeader[i]).strip():
                        c.drawAlignedString(X + int(len(result['QUALITY'])), d, str(result['QUANTITY']))
                        departmentTotal[i] += float(result['QUANTITY'])
                    i += 1
                    X += 80
            else:
                PrintRowTotal()
                d = current_d
                if check == 1:
                    d = dvalue(stdt, etdt, result, divisioncode)
                d = dvalue(stdt, etdt, result, divisioncode)
                X = 350
                i = 0
                c.drawString(31, d, str(result['MACHINE']))
                wrap(str(result['ITEM']), c.drawString, 40, 101, d, result, stdt, etdt)
                if current_d != prev_d:
                    d = prev_d
                # c.drawString(101, d, str(result['ITEM']))
                while i != len(QualityHeader):
                    if str(result['QUALITY']).strip() == str(QualityHeader[i]).strip():
                        c.drawAlignedString(X + int(len(result['QUALITY'])), d, str(result['QUANTITY']))
                        departmentTotal[i] += float(result['QUANTITY'])
                    i += 1
                    X += 80

        else:
            PrintRowTotal()
            d = current_d
            if check == 1:
                d = dvalue(stdt, etdt, result, divisioncode)
            d = dvalue(stdt, etdt, result, divisioncode)
            X = 350
            i = 0
            c.drawString(31, d, str(result['MACHINE']))
            wrap(str(result['ITEM']), c.drawString, 40, 101, d, result, stdt, etdt)
            if current_d != prev_d:
                d = prev_d
            # c.drawString(101, d, str(result['ITEM']))
            while i != len(QualityHeader):
                if str(result['QUALITY']).strip() == str(QualityHeader[i]).strip():
                    c.drawAlignedString(X + int(len(result['QUALITY'])), d, str(result['QUANTITY']))
                    departmentTotal[i] += float(result['QUANTITY'])
                i += 1
                X += 80
    RowWiseTotal(result)
    # print(departmentTotal)



def logic(result):
    global divisioncode
    global Itemname
    global Machine
    divisioncode.append(result['DEPARTMENT'])
    Itemname.append(result['ITEM'])
    Machine.append(result['MACHINE'])

def newpage():
    global d, Yaxis
    d = Yaxis - 45
    return d

def newrequest():
    global divisioncode
    global Itemname
    global Machine
    global pageSize, Xaxis, Yaxis
    divisioncode = []
    Itemname = []
    Machine = []
    pageSize = 0
    Xaxis = 0
    Yaxis = 0

def RowWiseTotal(result):
    global rowtotal, departmentTotaltotal
    rowtotal += float(result['QUANTITY'])
    departmentTotaltotal += float(result['QUANTITY'])

def PrintRowTotal():
    global rowtotal,X_axis
    c.drawAlignedString(X_axis + 30, d, str('{0:1.3f}'.format(rowtotal)))
    rowtotal = 0

def PrintTotal():
    global departmentTotal, QualityHeader, departmentTotaltotal,X_axis
    boldfonts(7)
    X = 350
    i = 0
    c.drawString(102, d, 'Department Total: ')
    while i != len(QualityHeader):
        c.drawAlignedString(X + int(len(QualityHeader[i])), d, '{0:1.3f}'.format(departmentTotal[i]))
        i += 1
        X += 80
    c.drawAlignedString(X_axis + 30, d, str('{0:1.3f}'.format(departmentTotaltotal)))
    fonts(7)
    departmentTotal = []
    departmentTotaltotal = 0


def textsize(c, result, d, stdt, etdt):
    # d = dvalue(stdt,etdt,result, divisioncode)
    logic(result)
    global check, item_breakupline_count
    # print('rohit  ', A4)
    #'{0:1.3f}'.format()
    y = 0
    if len(divisioncode) == 1:
        page()
        headerSql(stdt, etdt, divisioncode)
        headerRef(stdt, etdt, divisioncode)
        # d = dvalue(stdt, etdt, result, divisioncode)
        data(result, stdt, etdt, divisioncode)

    elif divisioncode[-1] == divisioncode[-2]:
        check = 1
        data(result, stdt, etdt, divisioncode)

    elif divisioncode[-1] != divisioncode[-2]:
        PrintRowTotal()
        linecount = 0
        while linecount != item_breakupline_count:
            d = dvalue(stdt, etdt, result, divisioncode)
            d = dvalue(stdt, etdt, result, divisioncode)
            linecount += 1
        PrintTotal()
        newrequest()
        d = newpage()
        c.setPageSize(portrait(A4))
        c.showPage()
        logic(result)
        page()
        headerSql(stdt, etdt, divisioncode)
        headerRef(stdt, etdt, divisioncode)
        check = 0
        data(result, stdt, etdt, divisioncode)
