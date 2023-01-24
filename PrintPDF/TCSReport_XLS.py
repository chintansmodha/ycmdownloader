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
    LSFileName = "TCS Report Sale Inv" + LSFileName + ".xlsx"
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

LSPath="D:/Report Development/Generated Reports/TCS Report/"
LSFileName = "TCS Report Sale Inv" + LSFileName + ".xlsx"
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
    worksheet.write('A1', "Voucher No.", format_dataleft)
    worksheet.write('B1', "Section Code (*)", merge_format)
    worksheet.write('C1', "Date of Payment (*)", format_dataleft)
    worksheet.write('D1', "Party Code", format_dataleft)
    worksheet.write('E1', "Party Name (*)", format_dataleft)
    worksheet.write('F1', "PAN No.", format_dataleft)
    worksheet.write('G1', "Party Type", merge_format)
    worksheet.write('H1', "Branch", merge_format)
    worksheet.write('I1', "Gross Amount (*)", format_dataright)
    worksheet.write('J1', "TDS Rate", merge_format)
    worksheet.write('K1', "Surcharge Rate", merge_format)
    worksheet.write('L1', "Eductation Cess", merge_format)
    worksheet.write('M1', "TDS Amount (*)", format_dataright)
    worksheet.write('N1', "No/Lower/Higher TDS Reason", merge_format)
    worksheet.write('O1', "Address 1", merge_format)
    worksheet.write('P1', "Address 2", merge_format)
    worksheet.write('Q1', "Address 3", merge_format)
    worksheet.write('R1', "Address 4", merge_format)
    worksheet.write('S1', "Address 5", merge_format)
    worksheet.write('T1', "State Description", merge_format)
    worksheet.write('U1', "State Code", merge_format)
    worksheet.write('V1', "Pin Code", merge_format)
    worksheet.write('W1', "Narration", merge_format)
    worksheet.write('X1', "RefNo", merge_format)
    worksheet.write('Y1', "Invoice No", format_dataleft)
    worksheet.write('Z1', "Invoice Date", format_dataleft)
    worksheet.write('AA1', "IsCredited", merge_format)
    worksheet.write('AB1', "ContactPerson", merge_format)
    worksheet.write('AC1', "MobileNo", merge_format)
    worksheet.write('AD1', "Email", merge_format)
    

def xmldata(result):
    global row
    global col

    worksheet.write(row, col, result['VCHNO'], format_dataleft)
    # worksheet.write(row, col+1, result['INVCODE'],  merge_format)
    worksheet.write(row, col+2, result['DATEOFPAYMENT'].strftime('%d-%m-%Y'), format_dataleft)
    worksheet.write(row, col+3, result['PANNO'], format_dataleft)
    worksheet.write(row, col+4, result['PARTY'], format_dataleft)
    worksheet.write(row, col+5, result['PANNO'], format_dataleft)
    worksheet.write(row, col+8, result['GROSSAMOUNT'], format_dataright)
    worksheet.write(row, col+12, result['TDSAMOUNT'], format_dataright)
    worksheet.write(row, col+24, result['INVOICENO'], format_dataleft)
    worksheet.write(row, col+25, result['INVOICEDATE'].strftime('%d-%m-%Y'), format_dataleft)
    row=row+1


def textsize( result,  stdt, etdt):
    xmlheader()
    xmldata(result)
