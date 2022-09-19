from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import xlsxwriter
from Global_Files import Connection_String as con

row = 3
col = 0

workbook = xlsxwriter.Workbook('jigar.xlsx')
worksheet = workbook.add_worksheet()

merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_size':10,
})
formatheader=workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_size':15,
})
format_dataright = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'right',
    'valign': 'vcenter',
    'font_size':10,
})
format_dataleft = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'left',
    'valign': 'vcenter',
    'font_size':10,
})
worksheet.set_column(0, 1, 10)
worksheet.set_column(2, 2, 20)
worksheet.set_column(3, 5, 10)
worksheet.set_column(6, 6, 80)
worksheet.set_column(7, 7, 15)
worksheet.set_column(8, 17, 10)

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
c = canvas.Canvas("1.pdf",pagesize=(landscape(A3)))
c.setPageSize(landscape(A3))
d = 730

store=[]
mrnno=[]
divisioncode=[]
pageno=0
CompanyQuantityTotal=0
CompanyBasicValueTotal=0
CompanyFreightTotal=0
CompanyTCSTotal=0
CompanyInsuranceTotal=0
CompanyOTHChargesTotal=0
CompanyIGSTTotal=0
CompanyCGSTTotal=0
CompanyUTGSTTotal=0

StoreQuantityTotal=0
StoreBasicValueTotal=0
StoreFreightTotal=0
StoreTCSTotal=0
StoreInsuranceTotal=0
StoreOTHChargesTotal=0
StoreIGSTTotal=0
StoreCGSTTotal=0
StoreUTGSTTotal=0

def page():
    global pageno
    pageno = pageno + 1
    return pageno

def fonts(size):
    global c
    c.setFont("MyOwnArial", size)

def dvalue():
    global d
    d=d-10
    return d

