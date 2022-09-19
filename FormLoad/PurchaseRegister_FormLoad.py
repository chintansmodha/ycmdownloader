from django.shortcuts import render
from Global_Files import Connection_String as con
GDataItemCode=[]
GDataCompanyCode=[]

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from ITEMTYPE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemCode:
        GDataItemCode.append(result)
    result = con.db.fetch_both(stmt)

stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from DIVISION order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataCompanyCode:
        GDataCompanyCode.append(result1)
    result1 = con.db.fetch_both(stmt1)

# Create your views here.
def home(request):
    return render(request,'index.html')

def PurchaseRegisterHtml(request):
    return render(request,'PurchaseRegister.html', {'GDataItemCode':GDataItemCode,'GDataCompanyCode':GDataCompanyCode})

