from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataParty=[]
GDataTransporter=[]
stmt = con.db.exec_immediate(con.conn, "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION from AGENT order by CODE,LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)
sql="select BP_Trpt.legalname1 as TransporterName from plantinvoice " \
    "Left join OrderPartner OP_Trpt    On      PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE" \
    "                                   And     PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE " \
    " Left join BusinessPartner BP_Trpt  On     OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID " \
    " group by BP_Trpt.legalname1 "


stmt = con.db.exec_immediate(con.conn, sql)
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataTransporter:
        GDataTransporter.append(result)
    result = con.db.fetch_both(stmt)
#
def home(request):
    return render(request,'index.html')

def ChallanRegisterCustomer(request):
    print("from fomr load")
    return render(request,'Challan_Register_Customer.html',{'GDataCompany':GDataCompany,'GDataParty':GDataParty,"GDataTransporter":GDataTransporter})