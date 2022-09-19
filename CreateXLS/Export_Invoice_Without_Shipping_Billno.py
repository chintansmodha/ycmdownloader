from datetime import datetime

import xlsxwriter
# from ProcessSelection import Export_Invoice_ProcessSelection as xlsfile
from GetDataFromDB import Export_Invoice_GetDataFromDB as xlsfilename
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
##################################
LSPath=''
LSFileName=''
row = 3
col = 0
workbook=''
worksheet=''
merge_format=''
formatheader=''
format_dataright=''
format_dataleft=''


def filename(filetype):
    global worksheet
    global workbook
    global LSFileName
    global LSPath
    global col
    col=0
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSPath = "D:/Report Development/Generated Reports/Export Invoice/"
    if filetype=='4':
        LSFileName = LSPath+"Invoice Without Shipping Bill No Register " + LSFileName + ".xls"
    else:
        LSFileName = LSPath + "Invoice Without Shipping Bill No Register " + LSFileName + ".xls"
    # LSFileName = "GSTRegister" + LSFileName + ".xlsx"
    workbook = xlsxwriter.Workbook(LSFileName)
    worksheet = workbook.add_worksheet()
    format()
def format():
    global worksheet
    global workbook
    global formatheader
    global format_dataleft
    global format_dataright
    global merge_format
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
def mergecolums():
    global worksheet
    global workbook
    global formatheader
    global format_dataleft
    global format_dataright
    global merge_format
    worksheet.set_column(0, 1, 10)
    worksheet.set_column(2, 2, 20)
    worksheet.set_column(3, 5, 10)
    worksheet.set_column(6, 6, 80)
    worksheet.set_column(7, 7, 15)
    worksheet.set_column(8, 17, 10)
##################################

row = 3
col = 0
workbook=''
worksheet=''


# def createxls():
#     global  workbook
#     global worksheet
LSName = datetime.now()
LSstring = str(LSName)
#     global LSFileName
LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                  17:19] + LSstring[
                                                                                                           20:]

LSPath="D:/Report Development/Generated Reports/Export Invoice/"
LSFileName = "Invoice Without Shipping Bill No Register " + LSFileName + ".xlsx"
#     workbook = xlsxwriter.Workbook(xlsfilename.LSFileName)
#     worksheet = workbook.add_worksheet()
workbook = xlsxwriter.Workbook(str(LSPath+LSFileName))
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

# def xmlheader(stdt,etdt,divisioncode):
    # worksheet.merge_range('A1:R1', divisioncode[-1], formatheader)
    # worksheet.merge_range('A2:R2', "GST Register From " + str(stdt.strftime('%d-%m-%Y')) + " To " + str(etdt.strftime('%d-%m-%Y')), merge_format)
def xmlheader():
    # worksheet.write('A3', "MRNNO", merge_format)
    # worksheet.write('B3', "MRNDT", merge_format)
    # worksheet.write('C3', "BILLNO", merge_format)
    # worksheet.write('D3', "BILLDATE", merge_format)
    # worksheet.write('E3', "FINNO", merge_format)
    # worksheet.write('F3', "FINDATE", merge_format)
    # worksheet.write('G3', "SUPPLIER", merge_format)
    # worksheet.write('H3', "GSTNO", merge_format)
    # worksheet.write('I3', "QUANTITY", merge_format)
    # worksheet.write('J3', "RATE", merge_format)
    # worksheet.write('K3', "BASICVAL", merge_format)
    # worksheet.write('L3', "FREIGHT", merge_format)
    # worksheet.write('M3', "TCS", merge_format)
    # worksheet.write('N3', "INSURANCE", merge_format)
    # worksheet.write('O3', "OTH.CHGE", merge_format)
    # worksheet.write('P3', "IGST", merge_format)
    # worksheet.write('Q3', "CGST", merge_format)
    # worksheet.write('R3', "UTGST", merge_format)
    print("header printing ")
    worksheet.write('A1', "Inv. Date	", merge_format)
    worksheet.write('B1', "Inv. No	Export", merge_format)
    worksheet.write('C1', "Inv No", merge_format)
    worksheet.write('D1', "Customer Name", merge_format)
    worksheet.write('E1', "EXPORT COUNTRY	", merge_format)
    worksheet.write('F1', "Item Description", merge_format)
    worksheet.write('G1', "HSN Code", merge_format)
    worksheet.write('H1', "Item Quantity	", merge_format)
    worksheet.write('I1', "Item Rate	", merge_format)
    worksheet.write('J1', "IGST Rate	", merge_format)
    worksheet.write('K1', "IGST Amount", merge_format)
    worksheet.write('L1', "Type Of Export	", merge_format)
    worksheet.write('M1', "Shipping Port Code Export", merge_format)
    worksheet.write('N1', "Shipping Bill Number Export", merge_format)
    worksheet.write('O1', "Shipping Bill Date Export	", merge_format)
    worksheet.write('P1', "EGM NO	", merge_format)
    worksheet.write('Q1', "EGM DATE	", merge_format)
    worksheet.write('R1', "Invoice Currency ", merge_format)
    worksheet.write('S1', "Exchange Rate	", merge_format)
    worksheet.write('T1', "Invoice Value In Currency", merge_format)
    worksheet.write('U1', "Invoice Value In INR", merge_format)
    worksheet.write('V1', "FOB Value In Currency", merge_format)
    worksheet.write('W1', "FOB Value In INR	", merge_format)
    # worksheet.write('X1', "EPCG LICENCE NO 	", merge_format)
    # worksheet.write('Y1', "ADVANCE LICENCE NO ", merge_format)
    # worksheet.write('Z1', "DBK RS	", merge_format)
    # worksheet.write('AA1', "EGM NO	", merge_format)
    # worksheet.write('AB1', "EGM DATE	", merge_format)
    # worksheet.write('AC1', "ADVANCE ", merge_format)
    # worksheet.write('AD1', "FINAL 	", merge_format)
    # worksheet.write('AE1', "OUTSTANDING", merge_format)
    # worksheet.write('AF1', "BANK REFEREBCE NO ", merge_format)

