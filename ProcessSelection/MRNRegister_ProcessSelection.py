import os
from datetime import datetime

from django.http import FileResponse
from django.views.static import serve

from django.shortcuts import render

from FormLoad import MRNRegister_FormLoad as views
from GetDataFromDB import MRNRegister_GetDataFromDB as MRNReg
from PrintPDF import MRNRegister_PrintPDF as pdfrpt
from GetDataFromDB import ItemWise_Details_GetDataFromDB as IWD
from PrintPDF import ItemWise_Details_PrintPDF as iwdpdfrpt
from GetDataFromDB import ItemWise_Summary_GetDataFromDB as IWS
from PrintPDF import ItemWise_Summary_PrintPDF as iwspdfrpt
from GetDataFromDB import SupplierWise_Details_GetDataFromDB as SWD
from PrintPDF import SupplierWise_Details_PrintPDF as swdpdfrpt
from GetDataFromDB import SupplierWise_Summary_GetDataFromDB as SWS
from PrintPDF import SupplierWise_Summary_PrintPDF as swspdfrpt

Exceptions=""
save_name=""
def MRNRegister(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]

    LSDepartment = request.GET.getlist('dept')
    LSSupplier = request.GET.getlist('sup')
    LSItemType = request.GET.getlist('itemtype')
    LSItem = request.GET.getlist('item')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCDepartment =request.GET.getlist('alldept')
    LCSupplier = request.GET.getlist('allsup')
    LCItemType = request.GET.getlist('allitype')
    LCItem = request.GET.getlist('allitem')
    LSReportType = int(request.GET['reporttype'])

    if LSReportType==1:
        LSFileName = "MRNRegister" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
        MRNReg.MRNRegister_PrintPDF(LSDepartment,LSSupplier,LSItemType,LSItem,LDStartDate,LDEndDate,LCDepartment,LCSupplier,LCItemType,LCItem,LSFileName,LSReportType)

    elif LSReportType==2:
        LSFileName = "SupplierWise_Details" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        swdpdfrpt.c = swdpdfrpt.canvas.Canvas(save_name + ".pdf")
        SWD.SupplierWise_Details_PrintPDF(LSDepartment, LSSupplier, LSItemType, LSItem, LDStartDate, LDEndDate, LCDepartment,LCSupplier, LCItemType, LCItem, LSFileName, LSReportType)

    elif LSReportType==3:
        LSFileName = "ItemWise_Details" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        iwdpdfrpt.c = iwdpdfrpt.canvas.Canvas(save_name + ".pdf")
        IWD.ItemWise_Details_PrintPDF(LSDepartment, LSSupplier, LSItemType, LSItem, LDStartDate, LDEndDate, LCDepartment,LCSupplier, LCItemType, LCItem, LSFileName, LSReportType)

    elif LSReportType==4:
        LSFileName = "SupplierWise_Summary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        swspdfrpt.c = swspdfrpt.canvas.Canvas(save_name + ".pdf")
        SWS.SupplierWise_Summary_PrintPDF(LSDepartment, LSSupplier, LSItemType, LSItem, LDStartDate, LDEndDate, LCDepartment,LCSupplier, LCItemType, LCItem, LSFileName, LSReportType)

    elif LSReportType==5:
        LSFileName = "ItemWise_Summary" + LSFileName
        save_name = os.path.join(os.path.expanduser("~"),LSFileName)
        iwspdfrpt.c = iwspdfrpt.canvas.Canvas(save_name + ".pdf")
        IWS.ItemWise_Summary_PrintPDF(LSDepartment, LSSupplier, LSItemType, LSItem, LDStartDate, LDEndDate, LCDepartment,LCSupplier, LCItemType, LCItem, LSFileName, LSReportType)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "MRNRegister.html",{'GDataDepartment': views.GDataDepartment, 'GDataSupplier': views.GDataSupplier, 'GDataItemType': views.GDataItemType, 'GDataItem': views.GDataItem,'Exception': Exceptions})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

