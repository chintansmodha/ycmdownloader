import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from ProcessSelection import PrintPalleteGatePass_ProcessSelection as PPGP
LDStartDate=''
LDEndDate=''
stdate=''
etdate=''
GDataCompany=[]
GDataParty=[]

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from Finbusinessunit where GROUPFLAG=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select NumberId,LEGALNAME1 from BUSINESSPARTNER order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

def home(request):
    return render(request,'index.html')

def PrintPalleteGatePassHtml(request):
    return render(request, 'PrintPalleteGatePass.html', {'GDataCompany': GDataCompany,'GDataParty':GDataParty})

def PrintPalleteGatePassTableHtml(request):
    global LDStartDate
    global LDEndDate
    global stdate
    global etdate
    LSCompany =  request.GET.getlist('dept')
    LSParty = request.GET.getlist('party')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    stdate = datetime.datetime.strptime(LDStartDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    etdate = datetime.datetime.strptime(LDEndDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    LSTemplateType=int(request.GET['temp'])
    a = PPGP.PrintPalleteGatePass_PrintPDF(LSCompany,LSParty,LDStartDate,LDEndDate,LSTemplateType,request)
    return a
