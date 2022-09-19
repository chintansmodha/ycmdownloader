from datetime import datetime

import xlsxwriter

# from ProcessSelection import Export_Invoice_ProcessSelection as xlsfile
# from GetDataFromDB import Export_Invoice_GetDataFromDB as xlsfilename
divisioncode=[]
brokergroup = []
party = []
pageno=0

freight = 0
gst = 0
insurance = 0
quantity = 0
baseamount = 0
dharaamount = 0
dharapaid = 0
dicountall = 0

##################################
LSPath=''
LSFileName=''
row = 0
col = 0
workbook=''
worksheet=''
merge_format=''
formatheader=''
format_dataright=''
format_dataleft=''
merge_row = ''
merge_row_name = ''
merge_bold = ''
sub_header_row = ''
total_format = ''


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
    LSPath = "D:/Report Development/Generated Reports/Broker Wise RD"
    LSFileName = LSPath + "Broker Wise RD " + LSFileName + ".xls"
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
    global merge_row
    global merge_row_name, merge_bold, sub_header_row, total_format
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
    merge_row = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 20,
    })
    merge_row_name = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 13,
    })
    merge_bold = workbook.add_format({
        'bold': 1,
        'border': 1,
        'valign': 'vcenter',
        'font_size': 11,
    })
    sub_header_row = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
    })
    total_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 12,
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

row = 0
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

LSPath="D:/Report Development/Generated Reports/Broker Wise RD"
LSFileName = "Broker Wise RD " + LSFileName + ".xlsx"
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
merge_row = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_size':20,
})
merge_row_name = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 13,
})
merge_bold = workbook.add_format({
        'bold': 1,
        'border': 1,
        'valign': 'vcenter',
        'font_size': 11,
})
sub_header_row = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
})
total_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 12,
    })

worksheet.set_column(0, 1, 10)
worksheet.set_column(2, 2, 20)
worksheet.set_column(3, 5, 10)
worksheet.set_column(6, 6, 80)
worksheet.set_column(7, 7, 15)
worksheet.set_column(8, 17, 10)


def xmlheader(stdt, etdt):
    global row, col
    worksheet.merge_range(str('A'+ str(row+1) +':' + 'P' + str(row+2)), divisioncode[-1], merge_row)
    worksheet.merge_range(str('A'+ str(row+3) +':' + 'P' + str(row+3)), 'Broker Wise RD (All Invoices)  Report  ' + str(stdt.strftime("%d - %b - %Y")) + '  From  ' + str(etdt.strftime("%d - %b - %Y")), sub_header_row)
    worksheet.write('A'+str(row+6), "Inv. No.	", merge_format)
    worksheet.write('B'+str(row+6), "Iss Date", merge_format)
    worksheet.write('C'+str(row+6), "Freight", merge_format)
    worksheet.write('D'+str(row+6), "GST", merge_format)
    worksheet.write('E'+str(row+6), "Insur	", merge_format)
    worksheet.write('F'+str(row+6), "Qty", merge_format)
    worksheet.write('G'+str(row+6), "Base Rt.", merge_format)
    worksheet.write('H'+str(row+6), "Base Amt.	", merge_format)
    worksheet.write('I'+str(row+6), "Inv.Rt.	", merge_format)
    worksheet.write('J'+str(row+6), "Dh.Rt.	", merge_format)
    worksheet.write('K'+str(row+6), "Dh.Amt.", merge_format)
    worksheet.write('L'+str(row+6), "Dh.Paid	", merge_format)
    worksheet.write('M'+str(row+6), "Dis All", merge_format)
    worksheet.write('N'+str(row+6), "Yarn Type", merge_format)
    worksheet.write('O'+str(row+6), "Initial Com%	", merge_format)
    worksheet.write('P'+str(row+6), "Balance Com ", merge_format)
    row = row + 7
    return row

def xmldata(result, row):
    global col
    worksheet.write(row, col, str(result['INVOICENO']), format_dataleft)
    worksheet.write(row, col+1, str(result['ISSUEDT'].strftime('%d-%m-%Y')),  merge_format)
    worksheet.write(row, col+2, '%.2f'%float(result['FREIGHT']), merge_format)
    worksheet.write(row, col+3, '%.2f'%float(result['GST']), merge_format)
    worksheet.write(row, col+4, '%.2f'%float(result['INSUR']), merge_format)
    worksheet.write(row, col+5, '%.2f'%float(result['QTY']), merge_format)
    worksheet.write(row, col+6, '%.2f'%float(result['BASERT']), merge_format)
    worksheet.write(row, col+7, '%.2f'%float(result['BASEAMT']), merge_format)
    worksheet.write(row, col+8, '%.2f'%float(result['INVRT']), merge_format)
    worksheet.write(row, col+9, '%.2f'%float(result['DHRT']), merge_format)
    worksheet.write(row, col+10, '%.2f'%float(result['DHAMT']), merge_format)
    worksheet.write(row, col+11, '%.2f'%float(result['DHPAID']), merge_format)
    worksheet.write(row, col+12, '%.2f'%float(result['DISALL']), merge_format)
    worksheet.write(row, col+13, str(result['YARNTYPE']), merge_format)
    worksheet.write(row, col+14, '%.2f'%float(result['INTIALCOMPER']), merge_format)
    worksheet.write(row, col+15, '%.2f'%float(result['BALANCECOMPER']), merge_format)
    row=row+1
    BrokergroupTotal(result)

