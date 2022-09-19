from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataBroker=[]
GDataBrokerGroup=[]

def BrokerGroupCompanyWiseOShtml(request):
    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION from AGENT order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataBroker:
            GDataBroker.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION from AGENTSGROUP order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataBrokerGroup:
            GDataBrokerGroup.append(result)
        result = con.db.fetch_both(stmt)

    return render(request,'BrokerGroupCompanyWiseOS.html',{'GDataCompany':GDataCompany,'GDataBroker':GDataBroker,'GDataBrokerGroup':GDataBrokerGroup})