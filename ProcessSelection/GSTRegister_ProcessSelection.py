import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import GSTRegister_FormLoad as views
from GetDataFromDB import GSTRegister_GetDataFromDB as GSTReg
from PrintPDF import GSTRegister_PrintPDF as pdfrpt
Exceptions=""

def GSTRegister(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "GSTRegister" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name+".pdf")

    LSCompanyUnitCode = request.GET.getlist('unit')
    LSParty = request.GET.getlist('party')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCParty =request.GET.getlist('allparty')
    LCCompanyCode = request.GET.getlist('allcomp')
    GSTReg.GSTRegister_PrintPDF(LSCompanyUnitCode,LSParty,LDStartDate,LDEndDate,LCParty,LCCompanyCode,LSFileName)
    #return render(request, "GSTRegister.html",{'GDataParty': views.GDataParty, 'GDataCompanyCode': views.GDataCompanyCode, 'Exception':Exceptions})
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "GSTRegister.html",{'GDataParty': views.GDataParty, 'GDataCompanyCode': views.GDataCompanyCode, 'Exception':Exceptions})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response