def page():
    global pageno
    pageno = pageno + 1
    return pageno



def dvalue():
    global d
    d=d-10
    return d


def logic(result):
    global divisioncode, brokergroup, party
    divisioncode.append(result['COMPANY'])
    brokergroup.append(result['BROKERGRP'])
    party.append(result['PARTY'])


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
    global brokergroup, party
    global row
    global col
    global workbook
    global worksheet
    divisioncode=[]
    pageno=0
    brokergroup=[]
    party = []
    row = 0
    col = 0
    workbook = ''
    worksheet = ''

def BrokergroupTotal(result):
    global freight, gst, insurance, dharapaid
    global quantity, baseamount, dharaamount, dicountall

    freight += float(result['FREIGHT'])
    gst += float(result['GST'])
    insurance += float(result['INSUR'])
    quantity += float(result['QTY'])
    baseamount += float(result['BASEAMT'])
    dharaamount += float(result['DHAMT'])
    dharapaid += float(result['DHPAID'])
    dicountall += float(result['DISALL'])

def BrokerTotalPrint(row):
    global freight, gst, insurance, dharapaid
    global quantity, baseamount, dharaamount, dicountall
    worksheet.merge_range('A' + str(row+1) + ':' + 'B' + str(row+1), 'Broker Group Total: ', total_format)
    worksheet.write(row, col + 2, '%.2f'%float(freight), merge_format)
    worksheet.write(row, col + 3, '%.2f'%float(gst), merge_format)
    worksheet.write(row, col + 4, '%.2f'%float(insurance), merge_format)
    worksheet.write(row, col + 5, '%.2f'%float(quantity), merge_format)
    worksheet.write(row, col + 6, '', merge_format)
    worksheet.write(row, col + 7, '%.2f'%float(baseamount), merge_format)
    worksheet.write(row, col + 8, '', merge_format)
    worksheet.write(row, col + 9, '', merge_format)
    worksheet.write(row, col + 10, '%.2f'%float(dharaamount), merge_format)
    worksheet.write(row, col + 11, '%.2f'%float(dharapaid), merge_format)
    worksheet.write(row, col + 12, '%.2f'%float(dicountall), merge_format)
    worksheet.write(row, col + 13, '', merge_format)
    worksheet.write(row, col + 14, '', merge_format)
    worksheet.write(row, col + 15, '', merge_format)
    freight = 0
    gst = 0
    insurance = 0
    quantity = 0
    baseamount = 0
    dharaamount = 0
    dharapaid = 0
    dicountall = 0


def textsize( result,  stdt, etdt):
    global row
    logic(result)
    if len(divisioncode) == 1:
        row = xmlheader(stdt, etdt)
        worksheet.merge_range(str('A' + str(row - 3) + ':' + 'P' + str(row - 3)), brokergroup[-1], merge_row_name)
        worksheet.merge_range(str('A' + str(row - 2) + ':' + 'P' + str(row - 2)), party[-1], merge_bold)
        row = row -1
        xmldata(result,row)

    elif divisioncode[-1] == divisioncode[-2]:
        if brokergroup[-1] == brokergroup[-2]:
            if party[-1] == party[-2]:
                row = row + 1
                xmldata(result, row)

            elif party[-1] != party[-2]:
                row = row + 2
                worksheet.merge_range(str('A' + str(row + 1) + ':' + 'P' + str(row + 1)), party[-1], merge_bold)
                row = row + 1
                xmldata(result, row)

        elif brokergroup[-1] != brokergroup[-2]:
            row = row + 1
            BrokerTotalPrint(row)
            row = row + 2
            worksheet.merge_range(str('A' + str(row + 1) + ':' + 'P' + str(row + 1)), brokergroup[-1], merge_row_name)
            worksheet.merge_range(str('A' + str(row + 2) + ':' + 'P' + str(row + 2)), party[-1], merge_bold)
            row = row + 2
            xmldata(result, row)

    elif divisioncode[-1] != divisioncode[-2]:
        row = row + 1
        BrokerTotalPrint(row)
        row = row + 3
        row = xmlheader(stdt, etdt)
        worksheet.merge_range(str('A' + str(row - 3) + ':' + 'P' + str(row - 3)), brokergroup[-1], merge_row_name)
        worksheet.merge_range(str('A' + str(row - 2) + ':' + 'P' + str(row - 2)), party[-1], merge_bold)
        row = row - 1
        xmldata(result, row)
