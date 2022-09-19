from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataBroker=[]
GDataParty=[]

def BrokerWiseOrderOS(request):
    global GDataCompany
    global GDataParty
    global GDataBroker
    GDataBroker=[]
    GDataParty=[]
    GDataCompany=[]

    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select numberid,legalname1 from businesspartner order by legalname1")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataParty:
            GDataParty.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from agent order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataBroker:
            GDataBroker.append(result)
        result = con.db.fetch_both(stmt)

    return render(request,'BrokerWiseOrderOS.html',{"GDataCompany":GDataCompany,"GDataParty":GDataParty,"GDataBroker":GDataBroker})
