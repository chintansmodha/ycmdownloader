import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
from GetDataFromDB import SummerizedBankBalance_GetDataFromDB as SBBPD
from PrintPDF import SummerizedBankBalance_PrintPDF as pdfrpt
from FormLoad import SummerizedBankBalance_FormLoad as views
LDStartDate=""
LDEndDate=""
Exceptions=""
save_name=""

def SummerizedBankBalance(request):
    global save_name
    global LDEndDate
    global LDStartDate
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]

    LSCompany = request.GET.getlist('comp')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCCompany = request.GET.getlist('allcomp')


    LSFileName = "SummerizedBankBalance" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    SBBPD.SummerizedBankBalance_PrintPDF(LSCompany,LDStartDate,LDEndDate,LCCompany)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,'SummerizedBankBalance.html',{'GDataCompany':views.GDataCompany})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
