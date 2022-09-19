from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render
from FormLoad import SalesOrder_FormLoad as views
from GetDataFromDB import SalesOrder_GetDataFromDB as SOGDFDB
from PrintPDF import SalesOrder_PrintPDF as pdfrpt
Exceptions=""
save_name=""
LSFileName=""

def SalesOrder(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "SalesOrder" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    LSDivision=request.GET.getlist('div')
    LSAgent=request.GET.getlist('agent')
    LSParty=request.GET.getlist('party')
    LSDocumentType=request.GET.getlist('doc')
    LSTemplate=request.GET.getlist('temp')
    LCDivision=request.GET.getlist('alldiv')
    LCAgent=request.GET.getlist('aallgent')
    LCParty=request.GET.getlist('allparty')
    LCDocumentType=request.GET.getlist('alldoc')
    LCTemplate=request.GET.getlist('alltemp')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])


    SOGDFDB.SalesOrder_GetData(LSDivision,LSAgent,LSParty,LSDocumentType,LSTemplate,LCDivision,LCAgent,LCParty,LCDocumentType,LCTemplate,LDStartDate,LDEndDate)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,'SalesOrder.html', {'GDataDivision':views.GDataDivision,'GDataAgent':views.GDataAgent,"GDataParty":views.GDataParty,"GDataDocumentType":views.GDataDocumentType,"GDataTemplate":views.GDataTemplate})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response