def xmldata(result):
    global row
    global col
    # worksheet.write(row, col,result["MRNNO"], format_dataleft)
    # worksheet.write(row, col+1,result["MRNDATE"].strftime('%d-%m-%Y'), format_dataleft)
    # worksheet.write(row, col+2,result["BILLNO"], format_dataleft)
    # worksheet.write(row, col+3,result["BILLDATE"].strftime('%d-%m-%Y'), format_dataleft)
    # worksheet.write(row, col+4,result["FINNO"], format_dataleft)
    # worksheet.write(row, col+5,result["FINDATE"].strftime('%d-%m-%Y'), format_dataleft)
    # worksheet.write(row, col+6,result["SUPPLIER"], format_dataleft)
    # worksheet.write(row, col+7,result["GSTNO"], format_dataleft)
    # worksheet.write(row, col+8,str("%.3f" % float(result["QUANTITY"])), format_dataright)
    # worksheet.write(row, col+9,str("%.3f" % float(result["RATE"])), format_dataright)
    # worksheet.write(row, col+10,str("%.3f" % float(result["BASICVALUE"])), format_dataright)
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

    worksheet.write(row, col, result['INVDATE'].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+1, result['INVCODE'],  merge_format)
    worksheet.write(row, col+2, result['EXPORTINVNO'], merge_format)
    worksheet.write(row, col+3, result['CUSTOMER'], merge_format)
    worksheet.write(row, col+4, result['EXPORTCOUNTRY'], merge_format)
    worksheet.write(row, col+5, result['PRODUCT'], merge_format)
    worksheet.write(row, col+6, result['HSNCODE'], merge_format)
    worksheet.write(row, col+7, result['QTY'], merge_format)
    worksheet.write(row, col+8, result['RATE'], merge_format)
    # worksheet.write(row, col+9, result[''], IGST    Rate, merge_format)
    # worksheet.write(row, col+10, result[""], IGST    Amount, merge_format)
    # worksheet.write(row, col+11, result[""], Type    Of    Export, merge_format)
    # worksheet.write(row, col+12, result[""], Shipping    Port    Code    Export, merge_format)
    # worksheet.write(row, col+13, result[""], Shipping    Bill    Number    Export, merge_format)
    # worksheet.write(row, col+14, result[""], Shipping    Bill    Date    Export, merge_format)
    # worksheet.write(row, col+15, result[""], EGM    NO, merge_format)
    # worksheet.write(row, col+16, result[""], EGM    DATE, merge_format)
    worksheet.write(row, col+17, result['INVOICECURRENCY'], merge_format)
    worksheet.write(row, col+18, result['EXCHANGERATE'], merge_format)
    worksheet.write(row, col+19, result['INVOICEVALUEINCURRENCY'], merge_format)
    worksheet.write(row, col+20, result['INVOICEVALUEOFINR'], merge_format)
    # worksheet.write(row, col+21, result[""], FOB    Value    In    Currency, merge_format)
    # worksheet.write(row, col+22, result[""], FOB    Value    In    INR, merge_format)
    # worksheet.write(row, col+23, result[""], EPCG    LICENCE    NO , merge_format)
    # worksheet.write(row, col+24,result[""], ADVANCE LICENCE NO , merge_format)
    # worksheet.write(row, col+25,result[""], DBK RS	, merge_format)
    # worksheet.write(row, col+26,result[""], EGM NO	, merge_format)
    # worksheet.write(row, col+27,result[""], EGM DATE	, merge_format)
    # worksheet.write(row, col+28,result[""], ADVANCE , merge_format)
    # worksheet.write(row, col+29,result[""], FINAL 	, merge_format)
    # worksheet.write(row, col+30,result[""], OUTSTANDING, merge_format)
    # worksheet.write(row, col31,result[""], BANK REFEREBCE NO , merge_format)
    row=row+1

