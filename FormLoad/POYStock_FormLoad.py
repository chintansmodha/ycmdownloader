from django.shortcuts import render
from Global_Files import Connection_String as con
GDataDepartment=[]
GDataItemCode=[]
GDataYear=[]
def POYStock(request):
    global GDataDepartment
    GDataDepartment=[]
    global GDataItemCode
    GDataItemCode=[]
    global GDataYear
    GDataYear=[]

    stmt = con.db.exec_immediate(con.conn, "select CODE, LONGDESCRIPTION from ITEMTYPE order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataItemCode:
            GDataItemCode.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select CODE,LONGDESCRIPTION from Logicalwarehouse order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataDepartment:
            GDataDepartment.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                     "select CODE,LONGDESCRIPTION from finfinancialyear order by code")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataYear:
            print(result)
            GDataYear.append(result)
        result = con.db.fetch_both(stmt)


    return render(request,"POY_Stock.html",{"GDataDepartment":GDataDepartment,"GDataItemCode":GDataItemCode,'GDataYear':GDataYear})