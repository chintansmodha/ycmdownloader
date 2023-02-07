from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render

from FormLoad import BankRecon_FormLoad as views
from GetDataFromDB import BankRecon_GetDataFromDB as BRGDFDB
from PrintPDF import BankRecon_PrintPDF as pdfrpt

def BankReconProcessSelection(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "BankReconciliation" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSCompany=request.GET.getlist("vchno")
    LSBank=request.GET.getlist("vchdate")
    LSAllCompany=request.GET.getlist("partycode")
    LSAllBank=request.GET.getlist("partycode")
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])

    BRGDFDB.BankReconGetDataFromDB(LSCompany,LSBank,LSAllCompany,LSAllBank,LDEndDate,LDStartDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'BankRecon.html',{'GDataCompany':views.GDataCompany,'GDataBank':views.GDataBank})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response




