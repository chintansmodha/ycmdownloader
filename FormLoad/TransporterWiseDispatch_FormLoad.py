from django.shortcuts import render
from Global_Files import Connection_String as con


GDataCompany = []
GDataBranch = []
GDataTransporter = []
GDataDispatch = []
GDataParty = []

stmt = con.db.exec_immediate(con.conn, "select CODE,LONGDESCRIPTION from Plant Order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

sql= " Select BP_Trpt.numberid, BP_Trpt.legalname1 as TransporterName from plantinvoice " \
     " Left join OrderPartner OP_Trpt    On      PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE" \
     "                                   And     PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE " \
     " Left join BusinessPartner BP_Trpt  On     OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID" \
     " group by BP_Trpt.numberid,BP_Trpt.legalname1 " \
        "Order by BP_Trpt.legalname1"
stmt = con.db.exec_immediate(con.conn, sql)
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataTransporter:
        GDataTransporter.append(result)
    result = con.db.fetch_both(stmt)

sql=(" Select Distinct TZ.Code, TZ.Longdescription "
" from Plantinvoice PI "
" Join OrderPartner OP    ON PI.CONSIGNEECUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode"
"                        And PI.CONSIGNEECUSTOMERSUPPLIERTYPE = OP.CustomerSupplierType"
" Join BusinessPartner BP ON OP.OrderbusinessPartnerNumberId = BP.NumberID"
" Join TransportZone TZ   ON BP.TRANSPORTZONECODE = TZ.CODE")
stmt = con.db.exec_immediate(con.conn,sql)
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDispatch:
        GDataDispatch.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select NUMBERID,LEGALNAME1  from BUSINESSPARTNER order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

def TWDFL(request):
    return render(request,"TransporterWiseDispatch.html",{'GDataCompany':GDataCompany,'GDataBranch':GDataBranch,'GDataDispatch':GDataDispatch,'GDataTransporter':GDataTransporter,'GDataParty':GDataParty})