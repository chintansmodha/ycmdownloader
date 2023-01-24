from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataAccount=[]

def TCSReportHtml(request):
    global GDataCompany
    global GDataAccount
    GDataCompany=[]
    GDataAccount=[]
    
    stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from FINBUSINESSUNIT order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from GLMASTER order by LONGDESCRIPTION")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataAccount:
            GDataAccount.append(result1)
        result1 = con.db.fetch_both(stmt1)

    return render(request,'TCSReport.html', {'GDataCompany':GDataCompany,'GDataAccount':GDataAccount})