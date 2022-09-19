from django.shortcuts import render
from Global_Files import Connection_String as con

GDataCompany=[]

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from Finbusinessunit where GROUPFLAG=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

def home(request):
    return render(request,'index.html')

def SummerizedBankBalanceHtml(request):
    return render(request,'SummerizedBankBalance.html',{'GDataCompany':GDataCompany})
