from django.shortcuts import render
from Global_Files import Connection_String as con
GDataLotNo=[]
GDataResource=[]

stmt = con.db.exec_immediate(con.conn, "select Unique(LOT.Code) As Code From LOT, RESOURCES "
                                       "Where RESOURCES.CODE in (Left(LOT.CODE,4),  Left(LOT.CODE,3)) "
                                       "Order By Code")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataLotNo:
        GDataLotNo.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION from RESOURCES order by CODE,LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataResource:
        GDataResource.append(result)
    result = con.db.fetch_both(stmt)

def LotNoListingHtml(request):
    return render(request,'LotNoListing.html',{'GDataLotNo':GDataLotNo,'GDataResource':GDataResource})