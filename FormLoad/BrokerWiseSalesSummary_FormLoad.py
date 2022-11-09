from django.shortcuts import render
from Global_Files import Connection_String as con
import os.path
from django.views.static import serve


#FormLoad
GDataCompanyCode=[]
GDataParty=[]
GDataBrokerGroup=[]

def bwssfl(request):

    global GDataCompanyCode
    global GDataParty
    global GDataBrokerGroup

    GDataCompanyCode=[]
    GDataParty=[]
    GDataBrokerGroup=[]

    stmt = con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataParty:
            GDataParty.append(result)
            result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from PLANT order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompanyCode:
            GDataCompanyCode.append(result)
            result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from AGENTSGROUP order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataBrokerGroup:
            GDataBrokerGroup.append(result)
            result = con.db.fetch_both(stmt)


    return render(request,'BrokerWiseSalesSummary.html',{'GDataParty':GDataParty,
    'GDataCompanyCode':GDataCompanyCode,'GDataBrokerGroup':GDataBrokerGroup})


