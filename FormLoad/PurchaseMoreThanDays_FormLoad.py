from django.shortcuts import render
from Global_Files import Connection_String as con
GDataItemCode=[]
GDataCompanyCode=[]
GDataQuality=[]
GDataProductionItemGroup=[]

def PurchaseMoreThanDaysHtml(request):
    global GDataItemCode
    global GDataQuality
    global GDataCompanyCode
    global GDataProductionItemGroup
    GDataQuality=[]
    GDataCompanyCode=[]
    GDataItemCode=[]
    GDataProductionItemGroup=[]
    stmt = con.db.exec_immediate(con.conn,"select ABSUNIQUEID, LONGDESCRIPTION from Product order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataItemCode:
            GDataItemCode.append(result)
        result = con.db.fetch_both(stmt)

    stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from Finbusinessunit order by LONGDESCRIPTION")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataCompanyCode:
            GDataCompanyCode.append(result1)
        result1 = con.db.fetch_both(stmt1)

    stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from QualityLevel order by LONGDESCRIPTION")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataQuality:
            GDataQuality.append(result1)
        result1 = con.db.fetch_both(stmt1)

    stmt1 = con.db.exec_immediate(con.conn,"select NUMBERID, legalname1 from Businesspartner order by legalname1")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataProductionItemGroup:
            GDataProductionItemGroup.append(result1)
        result1 = con.db.fetch_both(stmt1)
    return render(request,'PurchaseMoreThanDays.html', {'GDataItemCode':GDataItemCode,'GDataCompanyCode':GDataCompanyCode,'GDataQuality':GDataQuality,"GDataProductionItemGroup":GDataProductionItemGroup})
