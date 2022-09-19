from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from Global_Files import Connection_String as con
import Global_Files
unit=[]
costcenter=[]
supplier=[]
itemtype=[]
code=[]
ccode=[]
plant=[]
department=[]



stmt1 = con.db.exec_immediate(con.conn,"Select BusinessPartner.LegalName1 LONGDESCRIPTION ,OrderPartner.CUSTOMERSUPPLIERCODE CODE "
                                       "FROM ORDERPARTNER  Inner Join BusinessPartner   "
                                       "ON BusinessPartner.NumberId = OrderPartner.OrderBusinessPartnerNumberId "
                                       "WHERE OrderPartner.CUSTOMERSUPPLIERTYPE = 1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in supplier:
        supplier.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from itemtype order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in itemtype:
        itemtype.append(result1)
    result1 = con.db.fetch_both(stmt1)



stmt1 = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from plant order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in plant:
        plant.append(result1)
    result1 = con.db.fetch_both(stmt1)

# Create your views here.

def StoreUnBilled_GRNRegisterHtml(request):
    return render(request,'Store_UnBilled_GRN.html', {'plant': plant, 'costcenter': costcenter,'supplier': supplier,'itemtype': itemtype,'code':code,'ccode':ccode})


# Create your views here.
