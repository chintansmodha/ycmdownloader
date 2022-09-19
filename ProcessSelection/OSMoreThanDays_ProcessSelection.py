import os
from datetime import datetime

from django.http import FileResponse

from FormLoad import OSMoreThanDays_FormLoad as views
from django.shortcuts import render
from django.views.static import serve
from PrintPDF import OSMoreThanDays_PrintPDF as pdfrpt
from GetDataFromDB import OSMoreThanDays_GetDataFromDB as OMTDGDFD
Exceptions=""
def OSMoreThanDays(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "BrokerGroupCompanyWiseOS" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    Company = request.GET.getlist('unit')
    BrkGroup = request.GET.getlist('account')
    Days = request.GET.getlist('days')
    LCCompany = request.GET.getlist('allcomp')
    LCBroker = request.GET.getlist('allaccount')
    OMTDGDFD.OSMorethanDays_PrintPDF(Company, BrkGroup,Days,LCCompany,LCBroker,request)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "OSMoreThanDays.html",
                      {'GDataCompany': views.GDataCompany, 'GDataBroker': views.GDataBroker,
                       'GDataBrokerGroup': views.GDataBrokerGroup, 'Exception': Exceptions})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
