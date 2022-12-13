from django.shortcuts import render
from Global_Files import Connection_String as con

GDataCompany = []
GDataBranch = []
GDataParty = []


stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from finbusinessunit where groupflag=0 Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE,SHORTDESCRIPTION from FINBUSINESSUNIT Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBranch:
        GDataBranch.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select NUMBERID,LEGALNAME1 from BUSINESSPARTNER Order by NUMBERID")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

def PartyBillOSAsOnLedgerFormLoad(request):
    return render(request,"PartyBillOSAsOnLedger.html",{'GDataParty':GDataParty,'GDataBranch':GDataBranch,'GDataCompany':GDataCompany})

