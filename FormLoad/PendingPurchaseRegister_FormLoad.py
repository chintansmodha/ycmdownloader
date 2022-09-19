from django.shortcuts import render
from Global_Files import Connection_String as con
company=[]
party=[]

stmt1 = con.db.exec_immediate(con.conn,"Select * from Division  order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in company:
        company.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 = con.db.exec_immediate(con.conn,"Select BusinessPartner.LegalName1 LONGDESCRIPTION ,OrderPartner.CUSTOMERSUPPLIERCODE    "
                                       "FROM ORDERPARTNER  "
                                       "Inner Join BusinessPartner  "
                                       "ON BusinessPartner.NumberId = OrderPartner.OrderBusinessPartnerNumberId  "
                                       "WHERE OrderPartner.CUSTOMERSUPPLIERTYPE = 2 "
                                       "Order By LONGDESCRIPTION")

result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in party:
        party.append(result1)
    result1 = con.db.fetch_both(stmt1)

def PendingPurchaseRegisterHtml(request):
    return render(request,'PendingPurchaseRegister.html', {'company': company,'party': party})