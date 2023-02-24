from PrintPDF import BrokerWiseWOList_PrintPDF as pdfrpt
from datetime import datetime
import os
from GetDataFromDB import BrokerWiseWOList_GetDataFromDB as bwgd
from django.shortcuts import render
from FormLoad import BrokerWiseWOList_FormLoad as bwfl
from django.http import FileResponse

#Process Selection
Exceptions=""
def BrokerWiseWOList(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "BrokerWiseWOList" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompany=request.GET.getlist('comp')
    LSBrokerGroup=request.GET.getlist('brokergrp')
    LSAllCompanies=request.GET.getlist('allcomp')
    LSAllBrokerGroup=request.GET.getlist('allbrokergrp')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']

    pdfrpt.c=pdfrpt.canvas.Canvas(save_name + ".pdf")
    bwgd.BrokerWiseWOList_GetData(LSCompany,LSAllCompanies,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
       return render(request,'BrokerWiseWOList.html',{'GDataCompany': bwfl.GDataCompany,'GDataBrokerGroup': bwfl.GDataBrokerGroup})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    
    return response
