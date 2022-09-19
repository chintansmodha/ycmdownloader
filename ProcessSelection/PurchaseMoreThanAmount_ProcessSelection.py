import os
from datetime import datetime
from PrintPDF import PurchaseMoreThanAmount_PrintPDF as pdfrpt
from GetDataFromDB import PurchaseMoreThanAmount_GetDataFromDB as PMTAGDFDB
from FormLoad import PackingRegister_FormLoad as views
from django.shortcuts import render
from django.http import FileResponse
from django.views.static import serve

Exceptions = ""
save_name = ""
LSFileName = ""


def PurchaseMoreThanAmount(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = (
        LSstring[0:4]
        + LSstring[5:7]
        + LSstring[8:10]
        + LSstring[11:13]
        + LSstring[14:16]
        + LSstring[17:19]
        + LSstring[20:]
    )
    LSCompany = request.GET.getlist("unit")
    LSItem = request.GET.getlist("type")
    LSQuality = request.GET.getlist("qlt")
    LSSupplier = request.GET.getlist("supplier")
    LCCompany = request.GET.getlist("allcomp")
    LCItem = request.GET.getlist("alltype")
    LCQuality = request.GET.getlist("allqlt")
    LCSupplier = request.GET.getlist("allsupplier")
    LDStartDate = request.GET["startdate"]
    LDEndDate = request.GET["enddate"]
    LNAmount = request.GET["amt"]
    LSFileName = "PurchaseMoreThanAmount" + LSFileName
    save_name = os.path.join(
        os.path.expanduser("~"), LSFileName
    )
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    PMTAGDFDB.PurchaseMoreThanAmount_GetData(
        LSCompany,
        LSItem,
        LSQuality,
        LSSupplier,
        LCCompany,
        LCItem,
        LCQuality,
        LCSupplier,
        LDStartDate,
        LDEndDate,
        LNAmount,
        LSFileName,
    )
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(
            request,
            "PurchaseMoreThanDays.html",
            {
                "GDataItemCode": views.GDataItemCode,
                "GDataCompanyCode": views.GDataCompanyCode,
                "GDataQuality": views.GDataQuality,
                "GDataProductionItemGroup": views.GDataProductionItemGroup,
            },
        )
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
