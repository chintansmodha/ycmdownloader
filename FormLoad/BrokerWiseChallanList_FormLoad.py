# add query to display in ui
from django.shortcuts import render
from Global_Files import Connection_String as con
company=[]
party=[]
state=[]
itemtype=[]
shade=[]
broker=[]
# Create your views here.

# for Company
stmt1 = con.db.exec_immediate(con.conn,"SELECT Longdescription,code FROM FINBUSINESSUNIT WHERE GroupFlag = 1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in company:
        company.append(result1)
    result1 = con.db.fetch_both(stmt1)

# for party
stmt1 =con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in party:
        party.append(result1)
    result1 = con.db.fetch_both(stmt1)

# for state
stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from state")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in state:
        state.append(result1)
    result1 = con.db.fetch_both(stmt1)

# for itemtype
stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from itemtype")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in itemtype:
        itemtype.append(result1)
    result1 = con.db.fetch_both(stmt1)

# for BrokerGroup
stmt1 =con.db.exec_immediate(con.conn,"select  Longdescription,code from AGENTSGROUP")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in broker:
        broker.append(result1)
    result1 = con.db.fetch_both(stmt1)

# for shade
stmt1 =con.db.exec_immediate(con.conn,"SELECT USERGENERICGROUP.LONGDESCRIPTION FROM USERGENERICGROUP WHERE USERGENERICGROUPTYPECODE='P09'")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in shade:
        shade.append(result1)
    result1 = con.db.fetch_both(stmt1)


def BrokerWiseChallanListHtml(request):
    return render(request,'BrokerwiseChallanList.html',{'company':company,'party':party,'state':state,'itemtype':itemtype,'shade':shade,'broker':broker})
