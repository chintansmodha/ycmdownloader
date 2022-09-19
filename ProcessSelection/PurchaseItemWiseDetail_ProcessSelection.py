import imp
import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
from FormLoad import PurchaseItemWiseDetail_FormLoad as views
from GetDataFromDB import PurchaseItemWiseDetail_GetDataFromDB as PIWDGDFDB
from PrintPDF import PurchaseItemWiseDetail_PrintPDF as pdfrpt,PurchaseItemWiseSummary_PrintPDF as pdfrpt1
Exceptions=""
save_name=""
LSFileName=""


def PurchaseItemWiseDetail(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSCompany=request.GET.getlist('unit')
    LSItem=request.GET.getlist('type')
    LSQuality=request.GET.getlist('qlt')
    LCCompany=request.GET.getlist('allcomp')
    LCItem=request.GET.getlist('alltype')
    LCQuality=request.GET.getlist('allqlt')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    LSReportType = int(request.GET['reporttype'])
    if LSReportType==1:
        LSFileName="PurchaseItemWiseDetail"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), "C:/Users/DataTex/Downloads/",LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        PIWDGDFDB.PurchaseItemWiseDetail_GetData(LSCompany, LSItem, LSQuality,LCCompany,LCItem,LCQuality,LDStartDate, LDEndDate, LSFileName,LSReportType)
    elif LSReportType==2:
        LSFileName = "PurchaseItemWiseDetailSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"), "C:/Users/DataTex/Downloads/",LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        PIWDGDFDB.PurchaseItemWiseDetailSummary_GetData(LSCompany, LSItem, LSQuality,LCCompany,LCItem,LCQuality,LDStartDate, LDEndDate, LSFileName,LSReportType)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "PurchaseItemWiseDetail.html",
                      {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,"GDataQuality":views.GDataQuality,
                       'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

   #####################################################################################################################################################################################
   #####################################################################################################################################################################################
   #####################################################################################################################################################################################
   #####################################################################################################################################################################################
   ##################################################################################################################################################################################### 

def PurchaseItemWiseSummary(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSCompany=request.GET.getlist('unit')
    LSItem=request.GET.getlist('type')
    LSQuality=request.GET.getlist('qlt')
    LSPRItemGroup=request.GET.getlist('pritemgroup')
    LSPUItemGroup=request.GET.getlist('puitemgroup')
    LCCompany=request.GET.getlist('allcomp')
    LCItem=request.GET.getlist('alltype')
    LCQuality=request.GET.getlist('allqlt')
    LCPRItemGroup=request.GET.getlist('allpritemgroup')
    LCPUItemGroup=request.GET.getlist('allpuitemgroup')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    LSReportType = int(request.GET['reporttype'])
    if LSReportType==1:
        LSFileName="PurchaseItemGrpWiseItemSummary"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        PIWDGDFDB.PurchaseItemGrpWiseItemSummary_GetData(LSCompany, LSItem, LSQuality,LSPUItemGroup,LCCompany,LCItem,LCQuality,LCPUItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType)
    elif LSReportType==2:
        LSFileName = "ProductionItemGrpWiseSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        PIWDGDFDB.ProductionItemGrpWiseSummary_GetData(LSCompany, LSItem, LSQuality,LSPRItemGroup,LCCompany,LCItem,LCQuality,LCPRItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType)
    elif LSReportType==3:
        LSFileName = "ProductionItemGrpWiseItemSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        PIWDGDFDB.ProductionItemGrpWiseItemSummary_GetData(LSCompany, LSItem, LSQuality,LSPRItemGroup,LCCompany,LCItem,LCQuality,LCPRItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "PurchaseItemWiseSummary.html",
                      {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,"GDataQuality":views.GDataQuality,"GDataProductionItemGroup":views.GDataProductionItemGroup,
                       'Exception': Exceptions})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
