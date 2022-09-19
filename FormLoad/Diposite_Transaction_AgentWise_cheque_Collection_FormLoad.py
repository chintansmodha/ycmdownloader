from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataBroker=[]
GDataBrokerGroup=[]

stmt = con.db.exec_immediate(con.conn, "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)



stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from AGENTSGROUP order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataBrokerGroup:
        GDataBrokerGroup.append(result1)
    result1 = con.db.fetch_both(stmt1)


def home(request):
    return render(request,'index.html')

def DepositsTransactionAgentWiseChequeCollection(request):
    return render(request,'Diposits_Transaction_AgentWise_Cheque_Register.html',{'GDataCompany':GDataCompany,'GDataBrokerGroup':GDataBrokerGroup})