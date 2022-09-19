from ProcessSelection import IndentRequisition_ProcessSelection as INRQPS
from Global_Files import Connection_String as con
from django.shortcuts import render
import datetime
LDStartDate=''
LDEndDate=''
stdate=''
etdate=''
GDataCompany=[]

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

def home(request):
    return render(request,'index.html')

def IndentRequisitionHtml(request):
    return render(request, 'IndentRequisition.html',{'GDataCompany':GDataCompany})

def IndentRequisitionTableHtml(request):
    global LDStartDate
    global LDEndDate
    global stdate
    global etdate
    LSCompany = request.GET.getlist('dept')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    stdate = datetime.datetime.strptime(LDStartDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    etdate = datetime.datetime.strptime(LDEndDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    a = INRQPS.IndentRequisition_PrintPDF(LSCompany,LDStartDate,LDEndDate,request)
    return a