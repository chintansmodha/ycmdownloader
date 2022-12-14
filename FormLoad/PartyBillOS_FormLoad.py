from django.shortcuts import render
from Global_Files import Connection_String as con

Exceptions = ''

GDataCompany = []
GDataParty = []
GDataBroker = []
GDataYear=[]




def PartyBillOSHtml(request):
    global GDataBroker
    global GDataCompany
    global GDataParty
    global GDataYear
    GDataParty=[]
    GDataBroker=[]
    GDataCompany=[]
    GDataYear=[]


    stmt = con.db.exec_immediate(con.conn, "Select Code,varchar_format(FROMDATE,'YYYY-MM-DD') as FROMDATE"
                                           ",varchar_format(TODATE,'YYYY-MM-DD') as TODATE from FinFinancialYear order by Code desc")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataYear:
            GDataYear.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from FINBUSINESSUNIT where groupflag=1 order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt2 = con.db.exec_immediate(con.conn,"select Numberid,legalname1  from businesspartner order by legalname1")
    result = con.db.fetch_both(stmt2)
    while result != False:
        if result not in GDataParty:
            GDataParty.append(result)
        result = con.db.fetch_both(stmt2)

    stmt3 = con.db.exec_immediate(con.conn,"SELECT code,longdescription FROM agent order by longdescription ")
    result = con.db.fetch_both(stmt3)
    while result != False:
        if result not in GDataBroker:
            GDataBroker.append(result)
        result = con.db.fetch_both(stmt3)

    return render(request, 'PartyBillOS.html',
                  {'GDataCompany': GDataCompany, 'GDataParty': GDataParty, 'GDataBroker': GDataBroker, 'GDataYear':GDataYear })

