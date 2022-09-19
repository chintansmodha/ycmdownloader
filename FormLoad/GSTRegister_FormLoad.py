from django.shortcuts import render
from Global_Files import Connection_String as con
GDataParty=[]
GDataCompanyCode=[]

stmt = con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from PLANT order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataCompanyCode:
        GDataCompanyCode.append(result1)
    result1 = con.db.fetch_both(stmt1)

def GSTRegisterHtml(request):
    return render(request,'GSTRegister.html', {'GDataParty':GDataParty,'GDataCompanyCode':GDataCompanyCode})




# Create your views here.
