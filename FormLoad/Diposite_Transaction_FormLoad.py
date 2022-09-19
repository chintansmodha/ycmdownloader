from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataBroker=[]

stmt = con.db.exec_immediate(con.conn, "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION from AGENT order by CODE,LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBroker:
        GDataBroker.append(result)
    result = con.db.fetch_both(stmt)

def home(request):
    return render(request,'index.html')

def DepositsTransaction(request):
    return render(request,'Diposits_Transaction.html',{'GDataCompany':GDataCompany,'GDataBroker':GDataBroker})