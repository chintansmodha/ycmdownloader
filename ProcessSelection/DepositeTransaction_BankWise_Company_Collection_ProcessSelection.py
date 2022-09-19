import os
from datetime import datetime
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from FormLoad import Diposite_Transaction_Bank_Company_Collection_FormLoad as views
from GetDataFromDB import DepositeTransaction_Bank_Company_Collection_GetDataFromDB as DTGDB
from PrintPDF import Diposite_Transaction_Bank_Company_Collection_PrintPDF as pdfrpt
GAgentname = []
GCompany = []
save_name = ''
Exceptions=''

def DepositeTransactionBankCompanyCollectionRegister(request):
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

    allBank = str(LSallBank)
    if allBank == 'None' and len(LSBankCode) != 0:
        Bank = str(LSBankCode)
        LSBankCode = '(' + Bank[1:-1] + ')'
        sqlwhere = ' AND  BankMaster.Code IN ' + LSBankCode
        print('sqlwhere in company : ' + sqlwhere)


    print("sqlwhere : "+sqlwhere)

    DTGDB.BankWise_Transation(sqlwhere,LDStartDate,LDEndDate,request)

    filepath = save_name + ".pdf"
    print("file path : " + str(filepath))
    if not os.path.isfile(filepath):
        # return render(request, 'StoreRegister_Returnable_Table.html',
        #               {'unit': views.unit, 'costcenter': views.costcenter, 'party': views.party,
        #                'itemtype': views.itemtype,
        #                'code': views.code, 'ccode': views.ccode, 'Exception': PRV.Exceptions})
        return render(request, 'Diposits_Transaction_Bank_Company_Collection.html',
               {'GDataBank': views.GDataBank ,'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    print("after serve")
    return render(request, 'Diposits_Transaction_Bank_Company_Collection.html', {'GDataCompany': views.GDataBank,'Exception': Exceptions})