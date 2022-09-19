import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import BankCashStatement_FormLoad as views
from GetDataFromDB import BankCashStatement_GetDataFromDB as BCSPD
from PrintPDF import BankCashStatement_PrintPDF as pdfrpt
from GetDataFromDB import BankCashStatement_ACS_GetDataFromDB as BCSAPD
from PrintPDF import BankCashStatement_ACS_PrintPDF as pdfArpt
from GetDataFromDB import BankCashStatement_CS_GetDataFromDB as BCSCSPD
from PrintPDF import BankCashStatement_CS_PrintPDF as pdfCSrpt
from GetDataFromDB import BankCashStatement_ACN_GetDataFromDB as BCSACNPD
from PrintPDF import BankCashStatement_ACN_PrintPDF as pdfANrpt

Exceptions=""

def BankCashStatement(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "BankCashStatement" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Bank Cash Statement/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name+".pdf")
    pdfArpt.c = pdfArpt.canvas.Canvas(save_name+".pdf")
    pdfCSrpt.c = pdfCSrpt.canvas.Canvas(save_name + ".pdf")
    pdfANrpt.c = pdfANrpt.canvas.Canvas(save_name + ".pdf")

    LSCompanyUnitCode = request.GET.getlist('Comp')
    LSParty = request.GET.getlist('Bnk')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCParty =request.GET.getlist('allBnk')
    LCCompanyCode = request.GET.getlist('allComp')
    LSConsolidate=request.GET.getlist('Consolidate')
    LSACSummary=request.GET.getlist('A/C Summary')
    # print(LSCompanyUnitCode)
    # print(LSParty)
    # print(LDStartDate)
    # print(LDEndDate)
    # print(LCCompanyCode)
    # print(LCParty)
    # print(LSACSummary)
    # print(LSConsolidate)
    if LSConsolidate==['1'] and LSACSummary==['1']:
        BCSCSPD.BankCashStatement_CS_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty, LCCompanyCode, LSConsolidate,
                               LSACSummary, LSFileName)
    elif LSConsolidate==['1'] and LSACSummary==['0']:
        BCSACNPD.BankCashStatement_ACN_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty, LCCompanyCode,
                                       LSConsolidate,LSACSummary, LSFileName)
    elif LSConsolidate==['0'] and LSACSummary==['1']:
        BCSAPD.BankCashStatement_ACS_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty, LCCompanyCode,
                                         LSConsolidate, LSACSummary, LSFileName)

    elif LSConsolidate==['0'] and LSACSummary==['0']:
        BCSPD.BankCashStatement_PrintPDF(LSCompanyUnitCode,LSParty,LDStartDate,LDEndDate,LCParty,LCCompanyCode,LSConsolidate,LSACSummary,LSFileName)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "BankCashStatement.html",
                      {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,
                       'Exception': Exceptions})
    # if not os.path.isfile(filepath):
    #     return render(request, 'BankCashStatement.html', {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode})

    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
    # filepath = save_name + ".pdf"
    # if not os.path.isfile(filepath):
    #     return render(request, "GSTRegister.html",{'GDataParty': views.GDataParty, 'GDataCompanyCode': views.GDataCompanyCode, 'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))