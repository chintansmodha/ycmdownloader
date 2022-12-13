from Global_Files import Connection_String as con
from django.shortcuts import render

GDataCompany = []
GDataParty = []


stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from finbusinessunit where groupflag=0 Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)


stmt = con.db.exec_immediate(con.conn, "select NUMBERID,LEGALNAME1 from BUSINESSPARTNER Order by NUMBERID")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

def PartyWiseBookDebitsFormLoad(request):
    return render(request,"PartyWiseBookDebits.html",{'GDataCompany':GDataCompany,'GDataParty':GDataParty})

