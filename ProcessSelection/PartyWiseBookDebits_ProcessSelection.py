from FormLoad import PartyWiseBookDebits_FormLoad as views
from datetime import datetime
import os.path
from django.http import FileResponse
from django.shortcuts import render
from GetDataFromDB import PartyWiseBookDebits_GetDataFromDB
from PrintPDF import PartyWiseBookDebits_PrintPDF as pdfrpt1
from PrintPDF import PartyBillOS_PrintPDF2 as pdfrpt2
Exceptions=""
save_name=""
LSFileName=""
def PartyWiseBookDebits(request):
    global LSFileName
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "Party Bill OS" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),LSFileName)

    LDDate=request.GET['enddate']
    LSUpadated= request.GET['updated']
    LSCompany=request.GET.getlist('company')
    LSAllCompany=request.GET.getlist('allcompany')
    LSParty=request.GET.getlist('Party')
    LSAllParty=request.GET.getlist('allParty')
    LS1=request.GET['1']
    LS2=request.GET['2']
    LS3=request.GET['3']
    print(type(LSUpadated),LSUpadated)
    if LSUpadated=='Yes':
        pdfrpt1.c=pdfrpt1.canvas.Canvas(save_name + ".pdf")
        PartyWiseBookDebits_GetDataFromDB.PartyWiseBookDebits_GetData(LSCompany,LSAllCompany,LSParty,LSAllParty,LDDate,LS1,LS2,LS3)

    elif LSUpadated=='2':
        pass


    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request,"PartyWiseBookDebits.html",{'GDataCompany':views.GDataCompany,'GDataParty':views.GDataParty})
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response