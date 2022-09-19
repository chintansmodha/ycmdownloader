from django.shortcuts import render
from Global_Files import Connection_String as con
GDataBank=[]
GDataBroker=[]

stmt = con.db.exec_immediate(con.conn, "select code,longdescription from GLMaster where BankCashFlag In (0,1) order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataBank:
        GDataBank.append(result)
    result = con.db.fetch_both(stmt)


def home(request):
    return render(request,'index.html')

def DepositsTransactionBankCompanyCollection(request):
    return render(request,'Diposits_Transaction_Bank_Company_Collection.html',{'GDataBank':GDataBank})