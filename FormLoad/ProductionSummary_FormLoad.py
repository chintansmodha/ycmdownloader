from django.shortcuts import render
from Global_Files import Connection_String as con

Exceptions = ''

GDataDepartment = []
GDataProduction = []
GDataLot = []
GDataItem = []

stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

stmt2 = con.db.exec_immediate(con.conn,"select code  from LOT order by Code")
result = con.db.fetch_both(stmt2)
while result != False:
    if result not in GDataLot:
        GDataLot.append(result)
    result = con.db.fetch_both(stmt2)

stmt3 = con.db.exec_immediate(con.conn,"select AbsUniqueId, LONGDESCRIPTION from PRODUCT order by LONGDESCRIPTION ")
result = con.db.fetch_both(stmt3)
while result != False:
    if result not in GDataItem:
        GDataItem.append(result)
    result = con.db.fetch_both(stmt3)


def ProductionSummaryHtml(request):
    return render(request, 'ProductionSummary.html',
                  {'GDataDepartment': GDataDepartment, 'GDataProduction': GDataProduction, 'GDataLot': GDataLot, 'GDataItem': GDataItem })

