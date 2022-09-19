import os

from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import FinishedStockInHand_FormLoad as views

from GetDataFromDB import FinishedStockInHand_GetDataFromDB as FSIHGDFDB
from PrintPDF import FinishedStockInHand_PrintPDF as pdfFSIH
from GetDataFromDB import FinishedStockInHandSummItm_GetDataFromDB as FSIHSIGDFDB
from PrintPDF import FinishedStockInHandSummItm_PrintPDF as pdfFSIHSI
from GetDataFromDB import FinishedStockInHandSummItmShade_GetDataFromDB as FSIHSISGDFDB
from PrintPDF import FinishedStockInHandSummItmShade_PrintPDF as pdfFSIHSIS
from GetDataFromDB import FinishedStockInHandSummItmShdLot_GetDataFromDB as FSIHSISLGDFDB
from PrintPDF import FinishedStockInHandSummItmShdLot_PrintPDF as pdfFSIHSISL
from GetDataFromDB import FinishedStockInHandItmLotShd_GetDataFromDB as FSIHILSGDFDB
from PrintPDF import FinishedStockInHandItmLotShd_PrintPDF as pdfFSIHILS
from GetDataFromDB import FinishedStockInHandItmClBal_GetDataFromDB as FSIHICBDFDB
from PrintPDF import FinishedStockInHandItmClBal_PrintPDF as pdfFSIHICB
from GetDataFromDB import FinishedStockInHandLtBox_GetDataFromDB as FSIHLTBOX
from PrintPDF import FinishedStockInHandLtBox_PrintPDF as pdfLTBOX
from GetDataFromDB import FinishedStockInHandDeptBox_GetDataFromDB as FSIHDTBOX
from PrintPDF import FinishedStockInHandDeptBox_PrintPDF as pdfDTBOX
from GetDataFromDB import FinishedStockInHandShadeBox_GetDataFromDB as FSIHSHDBOX
from PrintPDF import FinishedStockInHandShadeBox_PrintPDF as pdfSSHDBOX


Exceptions=""

def FinishedStockInHand(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "FinishedStockInHand" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Finished Stock In Hand/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)


    LSDepartmentCode = request.GET.getlist('comp')
    LCDepartmentCode = request.GET.getlist('allcomp')
    LSQuality = request.GET.getlist('qwlty')
    LCQuality = request.GET.getlist('allqwlty')
    LSWinding = request.GET.getlist('wndtyp')
    LCWinding = request.GET.getlist('allwndtyp')
    LSLotNo = request.GET.getlist('lot')
    LCLotNo = request.GET.getlist('alllot')
    LSItem  = request.GET.getlist('itm')
    LCItem  = request.GET.getlist('allitm')
    LSItmtype = request.GET.getlist('itmtyp')
    LCItmtype = request.GET.getlist('allitmtyp')
    LSItmgrp = request.GET.getlist('itmgrp')
    LCItmgrp = request.GET.getlist('allitmgrp')
    LDAsondate = str(request.GET['asondate'])
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSType = str(request.GET['type'])
    # print(LSQuality)
    # print(LSType)
    # print(LDAsondate)
    # print(LDStartDate)
    # print(LSItmtype)

    if LSType == 'itmltwise':
        pdfFSIH.c = pdfFSIH.canvas.Canvas(save_name + ".pdf")
        FSIHGDFDB.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,
                                               LCWinding, LSLotNo, LCLotNo, LSItem,LCItem, LSItmtype, LCItmtype, LDAsondate)

    elif LSType == 'summitmwise':
        pdfFSIHSI.c = pdfFSIHSI.canvas.Canvas(save_name + ".pdf")
        FSIHSIGDFDB.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,LCWinding,
                                                 LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDAsondate)

    elif LSType == 'summitmshadewise':
        pdfFSIHSIS.c = pdfFSIHSIS.canvas.Canvas(save_name + ".pdf")
        FSIHSISGDFDB.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding, LCWinding,
                                                 LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDStartDate, LDEndDate)

    elif LSType == 'summitmshadeltwise':
        pdfFSIHSISL.c = pdfFSIHSISL.canvas.Canvas(save_name + ".pdf")
        FSIHSISLGDFDB.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,
                                               LCWinding, LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDAsondate)

    elif LSType == 'summitmltshadewise':
        pdfFSIHILS.c = pdfFSIHILS.canvas.Canvas(save_name + ".pdf")
        FSIHILSGDFDB.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding, LCWinding,
                                                  LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDStartDate,  LDEndDate)

    elif LSType == 'itmclbal':
        pdfFSIHICB.c = pdfFSIHICB.canvas.Canvas(save_name + ".pdf")
        FSIHICBDFDB.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding, LCWinding,
                                                 LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDAsondate)

    elif LSType == 'ltbox':
        pdfLTBOX.c = pdfLTBOX.canvas.Canvas(save_name + ".pdf")
        FSIHLTBOX.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,
                                               LCWinding, LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDAsondate)

    elif LSType == 'dtbox':
        pdfDTBOX.c = pdfDTBOX.canvas.Canvas(save_name + ".pdf")
        FSIHDTBOX.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,
                                               LCWinding, LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDAsondate)

    elif LSType == 'sdbox':
        pdfSSHDBOX.c = pdfSSHDBOX.canvas.Canvas(save_name + ".pdf")
        FSIHSHDBOX.FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,
                                               LCWinding, LSLotNo, LCLotNo, LSItem, LCItem, LSItmtype, LCItmtype, LDAsondate)


    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'FinishedStockInHand.html',
                      {'GDataDepartment': views.GDataDepartment, 'GDataQuality': views.GDataQuality, 'GDataWinding': views.GDataWinding,
                       'GDataLot': views.GDataLot, 'GDataItem': views.GDataItem, 'GDataItemType': views.GDataItemType,
                       'GDataItemTypeGroup': views.GDataItemTypeGroup, 'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
