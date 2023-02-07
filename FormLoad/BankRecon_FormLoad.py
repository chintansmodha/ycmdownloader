from Global_Files import Connection_String as con
from django.shortcuts import render

GDataBank=[]
GDataCompany=[]
def BankReconFormLoad(request):
    global GDataBank
    global GDataCompany
    GDataCompany=[]
    GDataBank=[]
    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from GLMASTER order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataBank:
            GDataBank.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from FINBUSINESSUNIT order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)
        
    return render(request,"BankRecon.html",{'GDataCompany':GDataCompany,'GDataBank':GDataBank})