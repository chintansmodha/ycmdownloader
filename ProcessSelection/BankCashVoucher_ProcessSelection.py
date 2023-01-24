from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render

from FormLoad import BankCashVoucher_FormLoad as views
from GetDataFromDB import BankCashVoucher_GetDataFromDB as BCVGDFDB
from PrintPDF import BankCashVoucher_PrintPDF as pdfrpt

def BankCashVoucher(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "BankCashVoucher" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    vchno=request.GET.getlist("vchno")
    vchdate=request.GET.getlist("vchdate")
    partycode=request.GET.getlist("partycode")

    BCVGDFDB.BankCashVoucher_GetData(vchdate,vchno,partycode)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'BankCashVoucherPDF.html',{'GDataCompany':views.GDataCompany,'GDataBank':views.GDataBank,'GDataVChNo':views.GDataVChNo,'GDataBankCashVoucher':views.GDataBankCashVoucher})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response