import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
import os.path
from Global_Files import Connection_String as con



# ****************************** Itemwise radio button checked ***********************
def ContractListMis(request):
    return render(request, 'ContractListMis.html')

# radio itemwise button click
def ContListItemWisefunctions(request):
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LDStartDates = "'" + LDStartDate + "'"
    LDEndDates = "'" + LDEndDate + "'"
    Syear = LDStartDate[0:4]
    Smonth = LDStartDate[5:7]
    Sday = LDStartDate[8:10]
    Eyear = LDEndDate[0:4]
    Emonth = LDEndDate[5:7]
    Eday = LDEndDate[8:10]
    # print(Syear, Smonth, Sday,Eyear  ,Emonth ,Eday )

    # Item Group Query
    GDataItemGroup = []
    sql= "Select            Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
         ", CAST(Sum(ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
         "From    SALESORDER SO " \
         "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
         "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
         "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
         "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
         "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
         "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
         "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
         "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
         "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
         "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
         "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
         "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
         "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
         "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
         "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
         "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
         "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
         "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
         "where   SO.PREVIOUSCODE is null " \
         "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
         "Group By Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') " \
         "Order by Itmgrp"


    # total
    ContTotal = 0

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        ContTotal += int(result['CONTQTY'])
        GDataItemGroup.append(result)
        result = con.db.fetch_both(stmt)

    # Item Query
    GDataItem = []
    sql = "Select            Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered')  As Item " \
          ", CAST(Sum(ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
          "From    SALESORDER SO " \
          "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SO.PREVIOUSCODE is null " \
          "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
          "Group By Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered') " \
          "Order by Itmgrp, Item "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataItem.append(result)
        result = con.db.fetch_both(stmt)

    # Agent Query
    GDataAgent = []
    sql = "Select            Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered') As Item " \
          ", Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') As Agent " \
          ", CAST(Sum(ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
          "From    SALESORDER SO " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SO.PREVIOUSCODE is null " \
          "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
          "Group By Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered') " \
          ", Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') " \
          "Order by Itmgrp, Item, Agent "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataAgent.append(result)
        result = con.db.fetch_both(stmt)



    # Details Table Query
    GDataCont = []
    sql = "Select            Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered') As Item " \
          ", Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') As Agent " \
          ", SO.CODE As ContNo  " \
          ", SO.COUNTERCODE As Counter " \
          ", SO.DOCUMENTTYPETYPE As DcmntType " \
          ", (Case SALESORDERIE.TYPEOFINVOICE When 0 Then 'Domestic' when 2 Then'Export' When 3 Then 'Deemed Export' " \
          "When 4 Then 'Jobwork' when 5 Then 'SEZ' When 6 Then 'Merchant Export' Else 'None' End) As OrdType " \
          ", Coalesce(CAST(Rate.CalculatedValueRcc AS Decimal(12,2)),0) As Rate " \
          ", Cast(Coalesce(DharaRate.VALUE, 0) As Decimal(10,2)) As RD " \
          ", Varchar_Format(SO.ORDERDATE, 'DD-MM-YYYY') As ContDt " \
          ", CAST((ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
          ", ConsineeBp.LEGALNAME1 AS COnsinee " \
          ", CustomerBp.LEGALNAME1 AS Customer " \
          ", DIVISION.LONGDESCRIPTION As Company " \
          "From    SALESORDER SO " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join ORDERPARTNER ConsineeOP            On      SO.ORDPRNCUSTOMERSUPPLIERCODE = ConsineeOP.CUSTOMERSUPPLIERCODE " \
          "And     ConsineeOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER ConsineeBp         On      ConsineeOP.ORDERBUSINESSPARTNERNUMBERID = ConsineeBp.NUMBERID " \
          "Left Join ORDERPARTNER CustomerOP       On      SO.ORDPRNCUSTOMERSUPPLIERCODE = CustomerOP.CUSTOMERSUPPLIERCODE " \
          "And     CustomerOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Left Join BUSINESSPARTNER CustomerBp    On      CustomerOP.ORDERBUSINESSPARTNERNUMBERID = CustomerBp.NUMBERID " \
          "Join DIVISION                           On      SO.DIVISIONCODE = DIVISION.CODE " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "Left Join INDTAXDETAIL DharaRate        ON      SOL.ABSUNIQUEID = DharaRate.ABSUNIQUEID " \
          "And     DharaRate.ITAXCODE = 'DRD' " \
          "And     DharaRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL Rate             ON      SOL.ABSUNIQUEID = Rate.ABSUNIQUEID " \
          "And     Rate.ITAXCODE = 'INR' " \
          "And     Rate.TAXCATEGORYCODE = 'OTH' " \
          "where   SO.PREVIOUSCODE is null " \
          "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
          "Order by Itmgrp, Item, Agent, ContNo "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataCont.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'ContractListItemMis.html', {'GDataItemGroup': GDataItemGroup, 'GDataItem': GDataItem,
                                                        'GDataAgent': GDataAgent, 'GDataCont': GDataCont,
                                                        'ContTotal': ContTotal, 'Syear':Syear, 'Smonth':Smonth, 'Sday':Sday,
                                                        'Eyear': Eyear, 'Emonth': Emonth, 'Eday': Eday})








# ****************************** Agentwise radio button checked ***********************