def xmlheader5():
    # worksheet.write('A3', "MRNNO", merge_format)
    # worksheet.write('B3', "MRNDT", merge_format)
    # worksheet.write('C3', "BILLNO", merge_format)
    # worksheet.write('D3', "BILLDATE", merge_format)
    # worksheet.write('E3', "FINNO", merge_format)
    # worksheet.write('F3', "FINDATE", merge_format)
    # worksheet.write('G3', "SUPPLIER", merge_format)
    # worksheet.write('H3', "GSTNO", merge_format)
    # worksheet.write('I3', "QUANTITY", merge_format)
    # worksheet.write('J3', "RATE", merge_format)
    # worksheet.write('K3', "BASICVAL", merge_format)
    # worksheet.write('L3', "FREIGHT", merge_format)
    # worksheet.write('M3', "TCS", merge_format)
    # worksheet.write('N3', "INSURANCE", merge_format)
    # worksheet.write('O3', "OTH.CHGE", merge_format)
    # worksheet.write('P3', "IGST", merge_format)
    # worksheet.write('Q3', "CGST", merge_format)
    # worksheet.write('R3', "UTGST", merge_format)
    print("header printing ")
    worksheet.write('A1', "Inv. Date	", merge_format)
    worksheet.write('B1', "Inv. No	Export", merge_format)
    worksheet.write('C1', "Inv No", merge_format)
    worksheet.write('D1', "Customer Name", merge_format)
    worksheet.write('E1', "EXPORT COUNTRY	", merge_format)
    worksheet.write('F1', "Item Description", merge_format)
    worksheet.write('G1', "HSN Code", merge_format)
    worksheet.write('H1', "Item Quantity	", merge_format)
    worksheet.write('I1', "Item Rate	", merge_format)
    worksheet.write('J1', "IGST Rate	", merge_format)
    worksheet.write('K1', "IGST Amount", merge_format)
    worksheet.write('L1', "Type Of Export	", merge_format)
    worksheet.write('M1', "Shipping Port Code Export", merge_format)
    worksheet.write('N1', "Shipping Bill Number Export", merge_format)
    worksheet.write('O1', "Shipping Bill Date Export	", merge_format)
    worksheet.write('P1', "Invoice Currency ", merge_format)
    worksheet.write('Q1', "Exchange Rate	", merge_format)
    worksheet.write('R1', "Invoice Value In Currency", merge_format)
    worksheet.write('S1', "Invoice Value In INR", merge_format)
    worksheet.write('T1', "FOB Value In Currency", merge_format)
    worksheet.write('U1', "FOB Value In INR	", merge_format)

