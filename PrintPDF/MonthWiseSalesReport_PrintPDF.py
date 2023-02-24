from reportlab.lib.pagesizes import  A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf",pagesize=(A4))
c.setPageSize(A4)
d = 760
month=[]
company=[]
prefix=[]

#Total variables for month
monthSalesQty=0
monthSalesAmt=0
monthJWQty=0
monthJWAmt=0
monthTotalQty=0
monthTotalAmt=0

#Total VAriable for company
companySalesQty=0
companySalesAmt=0
companyJWQty=0
companyJWAmt=0
companyTotalQty=0
companyTotalAmt=0

def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)
pageno=0


def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue(stdt, etdt, plant):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, plant,month)
        return d

def header(stdt,etdt,plant,month):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(310, 820, plant[-1]) 
    boldfonts(8)
    c.drawCentredString(310, 810, "Sales Summary From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    p=page()
    c.drawString(500,800,"Page No."+str(p))
    c.line(0, 790, 650, 790)
    c.line(0, 770, 650, 770)
    c.drawString(10, 778, "Prefix")
    c.drawString(50, 778, "Despatch")
    c.drawString(200, 778, "Sales Qty.")
    c.drawString(270, 778, "Sales Amt.")
    c.drawString(340, 778, "JW Qty.")
    c.drawString(410, 778, "JW Amt.")
    c.drawString(480, 778, "Total Qty.")
    c.drawString(550, 778, "Total Amt.")

def data(result,d):
    fonts(8)
    c.drawString(10, d, str(result['PREFIX']))
    c.drawString(50, d, str(result['DISPATCH']))
    c.drawAlignedString(230, d, str(result['SALESQTY']))
    c.drawAlignedString(300, d, str(result['SALESAMT']))
    c.drawAlignedString(340, d, str(result['JWQTY']))
    c.drawAlignedString(440, d, str(result['JWAMT']))
    c.drawAlignedString(500, d, str(result['TOTALQTY']))
    c.drawAlignedString(580, d, str(result['TOTALAMT']))
    Total(result)

def Total(result):
    #Total variables for month
    global monthSalesQty
    global monthSalesAmt
    global monthJWQty
    global monthJWAmt
    global monthTotalQty
    global monthTotalAmt
    global companySalesQty
    global companySalesAmt
    global companyJWQty
    global companyJWAmt
    global companyTotalQty
    global companyTotalAmt

    monthSalesQty = monthSalesQty +(float("%2f"%float(result['SALESQTY'])))
    monthSalesAmt = monthSalesAmt +(float("%2f"%float(result['SALESAMT'])))
    monthJWQty = monthJWQty +(float("%2f"%float(result['JWQTY'])))
    monthJWAmt = monthJWAmt +(float("%2f"%float(result['JWAMT'])))
    monthTotalQty = monthTotalQty +(float("%2f"%float(result['TOTALQTY'])))
    monthTotalAmt = monthTotalAmt +(float("%2f"%float(result['TOTALAMT'])))

    companySalesQty = companySalesQty +(float("%2f"%float(result['SALESQTY'])))
    companySalesAmt = companySalesAmt +(float("%2f"%float(result['SALESAMT'])))
    companyJWQty = companyJWQty +(float("%2f"%float(result['JWQTY'])))
    companyJWAmt = companyJWAmt +(float("%2f"%float(result['JWAMT'])))
    companyTotalQty = companyTotalQty +(float("%2f"%float(result['TOTALQTY'])))
    companyTotalAmt = companyTotalAmt +(float("%2f"%float(result['TOTALAMT'])))

def monthTotalPrint(d):
    boldfonts(8)
    global monthSalesQty
    global monthSalesAmt
    global monthJWQty
    global monthJWAmt
    global monthTotalQty
    global monthTotalAmt

    c.drawString(10,d,"Month Total :")
    c.drawAlignedString(230, d,str(monthSalesQty))
    c.drawAlignedString(300, d,str(monthSalesAmt))
    c.drawAlignedString(370, d,str(monthJWQty))
    c.drawAlignedString(440, d,str(monthJWAmt))
    c.drawAlignedString(510, d,str(monthTotalQty))
    c.drawAlignedString(580, d,str(monthTotalAmt))

    monthSalesQty =0
    monthSalesAmt =0
    monthJWQty =0
    monthJWAmt =0
    monthTotalQty =0
    monthTotalAmt =0

def companyTotalPrint(d):
    boldfonts(8)
    global companySalesQty
    global companySalesAmt
    global companyJWQty
    global companyJWAmt
    global companyTotalQty
    global companyTotalAmt

    c.drawString(10,d,"Company Total :")
    c.drawAlignedString(230, d,str(companySalesQty))
    c.drawAlignedString(300, d,str(companySalesAmt))
    c.drawAlignedString(370, d,str(companyJWQty))
    c.drawAlignedString(440, d,str(companyJWAmt))
    c.drawAlignedString(510, d,str(companyTotalQty))
    c.drawAlignedString(580, d,str(companyTotalAmt))

    companySalesQty =0
    companySalesAmt =0
    companyJWQty =0
    companyJWAmt =0
    companyTotalQty =0
    companyTotalAmt =0

def logic(result):
    month.append(result['MONTH'])
    company.append(result['COMPANY'])
    prefix.append(result['PREFIX'])
    

def newpage():
    global d
    d = 740
    return d

def newrequest():
    global pageno
    global d
    d = 760
    pageno=0
    
    global monthSalesQty
    global monthSalesAmt
    global monthJWQty
    global monthJWAmt
    global monthTotalQty
    global monthTotalAmt
    global companySalesQty
    global companySalesAmt
    global companyJWQty
    global companyJQAmt
    global companyTotalQty
    global companyTotalAmt

    monthSalesQty=0
    monthSalesAmt=0
    monthJWQty=0
    monthJWAmt=0
    monthTotalQty=0
    monthTotalAmt=0
    companySalesQty=0
    companySalesAmt=0
    companyJWQty=0
    companyJQAmt=0
    companyTotalQty=0
    companyTotalAmt=0

    global company
    global month
    global prefix
    company=[]
    prefix=[]
    month=[]


def textsize(c,result, d, stdt, etdt):
    d=dvalue(stdt, etdt, company)
    logic(result)
    if len(company) == 1:
        if len(month) == 1:
            header(stdt,etdt,company,month)
            c.drawString(10,d,month[-1])
            d = dvalue(stdt, etdt, company)
            data(result, d)                

    elif company[-1] == company[-2]:
        if month[-1] == month[-2]:
            if prefix[-1] == prefix[-2]:
                data(result, d)
            elif prefix[-1] != prefix[-2]:
                d = dvalue(stdt, etdt, company)  
                monthTotalPrint(d)
                d = dvalue(stdt, etdt, company) 
                d = dvalue(stdt, etdt, company) 
                c.drawString(10, d, str(month[-1]))
                d = dvalue(stdt, etdt, company)  
                data(result,d)

        elif month[-1] != month[-2]:
            monthTotalPrint(d)
            d = dvalue(stdt, etdt, company)    
            d = dvalue(stdt, etdt, company)       
            c.drawString(10, d, str(month[-1]))
            d = dvalue(stdt, etdt, company)
            data(result, d)
                
    elif company[-1] != company[-2]:
        monthTotalPrint(d)
        d = dvalue(stdt, etdt, company)    
        companyTotalPrint(d)
        c.setPageSize(A4)
        c.showPage()
        header(stdt, etdt, company,month)
        d=newpage()
        c.drawString(10, d, str(month[-1]))
        d= dvalue(stdt, etdt, company)
        data(result,d)         
           


def header1(stdt,etdt,plant,month):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(310, 820, plant[-1]) 
    boldfonts(8)
    c.drawCentredString(310, 810, "Sales Summary From " + stdt.strftime('%d-%m-%Y') + " To " + etdt.strftime('%d-%m-%Y'))
    p=page()
    c.drawString(500,800,"Page No."+str(p))
    c.line(0, 790, 650, 790)
    c.line(0, 770, 650, 770)
    c.drawString(10, 778, "Prefix")
    c.drawString(200, 778, "Sales Qty.")
    c.drawString(270, 778, "Sales Amt.")
    c.drawString(340, 778, "JW Qty.")
    c.drawString(410, 778, "JW Amt.")
    c.drawString(480, 778, "Total Qty.")
    c.drawString(550, 778, "Total Amt.")

def data1(result,d):
    fonts(8)
    c.drawString(10, d, str(result['PREFIX']))
    c.drawAlignedString(230, d, str(result['SALESQTY']))
    c.drawAlignedString(300, d, str(result['SALESAMT']))
    c.drawAlignedString(340, d, str(result['JWQTY']))
    c.drawAlignedString(440, d, str(result['JWAMT']))
    c.drawAlignedString(500, d, str(result['TOTALQTY']))
    c.drawAlignedString(580, d, str(result['TOTALAMT']))
    Total(result)




def textsize1(c,result, d, stdt, etdt):
    d=dvalue(stdt, etdt, company)
    logic(result)
    if len(company) == 1:
        if len(month) == 1:
            header1(stdt,etdt,company,month)
            c.drawString(10,d,month[-1])
            d = dvalue(stdt, etdt, company)
            data1(result, d)                

    elif company[-1] == company[-2]:
        if month[-1] == month[-2]:
            if prefix[-1] == prefix[-2]:
                data1(result, d)
            elif prefix[-1] != prefix[-2]:
                d = dvalue(stdt, etdt, company)  
                monthTotalPrint(d)
                d = dvalue(stdt, etdt, company) 
                d = dvalue(stdt, etdt, company) 
                c.drawString(10, d, str(month[-1]))
                d = dvalue(stdt, etdt, company)  
                data1(result,d)

        elif month[-1] != month[-2]:
            monthTotalPrint(d)
            d = dvalue(stdt, etdt, company)    
            d = dvalue(stdt, etdt, company)       
            c.drawString(10, d, str(month[-1]))
            d = dvalue(stdt, etdt, company)
            data1(result, d)
                
    elif company[-1] != company[-2]:
        monthTotalPrint(d)
        d = dvalue(stdt, etdt, company)    
        companyTotalPrint(d)
        c.setPageSize(A4)
        c.showPage()
        header1(stdt, etdt, company,month)
        d=newpage()
        c.drawString(10, d, str(month[-1]))
        d= dvalue(stdt, etdt, company)
        data1(result,d)   