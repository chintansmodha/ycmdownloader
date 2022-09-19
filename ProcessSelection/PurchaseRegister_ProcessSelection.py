import os
from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
from PrintPDF import PurchaseRegister_PrintPDF as pdfrpt
from GetDataFromDB import PurchaseRegister_GetDataFromDB as PurReg
from PrintPDF import PurchaseRegister_ItemSummary_PrintPDF as pdfrptitem
from GetDataFromDB import PurchaseRegister_ItemSummary_GetDataFromDB as PurItemSum
from PrintPDF import PurchaseRegister_ChargeSummary_PrintPDF as pdfrptcharge
from GetDataFromDB import PurchaseRegister_ChargeSummary_GetDataFromDB as PurChargeSum
from FormLoad import PurchaseRegister_FormLoad as views
Exceptions=""
save_name=""
LSFileName=""
def PurchaseRegister(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]

    LSCompanyUnitCode = request.GET.getlist('unit')
    LSItemTypeCode=request.GET.getlist('type')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCItemTypeCode =request.GET.getlist('alltype')
    LCCompanyCode = request.GET.getlist('allcomp')
    LSReportType = int(request.GET['reporttype'])

    if LSReportType==1:
        LSFileName="PurchaseRegister"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        PurReg.PurchaseRegister_PrintPDF(LSCompanyUnitCode, LSItemTypeCode, LDStartDate, LDEndDate, LSFileName, LCItemTypeCode, LCCompanyCode,LSReportType)
    elif LSReportType==2:
        LSFileName = "PurchaseRegister_ItemSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrptitem.c = pdfrptitem.canvas.Canvas(save_name + ".pdf")
        PurItemSum.PurchaseRegister_ItemSummary_PrintPDF(LSCompanyUnitCode, LSItemTypeCode, LDStartDate, LDEndDate, LSFileName, LCItemTypeCode, LCCompanyCode,LSReportType)
    elif LSReportType==3:
        LSFileName = "PurchaseRegister_ChargeSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrptcharge.c = pdfrptcharge.canvas.Canvas(save_name + ".pdf")
        PurChargeSum.PurchaseRegister_ChargeSummary_PrintPDF(LSCompanyUnitCode, LSItemTypeCode, LDStartDate, LDEndDate, LSFileName, LCItemTypeCode, LCCompanyCode,LSReportType)
    #return HttpResponse(response)
    #return render(request,"PurchaseRegister.html",{'GDataItemCode':views.GDataItemCode,'GDataCompanyCode':views.GDataCompanyCode,'Exception':Exceptions,'download':download})
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "PurchaseRegister.html",
                      {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,
                       'Exception': Exceptions})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