# radio Agentwise button click
def ContListAgentWisefunctions(request):
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LDStartDates = "'" + LDStartDate + "'"
    LDEndDates = "'" + LDEndDate + "'"
    Syear = LDStartDate[0:4]
    Smonth = LDStartDate[5:7]
    Sday = LDStartDate[8:10]
    Eyear = LDEndDate[0:4]
    Emonth = LDEndDate[5:7]
    Eday = LDEndDate[8:10]
    # print(Syear, Smonth, Sday,Eyear  ,Emonth ,Eday )

    # Agent Query
    GDataAgent = []
    sql= "Select            Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') As Agent " \
         ", CAST(Sum(ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
         "From    SALESORDER SO " \
         "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
         "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
         "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
         "where   SO.PREVIOUSCODE is null " \
         "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
         "Group By Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') " \
         "Order by Agent"


    # total
    ContTotal = 0

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        ContTotal += int(result['CONTQTY'])
        GDataAgent.append(result)
        result = con.db.fetch_both(stmt)

    # Item group Query
    GDataItemGroup = []
    sql = "Select            Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') As Agent " \
          ", Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
          ", CAST(Sum(ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
          "From    SALESORDER SO " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SO.PREVIOUSCODE is null " \
          "And     So.ORDERDATE Between " + LDStartDates + "       And     " + LDEndDates + " " \
          "Group By Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') " \
          ", Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') " \
          "Order by Agent, Itmgrp "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataItemGroup.append(result)
        result = con.db.fetch_both(stmt)


    # Item Query
    GDataItem = []
    sql = "Select            Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') As Agent " \
          ", Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered')  As Item " \
          ", CAST(Sum(ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
          "From    SALESORDER SO " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SO.PREVIOUSCODE is null " \
          "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
          "Group By Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') " \
          ", Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered')  " \
          "Order by Agent, Itmgrp, Item "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataItem.append(result)
        result = con.db.fetch_both(stmt)



    # Details Table Query
    GDataCont = []
    sql = "Select            Coalesce(AGENT.LONGDESCRIPTION, 'Agent  Name Not Entered') As Agent " \
          ", Coalesce(PRODUCT.LONGDESCRIPTION, 'Item  Name Not Entered')  As Item " \
          ", Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Name Not Entered') As Itmgrp " \
          ", SO.CODE As ContNo " \
          ", SO.COUNTERCODE As Counter " \
          ", SO.DOCUMENTTYPETYPE As DcmntType " \
          ", (Case SALESORDERIE.TYPEOFINVOICE When 0 Then 'Domestic' when 2 Then'Export' When 3 Then 'Deemed Export' " \
          "When 4 Then 'Jobwork' when 5 Then 'SEZ' When 6 Then 'Merchant Export' Else 'None' End) As OrdType " \
          ", Coalesce(CAST(Rate.CalculatedValueRcc AS Decimal(12,2)),0) As Rate " \
          ", Cast(Coalesce(DharaRate.VALUE, 0) As Decimal(10,2)) As RD " \
          ", Varchar_Format(SO.ORDERDATE, 'DD-MM-YYYY') As ContDt " \
          ", CAST((ROUND(SOl.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty " \
          ", ConsineeBp.LEGALNAME1 AS COnsinee " \
          ", CustomerBp.LEGALNAME1 AS Customer " \
          ", DIVISION.LONGDESCRIPTION As Company " \
          "From    SALESORDER SO " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join ORDERPARTNER ConsineeOP            On      SO.ORDPRNCUSTOMERSUPPLIERCODE = ConsineeOP.CUSTOMERSUPPLIERCODE " \
          "And     ConsineeOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER ConsineeBp         On      ConsineeOP.ORDERBUSINESSPARTNERNUMBERID = ConsineeBp.NUMBERID " \
          "Left Join ORDERPARTNER CustomerOP       On      SO.ORDPRNCUSTOMERSUPPLIERCODE = CustomerOP.CUSTOMERSUPPLIERCODE " \
          "And     CustomerOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Left Join BUSINESSPARTNER CustomerBp    On      CustomerOP.ORDERBUSINESSPARTNERNUMBERID = CustomerBp.NUMBERID " \
          "Join DIVISION                           On      SO.DIVISIONCODE = DIVISION.CODE " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERLINE SOL              ON      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "Left Join INDTAXDETAIL DharaRate        ON      SOL.ABSUNIQUEID = DharaRate.ABSUNIQUEID " \
          "And     DharaRate.ITAXCODE = 'DRD' " \
          "And     DharaRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL Rate             ON      SOL.ABSUNIQUEID = Rate.ABSUNIQUEID " \
          "And     Rate.ITAXCODE = 'INR' " \
          "And     Rate.TAXCATEGORYCODE = 'OTH' " \
          "where   SO.PREVIOUSCODE is null " \
          "And     So.ORDERDATE Between "+LDStartDates+"       And     "+LDEndDates+" " \
          "Order by Agent, Itmgrp, Item, ContNo "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataCont.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'ContractListAgntMis.html', {'GDataAgent': GDataAgent, 'GDataItemGroup': GDataItemGroup,
                                                        'GDataItem': GDataItem, 'GDataCont': GDataCont,
                                                        'ContTotal': ContTotal, 'Syear':Syear, 'Smonth':Smonth, 'Sday':Sday,
                                                        'Eyear': Eyear, 'Emonth': Emonth, 'Eday': Eday})
