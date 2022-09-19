import os
import os.path
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from FormLoad import PackingMaterialLedger_FormLoad as views
from PrintPDF import PackingMaterialLedgerSupplier_PrintPDF as pdfrpt
from PrintPDF import PackingMaterialLedgerCustomer_PrintPDF as pdfrptcust
from PrintPDF import PackingMaterialLedgerAll_PrintPDF as pdfrptall
from GetDataFromDB import PackingMaterialLedger_GetDataFromDB as PackingMaterialLedgerviews
from GetDataFromDB import PackingMaterialLedgerviewsCustomer_GetDataFromDB as PackingMaterialLedgerviewscust
from GetDataFromDB import PackingMaterialLedgerviewsAll_GetDataFromDB as PackingMaterialLedgerviewsall
from GetDataFromDB import PackingMaterialLadgerSum_GetDataFromDB as PmsGData
from PrintPDF import PackingMaterialLadgerSum_PrintPDF as PmsPDF
from GetDataFromDB import PackingMaterialLedgerSumCustomer_GetDataFromDB as PmLCGData
from PrintPDF import PackingMaterialLedgerSumCustomer_PrintPDF as PmLCPDF

Exceptions=""
save_name=""
def PackingMaterialLedger(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    # LSFileName = "PackingMaterialLedger" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Packing Material Ledger/",
    #                          LSFileName)
    # pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSCompany = request.GET.getlist('comp')
    LSParty = request.GET.getlist('party')
    LSItem = request.GET.getlist('item')
    LSPalleteType=request.GET.getlist('palletetype')
    LSReportType = int(request.GET['reporttype'])
    LCCompany = request.GET.getlist('allcomp')
    LCParty = request.GET.getlist('allparty')
    LCItem = request.GET.getlist('allitem')
    LCPalleteType=request.GET.getlist('allpalletetype')
    LDStartDate = request.GET['startdate']
    LDEndDate = request.GET['enddate']
    LDSummary = int(request.GET['sum'])
    # print(LDSummary)

    if LDSummary == 1:
        if LSReportType == 1:
            LSFileName = "PackingMaterialLedgerSupplier" + LSFileName
            save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Packing Material Ledger/",LSFileName)
            pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
            PackingMaterialLedgerviews.PackingMaterialLedgerSupplier_PrintPDF(LSCompany, LSParty, LSItem, LSPalleteType,LSReportType, LCCompany,LCParty, LCItem,LCPalleteType,LDStartDate, LDEndDate,request)

        if LSReportType == 2:
            LSFileName = "PackingMaterialLedgerCustomer" + LSFileName
            save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Packing Material Ledger/", LSFileName)
            pdfrptcust.c = pdfrptcust.canvas.Canvas(save_name + ".pdf")
            PackingMaterialLedgerviewscust.PackingMaterialLedgerCustomer_PrintPDF(LSCompany, LSParty, LSItem, LSPalleteType,LSReportType, LCCompany,LCParty, LCItem,LCPalleteType,LDStartDate, LDEndDate,request)

        if LSReportType == 3:
            LSFileName = "PackingMaterialLedgerAll" + LSFileName
            save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Packing Material Ledger/", LSFileName)
            pdfrptall.c = pdfrptall.canvas.Canvas(save_name + ".pdf")
            PackingMaterialLedgerviewsall.PackingMaterialLedgerAll_PrintPDF(LSCompany, LSParty, LSItem, LSPalleteType,LSReportType, LCCompany,LCParty, LCItem,LCPalleteType,LDStartDate, LDEndDate,request)

    elif  LDSummary == 2:
        if LSReportType == 1:
            LSFileName = "PackingMaterialLedgerSupplier" + LSFileName
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/Generated Reports/Packing Material Ledger/", LSFileName)
            PmsPDF.c = PmsPDF.canvas.Canvas(save_name + ".pdf")
            PmsGData.PackingMaterialLedgerSupplier_PrintPDF(LSCompany, LSParty, LSItem, LSPalleteType, LSReportType, LCCompany, LCParty, LCItem,
                                                                              LCPalleteType, LDStartDate, LDEndDate, request)
        elif LSReportType == 2:
            LSFileName = "PackingMaterialLedgerCustomer" + LSFileName
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/Generated Reports/Packing Material Ledger/", LSFileName)
            PmLCPDF.c = PmLCPDF.canvas.Canvas(save_name + ".pdf")
            PmLCGData.PackingMaterialLedgerCustomer_PrintPDF(LSCompany, LSParty, LSItem,LSPalleteType, LSReportType,
                                                                                  LCCompany, LCParty, LCItem,LCPalleteType, LDStartDate, LDEndDate,
                                                                                  request)

        elif LSReportType == 3:
            pass

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "PackingMaterialLedger.html",
                      {'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty,'GDataItem': views.GDataItem, 'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
