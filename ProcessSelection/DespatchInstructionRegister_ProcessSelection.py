import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import DespatchInstruction_FormLoad as views
from GetDataFromDB import DespatchInstructionRegister_GetDataFromDB as DIRPD
from PrintPDF import DespatchInstructionRegister_PrintPDF as pdfDIR
from GetDataFromDB import PendingDespatchInstruction_GetDataFromDB as PDIPD
from PrintPDF import PendingDespatchInstruction_PrintPDF as pdfPDI
from GetDataFromDB import PendingDespatchInstructionDatewise_GetDataFromDB as PDIDP
from PrintPDF import PendingDespatchInstructionDatewise_PrintPDF as pdfPDID
from GetDataFromDB import PendingDespatchInstructionItemwise_GetDataFromDB as PDIIP
from PrintPDF import PendingDespatchInstructionItemwise_PrintPDF as pdfPDII
from GetDataFromDB import PendingDespatchInstructionItemShadeWise_GetDataFromDB as PDIISWPD
from PrintPDF import PendingDespatchInstructionItemShadeWise_PrintPDF as pdfPDIISW
from GetDataFromDB import PendingDespatchInstructionShadeItemwise_GetDataFromDB as PDISIWPD
from PrintPDF import  PendingDespatchInstructionShadeItemwise_PrintPDF as pdfPDISIW

Exceptions=""

def DespatchInstructionRegister(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "DespatchInstructionRegister" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Despatch Instruction Register/", LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfDIR.c = pdfDIR.canvas.Canvas(save_name+".pdf")
    pdfPDI.c = pdfPDI.canvas.Canvas(save_name + ".pdf")
    pdfPDID.c = pdfPDID.canvas.Canvas(save_name + ".pdf")
    pdfPDII.c = pdfPDII.canvas.Canvas(save_name + ".pdf")
    pdfPDIISW.c = pdfPDIISW.canvas.Canvas(save_name + ".pdf")
    pdfPDISIW.c = pdfPDISIW.canvas.Canvas(save_name + ".pdf")

    LSCompanyUnitCode = request.GET.getlist('Comp')
    LSParty = request.GET.getlist('Item')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LCParty =request.GET.getlist('allItem')
    LCCompanyCode = request.GET.getlist('allComp')
    LSDocumentType=request.GET.getlist('DcmntType')
    LCDocumentType = request.GET.getlist('allDcmntType')
    LCReport = request.GET.getlist('Report')
    LCRemarks = request.GET.getlist('Remarks')
    LSAgent   = request.GET.getlist('agent')
    LCAgent  =  request.GET.getlist('allagent')
    LSShade = request.GET.getlist('shade')
    LCShade = request.GET.getlist('allshade')
    LSparty = request.GET.getlist('prty')
    LCparty = request.GET.getlist('allprty')
    LSAgentGroup = request.GET.getlist('AgentGrp')
    LCAgentGroup = request.GET.getlist('allAgentGrp')
    LSGrade = request.GET.getlist('grade')
    LCGrade = request.GET.getlist('allgrade')
    LSItem  = request.GET.getlist('Itm')
    LCItem  = request.GET.getlist('allItm')
    # print(LCReport)
    # print(LCDocumentType)
    # print(LSDocumentType)
    # LSACSummary=request.GET.getlist('A/C Summary')
    # print(LSCompanyUnitCode)
    print(LSParty)
    # print(LDStartDate)
    # print(LDEndDate)
    # print(LCCompanyCode)
    # print(LCParty)
    # print(LSACSummary)
    # print(LSConsolidate)
    if LCReport == ['Brokerwise']:
        PDIPD.PendingDespatchInstruction_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty,LCCompanyCode, LSDocumentType,
                                                  LCDocumentType, LCRemarks, LSAgent,  LCAgent, LSShade, LCShade, LSparty, LCparty, LSAgentGroup,
                                                  LCAgentGroup, LSGrade, LCGrade, LSItem, LCItem  ,LSFileName)

    elif LCReport == ['Datewise']:
        PDIDP.PendingDespatchInstructionDatewise_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty,
                                                    LCCompanyCode, LSDocumentType,
                                                    LCDocumentType, LCRemarks, LSAgent, LCAgent, LSShade, LCShade,
                                                    LSparty, LCparty, LSAgentGroup,
                                                    LCAgentGroup, LSGrade, LCGrade, LSItem, LCItem, LSFileName)

    elif LCReport == ['Itemwise']:
        PDIIP.PendingDespatchInstructionItemwise_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty,
                                                    LCCompanyCode, LSDocumentType,
                                                    LCDocumentType, LCRemarks, LSAgent, LCAgent, LSShade, LCShade,
                                                    LSparty, LCparty, LSAgentGroup,
                                                    LCAgentGroup, LSGrade, LCGrade, LSItem, LCItem, LSFileName)

    elif LCReport == ['Itemshadewise']:
        PDIISWPD.PendingDespatchInstructionItemShade_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty,
                                                     LCCompanyCode, LSDocumentType,
                                                     LCDocumentType, LCRemarks, LSAgent, LCAgent, LSShade, LCShade,
                                                     LSparty, LCparty, LSAgentGroup,
                                                     LCAgentGroup, LSGrade, LCGrade, LSItem, LCItem, LSFileName)

    elif LCReport == ['Shadeitemwise']:
        PDISIWPD.PendingDespatchInstructionShadeItemWise_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty,
                                                        LCCompanyCode, LSDocumentType,
                                                        LCDocumentType, LCRemarks, LSAgent, LCAgent, LSShade, LCShade,
                                                        LSparty, LCparty, LSAgentGroup,
                                                        LCAgentGroup, LSGrade, LCGrade, LSItem, LCItem, LSFileName)

    else:
        DIRPD.DespatchInstructionRegister_PrintPDF(LSCompanyUnitCode, LSParty, LDStartDate, LDEndDate, LCParty,LCCompanyCode, LSDocumentType,
                                                   LCDocumentType, LSFileName)

    filepath = save_name + ".pdf"

    if LCReport == ['Brokerwise'] or LCReport == ['Datewise'] or LCReport == ['Itemwise'] or LCReport == ['Itemshadewise'] or LCReport == ['Shadeitemwise']:
        if not os.path.isfile(filepath):
            return render(request, 'PendingDespatchInstruction.html',
                          {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,
                           'GDataAgentCode': views.GDataAgentCode, 'GDataItmCode': views.GDataItmCode,
                           'GDataShadeCode': views.GDataShadeCode, 'GDataGradeCode': views.GDataGradeCode,
                           'GDataPartyCode': views.GDataPartyCode, 'GDataAgentGroupCode': views.GDataAgentGroupCode,'Exception': Exceptions})
        # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = "attachment; filename=%s" % filepath
        return response

    else:
        if not os.path.isfile(filepath):
            return render(request, "DespatchInstructionRegister.html",
                          {'GDataItemCode': views.GDataItemCode, 'GDataCompanyCode': views.GDataCompanyCode,
                           'Exception': Exceptions})
        # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = "attachment; filename=%s" % filepath
        return response
    # filepath = save_name + ".pdf"
    # if not os.path.isfile(filepath):
    #     return render(request, "GSTRegister.html",{'GDataParty': views.GDataParty, 'GDataCompanyCode': views.GDataCompanyCode, 'Exception':Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))