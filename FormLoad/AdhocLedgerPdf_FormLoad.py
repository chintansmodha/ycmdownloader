from django.shortcuts import render
from Global_Files import Connection_String as con

GDataCompany=[]
GDataAccount=[]
GDataSubAccount=[]


stmt = con.db.exec_immediate(con.conn,"select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select code,longdescription from glmaster order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataAccount:
        GDataAccount.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select numberid,legalname1 from businesspartner order by legalname1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataSubAccount:
        GDataSubAccount.append(result)
    result = con.db.fetch_both(stmt)

# Create your views here.
def home(request):
    return render(request,'index.html')

def AdhocLedgerHtml(request):
    return render(request,'AdhocLedgerPDF.html',{'GDataCompany':GDataCompany,'GDataAccount':GDataAccount,'GDataSubAccount':GDataSubAccount})
