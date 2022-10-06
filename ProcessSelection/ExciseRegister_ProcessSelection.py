import os
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import render
import os.path
from django.views.static import serve
from GetDataFromDB import ExciseRegister_GetDataFromDB
from PrintPDF import ExciseRegisterDepartmentWise as pdfrpt1
from PrintPDF import ExciseRegister_InvNoWise as pdfrpt2
from PrintPDF import ExciseRegister_ChallanTypeWiseItemShade as pdfrpt3
from PrintPDF import ExciseRegister_ChallanTypeWise as pdfrpt4
from GetDataFromDB import ExciseRegister_GetDataFromDB as ErGetDB
from FormLoad import ExciseRegister_FormLoad as views
Exceptions=""

def ExciseRegister(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "ExciseRegister" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    LSCompany=request.GET.getlist('unit')
    LSChallanType=request.GET.getlist('chllantype')
    LSParty=request.GET.getlist('party')
    LSCharges=request.GET.getlist('charges')
    LSAllCompanies=request.GET.getlist('allcomp')
    LSAllChallanTypes=request.GET.getlist('allaccount')
    LSAllParties=request.GET.getlist('allparty')
    LSAllCharges=request.GET.getlist('allcharges')
    LSDepartment=request.GET.getlist('dept')
    LSItemType=request.GET.getlist('itemtype')
    LSChallanCategory=request.GET.getlist('') 
    LSAllDepartments=request.GET.getlist('alldept')
    LSAllItemTypes=request.GET.getlist('allitemtype')
    LSAllChallanCategories=request.GET.getlist('allchallancat')
    request.GET.getlist('challancat')
    LDStartDate=request.GET['startdate']
    LDEndDate=request.GET['enddate']
    LSReportType=request.GET['year']
    LSLotType=request.GET['lottype']

    if LSReportType=='1':
        LSFileName="ExciseRegisterDepartmentWise"+LSFileName
        save_name = os.path.join(os.path.expanduser("~"), LSFileName)
        pdfrpt1.c = pdfrpt1.canvas.Canvas(save_name + ".pdf")
        ErGetDB.ExciseRegister_GetData(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType)
    elif LSReportType=="2":
        LSFileName = "ExciseRegister_InvNoWise" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt2.c = pdfrpt2.canvas.Canvas(save_name + ".pdf")
        ErGetDB.ExciseRegister_InovNoWise_PrintPDF(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType)
    elif LSReportType=="3":
        LSFileName = "ExciseRegister_ChallanTypeWiseItemShade" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt3.c = pdfrpt3.canvas.Canvas(save_name + ".pdf")
        ErGetDB.ExciseRegister_ChallanTypeWiseItemShade_PrintPDF(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType)
    elif LSReportType=="4":
        LSFileName="ExciseRegister_ChallanTypeWise"+LSFileName
        save_name=os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt4.c = pdfrpt4.canvas.Canvas(save_name + ".pdf")
        ErGetDB.ExciseRegister_ChallanTypeWise_PrintPDF(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,"ExciseRegister.html",{'GDataItemType':views.GDataItemType,'GDataDepartment':views.GDataDepartment,
   'GDataParty':views.GDataParty,'GDataCompanyCode':views.GDataCompanyCode,'GDataChallanType':views.GDataChallanType,
   'GDataCharges':views.GDataCharges}) 
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response