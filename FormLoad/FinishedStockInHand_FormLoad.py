from django.shortcuts import render
from Global_Files import Connection_String as con


GDataDepartment = []
GDataQuality = []
GDataWinding = []
GDataLot = []
GDataItem = []
GDataItemType = []
GDataItemTypeGroup = []


stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

stmt2 = con.db.exec_immediate(con.conn,"Select CODE, ITEMTYPECODE, LONGDESCRIPTION From QUALITYLEVEL ORDER BY CODE ")
result = con.db.fetch_both(stmt2)
while result != False:
    if result not in GDataQuality:
        GDataQuality.append(result)
    result = con.db.fetch_both(stmt2)

stmt3 = con.db.exec_immediate(con.conn,"Select CODE, LONGDESCRIPTION From USERGENERICGROUP Where USERGENERICGROUPTYPECODE = 'WND' ORDER BY CODE ")
result = con.db.fetch_both(stmt3)
while result != False:
    if result not in GDataWinding:
        GDataWinding.append(result)
    result = con.db.fetch_both(stmt3)

stmt4 = con.db.exec_immediate(con.conn,"select code  from LOT order by Code")
result = con.db.fetch_both(stmt4)
while result != False:
    if result not in GDataLot:
        GDataLot.append(result)
    result = con.db.fetch_both(stmt4)

stmt5 = con.db.exec_immediate(con.conn,"select AbsUniqueId, LONGDESCRIPTION from PRODUCT order by LONGDESCRIPTION ")
result = con.db.fetch_both(stmt5)
while result != False:
    if result not in GDataItem:
        GDataItem.append(result)
    result = con.db.fetch_both(stmt5)

stmt6 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from itemtype order by LONGDESCRIPTION ")
result = con.db.fetch_both(stmt6)
while result != False:
    if result not in GDataItemType:
        GDataItemType.append(result)
    result = con.db.fetch_both(stmt6)



def FinishedStockInHandHTML(request):
    return render(request, 'FinishedStockInHand.html', {'GDataDepartment':GDataDepartment, 'GDataQuality':GDataQuality, 'GDataWinding':GDataWinding,
                            'GDataLot':GDataLot, 'GDataItem':GDataItem, 'GDataItemType':GDataItemType, 'GDataItemTypeGroup':GDataItemTypeGroup})

def FinishedStockInHandAgeingHTML(request):
    return render(request, 'FinishedStockInHandAgeing.html', {'GDataDepartment':GDataDepartment, 'GDataQuality':GDataQuality, 'GDataWinding':GDataWinding,
                            'GDataLot':GDataLot, 'GDataItem':GDataItem, 'GDataItemType':GDataItemType, 'GDataItemTypeGroup':GDataItemTypeGroup})
