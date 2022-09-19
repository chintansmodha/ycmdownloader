import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import GainLoss_FormLoad as views

from GetDataFromDB import  GainLosReport_GetFrom_DB as GainL
from PrintPDF import GainLoss_PrintPDF as pdf
from GetDataFromDB import GainLossReportBaseLot_GetFromDB as GainLBase
from PrintPDF import GainLossReportBaseLot_PrintPDF as pdfBase
from GetDataFromDB import GainLossReportLotWise_GetDataFromDB as GainLLot
from PrintPDF import GainLossReportLotwise_PrintPDF as pdfLot

def GainLoss(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "GainLoss" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LDStartdate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LDReportType = str(request.GET['type'])
    # print(LDReportType)

    if LDReportType == 'itmwise':
        pdf.c = pdf.canvas.Canvas(save_name + ".pdf")
        GainL.GainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate)

    elif LDReportType == 'baselotwise':
        pdfBase.c = pdfBase.canvas.Canvas(save_name + ".pdf")
        GainLBase.GainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate)

    elif LDReportType == 'lotwise':
        pdfLot.c = pdfLot.canvas.Canvas(save_name + ".pdf")
        GainLLot.GainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'no data'
        return render(request, 'GainLossReport.html', {'GDataDepartment': views.GDataDepartment,"GDataYear":views.GDataYear,
                                                       'YEAR':views.year, 'Exception': Exceptions})

    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # response = FileResponse(open(filepath, 'rb'))
    # response['Content-Disposition'] = "attachment; filename=%s" % filepath
    # return response