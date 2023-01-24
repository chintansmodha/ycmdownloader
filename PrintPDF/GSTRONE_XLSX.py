from datetime import datetime

import xlsxwriter
# from ProcessSelection import Export_Invoice_ProcessSelection as xlsfile
from GetDataFromDB import Export_Invoice_GetDataFromDB as xlsfilename

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


def filename():
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
    LSPath="D:/Report Development/Generated Reports/TCS Report/"
    LSFileName = "TDS Report Pur Inv" + LSFileName + ".xlsx"
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

row = 1
col = 0

LSName = datetime.now()
LSstring = str(LSName)
LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                  17:19] + LSstring[
                                                                                                           20:]

LSPath="D:/Report Development/Generated Reports/GSTRONE/"
LSFileName = "GSTRONE" + LSFileName + ".xlsx"
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
worksheet.set_column(0, 18, 25)
# worksheet.set_column(2, 2, 20)
# worksheet.set_column(3, 5, 10)
worksheet.set_column(6, 6, 80)
# worksheet.set_column(7, 7, 15)
# worksheet.set_column(8, 17, 10)

def xmlheader():
    worksheet.write('A1', "Sr. No.", format_dataleft)
    worksheet.write('B1', "Invoice Date", merge_format)
    worksheet.write('C1', "Invoice Number", format_dataleft)
    worksheet.write('D1', "Customer Billing Name", format_dataleft)
    worksheet.write('E1', "Customer Billing GSTIN", format_dataleft)
    worksheet.write('F1', "State Place of Supply (State/UT)", format_dataleft)
    worksheet.write('G1', "Is the item a GOOD (G) or SERVICE (S)", merge_format)
    worksheet.write('H1', "Item Description", merge_format)
    worksheet.write('I1', "HSN or SAC Code", format_dataright)
    worksheet.write('J1', "Item Quantity", merge_format)
    worksheet.write('K1', "Item Unit of Measurement", merge_format)
    worksheet.write('L1', "Item Rate", merge_format)
    worksheet.write('M1', " Total Item Discount Amount ", format_dataright)
    worksheet.write('N1', " Item Taxable Value ", merge_format)
    worksheet.write('O1', "CGST Rate", merge_format)
    worksheet.write('P1', " CGST Amount ", merge_format)
    worksheet.write('Q1', "SGST Rate", merge_format)
    worksheet.write('R1', " SGST Amount ", merge_format)
    worksheet.write('S1', "IGST Rate", merge_format)
    worksheet.write('T1', " IGST Amount ", merge_format)
    worksheet.write('U1', "CESS Rate", merge_format)
    worksheet.write('V1', " CESS Amount ", merge_format)
    worksheet.write('W1', "Is this a Bill of Supply?", merge_format)
    worksheet.write('X1', "Is this a Nil Rated/Exempt/Non GST Item?", merge_format)
    worksheet.write('Y1', "Original Invoice Date (In case of amendment)", format_dataleft)
    worksheet.write('Z1', "Original Invoice Number (In case of amendment)", format_dataleft)
    worksheet.write('AA1', "Original Customer Billing GSTIN (In case of amendment)", merge_format)
    worksheet.write('AB1', "GSTIN of Ecommerce Marketplace", merge_format)
    worksheet.write('AC1', "Date of Linked Advance Receipt", merge_format)
    worksheet.write('AD1', "Voucher Number of Linked Advance Receipt", merge_format)
    worksheet.write('AE1', "Adjustment Amount of the Linked Advance Receipt", merge_format)
    worksheet.write('AF1', "Type of Export", merge_format)
    worksheet.write('AG1', "Shipping Port Code - Export", merge_format)
    worksheet.write('AH1', "Shipping Bill Number - Export", merge_format)
    worksheet.write('AI1', "Shipping Bill Date - Export", merge_format)
    worksheet.write('AJ1', "Has GST/IDT TDS been deducted", merge_format)
    worksheet.write('AK1', "Is this Document Cancelled?", merge_format)
    worksheet.write('AL1', " TCS Amount ", merge_format)
    

