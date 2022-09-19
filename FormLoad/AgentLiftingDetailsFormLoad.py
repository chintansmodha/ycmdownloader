from django.shortcuts import render
from Global_Files import Connection_String as con


GDataBrokerGroup = []
GDataBroker = []
GDataPlant = []
GDataParty = []
GDataItem = []
GDataItemType = []
GDataItemQuality = []


stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION  from AGENTSGROUP order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBrokerGroup:
        GDataBrokerGroup.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION  from AGENT order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBroker:
        GDataBroker.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION  from PLANT order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataPlant:
        GDataPlant.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select NUMBERID,LEGALNAME1  from BUSINESSPARTNER order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select AbsUniqueId, LONGDESCRIPTION from PRODUCT order by LONGDESCRIPTION ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItem:
        GDataItem.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from itemtype order by LONGDESCRIPTION ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemType:
        GDataItemType.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from QUALITYLEVEL order by LONGDESCRIPTION ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemQuality:
        GDataItemQuality.append(result)
    result = con.db.fetch_both(stmt)


def AgentLiftingHTML(request):
    return render(request, 'AgentLiftingDetails.html',{'GDataBrokerGroup':GDataBrokerGroup  , 'GDataBroker':GDataBroker ,
                                                       'GDataPlant':GDataPlant  , 'GDataParty':GDataParty  , 'GDataItem':GDataItem  ,
                                                       'GDataItemType':GDataItemType  , 'GDataItemQuality':GDataItemQuality })
