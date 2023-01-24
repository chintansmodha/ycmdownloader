from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]

def TDSReportHtml(request):
    global GDataCompany
    global GDataAccount
    GDataCompany=[]

    
    stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from FINBUSINESSUNIT order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    return render(request,'TDSReport.html', {'GDataCompany':GDataCompany})