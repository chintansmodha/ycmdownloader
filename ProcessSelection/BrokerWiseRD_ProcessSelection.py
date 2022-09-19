import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import BrokerWiseRD_FormLoad as views

from GetDataFromDB import BrokerWiseRD_GetFromDB as BWRDGDB
from PrintPDF import BrokerWiseRD_PrintPDF as pdfBWRD
from GetDataFromDB import BrokerWiseRD_WithoutRDInv_GetFromDB as BWRDWIGDB
from PrintPDF import BrokerWiseRD_WithoutRDInv_PrintPDF as pdfBWRDWI
from GetDataFromDB import BrokerWiseRDAll_GetFromDB as BWRDAllGDB
from PrintPDF import BrokerWiseRDAll_PrintPDF as pdfBWRDAll

# For Data in Excel File ref
from GetDataFromDB import BrokerWiseRDEXL_GetFromDB as BWRDXLGDB
from CreateXLS import BrokerWiseRDEXL_CreateXLS as XLBWRD
from GetDataFromDB import BrokerWiseRDEXL_WithoutRDInv_GetFromDB as BWRDXLWIGDB
from CreateXLS import BrokerWiseRDEXL_WithoutRDInv_CreateXLS as XLBWRDWI
from GetDataFromDB import BrokerWiseRDEXLAll_GetFromDB as BWRDXLAllGDB
from CreateXLS import BrokerWiseRDEXLAll_CreateXLS as XLBWRDAll

Exceptions=""

def BrokerWiseRD(request):
    global Exceptions
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "BrokerWiseRD" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "C:/Users/DataTex/Downloads/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompanyCode = request.GET.getlist('comp')
    LCCompanyCode = request.GET.getlist('allcomp')
    LMCompanyCode = request.GET.getlist('mergecomp')

    LSBranch = request.GET.getlist('branch')
    LCBranch = request.GET.getlist('allbranch')

    LSBrokerGroup = request.GET.getlist('brokergrp')
    LCBrokerGroup = request.GET.getlist('allbrokergrp')

    LSBroker = request.GET.getlist('broker')
    LCBroker = request.GET.getlist('allbroker')

    LSParty = request.GET.getlist('party')
    LCParty = request.GET.getlist('allparty')

    LSYarntype = request.GET.getlist('yarn')
    LCYarntype = request.GET.getlist('allyarn')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])

    LRReporttype = str(request.GET['type'])
    LSButton = str(request.GET['button'])
    # print(LSButton)
    # print(LRReporttype)
    # print(LMCompanyCode)
    # print(LSBrokerGroup)
    # print(LSBroker)
    # print(LSParty)
    # print(LSYarntype)
    if LSButton == 'PDF':
        if LRReporttype == 'OnlyRD':
            pdfBWRD.c = pdfBWRD.canvas.Canvas(save_name+".pdf")
            BWRDGDB.BrokerWiseRD_PrintPDF(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch, LSBrokerGroup, LCBrokerGroup,
                                          LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype, LDStartDate, LDEndDate)

        elif LRReporttype == 'WithoutRD':
            pdfBWRDWI.c = pdfBWRDWI.canvas.Canvas(save_name + ".pdf")
            BWRDWIGDB.BrokerWiseRD_PrintPDF(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch, LSBrokerGroup,
                                          LCBrokerGroup,
                                          LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype, LDStartDate,
                                          LDEndDate)

        elif LRReporttype == 'All':
            pdfBWRDAll.c = pdfBWRDAll.canvas.Canvas(save_name + ".pdf")
            BWRDAllGDB.BrokerWiseRD_PrintPDF(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch, LSBrokerGroup,
                                            LCBrokerGroup,
                                            LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype, LDStartDate,
                                            LDEndDate)

        filepath = save_name + ".pdf"
        if not os.path.isfile(filepath):
            Exceptions = 'test'
            return render(request, 'BrokerWiseRD.html',
                          {'GDataCompany': views.GDataCompany, 'GDataBranch': views.GDataBranch,
                           'GDataBrokerGroup': views.GDataBrokerGroup
                              , 'GDataBroker': views.GDataBroker, 'GDataParty': views.GDataParty,
                           'GDataYarnType': views.GDataYarnType, 'Exception': Exceptions})


        # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = "attachment; filename=%s" % filepath
        return response

    elif LSButton == 'EXL':
        if LRReporttype == 'OnlyRD':
            LSFileName = "Broker Wise RD " + LSFileName + ".xlsx"
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/Generated Reports/Broker Wise RD/",
                                     LSFileName)
            BWRDXLGDB.BrokerWiseRDEXL_CreateXLS(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch, LSBrokerGroup, LCBrokerGroup,
                                      LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype, LDStartDate, LDEndDate,request)
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/ReportDevelopment/" + XLBWRD.LSFileName)
            filepath = XLBWRD.LSFileName

        elif LRReporttype == 'WithoutRD':
            LSFileName = "Broker Wise RD " + LSFileName + ".xlsx"
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/Generated Reports/Broker Wise RD/",
                                     LSFileName)
            BWRDXLWIGDB.BrokerWiseRDEXL_CreateXLS(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch,
                                                LSBrokerGroup, LCBrokerGroup,
                                                LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype,
                                                LDStartDate, LDEndDate, request)
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/ReportDevelopment/" + XLBWRDWI.LSFileName)
            filepath = XLBWRDWI.LSFileName

        elif LRReporttype == 'All':
            LSFileName = "Broker Wise RD " + LSFileName + ".xlsx"
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/Generated Reports/Broker Wise RD/",
                                     LSFileName)
            BWRDXLAllGDB.BrokerWiseRDEXL_CreateXLS(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch,
                                                  LSBrokerGroup, LCBrokerGroup,
                                                  LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype,
                                                  LDStartDate, LDEndDate, request)
            save_name = os.path.join(os.path.expanduser("~"),
                                     "D:/Report Development/ReportDevelopment/" + XLBWRDAll.LSFileName)
            filepath = XLBWRDAll.LSFileName

        # filepath = save_name + ".pdf"
        if not os.path.isfile(filepath):
            Exceptions = 'r'
            return render(request, 'BrokerWiseRD.html',
                          {'GDataCompany': views.GDataCompany, 'GDataBranch': views.GDataBranch,
                           'GDataBrokerGroup': views.GDataBrokerGroup
                              , 'GDataBroker': views.GDataBroker, 'GDataParty': views.GDataParty,
                           'GDataYarnType': views.GDataYarnType, 'Exception': Exceptions})


        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def Exception(request):
    Exceptions = 'r'
    return render(request, 'BrokerWiseRD.html',
                  {'GDataCompany': views.GDataCompany, 'GDataBranch': views.GDataBranch,
                   'GDataBrokerGroup': views.GDataBrokerGroup
                      , 'GDataBroker': views.GDataBroker, 'GDataParty': views.GDataParty,
                   'GDataYarnType': views.GDataYarnType, 'Exception': Exceptions})