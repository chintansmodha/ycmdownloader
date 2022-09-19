from Global_Files import Connection_String as con
from django.shortcuts import render

GDataItemCode = []
GDataCompanyCode = []

stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from finbusinessunit where groupflag=0")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemCode:
        GDataItemCode.append(result)
    result = con.db.fetch_both(stmt)

stmt1 = con.db.exec_immediate(con.conn, "select CODE,Longdescription from glmaster ")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataCompanyCode:
        GDataCompanyCode.append(result1)
    result1 = con.db.fetch_both(stmt1)

def home(request):
    return render(request,'index.html')

def BankCashStatementHtml(request):
    return render(request, 'BankCashStatement.html', {'GDataItemCode': GDataItemCode, 'GDataCompanyCode': GDataCompanyCode})

