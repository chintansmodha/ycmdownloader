import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve

from GetDataFromDB import Export_Invoice_GetDataFromDB as pdfrptexportinvoice
from PrintPDF import Export_Invoice_PrintPDF as pdfrptexportinvoice_pfd
from CreateXLS import Export_Invoice_Without_Shipping_Billno as xlsrpt
from Global_Files import Connection_String as con
from FormLoad import Export_Invoice_FormLoad as views
Exceptions=""
req=''
def Export_InvoiceRegister(request):
    global  req
    req=request
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]

    LScheckboxgoods = request.GET.get('checkboxgoods')
    LScheckboxcapitalgoods = request.GET.get('checkboxcapitalgoods')
    LScheckboxservice = request.GET.get('checkboxservice')

    LSallParty = request.GET.get('selectallparty')
    LSallcompany = request.GET.get('selectallcompany')

    LSParty = request.GET.getlist('selparty')
    LSCompany = request.GET.getlist('selcompany')

    LSReportType = request.GET.get('SortByReportType')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])

    # pdfrpt.c = pdfrpt.canvas.Canvas(LSFileName + ".pdf")
    # PurReg.PurchaseRegister_PrintPDF(LSCompanyUnitCode, LSItemTypeCode, LDStartDate, LDEndDate, LSFileName,
    #        LCItemTypeCode, LCCompanyCode, LSReportType)
    print("before calling if ")
    if LSReportType == '1':
        LSFileName = "Export Invoice Register " + LSFileName + ".pdf"
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Export Invoice/",
                                 LSFileName)
        pdfrptexportinvoice_pfd.c = pdfrptexportinvoice_pfd.canvas.Canvas(save_name)

        pdfrptexportinvoice.ExportInvoicePrintPDF(LSallParty, LSallcompany, LSParty, LSCompany,
                                                     LDStartDate, LDEndDate, LSReportType, LSFileName)
        filepath = save_name
    elif LSReportType == '2':
        LSFileName = " Supplier Details Buyer-Wise Register " + LSFileName +".pdf"
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Export Invoice/",
                                 LSFileName)
        pdfrptexportinvoice_pfd.c = pdfrptexportinvoice_pfd.canvas.Canvas(save_name )

        pdfrptexportinvoice.ExportInvoicePrintPDF(LSallParty, LSallcompany, LSParty, LSCompany,
                                                                LDStartDate, LDEndDate, LSReportType, LSFileName)
        filepath = save_name
    elif LSReportType == '3':
        LSFileName = " Supplier Details Item-Wise Register " + LSFileName
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Export Invoice/",
                                 LSFileName)
        pdfrptexportinvoice_pfd.c = pdfrptexportinvoice_pfd.canvas.Canvas(save_name + ".pdf")

        pdfrptexportinvoice.ExportInvoicePrintPDF(LSallParty, LSallcompany, LSParty, LSCompany,
                                                                LDStartDate, LDEndDate, LSReportType, LSFileName)
        filepath = xlsrpt.save_name
    elif LSReportType == '4':
        print("from 4  * * * * * ")
        LSFileName = " Invoice Without Shipping Bill No Register " + LSFileName + ".xlsx"
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Export Invoice/",
                                 LSFileName)
        print(save_name)
        pdfrptexportinvoice.ExportInvoiceXLS(LSallParty, LSallcompany, LSParty, LSCompany,
                                                                LDStartDate, LDEndDate, LSReportType)
        save_name = os.path.join(os.path.expanduser("~"),
                                 "D:/Report Development/ReportDevelopment/" + xlsrpt.LSFileName)
        filepath = xlsrpt.LSFileName

    elif LSReportType == '5':
        print("from 4  * * * * * ")
        LSFileName = " Invoice Without Shipping Bill No Register " + LSFileName + ".xlsx"
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Export Invoice/",
                                 LSFileName)
        pdfrptexportinvoice.ExportInvoiceXLS(LSallParty, LSallcompany, LSParty, LSCompany,
                                                                LDStartDate, LDEndDate, LSReportType)
        save_name = os.path.join(os.path.expanduser("~"),
                                 "D:/Report Development/ReportDevelopment/" + xlsrpt.LSFileName)
        filepath = xlsrpt.LSFileName



    # filepath = save_name
    # filepath = xlsrpt.LSFileName
    if not os.path.isfile(filepath):
        return render(request, 'Export_Invoice.html', {'company': views.company, 'party': views.party,'Exception':Exceptions})

    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    print(xlsrpt.LSPath)
    print(xlsrpt.LSFileName)
    # return serve(request, os.path.basename(xlsrpt.LSPath+xlsrpt.LSFileName), os.path.dirname(xlsrpt.LSFileName))

# print("before calling the  storeregister print pdf")
#        print("plane name " +LSallPlant)
#        print(LSallSupplier)
#        print(LSallItem)
#        print(LSPlant)
#        print(LSallSupplier)
#        print(LSItem)
#        print(LDStartDate)
#        print(LDEndDate)
# print(LSReportType)
