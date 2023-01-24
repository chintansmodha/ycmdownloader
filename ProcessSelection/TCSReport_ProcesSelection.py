from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render
from FormLoad import TCSReport_SaleInvoice_Formload as views
from GetDataFromDB import TCSReport_GetDataFromDB as TRG
from PrintPDF import TCSReport_XLS as xlsrpt
Exceptions=""
save_name=""
LSFileName=""

def TCSReportProcess(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "TCSReport" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)

    LSCompany=request.GET.getlist('unit')
    LCCompany=request.GET.getlist('allcomp')
    LSAccount=request.GET.getlist('account')
    LCAccount=request.GET.getlist('allaccount')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])


    TRG.TCSReport_GetData(LSCompany,LCCompany,LSAccount,LCAccount,LDStartDate,LDEndDate)
    filepath = xlsrpt.LSFileName
    if not os.path.isfile(filepath):
        return render(request,'TCSReport.html', {'GDataCompany':views.GDataCompany,'GDataAccount':views.GDataAccount})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response