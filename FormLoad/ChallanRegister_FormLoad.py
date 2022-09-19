# add query to display in ui
from django.shortcuts import render
from Global_Files import Connection_String as con
company=[]
party=[]
lot=[]
department=[]
agent=[]
winding=[]
shade=[]
quality=[]
# Create your views here.

stmt1 = con.db.exec_immediate(con.conn,"SELECT Longdescription,code FROM FINBUSINESSUNIT WHERE GroupFlag = 1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in company:
        company.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in party:
        party.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from lot")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in lot:
        lot.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from QUALITYLEVEL")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in quality:
        quality.append(result1)
    result1 = con.db.fetch_both(stmt1)

# stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from DEPARTMENT")
stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from COSTCENTER")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in department:
        department.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from AGENT")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in agent:
        agent.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from DEPARTMENT")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in winding:
        winding.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 =con.db.exec_immediate(con.conn,"SELECT USERGENERICGROUP.LONGDESCRIPTION FROM USERGENERICGROUP WHERE USERGENERICGROUPTYPECODE='P09'")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in shade:
        shade.append(result1)
    result1 = con.db.fetch_both(stmt1)

def home(request):
    return render(request, 'index.html')
def challanregisterhtml(request):
    return render(request,'ChallanRegister.html',{'company':company,'party':party,'lot':lot,'quality':quality,'department':department,'agent':agent,'winding':winding,'shade':shade})