def xmldata5(result):
    print("5 data")
    global row
    global col
    # worksheet.write(row, col,result["MRNNO"], format_dataleft)
    # worksheet.write(row, col+1,result["MRNDATE"].strftime('%d-%m-%Y'), format_dataleft)
    # worksheet.write(row, col+2,result["BILLNO"], format_dataleft)
    # worksheet.write(row, col+3,result["BILLDATE"].strftime('%d-%m-%Y'), format_dataleft)
    # worksheet.write(row, col+4,result["FINNO"], format_dataleft)
    # worksheet.write(row, col+5,result["FINDATE"].strftime('%d-%m-%Y'), format_dataleft)
    # worksheet.write(row, col+6,result["SUPPLIER"], format_dataleft)
    # worksheet.write(row, col+7,result["GSTNO"], format_dataleft)
    # worksheet.write(row, col+8,str("%.3f" % float(result["QUANTITY"])), format_dataright)
    # worksheet.write(row, col+9,str("%.3f" % float(result["RATE"])), format_dataright)
    # worksheet.write(row, col+10,str("%.3f" % float(result["BASICVALUE"])), format_dataright)
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

    worksheet.write(row, col, result['INVDATE'].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+1, result['INVCODE'],  merge_format)
    worksheet.write(row, col+2, result['EXPORTINVNO'], merge_format)
    worksheet.write(row, col+3, result['CUSTOMER'], merge_format)
    worksheet.write(row, col+4, result['EXPORTCOUNTRY'], merge_format)
    worksheet.write(row, col+5, result['PRODUCT'], merge_format)
    worksheet.write(row, col+6, result['HSNCODE'], merge_format)
    worksheet.write(row, col+7, result['QTY'], merge_format)
    worksheet.write(row, col+8, result['RATE'], merge_format)
    worksheet.write(row, col+9, 0, merge_format)
    worksheet.write(row, col+10,0, merge_format)
    worksheet.write(row, col+11, "Export without GST", merge_format)
    worksheet.write(row, col+12, result['SHIPPINGPORTCODEEXPORT'], merge_format)
    worksheet.write(row, col+13, result['SHIPPINGBILLNUMBEREXPORT'], merge_format)
    worksheet.write(row, col+14, result['SHIPPINGBILLDATEEXPORT'], merge_format)
    # worksheet.write(row, col+15, result[""], EGM    NO, merge_format)
    # worksheet.write(row, col+16, result[""], EGM    DATE, merge_format)
    worksheet.write(row, col+15, result['INVOICECURRENCY'], merge_format)
    worksheet.write(row, col+16, result['EXCHANGERATE'], merge_format)
    worksheet.write(row, col+17, result['INVOICEVALUEINCURRENCY'], merge_format)
    worksheet.write(row, col+18, result['INVOICEVALUEOFINR'], merge_format)
    worksheet.write(row, col+19, result['FOBVALUEINCC'], merge_format)
    worksheet.write(row, col+20, result['FOBVALUEINR'], merge_format)
    # worksheet.write(row, col+23, result[""], EPCG    LICENCE    NO , merge_format)
    # worksheet.write(row, col+24,result[""], ADVANCE LICENCE NO , merge_format)
    # worksheet.write(row, col+25,result[""], DBK RS	, merge_format)
    # worksheet.write(row, col+26,result[""], EGM NO	, merge_format)
    # worksheet.write(row, col+27,result[""], EGM DATE	, merge_format)
    # worksheet.write(row, col+28,result[""], ADVANCE , merge_format)
    # worksheet.write(row, col+29,result[""], FINAL 	, merge_format)
    # worksheet.write(row, col+30,result[""], OUTSTANDING, merge_format)
    # worksheet.write(row, col31,result[""], BANK REFEREBCE NO , merge_format)
    row=row+1
    print("5 data over")

def page():
    global pageno
    pageno = pageno + 1
    return pageno



def dvalue():
    global d
    d=d-10
    return d

def total(result):
    global CompanyQuantityTotal
    global CompanyBasicValueTotal
    global CompanyFreightTotal
    global CompanyOTHChargesTotal
    global StoreQuantityTotal
    global StoreBasicValueTotal
    global StoreFreightTotal
    global StoreOTHChargesTotal
    CompanyQuantityTotal = CompanyQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    CompanyBasicValueTotal = CompanyBasicValueTotal + float(("%.3f" % float(result['BASICVALUE'])))
    CompanyFreightTotal = CompanyFreightTotal + float(("%.3f" % float(result['FREIGHT'])))
    CompanyOTHChargesTotal = CompanyOTHChargesTotal + float(("%.3f" % float(result['OTHER'])))
    StoreQuantityTotal = StoreQuantityTotal + float(("%.3f" % float(result['QUANTITY'])))
    StoreBasicValueTotal = StoreBasicValueTotal + float(("%.3f" % float(result['BASICVALUE'])))
    StoreFreightTotal = StoreFreightTotal + float(("%.3f" % float(result['FREIGHT'])))
    StoreOTHChargesTotal = StoreOTHChargesTotal + float(("%.3f" % float(result['OTHER'])))


def logic(result):
    divisioncode.append(result['DIVCODE'])
    mrnno.append(result['MRNNO'])
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
    global row
    global col
    global workbook
    global worksheet
    divisioncode=[]
    pageno=0
    mrnno=[]
    row = 3
    col = 0
    workbook = ''
    worksheet = ''

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

def textsize( result,  stdt, etdt):
    xmldata(result)


def textsize5(result, stdt, etdt):

    xmldata5(result)
