import os
from datetime import datetime
from FormLoad import BrokerWiseOrderOS_FormLoad as views
from django.shortcuts import render
from django.views.static import serve

from PrintPDF import BrokerWiseOrderOS_PrintPDF as pdfrpt
from GetDataFromDB import BrokerWiseOrderOS_GetDataFromDB as BWOOGDFDB
Exceptions=""
save_name=""
LSFileName=""
def BrokerWiseOrderOS(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "BrokerWiseOrderOS" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/BrokerWiseOrderOS/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    Company = request.GET.getlist('unit')
    Broker = request.GET.getlist('account')
    Party = request.GET.getlist('subaccount')
    startdate = request.GET['startdate']
    enddate = request.GET['enddate']
    BWOOGDFDB.BrokerWiseOrderOS_PrintPDF(Company,Broker,Party,startdate,enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,'BrokerWiseOrderOS.html',{"GDataCompany":views.GDataCompany
            ,"GDataParty":views.GDataParty
            ,"GDataBroker":views.GDataBroker})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))