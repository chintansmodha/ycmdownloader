import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import ContractProgress_FormLoad as views

from GetDataFromDB import ContractProgress_GetFromDB as CPGetDB
from PrintPDF import ContractProgress_PrintPDF as pdfCP
from GetDataFromDB import ContractProgressContractNoWise_GetDataFromDB as CPCNWGetDB
from PrintPDF import ContractProgressContractNoWise_PrintPDF as pdfCPCNW
from PrintPDF import ContractProgressItem_PrintPDF as pdfCPIW
from GetDataFromDB import ContractProgressItem_GetFromDB as CPIWGetDB
from PrintPDF import ContractProgressShade_PrintPDF as pdfCPS
from GetDataFromDB import ContractProgressShade_GetFromDB as CPSGetDB

Exceptions=""

def ContractProgress(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "ContractProgress" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Contract Progress/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)


    LSBroker = request.GET.getlist('Broker')
    LCBroker = request.GET.getlist('allBroker')
    LSYarn = request.GET.getlist('Yarn')
    LCYarn = request.GET.getlist('allYarn')
    LSItem = request.GET.getlist('itm')
    LCItem = request.GET.getlist('allitm')
    LSShade = request.GET.getlist('Shade')
    LCShade = request.GET.getlist('allShade')
    LSParty  = request.GET.getlist('Party')
    LCParty  = request.GET.getlist('allParty')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSType = str(request.GET['type'])
    # print(LSType)
    # print(LSType)
    # print(LDAsondate)
    # print(LDStartDate)
    # print(LSItmtype)
    # print(LSShade)

    if  LSType == 'BrokerWise':
        pdfCP.c = pdfCP.canvas.Canvas(save_name + ".pdf")
        CPGetDB.ContractProgress_PrintPDF(LSBroker, LCBroker, LSYarn, LCYarn, LSItem, LCItem, LSShade, LCShade, LSParty,
                                          LCParty, LDStartDate,LDEndDate)

    elif LSType == 'ContractNoWise':
        pdfCPCNW.c = pdfCPCNW.canvas.Canvas(save_name + ".pdf")
        CPCNWGetDB.ContractProgress_PrintPDF(LSBroker, LCBroker, LSYarn, LCYarn, LSItem, LCItem, LSShade, LCShade, LSParty,
                                          LCParty, LDStartDate, LDEndDate)

    elif LSType == 'ItmWise':
        pdfCPIW.c = pdfCPIW.canvas.Canvas(save_name + ".pdf")
        CPIWGetDB.ContractProgress_PrintPDF(LSBroker, LCBroker, LSYarn, LCYarn, LSItem, LCItem, LSShade, LCShade,
                                             LSParty, LCParty, LDStartDate, LDEndDate)

    else:
        pdfCPS.c = pdfCPS.canvas.Canvas(save_name + ".pdf")
        CPSGetDB.ContractProgress_PrintPDF(LSBroker, LCBroker, LSYarn, LCYarn, LSItem, LCItem, LSShade, LCShade,
                                            LSParty, LCParty, LDStartDate, LDEndDate)


    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'ContractProgress.html',
                      {'GDataParty':views.GDataParty,'GDataBroker':views.GDataBroker, 'GDataItem':views.GDataItem, 'GDataItemType':views.GDataItemType,
                       'GDataShade':views.GDataShade, 'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
