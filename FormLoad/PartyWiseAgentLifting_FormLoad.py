from Global_Files import Connection_String as con
from django.shortcuts import render

GDataCompany = []
GDataParty = []
GDataYarnType = []
GDataSalesTax = []

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

stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from ITEMTYPE Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataYarnType:
        GDataYarnType.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE From ITax order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataSalesTax:
        GDataSalesTax.append(result)
    result = con.db.fetch_both(stmt)

def PartyWiseAgentLiftingFormLoad(request):
    return render(request,"PartyWiseAgentLifting.html",{'GDataCompany':GDataCompany,'GDataParty':GDataParty , 'GDataYarnType':GDataYarnType, 'GDataSalesTax' : GDataSalesTax })
