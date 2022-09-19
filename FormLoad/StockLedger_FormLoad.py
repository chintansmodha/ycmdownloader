from django.shortcuts import render
from Global_Files import Connection_String as con
GDataItemCode=[]
GDataCompanyCode=[]
GDataQuality=[]
GDataProductionItemGroup=[]

def StockLedgerHtml(request):
    global GDataItemCode
    global GDataQuality
    global GDataCompanyCode
    GDataQuality=[]
    GDataCompanyCode=[]
    GDataItemCode=[]
    stmt = con.db.exec_immediate(con.conn,"select ABSUNIQUEID, LONGDESCRIPTION from Product order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataItemCode:
            GDataItemCode.append(result)
        result = con.db.fetch_both(stmt)

    stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from Plant order by LONGDESCRIPTION")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataCompanyCode:
            GDataCompanyCode.append(result1)
        result1 = con.db.fetch_both(stmt1)

    stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from ItemType order by LONGDESCRIPTION")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataQuality:
            GDataQuality.append(result1)
        result1 = con.db.fetch_both(stmt1)
    return render(request,'StockLedger.html', {'GDataItemCode':GDataItemCode,'GDataCompanyCode':GDataCompanyCode,'GDataQuality':GDataQuality})
