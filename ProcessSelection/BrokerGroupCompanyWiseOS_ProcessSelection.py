import os
import os.path
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from FormLoad import BrokerGroupCompanyWiseOS_FormLoad as views
from GetDataFromDB import BrokerGroupCompanyWiseOS_GetDataFromDB as BrokerGrpCompWiseOS
from PrintPDF import BrokerGroupCompanyWiseOS_PrintPDF as pdfrpt
Exceptions=""
def BrokerGroupCompanyWiseOS(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "BrokerGroupCompanyWiseOS" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Broker Group Company Wise OS/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSCompany = request.GET.getlist('comp')
    LSBroker = request.GET.getlist('broker')
    LSBrokerGroup = request.GET.getlist('brokergrp')
    LCCompany = request.GET.getlist('allcomp')
    LCBroker = request.GET.getlist('allbroker')
    LCBrokerGroup = request.GET.getlist('allbrokergrp')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    print(LSCompany,LSBroker,LSBrokerGroup,LCCompany,LCBroker,LCBrokerGroup)
    BrokerGrpCompWiseOS.BrokerGroupCompanyWiseOS_PrintPDF(LSCompany,LSBroker,LSBrokerGroup,LCCompany,LCBroker,LCBrokerGroup,LDStartDate,LDEndDate,LSFileName)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "BrokerGroupCompanyWiseOS.html",{'GDataCompany':views.GDataCompany,'GDataBroker':views.GDataBroker,'GDataBrokerGroup':views.GDataBrokerGroup, 'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))