def xmlheader(stdt,etdt,divisioncode):
    worksheet.merge_range('A1:R1', divisioncode[-1], formatheader)
    worksheet.merge_range('A2:R2', "GST Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')), merge_format)
    worksheet.write('A3', "MRNNO", merge_format)
    worksheet.write('B3', "MRNDT", merge_format)
    worksheet.write('C3', "BILLNO", merge_format)
    worksheet.write('D3', "BILLDATE", merge_format)
    worksheet.write('E3', "FINNO", merge_format)
    worksheet.write('F3', "FINDATE", merge_format)
    worksheet.write('G3', "SUPPLIER", merge_format)
    worksheet.write('H3', "GSTNO", merge_format)
    worksheet.write('I3', "QUANTITY", merge_format)
    worksheet.write('J3', "RATE", merge_format)
    worksheet.write('K3', "BASICVAL", merge_format)
    worksheet.write('L3', "FREIGHT", merge_format)
    worksheet.write('M3', "TCS", merge_format)
    worksheet.write('N3', "INSURANCE", merge_format)
    worksheet.write('O3', "OTH.CHGE", merge_format)
    worksheet.write('P3', "IGST", merge_format)
    worksheet.write('Q3', "CGST", merge_format)
    worksheet.write('R3', "UTGST", merge_format)

def xmldata(result):
    global row
    global col
    worksheet.write(row, col,result["MRNNO"], format_dataleft)
    worksheet.write(row, col+1,result["MRNDATE"].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+2,result["BILLNO"], format_dataleft)
    worksheet.write(row, col+3,result["BILLDATE"].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+4,result["FINNO"], format_dataleft)
    worksheet.write(row, col+5,result["FINDATE"].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+6,result["SUPPLIER"], format_dataleft)
    worksheet.write(row, col+7,result["GSTNO"], format_dataleft)
    worksheet.write(row, col+8,str("%.3f" % float(result["QUANTITY"])), format_dataright)
    worksheet.write(row, col+9,str("%.3f" % float(result["RATE"])), format_dataright)
    worksheet.write(row, col+10,str("%.3f" % float(result["BASICVALUE"])), format_dataright)
    # worksheet.write(row, col+11,str("%.3f" % float(result["FREIGHT"])), format_dataright)
    # if result['TCS'] != None:
    #     worksheet.write(row, col+12,str("%.3f" % float(result["TCS"])), format_dataright)
    # if result['INSURANCE'] != None:
    #     worksheet.write(row, col+13,str("%.3f" % float(result["INSURANCE"])), format_dataright)
    # worksheet.write(row, col+14,str("%.3f" % float(result["OTHER"])), format_dataright)
    # if result['IGST'] != None:
    #     worksheet.write(row, col+15,str("%.3f" % float(result["IGST"])), format_dataright)
    # if result['CGST'] != None:
    #     worksheet.write(row, col+16,str("%.3f" % float(result["CGST"])), format_dataright)
    # if result['UTGST'] != None:
    #     worksheet.write(row, col+17,str("%.3f" % float(result["UTGST"])), format_dataright)
    # row=row+1


def header(stdt,etdt,divisioncode):
    fonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(595, 800, divisioncode[-1])
    fonts(9)
    c.drawCentredString(595, 780, "GST Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')))
    p=page()
    c.drawString(1100,780,"Page No."+str(p))
    c.line(0, 760, 1190, 760)
    c.line(0, 740, 1190, 740)
    #Upperline in header
    c.drawString(10, 750, "MRNNO")
    c.drawString(60, 750, "MRNDT")
    c.drawString(110, 750, "BILLNO")
    c.drawString(180, 750, "BILLDATE")
    c.drawString(230, 750, "FINNO")
    c.drawString(280, 750, "FINDATE")
    #LowerLine in header
    c.drawString(330, 750, "SUPPLIER")
    c.drawString(620, 750, "GSTNO")
    c.drawString(700, 750, "QUANTITY")
    c.drawString(760, 750, "RATE")
    c.drawString(800, 750, "BASICVAL")
    c.drawString(850, 750, "FREIGHT")
    c.drawString(900, 750, "TCS")
    c.drawString(930, 750, "INSURANCE")
    c.drawString(990, 750, "OTH.CHGE")
    c.drawString(1060, 750, "IGST")
    c.drawString(1110, 750, "CGST")
    c.drawString(1150, 750, "UTGST")
    xmlheader(stdt,etdt,divisioncode)

def data(result,d):
    global CompanyTCSTotal
    global CompanyInsuranceTotal
    global CompanyIGSTTotal
    global CompanyCGSTTotal
    global CompanyUTGSTTotal
    global StoreTCSTotal
    global StoreInsuranceTotal
    global StoreIGSTTotal
    global StoreCGSTTotal
    global StoreUTGSTTotal
    fonts(7)
    # Upperline in data
    c.drawString(10, d, result['MRNNO'])
    c.drawString(60, d, str(result['MRNDATE'].strftime('%d-%m-%Y')))
    c.drawString(110, d, result['BILLNO'])
    c.drawString(180, d, str(result['BILLDATE'].strftime('%d-%m-%Y')))
    c.drawString(230, d, result['FINNO'])
    c.drawString(280, d, str(result['FINDATE'].strftime('%d-%m-%Y')))
    c.drawString(330, d, result['SUPPLIER'])
    c.drawString(620, d, str(result['GSTNO']))
    c.drawAlignedString(730, d, str(("%.3f" % float(result['QUANTITY']))))
    c.drawAlignedString(770, d, str(("%.3f" % float(result['RATE']))))
    c.drawAlignedString(830, d, str(("%.3f" % float(result['BASICVALUE']))))
    subdata(result)
    xmldata(result)
    total(result)

def subdata(resultset):
    print(resultset['ID'])
    global CompanyTCSTotal
    global CompanyInsuranceTotal
    global CompanyIGSTTotal
    global CompanyCGSTTotal
    global CompanyUTGSTTotal
    global StoreTCSTotal
    global StoreInsuranceTotal
    global StoreIGSTTotal
    global StoreCGSTTotal
    global StoreUTGSTTotal
    sql = "Select (select sum(INDTAXDETAIL.CALCULATEDVALUE) from INDTAXDETAIL, ITAX where INDTAXDETAIL.TAXCATEGORYCODE='GST'" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE AND INDTAXDETAIL.ITAXCODE=ITAX.CODE" \
          " AND ITAX.FORMTYPECODE='IGS') AS IGST," \
          "(select sum(INDTAXDETAIL.CALCULATEDVALUE) from INDTAXDETAIL, ITAX where INDTAXDETAIL.TAXCATEGORYCODE='GST'" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE AND INDTAXDETAIL.ITAXCODE=ITAX.CODE" \
          " AND ITAX.FORMTYPECODE='CGS') AS CGST," \
          "(select sum(INDTAXDETAIL.CALCULATEDVALUE) from INDTAXDETAIL, ITAX where INDTAXDETAIL.TAXCATEGORYCODE='GST'" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE AND INDTAXDETAIL.ITAXCODE=ITAX.CODE" \
          " AND ITAX.FORMTYPECODE='SGS') AS UTGST," \
          "(select sum(INDTAXDETAIL.CALCULATEDVALUE) from INDTAXDETAIL where INDTAXDETAIL.TAXCATEGORYCODE='FRT'" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE) AS FREIGHT," \
          "(select sum(INDTAXDETAIL.CALCULATEDVALUE) from INDTAXDETAIL where INDTAXDETAIL.TAXCATEGORYCODE='INS'" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE) AS INSURANCE," \
          "(select sum(INDTAXDETAIL.CALCULATEDVALUE) from INDTAXDETAIL where INDTAXDETAIL.TAXCATEGORYCODE='TCS'" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE) AS TCS," \
          "(select COALESCE(sum(INDTAXDETAIL.CALCULATEDVALUE),'') from INDTAXDETAIL where INDTAXDETAIL.TAXCATEGORYCODE NOT IN ('GST','FRT','INS','TCS','SYS')" \
          " AND INDTAXDETAIL.ABSUNIQUEID=MRNDETAIL.ABSUNIQUEID AND INDTAXDETAIL.TAXTEMPLATECODE=MRNDETAIL.TAXTEMPLATECODE" \
          " AND INDTAXDETAIL.TAXTEMPLATETEMPLATETYPE=MRNDETAIL.TAXTEMPLATETEMPLATETYPE) AS OTHER" \
          " From    MRNDETAIL" \
          " Where MRNDETAIL.ABSUNIQUEID = '"+str(resultset['ID'])+"'"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        subdatatottal(result)
        c.drawAlignedString(870, d, str(("%.3f" % float(result['FREIGHT']))))

        if result['TCS'] != None:
            c.drawString(910, d, str(("%.3f" % float(result['TCS']))))
            CompanyTCSTotal = CompanyTCSTotal + float(("%.3f" % float(result['TCS'])))

        if result['INSURANCE'] != None:
            c.drawAlignedString(960, d, str(("%.3f" % float(result['INSURANCE']))))
            CompanyInsuranceTotal = CompanyInsuranceTotal + float(("%.3f" % float(result['INSURANCE'])))
            StoreInsuranceTotal = StoreInsuranceTotal + float(("%.3f" % float(result['INSURANCE'])))

        c.drawAlignedString(1020, d, str(("%.3f" % float(result['OTHER']))))

        if result['IGST'] != None:
            c.drawAlignedString(1070, d, str(("%.3f" % float(result['IGST']))))
            CompanyIGSTTotal = CompanyIGSTTotal + float(("%.3f" % float(result['IGST'])))
            StoreIGSTTotal = StoreIGSTTotal + float(("%.3f" % float(result['IGST'])))

        if result['CGST'] != None:
            c.drawAlignedString(1120, d, str(("%.3f" % float(result['CGST']))))
            CompanyCGSTTotal = CompanyCGSTTotal + float(("%.3f" % float(result['CGST'])))
            StoreCGSTTotal = StoreCGSTTotal + float(("%.3f" % float(result['CGST'])))

        if result['UTGST'] != None:
            c.drawAlignedString(1170, d, str(("%.3f" % float(result['UTGST']))))
            CompanyUTGSTTotal = CompanyUTGSTTotal + float(("%.3f" % float(result['UTGST'])))
            StoreUTGSTTotal = StoreUTGSTTotal + float(("%.3f" % float(result['UTGST'])))

        result = con.db.fetch_both(stmt)

def total(result):
    global CompanyQuantityTotal
    global CompanyBasicValueTotal
    global StoreQuantityTotal
    global StoreBasicValueTotal
    CompanyQuantityTotal = CompanyQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    CompanyBasicValueTotal = CompanyBasicValueTotal + float(("%.3f" % float(result['BASICVALUE'])))
    StoreQuantityTotal = StoreQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    StoreBasicValueTotal = StoreBasicValueTotal + float(("%.3f" % float(result['BASICVALUE'])))

def subdatatottal(result):
    global StoreFreightTotal
    global StoreOTHChargesTotal
    global CompanyFreightTotal
    global CompanyOTHChargesTotal
    StoreFreightTotal = StoreFreightTotal + float(("%.3f" % float(result['FREIGHT'])))
    StoreOTHChargesTotal = StoreOTHChargesTotal + float(("%.3f" % float(result['OTHER'])))
    CompanyFreightTotal = CompanyFreightTotal + float(("%.3f" % float(result['FREIGHT'])))
    CompanyOTHChargesTotal = CompanyOTHChargesTotal + float(("%.3f" % float(result['OTHER'])))

def logic(result):
    divisioncode.append(result['DIVCODE'])
    mrnno.append(result['ID'])
    store.append(result['STORE'])


def dlocvalue():
    global d
    d = d+20
    return d

def newpage():
    global d
    d = 730
    return d

def newrequest():
    global divisioncode
    global pageno
    global mrnno
    divisioncode=[]
    pageno=0
    mrnno=[]

def printtotal():
    global CompanyQuantityTotal
    global CompanyBasicValueTotal
    global CompanyFreightTotal
    global CompanyTCSTotal
    global CompanyInsuranceTotal
    global CompanyOTHChargesTotal
    global CompanyIGSTTotal
    global CompanyCGSTTotal
    global CompanyUTGSTTotal

    c.drawString(10, d, str(divisioncode[-2]) + " TOTAL : ")
    c.drawAlignedString(730, d, str("%.3f" % float(CompanyQuantityTotal)))
    c.drawAlignedString(830, d, str("%.3f" % float(CompanyBasicValueTotal)))
    c.drawAlignedString(870, d, str("%.3f" % float(CompanyFreightTotal)))
    c.drawAlignedString(910, d, str("%.3f" % float(CompanyTCSTotal)))
    c.drawAlignedString(960, d, str("%.3f" % float(CompanyInsuranceTotal)))
    c.drawAlignedString(1020, d, str("%.3f" % float(CompanyOTHChargesTotal)))
    c.drawAlignedString(1070, d, str("%.3f" % float(CompanyIGSTTotal)))
    c.drawAlignedString(1120, d, str("%.3f" % float(CompanyCGSTTotal)))
    c.drawAlignedString(1170, d, str("%.3f" % float(CompanyUTGSTTotal)))

def printstoretotal():
    global StoreTCSTotal
    global StoreInsuranceTotal
    global StoreIGSTTotal
    global StoreCGSTTotal
    global StoreUTGSTTotal
    global StoreQuantityTotal
    global StoreBasicValueTotal
    global StoreFreightTotal
    global StoreOTHChargesTotal

    c.drawString(110, d, str(store[-2]) + " TOTAL : ")
    c.drawAlignedString(730, d, str("%.3f" % float(StoreQuantityTotal)))
    c.drawAlignedString(830, d, str("%.3f" % float(StoreBasicValueTotal)))
    c.drawAlignedString(870, d, str("%.3f" % float(StoreFreightTotal)))
    c.drawAlignedString(910, d, str("%.3f" % float(StoreTCSTotal)))
    c.drawAlignedString(960, d, str("%.3f" % float(StoreInsuranceTotal)))
    c.drawAlignedString(1020, d, str("%.3f" % float(StoreOTHChargesTotal)))
    c.drawAlignedString(1070, d, str("%.3f" % float(StoreIGSTTotal)))
    c.drawAlignedString(1120, d, str("%.3f" % float(StoreCGSTTotal)))
    c.drawAlignedString(1170, d, str("%.3f" % float(StoreUTGSTTotal)))

def companyclean():
    global CompanyQuantityTotal
    global CompanyBasicValueTotal
    global CompanyFreightTotal
    global CompanyOTHChargesTotal
    global CompanyTCSTotal
    global CompanyInsuranceTotal
    global CompanyIGSTTotal
    global CompanyCGSTTotal
    global CompanyUTGSTTotal

    CompanyQuantityTotal = 0
    CompanyBasicValueTotal = 0
    CompanyFreightTotal = 0
    CompanyTCSTotal = 0
    CompanyInsuranceTotal = 0
    CompanyOTHChargesTotal = 0
    CompanyIGSTTotal = 0
    CompanyCGSTTotal = 0
    CompanyUTGSTTotal = 0
def cleanstore():
    global store
    store=[]

def storeclean():
    global StoreTCSTotal
    global StoreInsuranceTotal
    global StoreIGSTTotal
    global StoreCGSTTotal
    global StoreUTGSTTotal
    global StoreQuantityTotal
    global StoreBasicValueTotal
    global StoreFreightTotal
    global StoreOTHChargesTotal

    StoreQuantityTotal = 0
    StoreBasicValueTotal = 0
    StoreFreightTotal = 0
    StoreTCSTotal = 0
    StoreInsuranceTotal = 0
    StoreOTHChargesTotal = 0
    StoreIGSTTotal = 0
    StoreCGSTTotal = 0
    StoreUTGSTTotal = 0

def textsize(c, result, d, stdt, etdt):
    d=dvalue()
    logic(result)
    if len(divisioncode)==1:
        if len(store)==1:
            if len(mrnno)==1:
                header(stdt,etdt,divisioncode)
                fonts(7)
                c.drawString(10, d, str(store[-1]))
                d=dvalue()
                data(result, d)


    elif divisioncode[-2]==divisioncode[-1]:
        if store[-2]==store[-1]:
            if mrnno[-2]==mrnno[-1]:
                d=dlocvalue()
            elif  mrnno[-2]!=mrnno[-1]:
                data(result,d)
        elif store[-2]!=store[-1]:
            fonts(7)
            printstoretotal()
            storeclean()
            d=dvalue()
            c.drawString(10, d, str(store[-1]))
            d=dvalue()
            if mrnno[-2]==mrnno[-1]:
                d=dlocvalue()
            elif  mrnno[-2]!=mrnno[-1]:
                data(result,d)


    elif divisioncode[-2]!=divisioncode[-1]:
        printstoretotal()
        d=dvalue()
        printtotal()
        companyclean()
        storeclean()

        c.setPageSize(landscape(A3))
        c.showPage()

        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue()

        if len(store)==1:
            data(result,d)

        elif store[-2] == store[-1]:
            if mrnno[-2] == mrnno[-1]:
                d = dlocvalue()
            elif mrnno[-2] != mrnno[-1]:
                data(result, d)
        elif store[-2] != store[-1]:
            fonts(7)
            d=dvalue()
            c.drawString(10, d, str(store[-1]))
            d = dvalue()
            if mrnno[-2] == mrnno[-1]:
                d = dlocvalue()
            elif mrnno[-2] != mrnno[-1]:
                data(result, d)


