import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import ProductionSummary_FormLoad as views

from GetDataFromDB import ProductionSummary_GetDataFromDB as PRSGDB
from PrintPDF import ProductionSummary_PrintPDF as pdfPRS
from GetDataFromDB import ProductionSummaryDenier_GetDataFromDB as PRSDGDB
from PrintPDF import ProductionSummaryDenier_PrintPDF as pdfPRSD
from GetDataFromDB import ProductionSummaryDenierNodept_GetDataFromDB as PRSNDGDB
from GetDataFromDB import ProductionSummaryItem_GetDataFromDB as PSIGDB
from PrintPDF import ProductionSummaryItem_PrintPDF as pdfPSI
from GetDataFromDB import ProductionSummaryMachnCop_GetDataFromDB as PSMCGDDB
from PrintPDF import ProductionSummaryMachnCop_PrintPDF as pdfPSMC
from GetDataFromDB import ProductionSummaryItmSumm_GetDataFromDB as PSISGDDB
from PrintPDF import ProductionSummaryItmSumm_PrintPDF as pdfPSIS
from GetDataFromDB import ProductionSummaryItemCol_GetDataFromDB as PSICGDDB
# from PrintPDF import ProductionSummaryItemCol_PrintPDF as pdfPSIC
from PrintPDF import ProductionSummaryItmColWise_PrintPDF as pdfPSICW
from GetDataFromDB import ProductionSummaryProdSumm_GetDataFromDB as PSPSGDDB
from PrintPDF import ProductionSummaryProdSumm_PrintPDF as pdfPSPS
from GetDataFromDB import ProductionSummaryWindng_GetDataFromDB as PSWGDDB
from PrintPDF import ProductionSummaryWindng_PrintPDF as pdfPSW

Exceptions=""

def ProductionSummary(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "ProductionSummary" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Production Summary/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)


    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LSProduction = request.GET.getlist('prdtyp')
    LCProduction = request.GET.getlist('allprdtyp')
    LSLotNo = request.GET.getlist('lot')
    LCLotNo = request.GET.getlist('alllot')
    LSItm = request.GET.getlist('itm')
    LCItm = request.GET.getlist('allitm')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSType = str(request.GET['type'])
    LSType2 = str(request.GET['type2'])
    # print(LSType)
    # print(LSItmtype)
    # print('type :', LSType)
    # print('type2: ', LSType2)
    # print(LCItm, LSItm)


    if LSType == 'dpt':
        pdfPRS.c = pdfPRS.canvas.Canvas(save_name + ".pdf")
        PRSGDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate, LDEndDate)

    elif LSType == 'denier':
        if LSType2 == 'dep':
            pdfPRSD.c = pdfPRSD.canvas.Canvas(save_name + ".pdf")
            PRSDGDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo, LCLotNo,LSItm, LCItm,
                                          LDStartDate, LDEndDate)

        if LSType2 == 'nodep':
            pdfPRSD.c = pdfPRSD.canvas.Canvas(save_name + ".pdf")
            PRSNDGDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo, LCLotNo,LSItm, LCItm,
                                          LDStartDate, LDEndDate)

    elif LSType == 'item':
        pdfPSI.c = pdfPSI.canvas.Canvas(save_name + ".pdf")
        PSIGDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                            LCLotNo, LSItm, LCItm,LDStartDate, LDEndDate)

    elif LSType == 'machcops':
        pdfPSMC.c = pdfPSMC.canvas.Canvas(save_name + ".pdf")
        PSMCGDDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate,LDEndDate)

    elif LSType == 'itmsumm':
        pdfPSIS.c = pdfPSIS.canvas.Canvas(save_name + ".pdf")
        PSISGDDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate,LDEndDate)

    elif LSType == 'itmcol':
        # pdfPSIC.c = pdfPSIC.canvas.Canvas(save_name + ".pdf")
        pdfPSICW.c = pdfPSICW.canvas.Canvas(save_name + ".pdf")
        PSICGDDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate,LDEndDate)

    elif LSType == 'prosumm':
        pdfPSPS.c = pdfPSPS.canvas.Canvas(save_name + ".pdf")
        PSPSGDDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate,LDEndDate)

    elif LSType == 'windwse':
        pdfPSW.c = pdfPSW.canvas.Canvas(save_name + ".pdf")
        PSWGDDB.ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo, LCLotNo,LSItm, LCItm,
                                          LDStartDate, LDEndDate)


    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'ProductionSummary.html',
                      {'GDataDepartment': views.GDataDepartment, 'GDataProduction': views.GDataProduction, 'GDataLot': views.GDataLot, 'GDataItem': views.GDataItem ,'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response