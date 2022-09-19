import os
from datetime import datetime
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from FormLoad import Challan_Register_Customer_FormLoad as views
from GetDataFromDB import Challlan_Register_Customer_Purchase_GetDataFromDB as CRCPGDB
from PrintPDF import Challan_Register_Customer_Purchase_PrintPDF as pdfrpt

GAgentname = []
GCompany = []
save_name = ''
Exception=''


def ChallanRegisterCustomer_Purchase(request):
    sqlwhere=''
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Challan Register Customer Purchase/",
                             LSFileName)
    print("save name : "+save_name)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    # DTGDB.c = DTGDB.canvas.Canvas(save_name + ".pdf")
    LSparty = request.GET.get('allparty')
    LStransporter = request.GET.get('alltransporter')
    LScompany = request.GET.getlist('allcompany')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])

    LSselcompany = request.GET.getlist('comp')
    LSselparty = request.GET.getlist('party')
    LSseltransporter = request.GET.getlist('transporter')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    # LSReporttype = str(request.GET['reporttype'])
    print("process selection ")
    print(LSseltransporter)
    print(request.GET.getlist('transporter'))

    Company = str(LSselcompany)
    Company = '(' + Company[1:-1] + ')'

    if not LSselcompany:
        Company = " "
    elif LSselcompany:
        Company =  " And Company.Code in " + Company

    Party = str(LSselparty)
    Party = '(' + Party[1:-1]+ ')'

    if not LSselparty:
        Party =" "
    elif LSselparty:
        Party = " AND  agent.CODE IN "+ Party

    Transporter = str(LSseltransporter)
    Transporter = '('+Transporter[1:-1]+')'

    if not LSseltransporter:
        Transporter = ''
    elif LSseltransporter:
        Transporter = " AND BP_Trpt.Legalname1 IN "+Transporter


    sqlwhere = Company+ Party + Transporter


    print("from processs selection")
    print(sqlwhere)

    CRCPGDB.Challan_Register_Customer_Purchase(LSparty, LScompany, LStransporter,LSselparty, LSselcompany,LSseltransporter, LDStartDate, LDEndDate, request, sqlwhere)
    print("****************")
    print(Exception)
    print("****************")

    filepath = save_name + ".pdf"
    print("file path : " + str(filepath))
    if not os.path.isfile(filepath):
        print("file not found")
        return render(request, 'Challan_Register_Customer.html',
               {'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty,'GDataTransporter':views.GDataTransporter,'Exception': Exception})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # print("after serve")
    # return render(request, 'Diposits_Transaction_AgentWise_Cheque_Register.html',{'GDataCompany': views.GDataCompany, 'GDataBroker': views.GDataBroker,'Exception': Exception})
