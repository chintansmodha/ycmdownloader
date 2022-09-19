import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
import os.path
from Global_Files import Connection_String as con

GDataItemType = []
GDataOrderType = []

stmt = con.db.exec_immediate(con.conn, "Select          Unique(SOD.ITEMTYPEAFICODE) As ItmType "
                                       "From    SALESORDER "
                                       "Join    SALESORDERDELIVERY SOD          ON      SALESORDER.CODE = SOD.SALESORDERLINESALESORDERCODE "
                                       "And     SALESORDER.COUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE "
                                       "where   SOD.RECEIVINGSTATUS <> 2 "
                                       "And     SALESORDER.ORDERDATE >= '2021-01-01' "
                                       "Order By   ItmType ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemType:
        GDataItemType.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn, "Select          Unique(Case SALESORDERIE.TYPEOFINVOICE When 0 Then 'Domestic' "
                                       " when 2 Then'Export' When 3 Then 'Deemed Export' "
                                       "When 4 Then 'Jobwork' when 5 Then 'SEZ' When 6 Then 'Merchant Export' Else 'None' End) As OrdType "
                                       ", SALESORDERIE.TYPEOFINVOICE As OrderTypeCde "
                                       "From    SALESORDER "
                                       "Join    SALESORDERIE    On      SALESORDER.CODE = SALESORDERIE.CODE  "
                                       "And     SALESORDER.COUNTERCODE = SALESORDERIE.COUNTERCODE "
                                       "Join    SALESORDERDELIVERY SOD          ON      SALESORDERIE.CODE = SOD.SALESORDERLINESALESORDERCODE "
                                       "And     SALESORDERIE.COUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE "
                                       "where   SOD.RECEIVINGSTATUS <> 2 "
                                       "And     SALESORDER.ORDERDATE >= '2021-01-01' "
                                       "Order By OrderTypeCde ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataOrderType:
        GDataOrderType.append(result)
    result = con.db.fetch_both(stmt)

# ****************************** Itemwise radio button checked ***********************
def ContractsPendingMis(request):
    orderType = str(request.GET.getlist('orderType'))
    itemtype = str(request.GET.getlist('itemType'))
    orderTypes = orderType[1:-1]
    itemtypes = itemtype[1:-1]
    orderTypeSlct = orderType[2:-2]
    itemtypeSlct = itemtype[2:-2]
    if orderTypes == "" and itemtypes == "":
        order = ""
        itemType = ""
    else:
        # print(itemtypes)
        if itemtypes == "'1 '":
            itemType = ""
            # print(itemtypes, 'itm  ')

        else:
            itemType = " And SOD.ITEMTYPEAFICODE = " + '(' + itemtypes + ')'

        if orderTypes == "'1'":
            order = ""
            # print(orderTypes, 'ord')

        else:
            order = " And SALESORDERIE.TYPEOFINVOICE = " + '(' + orderTypes + ')'

    # print(orderTypes, itemtypes)

    # *********************** ITEM Group *********************
    GDataItemGroup = []

    sql = "Select            Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Not Entered') As Itmgrp " \
          ", CAST(Sum(ROUND(SOD.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty  " \
          ", Cast(Case When Sum(SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY) < 0 " \
          "Then 0 Else Sum(ROUND((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY),0)) End As Decimal(20,0)) As  DespatchNotGvn  " \
          ", Cast(Sum(Case When SOD.RECEIVINGSTATUS <> 2 Then Round(SOD.USEDUSERPRIMARYQUANTITY,0)  Else 0 End) As Decimal(20,0)) As GoodsNotRcvd " \
          ", Cast(Sum(Round((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY + (Case When SOD.RECEIVINGSTATUS <> 2 Then SOD.USEDUSERPRIMARYQUANTITY  Else 0 End)),0)) As Decimal(20,0)) As TotalPdgDelv " \
          "From    SALESORDER SO " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join    SALESORDERDELIVERY SOD          ON      SO.CODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SO.COUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOD.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOD.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOD.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOD.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOD.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOD.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOD.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOD.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOD.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOD.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp   On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SOD.RECEIVINGSTATUS <> 2 And     SO.ORDERDATE >= '2021-01-01' "+itemType+" "+order+" " \
          "Group By Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Not Entered') " \
          "Order by Itmgrp "

    # **** Totals Cal..... *******
    ContTotal = 0
    DespNtGvn = 0
    GdNtRcvd = 0
    TotlPndg = 0

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        ContTotal += float(result['CONTQTY'])
        DespNtGvn += float(result['DESPATCHNOTGVN'])
        GdNtRcvd += float(result['GOODSNOTRCVD'])
        TotlPndg += float(result['TOTALPDGDELV'])
        GDataItemGroup.append(result)
        result = con.db.fetch_both(stmt)

    # ********************************** ITEM **********************************
    GDataItem = []

    sql = "Select            Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Not Entered') As Itmgrp " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", CAST(Sum(ROUND(SOD.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty  " \
          ", Cast(Case When Sum(SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY) < 0 " \
          "Then 0 Else Sum(ROUND((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY),0)) End As Decimal(20,0)) As  DespatchNotGvn  " \
          ", Cast(Sum(Case When SOD.RECEIVINGSTATUS <> 2 Then Round(SOD.USEDUSERPRIMARYQUANTITY,0)  Else 0 End) As Decimal(20,0)) As GoodsNotRcvd " \
          ", Cast(Sum(Round((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY + (Case When SOD.RECEIVINGSTATUS <> 2 Then SOD.USEDUSERPRIMARYQUANTITY  Else 0 End)),0)) As Decimal(20,0)) As TotalPdgDelv " \
          "From    SALESORDER SO " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join    SALESORDERDELIVERY SOD          ON      SO.CODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SO.COUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOD.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOD.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOD.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOD.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOD.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOD.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOD.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOD.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOD.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOD.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp   On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "Left Join QUALITYLEVEL                  On      SOD.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "And     SOD.QUALITYCODE = QUALITYLEVEL.CODE " \
          "where   SOD.RECEIVINGSTATUS <> 2  And     SO.ORDERDATE >= '2021-01-01' "+itemType+" "+order+" " \
          "Group   By Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Not Entered') " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') " \
          "Order by Itmgrp, Item "

    # **** Totals Cal..... *******
    ItmContTotal = 0
    ItmDespNtGvn = 0
    ItmGdNtRcvd = 0
    ItmTotlPndg = 0

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        ItmContTotal += float(result['CONTQTY'])
        ItmDespNtGvn += float(result['DESPATCHNOTGVN'])
        ItmGdNtRcvd += float(result['GOODSNOTRCVD'])
        ItmTotlPndg += float(result['TOTALPDGDELV'])
        GDataItem.append(result)
        result = con.db.fetch_both(stmt)


    #     *****************************  Cont NO table/ Bottom Table  *********************
    GDataCotno = []

    sql = "Select                  Coalesce(SaleGrp.LONGDESCRIPTION, 'Item Group Not Entered') As Itmgrp " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", SO.Code As ContNo " \
          ", SO.COUNTERCODE As ContCounterCode " \
          ", SO.DOCUMENTTYPETYPE As DctType " \
          ", Varchar_Format(SO.ORDERDATE , 'DD-MM-YYYY') As ContDt " \
          ", BP.LEGALNAME1 As Customer " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", Cast(Round(SOD.USERPRIMARYQUANTITY,0) As Decimal(20,0)) As Qty " \
          ", Cast(Round(SOD.USEDUSERPRIMARYQUANTITY,0) As Decimal(20,0)) As BalDesp " \
          ", Coalesce(CAST(ContRate.CalculatedValueRcc AS Decimal(12,2)),0) As Rate " \
          ", Cast(Coalesce(DharaRate.VALUE, 0) As Decimal(10,2)) As Drate " \
          ", Coalesce(AGENT.LONGDESCRIPTION, 'Broker Name Not Entered') As Broker " \
          ", COALESCE(SO.EXTERNALREFERENCE,'') ||'  '|| COALESCE(Varchar_Format(SO.EXTERNALREFERENCEDATE, 'DD-MM-YYYY'),'') As RefNo " \
          "From SALESORDER SO " \
          "Join ORDERPARTNER OP                    On      SO.ORDPRNCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE " \
          "And     OP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER Bp                 On      OP.ORDERBUSINESSPARTNERNUMBERID = Bp.NUMBERID " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join    SALESORDERLINE SOL              On      SO.CODE = SOL.SALESORDERCODE  " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE  " \
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
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join QUALITYLEVEL                  On      SOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "And     SOL.QUALITYCODE = QUALITYLEVEL.CODE " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "Join    SALESORDERDELIVERY SOD          ON      SOL.SALESORDERCODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SOL.SALESORDERCOUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "AND     SOL.ORDERLINE = SOD.SALESORDERLINEORDERLINE " \
          "Left JOIN ItemSubcodeTemplate IST       ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then SOL.SUBCODE01 When 2 Then SOL.SUBCODE02 When 3 Then SOL.SUBCODE03 When 4 Then SOL.SUBCODE04 When 5 Then SOL.SUBCODE05 " \
          "When 6 Then SOL.SUBCODE06 When 7 Then SOL.SUBCODE07 When 8 Then SOL.SUBCODE08 When 9 Then SOL.SUBCODE09 When 10 Then SOL.SUBCODE10 End = UGG.Code " \
          "Left Join INDTAXDETAIL ContRate         ON      SOL.ABSUNIQUEID = ContRate.ABSUNIQUEID " \
          "And     ContRate.ITAXCODE = 'BSR' " \
          "And     ContRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL DharaRate        ON      SOL.ABSUNIQUEID = DharaRate.ABSUNIQUEID " \
          "And     DharaRate.ITAXCODE = 'DRD' " \
          "And     DharaRate.TAXCATEGORYCODE = 'OTH' " \
          "where   SOD.RECEIVINGSTATUS <> 2 And     SO.ORDERDATE >= '2021-01-01' "+itemType+" "+order+" " \
          "Order by Itmgrp, Item, ContNo"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataCotno.append(result)
        result = con.db.fetch_both(stmt)


    return render(request, 'ContractsPendingMis.html', {'GDataItemType':GDataItemType, 'GDataOrderType':GDataOrderType,
                                                        'orderTypeSlct':orderTypeSlct ,'itemtypeSlct':itemtypeSlct ,
                                                        'GDataItemGroup': GDataItemGroup,
                                                        'ContTotal': int(ContTotal),
                                                        'DespNtGvn': int(DespNtGvn),
                                                        'GdNtRcvd': int(GdNtRcvd),
                                                        'TotlPndg': int(TotlPndg),

                                                        'GDataItem': GDataItem,
                                                        'ItmContTotal': int(ItmContTotal),
                                                        'ItmDespNtGvn': int(ItmDespNtGvn),
                                                        'ItmGdNtRcvd': int(ItmGdNtRcvd),
                                                        'ItmTotlPndg': int(ItmTotlPndg),

                                                        'GDataCotno': GDataCotno})





