import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import FinishedStockInHand_FormLoad as views

from GetDataFromDB import FinishedStockInHandAgeing_GetDataFromDB as FSIH_A
from PrintPDF import FinishedStockInHandAgeing_PrintPDF as pdf




def FinishedStockInHandAgeing(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "FinishedStockInHand" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Finished Stock In Hand/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LSWinding = request.GET.getlist('wndtyp')
    LCWinding = request.GET.getlist('allwndtyp')
    LSLotNo = request.GET.getlist('lot')
    LCLotNo = request.GET.getlist('alllot')
    LSItem = request.GET.getlist('itm')
    LCItem = request.GET.getlist('allitm')
    LSItmtype = request.GET.getlist('itmtyp')
    LCItmtype = request.GET.getlist('allitmtyp')
    LDBoxondate = str(request.GET['boxondate'])
    LDAsondate = str(request.GET['asondate'])
    LSType = str(request.GET['type'])
    LSDays = request.GET.getlist('input')
    LSDay = []
    for i in LSDays:
        if i:
            LSDay.append(int(i))

    pdf.c = pdf.canvas.Canvas(save_name + ".pdf")
    FSIH_A.FinishedStockInHandAgeing_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSWinding,
                                           LCWinding, LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype,
                                           LDBoxondate, LDAsondate, LSDay)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'no data'
        return render(request, 'FinishedStockInHandAgeing.html', {'GDataDepartment':views.GDataDepartment, 'GDataQuality':views.GDataQuality,
                                                                  'GDataWinding':views.GDataWinding,'GDataLot':views.GDataLot, 'GDataItem':views.GDataItem,
                                                                  'GDataItemType':views.GDataItemType, 'GDataItemTypeGroup':views.GDataItemTypeGroup,
                                                                  'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response