def xmldata(result):
    global row
    global col
    worksheet.write(row, col, str(row), format_dataleft)
    worksheet.write(row, col+1, result['INVOICEDATE'].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+2, result['INVNO'],  merge_format)
    worksheet.write(row, col+3, result['CUSTOMERNAME'], format_dataleft)
    worksheet.write(row, col+4, result['CUSTOMERGSTNO'], format_dataleft)
    worksheet.write(row, col+5, result['PLACEOFSUPPLY'], format_dataleft)
    worksheet.write(row, col+6, result['ITEMGOODSORSERVICES'], format_dataleft)
    worksheet.write(row, col+7, result['ITEMDESCRIPTION'], format_dataright)
    worksheet.write(row, col+8, result['HSNCODE'], format_dataright)
    worksheet.write(row, col+9, result['ITEMQUANTITY'], format_dataleft)
    worksheet.write(row, col+10, result['ITEMUNITOFMEASUREMENT'], format_dataleft)
    worksheet.write(row, col+11, result['ITEMRATE'], format_dataleft)
    worksheet.write(row, col+12, result['TOTALITEMDISCOUNTAMOUNT'], format_dataleft)
    worksheet.write(row, col+13, result['ITEMTAXABLEVALUE'], format_dataleft)
    worksheet.write(row, col+14, result['CGSTRATE'], format_dataleft)
    worksheet.write(row, col+15, result['CGSTAMOUNT'], format_dataleft)
    worksheet.write(row, col+16, result['UTGSTRATE'], format_dataleft)
    worksheet.write(row, col+17, result['UTGSTAMOUNT'], format_dataleft)
    worksheet.write(row, col+18, result['IGSTRATE'], format_dataleft)
    worksheet.write(row, col+19, result['IGSTAMOUNT'], format_dataleft)
    worksheet.write(row, col+20, result['CESSRATE'], format_dataleft)
    worksheet.write(row, col+21, result['CESSAMOUNT'], format_dataleft)
    worksheet.write(row, col+22, result['BILLOFSUPPLY'], format_dataleft)
    worksheet.write(row, col+23, result['REVERSECHARGE'], format_dataleft)
    worksheet.write(row, col+24, result['NILLRATEDITEM'], format_dataleft)
    worksheet.write(row, col+25, result['ORIGINALINVDATE'], format_dataleft)
    worksheet.write(row, col+26, result['ORIGINALINVNUMBER'], format_dataleft)
    worksheet.write(row, col+27, result['ORIGINALINVCUSTOMER'], format_dataleft)
    worksheet.write(row, col+28, result['GSTINOFECOMMERCE'], format_dataleft)
    worksheet.write(row, col+29, result['DATEOFLINKEDADVANCERECEIPT'], format_dataleft)
    worksheet.write(row, col+30, result['VOUCHERNUMBEROFLINKEDADVANCERECEIPT'], format_dataleft)
    worksheet.write(row, col+31, result['ADVANCEADJAMOUNT'], format_dataleft)
    worksheet.write(row, col+32, result['TYPEOFEXPORT'], format_dataleft)
    worksheet.write(row, col+33, result['SHIPPINGPORTCODEEXPORT'], format_dataleft)
    worksheet.write(row, col+34, result['SHIPPINGBILLNUMBEREXPORT'], format_dataleft)
    worksheet.write(row, col+35, result['SHIPPINGBILLDATEEXPORT'], format_dataleft)
    worksheet.write(row, col+36, result['HASGST_IDT_TDS_DEDUCTED'], format_dataleft)
    worksheet.write(row, col+37, result['ISTHISDOCUMENTCANCELLED'], format_dataleft)
    worksheet.write(row, col+38, result['TCSAMOUNT'], format_dataleft)
    row=row+1


def textsize( result,  stdt, etdt):
    xmlheader()
    xmldata(result)
