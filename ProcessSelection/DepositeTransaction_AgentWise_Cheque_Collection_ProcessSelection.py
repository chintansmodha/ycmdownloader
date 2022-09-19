import os
from datetime import datetime
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from FormLoad import Diposite_Transaction_AgentWise_cheque_Collection_FormLoad as views
from GetDataFromDB import DepositeTransaction_AgentWise_Cheque_Collection_GetDataFromDB as DTGDB
from PrintPDF import Diposite_Transaction_Agent_Wise_Cheque_Collection_PrintPDF as pdfrpt
GAgentname = []
GCompany = []
save_name = ''
Exception=''


def DepositeTransactionAgentChequeCollectionRegister(request):
    sqlwhere=''
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Desposits Transsation/",
                             LSFileName)
    print("save name : "+save_name)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    # DTGDB.c = DTGDB.canvas.Canvas(save_name + ".pdf")
    LSallBank = request.GET.get('allbank')
    LSBankCode = request.GET.getlist('selbank')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])

    LSselcompany = request.GET.getlist('selcompany')
    LSselbroker = request.GET.getlist('selbroker')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSReporttype = str(request.GET['reporttype'])

    try:
        LSallbroker = str(request.GET['allbroker'])
        if LSallbroker == 'None' and len(LSselcompany) != 0 or str(LSallbroker) == 'False':
            broker = str(LSselbroker)
            LSbrokercode = '(' + broker[1:-1] + ')'
            sqlwhere += ' AND  agent.CODE IN ' + LSbrokercode
    except:
        LSallbroker = False

    try:
        LSallcompany = str(request.GET['allcompany'])
        if LSallcompany == 'None' and len(LSselcompany) != 0 or str(LSallcompany) == 'False':
            company = str(LSselcompany)
            LSCompanycode = '(' + company[1:-1] + ')'
            sqlwhere += ' AND  BUnit.CODE IN ' + LSCompanycode
    except:
        LSallcompany = False

    DTGDB.AgentWise_Cheque_Collection_Transation(LSallbroker, LSallcompany, LSselbroker, LSselcompany, LDStartDate, LDEndDate, request,
                               LSReporttype)


    filepath = save_name + ".pdf"
    print("file path : " + str(filepath))
    if not os.path.isfile(filepath):
        return render(request, 'Diposits_Transaction_AgentWise_Cheque_Register.html',
               {'GDataCompany': views.GDataCompany, 'GDataBroker': views.GDataBroker,'Exception': Exception})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # print("after serve")
    # return render(request, 'Diposits_Transaction_AgentWise_Cheque_Register.html',{'GDataCompany': views.GDataCompany, 'GDataBroker': views.GDataBroker,'Exception': Exception})
