from django.shortcuts import render

from Global_Files import Connection_String as con
import Global_Files
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

def SalesRegisterHtml(request):
    return render(request,'SalesRegister.html', {'unit': unit, 'costcenter': costcenter,'party': party,'itemtype': itemtype,'code':code,'ccode':ccode})


# Create your views here.
