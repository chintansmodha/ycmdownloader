import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve

from GetDataFromDB import Store_UnBilled_Register_GRNWise_GetDataFromDB as pdfrptunbillgrn
from PrintPDF import Store_UnBilled_Register_GRNWise_PrintPDF as pdfrptunbillgrn_pfd
from GetDataFromDB import Store_UnBilled_Register_SupplierWise_GetDataFromDB as pdfrptunbillsupplier
from PrintPDF import Store_UnBilled_Register_SupplierWise_PrintPDF as pdfrptunbillsupplier_pdf
from Global_Files import Connection_String as con
from FormLoad import Store_Unbilled_GRN_FormLoad as views
Exceptions=""

def UnBilled_GRN_Register(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]

    LScheckboxgoods = request.GET.get('checkboxgoods')
    LScheckboxcapitalgoods = request.GET.get('checkboxcapitalgoods')
    LScheckboxservice = request.GET.get('checkboxservice')

    LSallPlant = request.GET.get('selectallplant')
    LSallSupplier = request.GET.get('selectallsupplier')
    LSallItem = request.GET.get('selectallitem')

    LSPlant = request.GET.getlist('selplant')
    LSSupplier = request.GET.getlist('selsupplier')
    LSItem = request.GET.getlist('selitem')

    LSReportType = request.GET.get('SortByReportType')

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])

    # pdfrpt.c = pdfrpt.canvas.Canvas(LSFileName + ".pdf")
    # PurReg.PurchaseRegister_PrintPDF(LSCompanyUnitCode, LSItemTypeCode, LDStartDate, LDEndDate, LSFileName,
    #        LCItemTypeCode, LCCompanyCode, LSReportType)
    print("before calling if ")
    if LSReportType == '1':
        LSFileName = "Store UnBilled GRN Wise Register " + LSFileName
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Store_Unbilled_Register_GRN_Wise/",
                                 LSFileName)
        pdfrptunbillgrn_pfd.c = pdfrptunbillgrn_pfd.canvas.Canvas(save_name + ".pdf")

        pdfrptunbillgrn.StoreRegisterGRNWisePrintPDF(LSallPlant, LSallSupplier, LSallItem, LSPlant, LSSupplier, LSItem,
                                                     LDStartDate, LDEndDate, LSReportType, LSFileName, LScheckboxgoods,
                                                     LScheckboxcapitalgoods, LScheckboxservice)
    elif LSReportType == '2':
        LSFileName = "Store UnBilled Supplier Wise Register " + LSFileName
        save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Store_Unbilled_Register_Supplier_Wise/",
                                 LSFileName)
        pdfrptunbillsupplier_pdf.c = pdfrptunbillsupplier_pdf.canvas.Canvas(save_name + ".pdf")

        pdfrptunbillsupplier.StoreRegisterSupplierWisePrintPDF(LSallPlant, LSallSupplier, LSallItem, LSPlant,
                                                               LSSupplier,
                                                               LSItem, LDStartDate, LDEndDate, LSReportType, LSFileName,
                                                               LScheckboxgoods, LScheckboxcapitalgoods,
                                                               LScheckboxservice)
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "Store_Unbilled_GRN.html",
                  {'plant': views.plant, 'costcenter': views.costcenter, 'supplier': views.supplier,
                   'itemtype': views.itemtype, 'code': views.code, 'ccode': views.ccode,'Exception':Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

# print("before calling the  storeregister print pdf")
#        print("plane name " +LSallPlant)
#        print(LSallSupplier)
#        print(LSallItem)
#        print(LSPlant)
#        print(LSallSupplier)
#        print(LSItem)
#        print(LDStartDate)
#        print(LDEndDate)
# print(LSReportType)
