from FormLoad import PartyWiseAgentLifting_FormLoad as pwalfl
from GetDataFromDB import PartyWiseAgentLifting_GetDataFromDB as pwalgdfdb
from PrintPDF import PartyWiseAgentLiftingMiniatureCopy_PrintPDF as pdfrpt1
from PrintPDF import PartWiseAgentLiftingNo_PrintPDF as pdfrpt2
import os
from django.shortcuts import render
from django.http import FileResponse
from datetime import datetime
def PartyWiseAgentLiftingProcessSelection(request):

    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "Party Wise Agent Lifting" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompany=request.GET.getlist('company')
    LSAllCompany=request.GET.getlist('allcompany')
    LSParty=request.GET.getlist('Party')
    LSAllParty=request.GET.getlist('allParty')
    LSYarnType=request.GET.getlist('Yarn')
    LSAllYarnType=request.GET.getlist('allYarn')
    LSSalesTax=request.GET.getlist('salestax')
    LSAllSalesTax=request.GET.getlist('allst')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    MiniatureType=request.GET['mc']

    if MiniatureType=='Yes':
        LSFileName="PartyWiseAgentLiftingMiniatureCopyYES"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt1.c=pdfrpt1.canvas.Canvas(save_name + ".pdf")
        pwalgdfdb.PWALGDFDBYES(LSCompany,LSAllCompany,LSParty,LSAllParty,LSYarnType,LSAllYarnType,LDStartDate,LDEndDate,LSSalesTax,LSAllSalesTax)

    elif MiniatureType=='No':
        LSFileName="PartyWiseAgentLiftingMiniatureCopyNO"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt2.c=pdfrpt2.canvas.Canvas(save_name + ".pdf")
        pwalgdfdb.PWALGDFDBNO(LSCompany,LSAllCompany,LSParty,LSAllParty,LSYarnType,LSAllYarnType,LDStartDate,LDEndDate,LSSalesTax,LSAllSalesTax)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,"PartyWiseAgentLifting.html",{'GDataCompany':pwalfl.GDataCompany,'GDataParty':pwalfl.GDataParty,'GDataYarnType':pwalfl.GDataYarnType,'GDataSalesTax':pwalfl.GDataSalesTax})

    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    
    return response
    