# ****************************** Agentwise radio button checked ***********************
def AgentWisefunctions(request):
    orderType = str(request.GET.getlist('orderType'))
    itemtype = str(request.GET.getlist('itemType'))
    orderTypes = orderType[1:-1]
    itemtypes = itemtype[1:-1]
    orderTypeSlct = orderType[2:-2]
    itemtypeSlct = itemtype[2:-2]
    if orderTypes == "" and itemtypes == "":
        order = ""
        itemType = ""
    else:
        # print(itemtypes)
        if itemtypes == "'1 '":
            itemType = ""
            # print(itemtypes, 'itm  ')

        else:
            itemType = " And SOD.ITEMTYPEAFICODE = " + '(' + itemtypes + ')'

        if orderTypes == "'1'":
            order = ""
            # print(orderTypes, 'ord')

        else:
            order = " And SALESORDERIE.TYPEOFINVOICE = " + '(' + orderTypes + ')'

    # print(orderTypes, itemtypes)

    # *********************** Agents *********************
    GDataItemGroup = []

    sql = "Select            Coalesce(AGENT.LONGDESCRIPTION,'Broker Name Not Entered') As Broker " \
          ", CAST(Sum(ROUND(SOD.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty  " \
          ", Cast(Case When Sum(SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY) < 0 " \
          "Then 0 Else Sum(ROUND((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY),0)) End As Decimal(20,0)) As  DespatchNotGvn  " \
          ", Cast(Sum(Case When SOD.RECEIVINGSTATUS <> 2 Then Round(SOD.USEDUSERPRIMARYQUANTITY,0)  Else 0 End) As Decimal(20,0)) As GoodsNotRcvd " \
          ", Cast(Sum(Round((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY + (Case When SOD.RECEIVINGSTATUS <> 2 Then SOD.USEDUSERPRIMARYQUANTITY  Else 0 End)),0)) As Decimal(20,0)) As TotalPdgDelv " \
          "From    SALESORDER SO " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join    SALESORDERDELIVERY SOD          ON      SO.CODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SO.COUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOD.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOD.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOD.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOD.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOD.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOD.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOD.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOD.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOD.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOD.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join    USERGENERICGROUP SaleGrp   On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SOD.RECEIVINGSTATUS <> 2 And     SO.ORDERDATE >= '2021-01-01' "+itemType+" "+order+" " \
          "Group By Coalesce(AGENT.LONGDESCRIPTION,'Broker Name Not Entered') " \
          "Order by Broker "

    # **** Totals Cal..... *******
    ContTotal = 0
    DespNtGvn = 0
    GdNtRcvd = 0
    TotlPndg = 0

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        ContTotal += float(result['CONTQTY'])
        DespNtGvn += float(result['DESPATCHNOTGVN'])
        GdNtRcvd += float(result['GOODSNOTRCVD'])
        TotlPndg += float(result['TOTALPDGDELV'])
        GDataItemGroup.append(result)
        result = con.db.fetch_both(stmt)

    # ********************************** ITEM **********************************
    GDataItem = []

    sql = "Select            Coalesce(AGENT.LONGDESCRIPTION,'Broker Name Not Entered') As Broker " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", CAST(Sum(ROUND(SOD.USERPRIMARYQUANTITY,0)) AS Decimal(20,0)) As ContQty  " \
          ", Cast(Case When Sum(SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY) < 0 " \
          "Then 0 Else Sum(ROUND((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY),0)) End As Decimal(20,0)) As  DespatchNotGvn  " \
          ", Cast(Sum(Case When SOD.RECEIVINGSTATUS <> 2 Then Round(SOD.USEDUSERPRIMARYQUANTITY,0)  Else 0 End) As Decimal(20,0)) As GoodsNotRcvd " \
          ", Cast(Sum(Round((SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY + (Case When SOD.RECEIVINGSTATUS <> 2 Then SOD.USEDUSERPRIMARYQUANTITY  Else 0 End)),0)) As Decimal(20,0)) As TotalPdgDelv " \
          "From    SALESORDER SO " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join    SALESORDERDELIVERY SOD          ON      SO.CODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SO.COUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOD.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOD.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOD.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOD.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOD.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOD.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOD.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOD.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOD.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOD.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOD.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join QUALITYLEVEL                  On      SOD.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "And     SOD.QUALITYCODE = QUALITYLEVEL.CODE " \
          "Left Join    USERGENERICGROUP SaleGrp   On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "where   SOD.RECEIVINGSTATUS <> 2  And     SO.ORDERDATE >= '2021-01-01' "+itemType+" "+order+" " \
          "Group   By Coalesce(AGENT.LONGDESCRIPTION,'Broker Name Not Entered') " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') " \
          "Order by Broker, Item "

    # **** Totals Cal..... *******
    ItmContTotal = 0
    ItmDespNtGvn = 0
    ItmGdNtRcvd = 0
    ItmTotlPndg = 0

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        ItmContTotal += float(result['CONTQTY'])
        ItmDespNtGvn += float(result['DESPATCHNOTGVN'])
        ItmGdNtRcvd += float(result['GOODSNOTRCVD'])
        ItmTotlPndg += float(result['TOTALPDGDELV'])
        GDataItem.append(result)
        result = con.db.fetch_both(stmt)


    #     *****************************  Cont NO table/ Bottom Table  *********************
    GDataCotno = []

    sql = "Select                  Coalesce(AGENT.LONGDESCRIPTION,'Broker Name Not Entered') As Broker " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", SO.Code As ContNo " \
          ", SO.COUNTERCODE As ContCounterCode " \
          ", SO.DOCUMENTTYPETYPE As DctType " \
          ", Varchar_Format(SO.ORDERDATE , 'DD-MM-YYYY') As ContDt " \
          ", BP.LEGALNAME1 As Customer " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", Cast(Round(SOD.USERPRIMARYQUANTITY,0) As Decimal(20,0)) As Qty " \
          ", Cast(Round(SOD.USEDUSERPRIMARYQUANTITY,0)  As Decimal(20,0)) As BalDesp " \
          ", Coalesce(CAST(ContRate.CalculatedValueRcc AS Decimal(12,2)),0) As Rate " \
          ", Cast(Coalesce(DharaRate.VALUE, 0) As Decimal(10,2)) As Drate " \
          ", COALESCE(SO.EXTERNALREFERENCE,'') ||'  '|| COALESCE(Varchar_Format(SO.EXTERNALREFERENCEDATE, 'DD-MM-YYYY'),'') As RefNo " \
          "From SALESORDER SO " \
          "Join ORDERPARTNER OP                    On      SO.ORDPRNCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE " \
          "And     OP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER Bp                 On      OP.ORDERBUSINESSPARTNERNUMBERID = Bp.NUMBERID " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Join    SALESORDERLINE SOL              On      SO.CODE = SOL.SALESORDERCODE  " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE  " \
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
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left Join QUALITYLEVEL                  On      SOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "And     SOL.QUALITYCODE = QUALITYLEVEL.CODE " \
          "Left Join    USERGENERICGROUP SaleGrp        On      PRODUCT.THIRDUSERGRPUSERGENGRPTYPECOD = SaleGrp.USERGENERICGROUPTYPECODE " \
          "And     PRODUCT.THIRDUSERGRPCODE = SaleGrp.CODE " \
          "And     SaleGrp.USERGENERICGROUPTYPECODE = 'SAG' " \
          "Join    SALESORDERDELIVERY SOD          ON      SOL.SALESORDERCODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SOL.SALESORDERCOUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "AND     SOL.ORDERLINE = SOD.SALESORDERLINEORDERLINE " \
          "Left JOIN ItemSubcodeTemplate IST       ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then SOL.SUBCODE01 When 2 Then SOL.SUBCODE02 When 3 Then SOL.SUBCODE03 When 4 Then SOL.SUBCODE04 When 5 Then SOL.SUBCODE05 " \
          "When 6 Then SOL.SUBCODE06 When 7 Then SOL.SUBCODE07 When 8 Then SOL.SUBCODE08 When 9 Then SOL.SUBCODE09 When 10 Then SOL.SUBCODE10 End = UGG.Code " \
          "Left Join INDTAXDETAIL ContRate         ON      SOL.ABSUNIQUEID = ContRate.ABSUNIQUEID " \
          "And     ContRate.ITAXCODE = 'BSR' " \
          "And     ContRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL DharaRate        ON      SOL.ABSUNIQUEID = DharaRate.ABSUNIQUEID " \
          "And     DharaRate.ITAXCODE = 'DRD' " \
          "And     DharaRate.TAXCATEGORYCODE = 'OTH' " \
          "where   SOD.RECEIVINGSTATUS <> 2 And     SO.ORDERDATE >= '2021-01-01' "+itemType+" "+order+" " \
          "Order by Broker, Item, ContNo"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataCotno.append(result)
        result = con.db.fetch_both(stmt)


    return render(request, 'ContractsPendingAgentMis.html', {'GDataItemType':GDataItemType, 'GDataOrderType':GDataOrderType,
                                                        'orderTypeSlct':orderTypeSlct ,'itemtypeSlct':itemtypeSlct ,
                                                        'GDataItemGroup': GDataItemGroup,
                                                        'ContTotal': int(ContTotal),
                                                        'DespNtGvn': int(DespNtGvn),
                                                        'GdNtRcvd': int(GdNtRcvd),
                                                        'TotlPndg': int(TotlPndg),

                                                        'GDataItem': GDataItem,
                                                        'ItmContTotal': int(ItmContTotal),
                                                        'ItmDespNtGvn': int(ItmDespNtGvn),
                                                        'ItmGdNtRcvd': int(ItmGdNtRcvd),
                                                        'ItmTotlPndg': int(ItmTotlPndg),

                                                        'GDataCotno': GDataCotno})