from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from Global_Files import Connection_String as con
import Global_Files
company=[]
party=[]

stmt1 = con.db.exec_immediate(con.conn,"SELECT Longdescription,code FROM FINBUSINESSUNIT WHERE GroupFlag = 1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in company:
        company.append(result1)
    result1 = con.db.fetch_both(stmt1)

result1=''
stmt1 =con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in party:
        party.append(result1)
    result1 = con.db.fetch_both(stmt1)

# Create your views here.

def Export_InvoiceHtml(request):
    return render(request,'Export_Invoice.html', {'company': company, 'party': party})


# Create your views here.
