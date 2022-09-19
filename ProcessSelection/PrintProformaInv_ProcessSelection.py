import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve
import os.path
from FormLoad import PrintProformaInv_Formload as views
from GetDataFromDB import PrintProformaInv_GetDataFromDB as PPIGD
from PrintPDF import PrintProformaInv_PrintPDF as pdfrpt
from GetDataFromDB import PrintProformaPrePackLis_GetDataFromDB as PPIPPLGD
from PrintPDF import PrintProformaPrePackLis_PrintPDF as pdfrptPPL
from GetDataFromDB import PrintProformaPreCustom_GetDataFromDB as PPIPCGD
from PrintPDF import PrintProformaPreCustom_PrintPDF as pdfrptPC
from GetDataFromDB import PrintProformaCommercial_GetDataFromDB as PPICGD
from PrintPDF import PrintProformaCommercial_PrintPDF as pdfrptC
from GetDataFromDB import PrintProformaBL_GetDataFromDB as PPBLGD
from PrintPDF import PrintProformaBL_PrintPDF as pdfrptBL
from GetDataFromDB import PrintProformaAnx_GetDataFromDB as PPAnxGD
from PrintPDF import PrintProformaAnx_PrintPDF as pdfrptAnx
from GetDataFromDB import PrintProformaCrtfct_GetDataFromDB as PPCerft
from PrintPDF import PrintProformaCrtfct_PrintPDF as pdfPPC

Exceptions = ''

def PrintProformaInv_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " SO.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(SO.ORDERDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPIGD.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintProformaInv_Table.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exception': PPIGD.Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response


def PackingListPreShipProforma_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrptPPL.c = pdfrptPPL.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " PLANTINVOICE.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPIPPLGD.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'Exceptions'
        return render(request, 'PrintProformaPrePackLis.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exceptions': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def PreCustom_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrptPC.c = pdfrptPC.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " PLANTINVOICE.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPIPCGD.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'Exceptions'
        return render(request, 'PrintProformaPreCustom.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exceptions': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def Commercial_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrptC.c = pdfrptC.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " PLANTINVOICE.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPICGD.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'Exceptions'
        return render(request, 'PrintProformaCommercial.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exceptions': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def BLInstruction_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrptBL.c = pdfrptBL.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " PLANTINVOICE.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPBLGD.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'Exceptions'
        return render(request, 'PrintProformaBLInstruction.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exceptions': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def Annex_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrptAnx.c = pdfrptAnx.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " PLANTINVOICE.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPAnxGD.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'Exceptions'
        return render(request, 'PrintProformaAnex.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exceptions': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def Certificate_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintProformaInvoice" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Proforma Invoice/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfPPC.c = pdfPPC.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    InvoiceNo = request.GET.getlist('InvoiceNo')
    InvoiceDt = request.GET.getlist('InvoiceDt')

    InvoiceNos = " PLANTINVOICE.CODE in " + "(" + str(InvoiceNo)[1:-1] + ")"
    InvoiceDts = " AND VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') in  " + "(" + str(InvoiceDt)[1:-1] + ")"

    PPCerft.PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = 'Exceptions'
        return render(request, 'PrintProformaCertficate.html',
                      {'GDataProformaInSummary': views.GDataProformaInSummary, 'Exceptions': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response