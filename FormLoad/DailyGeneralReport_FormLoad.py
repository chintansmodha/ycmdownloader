from django.shortcuts import render
from Global_Files import Connection_String as con
GDataDepartment=[]
GDataItemCode=[]
def DailyGeneralReport(request):
    global GDataDepartment
    GDataDepartment=[]
    global GDataItemCode
    GDataItemCode=[]

    stmt = con.db.exec_immediate(con.conn, "select CODE, LONGDESCRIPTION from ITEMTYPE order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataItemCode:
            GDataItemCode.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select CODE,LONGDESCRIPTION from Plant order by CODE")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataDepartment:
            GDataDepartment.append(result)
        result = con.db.fetch_both(stmt)


    return render(request,"DailyGeneralReport.html",{"GDataDepartment":GDataDepartment,"GDataItemCode":GDataItemCode})