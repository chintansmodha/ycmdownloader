import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
Exceptions=""
save_name=""
LSFileName=""
def POYStock(request):
    from FormLoad import POYStock_FormLoad as view
    from PrintPDF import POYStock_PrintPDF as pdfrpt
    from GetDataFromDB import POYStock_GetDataFromDB as DGRGDFDB
    from PrintPDF import POYStockDetail_PrintPDF as Detpdfrpt
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] \
                 + LSstring[8:10] + LSstring[11:13] +\
                 LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    Department=request.GET.getlist("unit")
    ItemType = request.GET.getlist("type")
    startdate=request.GET['startdate']
    enddate = request.GET['enddate']
    year= request.GET['year']
    ReportType = '1' #request.GET['ReportType']
    if ReportType == '1':
        LSFileName = "POYStockSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),                               LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        DGRGDFDB.POYStock_PrintPDF(Department,ItemType,startdate,enddate,year)

    elif ReportType == '2':
        LSFileName = "POYStockDetail" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),
                                 LSFileName)
        Detpdfrpt.c = Detpdfrpt.canvas.Canvas(save_name + ".pdf")
        DGRGDFDB.POYStockDetail_PrintPDF(Department,ItemType,startdate,enddate,year)

    filepath = save_name + ".pdf"
    print(filepath)
    if not os.path.isfile(filepath):
        return render(request,"POY_Stock.html",{"GDataDepartment":view.GDataDepartment,"GDataItemCode":view.GDataItemCode})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response