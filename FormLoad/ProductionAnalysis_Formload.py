from django.shortcuts import render
from Global_Files import Connection_String as con

Exceptions = ''

GDataDepartment = []
GDataItem = []
GDataItemType = []
GDataProduction = []
GDataQuality = []
GDataShade = []
GDataMachine = []
GDataLot = []

stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select AbsUniqueId,LONGDESCRIPTION  from Product order by AbsUniqueId")
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

stmt = con.db.exec_immediate(con.conn,"Select CODE, ITEMTYPECODE, LONGDESCRIPTION From QUALITYLEVEL ORDER BY CODE ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataQuality:
        GDataQuality.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"SELECT CODE , LONGDESCRIPTION From USERGENERICGROUP Order by CODE ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataShade:
        GDataShade.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"SELECT DISTINCT (Cast( Code AS VARCHAR(4))) As Code FROM LOT order by Code ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataMachine:
        GDataMachine.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select code  from LOT order by Code")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataLot:
        GDataLot.append(result)
    result = con.db.fetch_both(stmt)


def ProductionAnalysisHtml(request):
    return render(request, 'ProductionAnalysis.html',
                  {'GDataDepartment': GDataDepartment,'GDataItem':GDataItem, 'GDataItemType': GDataItemType, 'GDataProduction': GDataProduction,
                   'GDataQuality': GDataQuality, 'GDataShade': GDataShade, 'GDataMachine': GDataMachine, 'GDataLot': GDataLot })

