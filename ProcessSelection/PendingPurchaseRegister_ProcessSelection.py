import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve

from PrintPDF import PendingPurchaseRegister_PrintPDF as pdfrpt
from GetDataFromDB import PendingPurchaseRegister_GetDataFromDB as PPR
from FormLoad import PendingPurchaseRegister_FormLoad as views

def PendingPurchaseRegister(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Pending Purchase Register/",LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    LSCompanyCode = request.GET.getlist('selcompany')
    LSparty =request.GET.getlist('selparty')
    LSallCompany =request.GET.get('selectallcompany')
    LSallParty =request.GET.get('selectallparty')
    LSallByPending =request.GET.get('selectallPending')
    LSallPartlyPending=request.GET.get('selectallPartlyPending')
    LSallClose =request.GET.get('selectallClose')
    PPR.PrintPDF(LSCompanyCode, LSparty, LSFileName,LSallCompany,LSallParty,LSallByPending,LSallPartlyPending,LSallClose)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,"PendingPurchaseRegister.html",{'company': views.company,'party': views.party})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

