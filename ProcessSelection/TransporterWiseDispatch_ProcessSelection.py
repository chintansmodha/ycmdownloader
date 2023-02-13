import os
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import render
import os.path
from django.views.static import serve
from PrintPDF import TWDD_PrintPDF as pdfrpt1
from PrintPDF import TWDS_PrintPDF as pdfrpt2
from PrintPDF import TWPWDD_PrintPDF as pdfrpt3
from PrintPDF import TWPWDS_PrintPDF as pdfrpt4
from GetDataFromDB import TransporterWiseDispatch_GetDataFromDB as TWDGDFDB
from FormLoad import TransporterWiseDispatch_FormLoad as TWDFL
Exceptions=""

def TransporterWiseDispatchProcessSelection(request):
    print("are you here")
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "Transporter Wise Dispatch" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompany=request.GET.getlist('unit')
    LSBranch=request.GET.getlist('branch')
    LSTransporter=request.GET.getlist('transporter')
    LSDispatch=request.GET.getlist('dispatch')
    LSParty=request.GET.getlist('party')
    LSAllCompany=request.GET.getlist('allunit')
    LSAllBranch=request.GET.getlist('allbranch')
    LSAllTransporter=request.GET.getlist('alltransporter')
    LSAllDispatch=request.GET.getlist('alldispatch')
    LSAllParty=request.GET.getlist('allparty')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    LSReportType=request.GET['ReportType']

    if LSReportType=='1':
        LSFileName="TransporterWiseDispatchDetail"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        TWDGDFDB.TWDDGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType)
    elif LSReportType=="2":
        LSFileName = "TransporterWiseDispatchSummary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt2.c = pdfrpt2.canvas.Canvas(save_name + ".pdf")
        TWDGDFDB.TWDSGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType)
    elif LSReportType=="3":
        LSFileName = "TransporterWisePartyWiseDispatchDetail" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt3.c = pdfrpt3.canvas.Canvas(save_name + ".pdf")
        TWDGDFDB.TWPWDDGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType)
    elif LSReportType=="4":
        LSFileName="TransporterWisePartyWiseDispatchSummary"+LSFileName
        save_name=os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt4.c = pdfrpt4.canvas.Canvas(save_name + ".pdf")
        TWDGDFDB.TWPWDSGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,"TransporterWiseDispatch.html",{'GDataCompany':TWDFL.GDataCompany,'GDataBranch':TWDFL.GDataBranch,'GDataDispatch':TWDFL.GDataDispatch,'GDataTransporter':TWDFL.GDataTransporter,'GDataParty':TWDFL.GDataParty}) 
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response