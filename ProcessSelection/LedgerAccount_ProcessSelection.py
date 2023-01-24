from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render

from FormLoad import LedgerAccount_FormLoad as views
from GetDataFromDB import LedgerAccount_GetDataFromDB as LAGDFDB
from PrintPDF import LedgerAccount_PrintPDF as pdfrpt
from PrintPDF import LedgerAccount_Ledger_PrintPDF as pdfrpt1

def LedgerAccount_Process(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    

    LSCompany=request.GET.getlist("unit")
    LCCompany = request.GET.getlist("allcomp")
    startdate=request.GET['startdate']
    enddate=request.GET['enddate']
    print(startdate,enddate)
    if request.GET.getlist('book')[0] == '1':
        LSFileName = "LedgerAccountSDL" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        reportName="Sundry Debtors Ledger"
        GLCode =" and glmaster.code in ('2010122245')"
        LAGDFDB.LedgerAccount_GetDataLedger(LSCompany,LCCompany,GLCode,startdate,enddate,reportName)
    if request.GET.getlist('book')[0] == '3':
        LSFileName = "LedgerAccountSDS" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        reportName="Sundry Debtors Summary"
        GLCode =" and glmaster.code in ('2010122245')"
        LAGDFDB.LedgerAccount_GetDataSummary(LSCompany,LCCompany,GLCode,startdate,enddate,reportName)
    if request.GET.getlist('book')[0] == '2':
        LSFileName = "LedgerAccountSCL" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        reportName="Sundry Creditors Ledger"
        GLCode =" and glmaster.code in ('1010101210')"
        LAGDFDB.LedgerAccount_GetDataLedger(LSCompany,LCCompany,GLCode,startdate,enddate,reportName)
    if request.GET.getlist('book')[0] == '4':
        LSFileName = "LedgerAccountSCS" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        reportName="Sundry Creditors Summary"
        GLCode =" and glmaster.code in ('1010101210')"
        LAGDFDB.LedgerAccount_GetDataSummary(LSCompany,LCCompany,GLCode,startdate,enddate,reportName)

    # LAGDFDB.LedgerAccount_GetData(LSCompany,LCCompany,startdate,enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,'LedgerAccount.html',{'GDataCompany':views.GDataCompany})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response