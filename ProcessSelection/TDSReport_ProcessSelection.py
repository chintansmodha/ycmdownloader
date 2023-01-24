from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render
from FormLoad import TDSReport_PurInvoice_Formload as views
from GetDataFromDB import TDSReport_GetDataFromDB as TRG
from GetDataFromDB import GSTROne_GetDataFromDB as GSTG
from PrintPDF import TDSReport_XLS as xlsrpt
Exceptions=""
save_name=""
LSFileName=""

def TDSReportProcess(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "TDSReport" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)

    LSCompany=request.GET.getlist('unit')
    LCCompany=request.GET.getlist('allcomp')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    
    TRG.TDSReport_GetData(LSCompany,LCCompany,LDStartDate,LDEndDate)
    
    filepath = xlsrpt.LSFileName
    if not os.path.isfile(filepath):
        return render(request,'TDSReport.html', {'GDataCompany':views.GDataCompany})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response