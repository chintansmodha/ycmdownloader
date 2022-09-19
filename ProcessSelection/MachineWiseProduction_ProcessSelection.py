import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import MachineWiseProduction_Formload as views

from GetDataFromDB import MachineWiseProduction_GetDataFromDB as MWP_G
from PrintPDF import MachineWiseProduction_PrintPDF as MWP_P
from GetDataFromDB import MachineWiseProductionAllQulty_GetDataFromDB as MWPA_G
from PrintPDF import MachineWiseProductionAllQulty_PrintPDF as MWPA_P

def MachineWiseProduction(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "MachinWiseProduction" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LDProductionDate = str(request.GET['productiondate'])
    LDEndDate = str(request.GET['enddate'])
    LDReportType = str(request.GET['type'])
    # print(LDReportType)

    if LDReportType == 'squality':
        MWP_P.c = MWP_P.canvas.Canvas(save_name + ".pdf")
        MWP_G.MachineWiseProduction_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDProductionDate, LDEndDate)

    elif LDReportType == 'Aquality':
        MWPA_P.c = MWPA_P.canvas.Canvas(save_name + ".pdf")
        MWPA_G.MachineWiseProduction_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDProductionDate, LDEndDate)


    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'no data'
        return render(request, 'MachineWiseProduction.html', {'GDataDepartment':views.GDataDepartment, 'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

    # response = FileResponse(open(filepath, 'rb'))
    # response['Content-Disposition'] = "attachment; filename=%s" % filepath
    # return response