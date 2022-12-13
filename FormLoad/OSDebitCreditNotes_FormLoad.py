from django.shortcuts import render
from Global_Files import Connection_String as con

GDataCompany = []
GDataParty = []
GDataBroker = []

stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION  from PLANT order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select NUMBERID,LEGALNAME1 from BUSINESSPARTNER Order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)
stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from AGENT Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBroker:
        GDataBroker.append(result)
    result = con.db.fetch_both(stmt)

def OSDebitCreditNotesFromLoad(request):
    return render(request,"OSDebitCreditNotes.html",{'GDataCompany':GDataCompany,'GDataParty':GDataParty,'GDataBroker':GDataBroker})

