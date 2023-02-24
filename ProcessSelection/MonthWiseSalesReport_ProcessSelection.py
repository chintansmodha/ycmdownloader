from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render

from FormLoad import MothwiseSalesReport_FormLoad as views
from GetDataFromDB import MonthWiseSalesReport_GetDataFromDB as MVSGDFDB
from PrintPDF import MonthWiseSalesReport_PrintPDF as pdfrpt

def MonthWiseSalesReport(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    print(LSstring)

    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    print(LSFileName)
    LSFileName = "MonthWiseSalesReport" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    startdate=request.GET["startdate"]
    enddate=request.GET["enddate"]
    comp=request.GET.getlist("unit")
    allcomp=request.GET.getlist("allcomp")
    prefix=request.GET.getlist("prefix")
    allprefix=request.GET.getlist("allprefix")
    if request.GET.getlist('dispatch')[0] == "1":
        MVSGDFDB.MonthWiseSalesReport_GetData(startdate,enddate,comp,allcomp,prefix,allprefix)
    else:
        MVSGDFDB.MonthWiseSalesReport_GetData1(startdate,enddate,comp,allcomp,prefix,allprefix)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,'MonthwiseSalesReport.html',{'GDataCompany':views.GDataCompany,'GDataPrefix':views.GDataPrefix})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response