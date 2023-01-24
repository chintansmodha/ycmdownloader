from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render
from FormLoad import GSTRONE_FormLoad as views
from GetDataFromDB import GSTROne_GetDataFromDB as GSTG
from PrintPDF import GSTRONE_XLSX as xlsrpt
Exceptions=""
save_name=""
LSFileName=""

def GSTRONEPROCESS(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "GSTRONE" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)

    LSCompany=request.GET.getlist('unit')
    LCCompany=request.GET.getlist('allcomp')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    
    GSTG.GSTRONE_GetData(LSCompany,LCCompany,LDStartDate,LDEndDate)
    
    filepath = xlsrpt.LSFileName
    if not os.path.isfile(filepath):
        return render(request,'GSTRONE.html', {'GDataCompany':views.GDataCompany})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response