from Global_Files import Connection_String as con
from django.shortcuts import render

GDataCompany = []
GDataBranch = []
GDataBrokerGroup = []
GDataBroker = []
GDataParty = []
GDataYarnType = []

stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from finbusinessunit where groupflag=0 Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE,SHORTDESCRIPTION from FINBUSINESSUNIT where groupflag=0 Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBranch:
        GDataBranch.append(result)
    result = con.db.fetch_both(stmt)


stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from AGENTSGROUP Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBrokerGroup:
        GDataBrokerGroup.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from AGENT Order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBroker:
        GDataBroker.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select NUMBERID,LEGALNAME1 from BUSINESSPARTNER Order by NUMBERID")
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


def BrokerWiseRD(request):
    return render(request, 'BrokerWiseRD.html', {'GDataCompany':GDataCompany , 'GDataBranch':GDataBranch , 'GDataBrokerGroup':GDataBrokerGroup
                                                , 'GDataBroker':GDataBroker , 'GDataParty':GDataParty , 'GDataYarnType':GDataYarnType })