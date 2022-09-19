import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import PackingReport_FormLoad as views

from GetDataFromDB import PackingReport_GetDataFromDB as PRGFDB
from PrintPDF import PackingReport_PrintPDF as pdfPR
from GetDataFromDB import PackingReportSumm_GetDataFromDB as PRSGFDB
from PrintPDF import PackingReportSumm_PrintPDF as pdfPRS
from GetDataFromDB import PackingReportPackList_GetDataFromDB as PRPLGFDB
from PrintPDF import PackingReportPackList_PrintPDF as pdfPRPL
from GetDataFromDB import PackingReportItmTyp_GetDataFromDB as PRIGFDB
from PrintPDF import PackingReportItmTyp_PrintPDF as pdfPRI
from GetDataFromDB import PackingReportBoxNtAlwd_GetDataFromDB as PRBGFDB
from PrintPDF import PackingReportBoxNtAlwd_PrintPDF as pdfPRB


Exceptions=""

def PackingReport(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "PackingReport" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Packing Report/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)


    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LSProduction = request.GET.getlist('prdtyp')
    LCProduction = request.GET.getlist('allprdtyp')
    LSLotNo = request.GET.getlist('lot')
    LCLotNo = request.GET.getlist('alllot')
    LSMachine = request.GET.getlist('mach')
    LCMachine = request.GET.getlist('allmach')
    LSWinding = request.GET.getlist('wndtyp')
    LCWinding = request.GET.getlist('allwndtyp')
    LSQuality = request.GET.getlist('qwlty')
    LCQuality = request.GET.getlist('allqwlty')
    LSPallet = request.GET.getlist('pallt')
    LCPallet = request.GET.getlist('allpallt')
    LSItmtype = request.GET.getlist('itm')
    LCItmtype = request.GET.getlist('allitmtyp')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSType = str(request.GET['type'])
    # print(LSType)
    # print(LSItmtype)



    if LSType == 'dtl':
            pdfPR.c = pdfPR.canvas.Canvas(save_name + ".pdf")
            PRGFDB.PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                               LCLotNo, LSMachine, LCMachine, LSWinding,
                                               LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LDStartDate, LDEndDate)

    elif LSType == 'summ':
        pdfPRS.c = pdfPRS.canvas.Canvas(save_name + ".pdf")
        PRSGFDB.PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                      LCLotNo, LSMachine, LCMachine, LSWinding,
                                      LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LDStartDate, LDEndDate)

    elif LSType == 'pacl':
        pdfPRPL.c = pdfPRPL.canvas.Canvas(save_name + ".pdf")
        PRPLGFDB.PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                      LCLotNo, LSMachine, LCMachine, LSWinding,
                                      LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LDStartDate, LDEndDate)

    elif LSType == 'itntyp':
        pdfPRI.c = pdfPRI.canvas.Canvas(save_name + ".pdf")
        PRIGFDB.PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                        LCLotNo, LSMachine, LCMachine, LSWinding,
                                        LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LSItmtype, LCItmtype, LDStartDate, LDEndDate)

    elif LSType == 'boxnt':
        pdfPRB.c = pdfPRB.canvas.Canvas(save_name + ".pdf")
        PRBGFDB.PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                         LCLotNo, LSMachine, LCMachine, LSWinding,
                                         LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LDStartDate, LDEndDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PackingReport.html',
                      {'GDataDepartment': views.GDataDepartment, 'GDataProduction': views.GDataProduction, 'GDataLot': views.GDataLot, 'GDataMachine': views.GDataMachine,
                       'GDataWinding': views.GDataWinding, 'GDataQuality': views.GDataQuality, 'GDataPallet': views.GDataPallet, 'GDataItemType': views.GDataItemType ,'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
