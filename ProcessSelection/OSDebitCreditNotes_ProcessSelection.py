from FormLoad import OSDebitCreditNotes_FormLoad as OSDCNFL
from GetDataFromDB import OSDebitCreditNotes_GetDataFromDB as OSDCNGDFDB
from PrintPDF import OSCreditNotesInterCompanySummaryWise_PrintPDF as pdfrpt1
from PrintPDF import OSCreditNotes_PrintPDF as pdfrpt2
from PrintPDF import OSCreditNotesInterCompany_PrintPDF as pdfrpt3
from PrintPDF import OSCreditNotesSummarywise_PrintPDF as pdfrpt4
from PrintPDF import OSDebitNotesInterCompanySummaryWise_PrintPDF as pdfrpt5
from PrintPDF import OSDebitNotes_PrintPDF as pdfrpt6
from PrintPDF import OSDebitNotesInterCompany_PrintPDF as pdfrpt7
from PrintPDF import OSDebitNotesSummaryWise_PrintPDF as pdfrpt8
import os
from django.shortcuts import render
from django.http import FileResponse
from datetime import datetime
def OSDebitCreditNotesProcessSelection(request):

    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "OSDebit Credit Notes AsOn" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompany=request.GET.getlist('company')
    LSAllCompany=request.GET.getlist('allcompany')
    LSParty=request.GET.getlist('Party')
    LSAllParty=request.GET.getlist('allParty')
    LSBroker=request.GET.getlist('Broker')
    LSAllBroker=request.GET.getlist('allBroker')
    LDAsOnDate=request.GET['asondate']
    Type=request.GET['type']
    InterCompany=request.GET['ic']
    Summary=request.GET['summary']

    if Type=='Credit'and InterCompany=='Yes' and Summary=='Yes':
        LSFileName="OSCreditNotesInterCompanySummaryWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt1.c=pdfrpt1.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSCreditNotesInterCompanySummaryWise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)

    elif Type=='Credit'and InterCompany=='No' and Summary=='No':
        LSFileName="OSCreditNotes"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt2.c=pdfrpt2.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSCreditNotes(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)
    
    elif Type=='Credit'and InterCompany=='Yes' and Summary=='No':
        LSFileName="OSCreditNotesInterCompany"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt3.c=pdfrpt3.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSCreditNotesInterCompany(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)

    elif Type=='Credit'and InterCompany=='No' and Summary=='Yes':
        LSFileName="OSCreditNotesSummarywise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt4.c=pdfrpt4.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSCreditNotesSummarywise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)

    elif Type=='Debit'and InterCompany=='Yes' and Summary=='Yes':
        LSFileName="OSDebitNotesInterCompanySummaryWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt5.c=pdfrpt5.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSDebitNotesInterCompanySummaryWise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)

    elif Type=='Debit'and InterCompany=='No' and Summary=='No':
        LSFileName="OSDebitNotes"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt6.c=pdfrpt6.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSDebitNotes(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)
    
    elif Type=='Debit'and InterCompany=='Yes' and Summary=='No':
        LSFileName="OSDebitNotesInterCompany"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt7.c=pdfrpt7.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSDebitNotesInterCompany(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)

    elif Type=='Debit'and InterCompany=='No' and Summary=='Yes':
        LSFileName="OSDebitNotesSummaryWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt8.c=pdfrpt8.canvas.Canvas(save_name + ".pdf")
        OSDCNGDFDB.OSDebitNotesSummaryWise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate)

    
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,"OSDeditCreditNotes.html",{'GDataCompany':OSDCNFL.GDataCompany,'GDataParty':OSDCNFL.GDataParty,'GDataBroker':OSDCNFL.GDataBroker})

    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    
    return response
    