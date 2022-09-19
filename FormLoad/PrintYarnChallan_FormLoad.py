from django.shortcuts import render
from Global_Files import Connection_String as con
from ProcessSelection import PrintYarnChallan_ProcessSelection as PYCPD
import datetime
# Create your views here.
GDataCompany=[]
GDataParty=[]
GTransportZone=[]
stdate=''
etdate=''
LDStartDate = ''
LDEndDate = ''

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from Finbusinessunit where GROUPFLAG=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select NUMBERID,LEGALNAME1 from BUSINESSPARTNER order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from TRANSPORTZONE order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GTransportZone:
        GTransportZone.append(result)
    result = con.db.fetch_both(stmt)

def home(request):
    return render(request,'index.html')

def PrintChallanHtml(request):
    return render(request, 'PrintChallan.html',{'GDataCompany':GDataCompany,'GDataParty':GDataParty,'GTransportZone':GTransportZone})

def PrintChallanTableHtml(request):
    global LDStartDate
    global LDEndDate
    LSCompany = request.GET.getlist('comp')
    LSParty = request.GET.getlist('party')
    LSDespatch = request.GET.getlist('desp')
    LDStartDate = str(request.GET['startdate'])
    stdate = datetime.datetime.strptime(LDStartDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    print(LDStartDate)
    print(stdate)
    LDEndDate = str(request.GET['enddate'])
    etdate = datetime.datetime.strptime(LDEndDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    print(LDEndDate)
    print(etdate)
    LSReportType = int(request.GET['reporttype'])
    a = PYCPD.PrintChallan_PrintPDF(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType, request)
    # a = PYCPD.PrintChallan_PrintPDF(LSCompany, LSParty, LDStartDate, LDEndDate, LSReportType,request)

    return a

