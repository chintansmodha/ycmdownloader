from django.shortcuts import render
from Global_Files import Connection_String as con

GDataDepartment=[]
GDataIssue2Department=[]
GDataSupplier=[]

stmt = con.db.exec_immediate(con.conn,"select code,longdescription from LOGICALWAREHOUSE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select code,longdescription from LOGICALWAREHOUSE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataIssue2Department:
        GDataIssue2Department.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select numberid,legalname1 from businesspartner order by legalname1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataSupplier:
        GDataSupplier.append(result)
    result = con.db.fetch_both(stmt)

# Create your views here.
def home(request):
    return render(request,'index.html')

def YarnIssueRegisterHtml(request):
    return render(request, 'YarnIssueRegister.html',
                  {'GDataDepartment': GDataDepartment, 'GDataIssue2Department': GDataIssue2Department,
                   'GDataSupplier': GDataSupplier})
