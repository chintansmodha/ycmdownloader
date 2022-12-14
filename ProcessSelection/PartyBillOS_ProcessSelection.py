from datetime import datetime
import os.path

from django.http import FileResponse
from django.shortcuts import render
from FormLoad import PartyBillOS_FormLoad as views
from GetDataFromDB import PartyBillOS_GetDataFromDB
from PrintPDF import PartyBillOS_PrintPDF as pdfrpt
Exceptions=""
save_name=""
LSFileName=""



def PartyBillOSPS(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "SalesOrder" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

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


    print(type(LSType))
    if LSType=='1':
        if LSInter == '1' and LSSummary =='1':
            pass
        elif LSInter == '1' and LSSummary =='2':
            print("jbcksdbksdkcvksdbkhb")
            PartyBillOS_GetDataFromDB.GetDataSummary(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate,LDYear)
        elif LSInter == '2' and LSSummary =='1':
            pass
        elif LSInter == '2' and LSSummary =='2':
            pass
    elif LSType=='2':
        pass
    elif LSType=='3':
        pass

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PartyBillOS.html',
                  {'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty, 'GDataBroker': views.GDataBroker, 'GDataYear':views.GDataYear })
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response