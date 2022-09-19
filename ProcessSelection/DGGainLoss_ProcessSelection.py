import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import DGGainLoss_Formload as views

from GetDataFromDB import DGGainLoss_GetFromDB as DGLOTDB
from PrintPDF import DGGainLoss_PrinrPDF as DGLOTpdf
from GetDataFromDB import DGGainLossItm_GetFromDB as DGITMDB
from PrintPDF import DGGainLossItm__PrintPDF as DGITMpdf




def DGGainLoss(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "DGGainLoss" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LDStartdate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LDReportType = str(request.GET['type'])
    # print(LDReportType)

    if LDReportType == 'lotwise':
        DGLOTpdf.c = DGLOTpdf.canvas.Canvas(save_name + ".pdf")
        DGLOTDB.DGGainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate )

    else:
        DGITMpdf.c = DGITMpdf.canvas.Canvas(save_name + ".pdf")
        DGITMDB.DGGainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate )

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'no data'
        return render(request, 'DGGainLoss.html', {'GDataDepartment':views.GDataDepartment, 'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response