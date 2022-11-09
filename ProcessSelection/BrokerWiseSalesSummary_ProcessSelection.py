from PrintPDF import BrokerWiseSalesSummaryItemWiseSummaryWise_PrintPDF as pdfrpt1
from PrintPDF import BrokerWiseSalesSummary_PrintPDF as pdfrpt2
from PrintPDF import BrokerWiseSalesSummaryItemWise_PrintPDF as pdfrpt3
from PrintPDF import BrokerWiseSalesSummarySummaryWise_PrintPDF as pdfrpt4
from datetime import datetime
import os
from GetDataFromDB import BrokerWiseSalesSummary_GetDataFromDB as bwssgdfdb
from django.shortcuts import render
from FormLoad import BrokerWiseSalesSummary_FormLoad as bwssfl
from django.http import FileResponse

#Process Selection
Exceptions=""
def bwssps(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "BrokerWiseSalesSummary" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompany=request.GET.getlist('unit')
    LSParty=request.GET.getlist('party')
    LSBrokerGroup=request.GET.getlist('broker')
    LSAllCompanies=request.GET.getlist('allcomp')
    LSAllParties=request.GET.getlist('allparty')
    LSAllBrokerGroup=request.GET.getlist('allbroker')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    ItemWise=request.GET['item']
    SummaryWise=request.GET['summary1']
    pdfrpt=''
    if ItemWise=='yes' and SummaryWise=='yes':
        LSFileName="BrokerWiseSalesSummaryItemWiseSummaryWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt1.c=pdfrpt1.canvas.Canvas(save_name + ".pdf")
        bwssgdfdb.BrokerWiseSalesSummaryItemWiseSummaryWise(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
        ItemWise,SummaryWise)
    elif ItemWise=='no' and SummaryWise=='no':
        LSFileName="BrokerWiseSalesSummary"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt2.c=pdfrpt2.canvas.Canvas(save_name + ".pdf")
        bwssgdfdb.BrokerWiseSalesSummary(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
        ItemWise,SummaryWise)
    elif ItemWise=='yes' and SummaryWise=='no':
        LSFileName="BrokerWiseSalesSummaryItemWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt3.c=pdfrpt3.canvas.Canvas(save_name + ".pdf")
        bwssgdfdb.BrokerWiseSalesSummaryItemWise(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
        ItemWise,SummaryWise)
    elif ItemWise=='no' and SummaryWise=='yes':
        LSFileName="BrokerWiseSalesSummarySummaryWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt4.c=pdfrpt4.canvas.Canvas(save_name + ".pdf")
        bwssgdfdb.BrokerWiseSalesSummarySummaryWise(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
        ItemWise,SummaryWise,)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,'BrokerWiseSalesSummary.html',{'GDataParty':bwssfl.GDataParty,
        'GDataCompanyCode':bwssfl.GDataCompanyCode,'GDataBrokerGroup':bwssfl.GDataBrokerGroup})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    
    return response
