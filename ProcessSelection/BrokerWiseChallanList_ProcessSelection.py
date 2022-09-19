# function to generate report
import os
from datetime import datetime
from django.views.static import serve
from babel.numbers import format_currency
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from FormLoad import BrokerWiseChallanList_FormLoad as views
from PrintPDF import BrokerWiseChallanList_PrintPDF as pdfrpt
from PrintPDF import PrintYeanChallanBoxNoWisePDF as printchallanrpt
from GetDataFromDB import BrokerWiseChallanList_GetDataFromDB as BWCL

from django.http import FileResponse

Exception = ""
counter = 0

def BrokerWiseChallanList(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    sqlwhere = ''
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName="BrokerWiseChallanList_"+LSFileName
    pdfrpt.c = pdfrpt.canvas.Canvas(LSFileName + ".pdf")
    LSselcompany = request.GET.getlist('selcompany')
    LSselparty = request.GET.getlist('selparty')
    LSselstate = request.GET.getlist('selstate')
    LSselBrokergroup = request.GET.getlist('selbroker')
    LSselitemtype = request.GET.getlist('selitemtype')
    LSselshade = request.GET.getlist('selshade')
    LSRegistertype=str(request.GET['CboRegisterType'])
    LSPrintLotNo=str(request.GET['CboPrintlotno'])

    try:
        LSallcompany = str(request.GET['allcompany'])
    except:
        LSallcompany = False
    try:
        LSallparty = str(request.GET['allparty'])
    except:
        LSallparty = False
    try:
        LSallstate = str(request.GET['allstate'])
    except:
        LSallstate = False
    try:
        LSallbroker = str(request.GET['allbroker'])
    except:
        LSallbroker = False
    try:
        LSallitemtype = str(request.GET['allitemtype'])
    except:
        LSallitemtype = False
    try:
        LSallshade = str(request.GET['allshade'])
    except:
        LSallshade = False
    try:
        if LSallcompany == 'None' and len(LSselcompany) != 0 or str(LSallcompany) == 'False':
            ccompany = str(LSselcompany)
            LSCompanycode = '(' + ccompany[1:-1] + ')'
            sqlwhere += ' AND  BUnit.CODE IN ' + LSCompanycode

        if LSallparty == 'None' and len(LSselparty) != 0 or str(LSallparty) == 'False':
            party = str(LSselparty)
            LSPartycode = '(' + party[1:-1] + ')'
            sqlwhere += ' AND BusinessPartner.NumberID IN ' + LSPartycode

        if LSallstate == 'None' and len(LSselstate) != 0 or str(LSallstate) == 'False':
            state = str(LSselstate)
            LSStatecode = '(' + state[1:-1] + ')'
            sqlwhere += ' AND  State.CODE IN ' + LSStatecode

        if LSallitemtype == 'None' and len(LSselitemtype) != 0 or str(LSallitemtype) == 'False':
            itemtype = str(LSselitemtype)
            LSitemtpyecode = '(' + itemtype[1:-1] + ')'
            sqlwhere += ' AND BusinessPartner.NumberID IN ' + LSitemtpyecode

        if LSallbroker == 'None' and len(LSselBrokergroup) != 0 or str(LSallbroker) == 'False':
            broker = str(LSselBrokergroup)
            LSselBrokergroupcode = '(' + broker[1:-1] + ')'
            sqlwhere += ' AND UGG.CODE IN ' + LSselBrokergroupcode

        if LSallshade == 'None' and len(LSselshade) != 0 or str(LSallshade) == 'False':
            shade = str(LSselshade)
            LSshadecode = '(' + shade[1:-1] + ')'
            sqlwhere += ' AND UGG.CODE IN ' + LSshadecode
    except:
        pass

    LSRegistertype = str(request.GET['CboRegisterType'])
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSFileName = "BrokerWiseChallanList" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),
    #                          "D:/Report Development/Generated Reports/Broker Wise Challan List/",
    #                          LSFileName)

    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    print("file path : "+save_name)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    # printchallanrpt.c = printchallanrpt.canvas.Canvas(save_name + ".pdf")
    BWCL.BrokerWiseChallanList_PrintPDF(LSselcompany, LSselparty, LSselstate, LSselBrokergroup, LSselitemtype,
                                        LSselshade, LSallparty, LSallshade, LSallstate, LSallbroker, LSallcompany,
                                        LSallitemtype, LDStartDate, LDEndDate, LSRegistertype, sqlwhere,LSFileName,LSPrintLotNo,request)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'BrokerwiseChallanList.html',
                      {'company': views.company, 'party': views.party, 'state': views.state, 'itemtype': views.itemtype, 'shade': views.shade,
                       'broker': views.broker, 'Exception': Exception})

    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response