import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import AdhocLedgerPdf_FormLoad as views
from GetDataFromDB import AdhocLedger_GetDataFromDB as ADLPD
from PrintPDF import AdhocLedger_PrintPDF as pdfADL
from GetDataFromDB import AdhocLedgerSumryYS_GetDataFromDB as ADLSYSPD
from PrintPDF import AdhocLedgerSumryYS_PrintPDF as pdfADLSYS
from GetDataFromDB import AdhocLedgerTxn_GetDataFromDB as ADLTXNPD
from PrintPDF import AdhocLedgerTxn_PrintPDF as pdfADLTXN

Exceptions=""

def AdhocLedger(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "AdhocLedger" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Adhoc Ledger/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfADL.c = pdfADL.canvas.Canvas(save_name + ".pdf")
    pdfADLSYS.c = pdfADLSYS.canvas.Canvas(save_name + ".pdf")
    pdfADLTXN.c = pdfADLTXN.canvas.Canvas(save_name + ".pdf")

    LSCompanyUnitCode = request.GET.getlist('unit')
    LSAccountCode = request.GET.getlist('account')
    LSSubAccountCode = request.GET.getlist('subaccount')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCAccountCode = request.GET.getlist('allaccount')
    LCSubAccountCode = request.GET.getlist('allsubaccount')
    LCCompanyUnitCode = request.GET.getlist('allcomp')
    LCSummary = request.GET.getlist('Summary')
    LCEject = request.GET.getlist('Eject')
    LCNarration = request.GET.getlist('Narration')
    LCAddress = request.GET.getlist('Address')
    LMMergeCompany = request.GET.getlist('compmerge')
    LMMergeSubAcc  = request.GET.getlist('mergesubacc')
    LSTxnSumm      = request.GET.getlist('TxnSumm')
    # print("mergeComp: ",LMMergeCompany)
    # print("mergeSubAcc: ",LMMergeSubAcc)
    # print('Summary: ',LCSummary)
    # print("Summary :", LCSummary )
    # print("Eject :", LCEject)
    # print("Narration: ",LCNarration)
    # print("Address: ", LCAddress)

    if LSTxnSumm == ['1']:
        ADLTXNPD.AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate, LCAccountCode,
                             LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LCAddress, LMMergeSubAcc, LMMergeCompany)

    else:
        if LCSummary == ['0']:
            ADLPD.AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate, LCAccountCode,
                                   LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LMMergeCompany, LMMergeSubAcc)

        elif LCSummary == ['1']:
            ADLSYSPD.AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate, LCAccountCode,
                             LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LCAddress, LMMergeSubAcc)

        else:
            ADLPD.AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate,LCAccountCode,
                                       LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LMMergeCompany, LMMergeSubAcc)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "AdhocLedger.html",
                      {'GDataCompany': views.GDataCompany, 'GDataAccount': views.GDataAccount,
                       'GDataSubAccount': views.GDataSubAccount, 'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response