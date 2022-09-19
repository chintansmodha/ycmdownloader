import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import ProductionAnalysis_Formload as views

from GetDataFromDB import ProductionAnalysis_GetFromDB as PrdnA_GetFromDB
from PrintPDF import ProductionAnalysis_PrintPDF as PrdnA_Pdf
from GetDataFromDB import ProductionAnalysisDt_GetFromDB as PrdnA2_GetFromDB
from PrintPDF import ProductionAnalysisDt_PrintPDF as PrdnA2_Pdf
from GetDataFromDB import ProductionAnalysisMach_GetFromDB as PrdnAMch_GetFromDB
from PrintPDF import ProductionAnalysisMach_PrintPDF as PrdnAMch_Pdf


Exceptions=""

def ProductionAnalysis(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "ProductionAnalysis" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Production Analysis/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)


    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LSItemCode = request.GET.getlist('item')
    LCItemCode = request.GET.getlist('allitem')
    LSItmtype = request.GET.getlist('itmtyp')
    LCItmtype = request.GET.getlist('allitmtyp')
    LSProduction = request.GET.getlist('prdtyp')
    LCProduction = request.GET.getlist('allprdtyp')
    LSQuality = request.GET.getlist('qwlty')
    LCQuality = request.GET.getlist('allqwlty')
    LSShadeCode = request.GET.getlist('shade')
    LCShadeCode = request.GET.getlist('allshade')
    LSMachine = request.GET.getlist('mach')
    LCMachine = request.GET.getlist('allmach')
    LSLotNo = request.GET.getlist('lot')
    LCLotNo = request.GET.getlist('alllot')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSType = str(request.GET['type'])
    # print(LSType)
    # print(LSItmtype)



    if LSType == 'SItmWise':
        PrdnA_Pdf.c = PrdnA_Pdf.canvas.Canvas(save_name + ".pdf")
        PrdnA_GetFromDB.ProductionAnalysis_PrintPDF( LSDepartmentCode, LCDepartmentCode, LSItemCode, LCItemCode, LSItmtype, LCItmtype,
                                                     LSProduction, LCProduction, LSQuality, LCQuality, LSShadeCode, LCShadeCode,
                                                     LSMachine, LCMachine, LSLotNo, LCLotNo, LDStartDate, LDEndDate)

    elif LSType == 'machwise':
        PrdnAMch_Pdf.c = PrdnAMch_Pdf.canvas.Canvas(save_name + ".pdf")
        PrdnAMch_GetFromDB.ProductionAnalysis_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSItemCode, LCItemCode,
                                                    LSItmtype, LCItmtype,LSProduction, LCProduction, LSQuality, LCQuality, LSShadeCode,
                                                    LCShadeCode, LSMachine, LCMachine, LSLotNo, LCLotNo, LDStartDate, LDEndDate)

    elif LSType == 'SItmWiseDt':
        PrdnA2_Pdf.c = PrdnA2_Pdf.canvas.Canvas(save_name + ".pdf")
        PrdnA2_GetFromDB.ProductionAnalysis_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSItemCode, LCItemCode,
                                                    LSItmtype, LCItmtype, LSProduction, LCProduction, LSQuality, LCQuality, LSShadeCode,
                                                    LCShadeCode, LSMachine, LCMachine, LSLotNo, LCLotNo, LDStartDate, LDEndDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'ProductionAnalysis.html',
                             {'GDataDepartment': views.GDataDepartment, 'GDataItem': views.GDataItem,
                              'GDataItemType': views.GDataItemType, 'GDataProduction': views.GDataProduction,
                              'GDataQuality': views.GDataQuality, 'GDataShade': views.GDataShade, 'GDataMachine': views.GDataMachine,
                              'GDataLot': views.GDataLot,'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
