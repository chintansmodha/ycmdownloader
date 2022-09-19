import os
import os.path
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
from FormLoad import LotNoListing_FormLoad as views
from GetDataFromDB import LotNoListing_GetDataFromDB as LotListing
from PrintPDF import LotNoListing_PrintPDF as pdfrpt
Exceptions=""
def LotNoListing(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "LotNoListing" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Lot No Listing/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSResource = request.GET.getlist('res')
    LSLotNo = request.GET.getlist('lotno')
    LCResource = request.GET.getlist('allres')
    LCLotNo = request.GET.getlist('alllotno')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LDProductFamily = int(request.GET['Product'])
    # print(LDProductFamily)

    LotListing.LotNoListing_PrintPDF(LSResource,LSLotNo,LCResource,LCLotNo,LDStartDate,LDEndDate,LSFileName,LDProductFamily)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "LotNoListing.html",
                      {'GDataResource': views.GDataResource, 'GDataLotNo': views.GDataLotNo,'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response