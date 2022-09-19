from Global_Files import Connection_String as con
from django.shortcuts import render
import datetime
GDataPalleteType=[]
GDataCompany=[]
GDataParty=[]
GDataItem=[]
LDStartDate=''
LDEndDate=''
stdate=''
etdate=''

stmt = con.db.exec_immediate(con.conn, "select code,longdescription from PLANT order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select NumberId,LEGALNAME1 from BUSINESSPARTNER order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from ITEMTYPE WHERE CODE='PKG' order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItem:
        GDataItem.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from UserGenericGroup WHERE UserGenericGroupTypeCode='PKG' order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataPalleteType:
        GDataPalleteType.append(result)
    result = con.db.fetch_both(stmt)

def PackingMaterialLedger(request):
    return render(request, 'PackingMaterialLedger.html', {'GDataCompany':GDataCompany,'GDataParty': GDataParty,'GDataItem':GDataItem,'GDataPalleteType':GDataPalleteType})