from django.shortcuts import render
from Global_Files import Connection_String as con


GDataBroker = []
GDataParty = []
GDataItem = []
GDataItemType = []
GDataShade = []


stmt = con.db.exec_immediate(con.conn,"select NUMBERID,LEGALNAME1  from BUSINESSPARTNER order by NUMBERID")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION  from AGENT order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBroker:
        GDataBroker.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select AbsUniqueId, LONGDESCRIPTION from PRODUCT order by AbsUniqueId ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItem:
        GDataItem.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from itemtype order by CODE ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemType:
        GDataItemType.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from USERGENERICGROUP order by CODE ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataShade:
        GDataShade.append(result)
    result = con.db.fetch_both(stmt)


def ContractProgressHTML(request):
    return render(request, 'ContractProgress.html', {'GDataParty':GDataParty,  'GDataBroker':GDataBroker,
                                                     'GDataItem':GDataItem, 'GDataItemType':GDataItemType, 'GDataShade':GDataShade})
