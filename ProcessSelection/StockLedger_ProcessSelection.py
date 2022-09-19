Exceptions=""
save_name=""
LSFileName=""
from FormLoad import StockLedger_FormLoad as views
from GetDataFromDB import  StockLedger_GetDataFromDB as SLGDFDB
from PrintPDF import StockLedger_PrintPDF as pdfrpt
import os
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
def StockLedger(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSCompany=request.GET.getlist('unit')
    LSItem=request.GET.getlist('type')
    LSItemGroup=request.GET.getlist('itemgrp')
    LCCompany=request.GET.getlist('allcomp')
    LCItem=request.GET.getlist('alltype')
    LCItemGroup=request.GET.getlist('allitemgrp')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    LSReportType = int(request.GET['reporttype'])
    if LSReportType==1:
        LSFileName="StockLedger"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        SLGDFDB.StockLedger_GetData(LSCompany, LSItem, LSItemGroup,LCCompany,LCItem,LCItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType)
    elif LSReportType==2:
        LSFileName = "StockLedgerSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        SLGDFDB.StockLedgerSummary_GetData(LSCompany, LSItem, LSItemGroup,LCCompany,LCItem,LCItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "StockLedger.html",
                      {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,"GDataQuality":views.GDataQuality,
                       'Exception': Exceptions})

    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
