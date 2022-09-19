from django.shortcuts import render
from ProcessSelection import AdhocLedger_BankCashVoucher_ProcessSelection
from ProcessSelection import MISBrokerWiseOS_SI_InvoiceDetails_ProcessSelection
from ProcessSelection import AdhocLedger_PurchaseBill_ProcessSelection
from FormLoad import AdhocLedger_FormLoad as ALFL
type=''
def Doctype(request):
    global type
    type =''
    LSDocType = str(request.GET['doctype'])
    if LSDocType == 'BR ' or LSDocType == 'CR ':
        type='Receipt'
        return AdhocLedger_BankCashVoucher_ProcessSelection.BankCashVoucher(request,type)
    if LSDocType == 'BP ' or LSDocType == 'CP ':
        type = 'Payment'
        return AdhocLedger_BankCashVoucher_ProcessSelection.BankCashVoucher(request,type)
    if LSDocType == 'SD ':
        return MISBrokerWiseOS_SI_InvoiceDetails_ProcessSelection.InvoiceDetails(request)
    if LSDocType == 'PD ':
        return AdhocLedger_PurchaseBill_ProcessSelection.PurchaseBill(request)
    else:
        return render(request,'AdhocLedger.html',{'GDataCompany':ALFL.GDataCompany,'GDataAccount':ALFL.GDataAccount,'GDataSubAccount':ALFL.GDataSubAccount,"Exception":"Please Select Document type from [BP,BR,CP,CR,SD,PD]","GDataYear":ALFL.GDataYear})