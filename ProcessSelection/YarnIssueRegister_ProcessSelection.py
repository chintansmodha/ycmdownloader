import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import YarnIssueRegister_FormLoad as views
from GetDataFromDB import YarnIssueRegister_GetFromDB as YIR
from PrintPDF import YarnIssueRegister_PrintPDF as pdfYIR
from GetDataFromDB import YarnIssueRegisterItemwise_GetFromDB as YIRI
from PrintPDF import YarnIssueRegisterItemwise_PrintPDF as pdfYIRI
from GetDataFromDB import YarnIssueRegisterItemLotwise_GetFromDB as YIRIL
from PrintPDF import YarnIssueRegisterItemLotwise_PrintPDF as pdfYIRIL

Exceptions=""

def YarnIssueRegister(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "YarnIssueRegister" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Yarn Issue Register/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfYIR.c = pdfYIR.canvas.Canvas(save_name + ".pdf")
    pdfYIRI.c = pdfYIRI.canvas.Canvas(save_name + ".pdf")
    pdfYIRIL.c = pdfYIRIL.canvas.Canvas(save_name + ".pdf")

    LSDepartmentCode = request.GET.getlist('Departmnt')
    LSIssue2DepartmentCode = request.GET.getlist('Issue2Departmnt')
    LSSupplierCode = request.GET.getlist('supplier')
    LCIssue2DepartmentCode = request.GET.getlist('allIssue2Departmnt')
    LCSupplierCode = request.GET.getlist('allsupplier')
    LCDepartmentCode = request.GET.getlist('allDepartmnt')
    LCSummary = request.GET.getlist('summary')
    LCStatus = request.GET.getlist('status')
    LSPROGRESStype = request.GET.getlist('PROGRESStype')
    LCPROGRESStype = request.GET.getlist('allPROGRESStype')
    LSDesttype = request.GET.getlist('Desttype')
    LCDesttype = request.GET.getlist('allDesttype')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    # print(LCStatus)
    # print(LCSummary)
    # print(LDStartDate)


    if LCSummary == ['Details']:
        if LCStatus == ['All Issues']:
            YIR.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode, LCIssue2DepartmentCode, LCSupplierCode,
                                               LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                               LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)


        elif LCStatus == ['Confirmed Issues Only']:

            YIR.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode,LCIssue2DepartmentCode, LCSupplierCode,
                                             LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                             LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

        else:

            YIR.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode,LCIssue2DepartmentCode, LCSupplierCode,
                                             LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                             LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

    elif LCSummary == ['Summary-Itemwise']:
        if LCStatus == ['All Issues']:
            YIRI.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode, LCIssue2DepartmentCode, LCSupplierCode,
                                               LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                               LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

        elif LCStatus == ['Confirmed Issues Only']:

            YIRI.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode,LCIssue2DepartmentCode, LCSupplierCode,
                                              LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                              LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

        else:
            YIRI.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode,LCIssue2DepartmentCode, LCSupplierCode,
                                              LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                              LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

    else:
        if LCStatus == ['All Issues']:
            YIRIL.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode, LCIssue2DepartmentCode, LCSupplierCode,
                                               LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                               LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

        elif LCStatus == ['Confirmed Issues Only']:
            YIRIL.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode,LCIssue2DepartmentCode, LCSupplierCode,
                                               LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                               LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

        else:
            YIRIL.YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode,LCIssue2DepartmentCode, LCSupplierCode,
                                               LCDepartmentCode, LCSummary, LDStartDate, LDEndDate,
                                               LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, "YarnIssueRegister.html",
                      {'GDataDepartment': views.GDataDepartment, 'GDataIssue2Department': views.GDataIssue2Department,
                   'GDataSupplier': views.GDataSupplier, 'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response
