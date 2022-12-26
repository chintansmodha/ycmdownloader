from datetime import datetime
import os.path
from django.http import FileResponse
from django.shortcuts import render
from FormLoad import PartyBillOS_FormLoad as views
from GetDataFromDB import PartyBillOS_GetDataFromDB
from PrintPDF import PartyBillOS_PrintPDF1 as pdfrpt1
from PrintPDF import PartyBillOS_PrintPDF2 as pdfrpt2
from PrintPDF import PartyBillOS_PrintPDF3 as pdfrpt3
from PrintPDF import PartyBillOS_PrintPDF4 as pdfrpt4
Exceptions=""
save_name=""
LSFileName=""



def PartyBillOSPS(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "Party Bill OS" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)

    LSCompany=request.GET.getlist('unit')
    LSAllCompany=request.GET.getlist('allcomp')
    LSParty=request.GET.getlist('account')
    LSAllParty=request.GET.getlist('allaccount')
    LSBroker=request.GET.getlist('subaccount')
    LSAllBroker=request.GET.getlist('allsubaccount')
    LSType = request.GET['type']
    LSInter = request.GET['inter']
    LSSummary = request.GET['summary']
    LDAsOnDate=request.GET['startdate']
    LDYear=request.GET['year']

    if LSType=='1':
        pass
        if LSSummary=='1':
            PartyBillOS_GetDataFromDB.GetDataSummary(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate,LDYear)
        elif LSSummary=='2':
            pass
    elif LSType=='2':
        LSFileName="PartyBillOSCredit"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt1.c=pdfrpt1.canvas.Canvas(save_name + ".pdf")
        PartyBillOS_GetDataFromDB.GetDataSummary21(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate,LDYear)
        
    elif LSType=='3':
        LSFileName="PartyBillOSDebit"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt3.c=pdfrpt3.canvas.Canvas(save_name + ".pdf")
        PartyBillOS_GetDataFromDB.GetDataSummary31(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate,LDYear)
    
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PartyBillOS.html',{'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty, 'GDataBroker': views.GDataBroker, 'GDataYear':views.GDataYear })
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response