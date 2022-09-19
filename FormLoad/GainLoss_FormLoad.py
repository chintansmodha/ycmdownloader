from django.shortcuts import render
from Global_Files import Connection_String as con

GDataDepartment=[]
GDataYear=[]
year = 0
stmt = con.db.exec_immediate(con.conn, "Select Code,varchar_format(FROMDATE,'YYYY-MM-DD') as FROMDATE"
                                           ",varchar_format(TODATE,'YYYY-MM-DD') as TODATE from FinFinancialYear order by FROMDATE Desc")
result = con.db.fetch_both(stmt)
#YearBeginingDate = result!FROMDATE
while result != False:
    if result not in GDataYear:
        if year == 0:
            year = int(result['CODE'])
        GDataYear.append(result)
    result = con.db.fetch_both(stmt)


stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

# Create your views here.

def GainLossHtml(request):
    return render(request,'GainLossReport.html',{'GDataDepartment':GDataDepartment,"GDataYear":GDataYear, 'YEAR':year})
