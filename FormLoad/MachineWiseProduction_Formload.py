from django.shortcuts import render
from Global_Files import Connection_String as con

GDataDepartment=[]


stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

# Create your views here.

def MachineWiseProductionHtml(request):
    return render(request,'MachineWiseProduction.html',{'GDataDepartment':GDataDepartment})
