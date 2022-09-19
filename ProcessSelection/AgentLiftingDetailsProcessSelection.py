import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import AgentLiftingDetailsFormLoad as views


Exceptions=""

from GetDataFromDB import AgentLiftingGetDataFromDB as AgLGDB
from PrintPDF import AgentLifting_PrintPDF as pdfAGL
from GetDataFromDB import AgentLiftingItemGetDataFromDB as AgLIGDB
from PrintPDF import AgentLiftingItem_PrintPDF as pdfAGLI
from GetDataFromDB import AgentLiftingFinalSummGetDataFromDB as AgLFSummGDB
from PrintPDF import AgentLiftingFinalSumm_PrintPDF as pdfAGLFSumm
from GetDataFromDB import AgentLiftingSummYsGetDataFromDB as AgLSuGDB
from PrintPDF import AgentLiftingSummYs_PrintPDF as pdfAGLSu
from GetDataFromDB import AgentLiftingItemSummYsGetDataFromDB as AgLISuGDB
from PrintPDF import AgentLiftingItemSummYs_PrintPDF as pdfAGLISu

def AgentLifting(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "AgentLifting" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Agent Lifting Details/", LSFileName)

    LSBrokerGrp = request.GET.getlist('BrokerGrp')
    LCBrokerGrp = request.GET.getlist('allBrokerGrp')
    LSBroker = request.GET.getlist('Broker')
    LCBroker = request.GET.getlist('allBroker')
    LSPlant = request.GET.getlist('Plant')
    LCPlant = request.GET.getlist('allPlant')
    LSParty  = request.GET.getlist('Party')
    LCParty  = request.GET.getlist('allParty')
    LSItem = request.GET.getlist('itm')
    LCItem = request.GET.getlist('allitm')
    LSYarn = request.GET.getlist('Yarn')
    LCYarn = request.GET.getlist('allYarn')
    LSQuality = request.GET.getlist('Qlty')
    LCQuality = request.GET.getlist('allQlty')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSMergePlant = ''
    LSSummary = ''
    try:
        LSMergePlant = str(request.GET['mergeplant'])
        LSSummary = str(request.GET['summ'])
    except:
        pass
    LSOrder = str(request.GET['reportOrdder'])
    # print(LSMergePlant, LSOrder, LSSummary)
    # print(LDAsondate)
    # print(LDStartDate)
    # print(LSItmtype)
    # print(LSShade)

    if  LSOrder == 'partyWise':
        if int(LSSummary) == 0:
            pdfAGL.c = pdfAGL.canvas.Canvas(save_name + ".pdf")
            AgLGDB.AgentLifting_PrintPDF(LSBrokerGrp, LCBrokerGrp, LSBroker, LCBroker, LSPlant, LCPlant, LSParty, LCParty,
                                     LSItem, LCItem, LSYarn, LCYarn, LSQuality, LCQuality, LDStartDate, LDEndDate, LSMergePlant, LSSummary)
        else:
            pdfAGLSu.c = pdfAGLSu.canvas.Canvas(save_name + ".pdf")
            AgLSuGDB.AgentLifting_PrintPDF(LSBrokerGrp, LCBrokerGrp, LSBroker, LCBroker, LSPlant, LCPlant, LSParty,
                                         LCParty, LSItem, LCItem, LSYarn, LCYarn, LSQuality, LCQuality, LDStartDate, LDEndDate,
                                         LSMergePlant, LSSummary)

    elif LSOrder == 'itemWise' :
        if int(LSSummary) == 0:
            pdfAGLI.c = pdfAGLI.canvas.Canvas(save_name + ".pdf")
            AgLIGDB.AgentLifting_PrintPDF(LSBrokerGrp, LCBrokerGrp, LSBroker, LCBroker, LSPlant, LCPlant, LSParty, LCParty,
                                         LSItem, LCItem, LSYarn, LCYarn, LSQuality, LCQuality, LDStartDate, LDEndDate, LSMergePlant, LSSummary)
        else:
            pdfAGLISu.c = pdfAGLISu.canvas.Canvas(save_name + ".pdf")
            AgLISuGDB.AgentLifting_PrintPDF(LSBrokerGrp, LCBrokerGrp, LSBroker, LCBroker, LSPlant, LCPlant, LSParty,
                                          LCParty, LSItem, LCItem, LSYarn, LCYarn, LSQuality, LCQuality, LDStartDate, LDEndDate,
                                          LSMergePlant, LSSummary)

    elif LSOrder == 'finalsumm':
        pdfAGLFSumm.c = pdfAGLFSumm.canvas.Canvas(save_name + ".pdf")
        AgLFSummGDB.AgentLifting_PrintPDF(LSBrokerGrp, LCBrokerGrp, LSBroker, LCBroker, LSPlant, LCPlant, LSParty, LCParty,
                                      LSItem, LCItem, LSYarn, LCYarn, LSQuality, LCQuality, LDStartDate, LDEndDate,LSMergePlant, LSSummary)


    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'AgentLiftingDetails.html',
                      {'GDataBrokerGroup': views.GDataBrokerGroup, 'GDataBroker': views.GDataBroker,
                       'GDataPlant': views.GDataPlant, 'GDataParty': views.GDataParty, 'GDataItem': views.GDataItem,
                       'GDataItemType': views.GDataItemType, 'GDataItemQuality': views.GDataItemQuality, 'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
