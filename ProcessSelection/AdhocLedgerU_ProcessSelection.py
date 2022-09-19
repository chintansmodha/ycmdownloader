import os
from datetime import datetime
import re
from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from PrintPDF import AdhocLedgerU_PrintPDF as alpp
from GetDataFromDB import AdhocLedgerU_GetDataFromDB
from FormLoad import AdhocLedgerU_FormLOad as views
def adhocLedgerU_ProcessData(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "AdhocLedgerU" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    alpp.c = alpp.canvas.Canvas(save_name + ".pdf")
    Year = request.GET['year']
    startdate = request.GET['startdate']
    enddate = request.GET['enddate']
    LSCompany = request.GET.getlist('unit')
    LCCompany = request.GET.getlist('allcomp')
    LSParty = request.GET.getlist('account')
    LCParty = request.GET.getlist('allaccount')
    LSAccount = request.GET.getlist('subaccount')
    LCAccount = request.GET.getlist('allsubaccount')
    Narration = request.GET['nar']
    Eject = request.GET['eject']
    AdhocLedgerU_GetDataFromDB.adhocLedgerU_GerData(Year,startdate,enddate,LSCompany,LCCompany,LSParty,LCParty,LSAccount,LCAccount,Narration,Eject)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "AdhocLedger.html",
                      {'GDataCompany': views.GDataCompany, 'GDataAccount': views.GDataAccount,
                       'GDataSubAccount': views.GDataSubAccount})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response