from django.shortcuts import render
from Global_Files import Connection_String as con

GDataCompany=[]
GDataAccount=[]
GDataSubAccount=[]
GDataYear=[]
def AdhocLedgerU(request):
    global GDataYear
    global GDataAccount
    global GDataCompany
    global GDataSubAccount

    stmt = con.db.exec_immediate(con.conn, "Select Code,varchar_format(FROMDATE,'YYYY-MM-DD') as FROMDATE"
                                           ",varchar_format(TODATE,'YYYY-MM-DD') as TODATE from FinFinancialYear order by Code desc")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataYear:
            GDataYear.append(result)
        result = con.db.fetch_both(stmt)
    print(GDataYear)

    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select code,longdescription from glmaster order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataSubAccount:
            GDataSubAccount.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select numberid,legalname1 from businesspartner order by legalname1")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataAccount:
            GDataAccount.append(result)
        result = con.db.fetch_both(stmt)

    return render(request,'AdhocLedgerU.html',{'GDataCompany':GDataCompany,'GDataAccount':GDataAccount,'GDataSubAccount':GDataSubAccount,"GDataYear":GDataYear})
