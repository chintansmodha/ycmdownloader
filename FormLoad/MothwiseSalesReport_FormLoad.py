from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataPrefix=[]

def MonthwiseSalesReport(request):
    stmt = con.db.exec_immediate(con.conn,"select code,longdescription from Plant order by Code")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select distinct InvoiceTypeCode from PlantInvoice order by InvoiceTypeCode")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataPrefix:
            GDataPrefix.append(result)
        result = con.db.fetch_both(stmt)

    return render(request,'MonthwiseSalesReport.html',{'GDataCompany':GDataCompany,'GDataPrefix':GDataPrefix})