from django.shortcuts import render

from Global_Files import Connection_String as con
import Global_Files
from ProcessSelection import StoreRegister_ProcessSelection  as SRR
unit=[]
costcenter=[]
party=[]
itemtype=[]
code=[]
ccode=[]

# stmt1 = con.db.exec_immediate(con.conn,"SELECT * FROM FINBUSINESSUNIT WHERE GroupFlag = 0")
stmt1 = con.db.exec_immediate(con.conn,"SELECT * FROM plant")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in unit:
        unit.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 = con.db.exec_immediate(con.conn,"SELECT LONGDESCRIPTION,CODE from COSTCENTER  order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in costcenter:
        costcenter.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in party:
        party.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from itemtype order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in code:
        code.append(result1)
    result1 = con.db.fetch_both(stmt1)


# Create your views here.
def home(request):
    return render(request, 'index.html')

def StoreRegisterHtml(request):
    return render(request,'StoreRegister.html', {'unit': unit, 'costcenter': costcenter,'party': party,'itemtype': itemtype,'code':code,'ccode':ccode})
    # global LDStartDate
    # global LDEndDate
    # LSCompany = request.GET.getlist('comp')
    # LSParty = request.GET.getlist('party')
    # LDStartDate = str(request.GET['startdate'])
    # LDEndDate = str(request.GET['enddate'])
    # LSReportType = int(request.GET['reporttype'])
    # a = SRR.StoreRegister(LSCompany, LSParty, LDStartDate, LDEndDate, LSReportType,request)
    # return a

# Create your views here.
