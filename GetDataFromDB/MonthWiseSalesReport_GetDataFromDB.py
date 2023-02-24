from datetime import datetime
from Global_Files import Connection_String as con
from Global_Files import AmmountINWords as amw
from PrintPDF import MonthWiseSalesReport_PrintPDF as MWSRPP


def MonthWiseSalesReport_GetData(startdate,enddate,comp,allcomp,prefix,allprefix):
    if not allcomp and not comp or allcomp:
        comp = " "
    elif comp:
        comp = " AND Plant.CODE in (" + str(comp)[1:-1] + ")"

    if not allprefix and not prefix or allprefix:
        prefix = " "
    elif prefix:
        prefix = " AND PI.InvoiceTypeCode in (" + str(prefix)[1:-1] + ")"
    sql=(
        " Select Plant.Longdescription as Company, MONTHNAME(PI.INVOICEDATE) ||' '|| YEAR(PI.INVOICEDATE) as month ,PI.InvoiceTypeCode AS PREFIX,TZ.LONGDESCRIPTION as Dispatch "
        " ,cast(sum(PI.TOTALQUANTITY) as decimal(18,2)) as  Salesqty "
        " ,cast(sum(PI.BASICVALUE) as decimal(18,2)) as Salesamt "
        " ,0 as jwqty "
        " ,0 as jwamt "
        " ,cast(sum(PI.TOTALQUANTITY)as decimal(18,2)) as totalqty "
        " ,cast(sum(PI.BASICVALUE) as decimal(18,2)) as totalamt "
        " from PlantInvoice as PI "
" Join Plant on PI.FACTORYCODE = Plant.Code "
" Join OrderPartner OP    ON PI.CONSIGNEECUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode "
                        " And PI.CONSIGNEECUSTOMERSUPPLIERTYPE = OP.CustomerSupplierType "
 " Join BusinessPartner BP ON OP.OrderbusinessPartnerNumberId = BP.NumberID "
 " Join TransportZone TZ   ON BP.TRANSPORTZONECODE = TZ.CODE "
 " Where PI.INVOICEDATE BETWEEN '"+startdate+"' AND '"+enddate+"' "+comp+prefix+""
 " Group by Plant.Longdescription, MONTHNAME(PI.INVOICEDATE) ||' '|| YEAR(PI.INVOICEDATE),PI.InvoiceTypeCode,TZ.LONGDESCRIPTION"
 " Order By Company, month,prefix,dispatch"
    )
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    stdt = datetime.strptime(startdate, '%Y-%m-%d').date()
    etdt = datetime.strptime(enddate, '%Y-%m-%d').date()
    while result != False:
        MWSRPP.textsize(MWSRPP.c, result, MWSRPP.d,stdt,etdt)
        MWSRPP.d = MWSRPP.dvalue(stdt,etdt,MWSRPP.company)
        result = con.db.fetch_both(stmt)

    MWSRPP.d = MWSRPP.dvalue(stdt, etdt, MWSRPP.company)    
    MWSRPP.monthTotalPrint(MWSRPP.d)
    MWSRPP.d = MWSRPP.dvalue(stdt, etdt, MWSRPP.company)    
    MWSRPP.companyTotalPrint(MWSRPP.d)
    MWSRPP.c.showPage()
    MWSRPP.c.save()
    MWSRPP.newrequest()
    MWSRPP.d = MWSRPP.newpage()


def MonthWiseSalesReport_GetData1(startdate,enddate,comp,allcomp,prefix,allprefix):
    if not allcomp and not comp or allcomp:
        comp = " "
    elif comp:
        comp = " AND Plant.CODE in (" + str(comp)[1:-1] + ")"

    if not allprefix and not prefix or allprefix:
        prefix = " "
    elif prefix:
        prefix = " AND PI.InvoiceTypeCode in (" + str(prefix)[1:-1] + ")"
    sql=(
        " Select Plant.Longdescription as Company, MONTHNAME(PI.INVOICEDATE) ||' '|| YEAR(PI.INVOICEDATE) as month "
        ",PI.InvoiceTypeCode AS PREFIX "
        " ,cast(sum(PI.TOTALQUANTITY) as decimal(18,2)) as  Salesqty "
        " ,cast(sum(PI.BASICVALUE) as decimal(18,2)) as Salesamt "
        " ,0 as jwqty "
        " ,0 as jwamt "
        " ,cast(sum(PI.TOTALQUANTITY)as decimal(18,2)) as totalqty "
        " ,cast(sum(PI.BASICVALUE) as decimal(18,2)) as totalamt "
        " from PlantInvoice as PI "
" Join Plant on PI.FACTORYCODE = Plant.Code "
" Join OrderPartner OP    ON PI.CONSIGNEECUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode "
                        " And PI.CONSIGNEECUSTOMERSUPPLIERTYPE = OP.CustomerSupplierType "
 " Join BusinessPartner BP ON OP.OrderbusinessPartnerNumberId = BP.NumberID "
 " Join TransportZone TZ   ON BP.TRANSPORTZONECODE = TZ.CODE "
 " Where PI.INVOICEDATE BETWEEN '"+startdate+"' AND '"+enddate+"' "+comp+prefix+""
 " Group by Plant.Longdescription, MONTHNAME(PI.INVOICEDATE) ||' '|| YEAR(PI.INVOICEDATE),PI.InvoiceTypeCode"
 " Order By Company, month,prefix"
    )
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    stdt = datetime.strptime(startdate, '%Y-%m-%d').date()
    etdt = datetime.strptime(enddate, '%Y-%m-%d').date()
    while result != False:
        MWSRPP.textsize1(MWSRPP.c, result, MWSRPP.d,stdt,etdt)
        MWSRPP.d = MWSRPP.dvalue(stdt,etdt,MWSRPP.company)
        result = con.db.fetch_both(stmt)

    MWSRPP.d = MWSRPP.dvalue(stdt, etdt, MWSRPP.company)    
    MWSRPP.monthTotalPrint(MWSRPP.d)
    MWSRPP.d = MWSRPP.dvalue(stdt, etdt, MWSRPP.company)    
    MWSRPP.companyTotalPrint(MWSRPP.d)
    MWSRPP.c.showPage()
    MWSRPP.c.save()
    MWSRPP.newrequest()
    MWSRPP.d = MWSRPP.newpage()