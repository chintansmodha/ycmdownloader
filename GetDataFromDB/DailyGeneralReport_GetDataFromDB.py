from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import DailyGeneralReport_PrintPDF as Sumpdfrpt
from PrintPDF import DailyGeneralReportDetail_PrintPDF as Detpdfrpt
 
Logicalwarehouse=[]
def DailyGeneralReportSummary_PrintPDF(Department,ItemType,startdate,enddate):
    global Logicalwarehouse
    Logicalwarehouse=[]
    if not Department:
        Dept=" "
        sql= "select CODE from Plant order by Longdescription"
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            Logicalwarehouse.append(result)
            result = con.db.fetch_both(stmt)
    elif Department:
        sql= "select CODE from Plant where Plant.Code in( "+str(Department)[1:-1]+") order by Longdescription"
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            Logicalwarehouse.append(result)
            result = con.db.fetch_both(stmt)

    print(Logicalwarehouse)
    if not ItemType:
        Item=" "
    elif ItemType:
        Item = " AND Product.ITEMTYPECODE in (" + str(ItemType)[1:-1]+")"


    for i in Logicalwarehouse:
        sql =  "Select "\
                "SUBSTRING(BKLElements.LOTCODE, 1, 3) as MC"\
                ",BKLElements.LOTCODE as LotCode "\
                ",BKLElements.SHADENAME"\
                " ,Product.Longdescription as Item"\
                ",Plant.Longdescription as Plant"\
                ",cast(sum(BKLElements.ACTUALNETWT)as decimal(18,3)) as Today"\
                ",cast(sum(case when ST.TRANSACTIONDATE between FIRST_DAY('"+enddate+"') and '"+enddate+"' then ACTUALNETWT else 0 end)as decimal(18,3)) as uptodate"\
                ",'' previouslots"\
                " from BKLElements"\
                " JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')  "\
                " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')  "\
                " Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE   "\
                " And     FIKD.ItemUniqueId = Product.AbsUniqueId  "\
                " Join Plant On      BKLELEMENTS.Plantcode = Plant.code    "\
                " Join    StockTransaction ST      On      BKLELEMENTS.CODE = ST.CONTAINERELEMENTCODE"\
                " where ST.TRANSACTIONDATE Between '"+startdate+"' And '"+enddate+"' AND Plant.CODE = '"+str(i['CODE'])+"' "+Item+""\
                " Group by Plant.Longdescription,BKLElements.LOTCODE,BKLElements.SHADENAME,Product.Longdescription"\
                " Order by Plant.Longdescription"
        
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        if result != False:
            Sumpdfrpt.productionheader(datetime.strptime(startdate,'%Y-%m-%d')
                ,datetime.strptime(enddate,'%Y-%m-%d'), str(result['PLANT']))
            while result != False:
                Sumpdfrpt.productiontextsize(Sumpdfrpt.c, result, Sumpdfrpt.d,datetime.strptime(startdate,'%Y-%m-%d'),datetime.strptime(enddate,'%Y-%m-%d'))
                result = con.db.fetch_both(stmt)
            if result == False:
                Sumpdfrpt.d = Sumpdfrpt.dvalue(startdate, enddate, Sumpdfrpt.divisioncode)
                Sumpdfrpt.machinetotal()
                Sumpdfrpt.d = Sumpdfrpt.dvalue(startdate, enddate, Sumpdfrpt.divisioncode)
                Sumpdfrpt.productionprinttotal()
                Sumpdfrpt.productionnewrequest()
            Sumpdfrpt.c.showPage()
            Sumpdfrpt.d = Sumpdfrpt.newpage()

        sql = "Select           Product.Longdescription as ProductName" \
            ",Costcenter.SHORTDESCRIPTION as Base" \
            ",Product.ABSUNIQUEID as ABSUNIQUEID" \
            ",Plant.Longdescription as Divcode" \
            ",COALESCE(St.Lotcode,'') as Lotcode" \
            ",cast(sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End)as decimal(18,3)) as OpBal" \
            ",cast(sum(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,3)) as RecQty" \
            ",cast(sum(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,3)) as IssQty" \
            ",cast(sum(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End)as decimal(18,3)) as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Costcenter                 On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.code" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " where ST.TRANSACTIONDATE Between '"+startdate+"' And '"+enddate+"' AND Plant.CODE = '"+str(i['CODE'])+"' "+Item+""\
            " Group By Plant.Longdescription,Product.Longdescription,Product.ABSUNIQUEID,St.Lotcode,Costcenter.SHORTDESCRIPTION" \
            " Order By Plant.Longdescription,Product.Longdescription"

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        print(sql)
        if result != False:
            Sumpdfrpt.header(datetime.strptime(startdate, '%Y-%m-%d')
                                       , datetime.strptime(enddate, '%Y-%m-%d'), str(result['DIVCODE']))
            while result != False:
                Sumpdfrpt.textsize(Sumpdfrpt.c, result, Sumpdfrpt.d,datetime.strptime(startdate,'%Y-%m-%d'),datetime.strptime(enddate,'%Y-%m-%d'))
                result = con.db.fetch_both(stmt)
            if result == False:
                Sumpdfrpt.d = Sumpdfrpt.dvalue(startdate, enddate, Sumpdfrpt.divisioncode)
                Sumpdfrpt.printtotal()
            Sumpdfrpt.c.showPage()
            Sumpdfrpt.d = Sumpdfrpt.newpage()
    Sumpdfrpt.c.save()
    Sumpdfrpt.newrequest()
    Sumpdfrpt.d = Sumpdfrpt.newpage()

def DailyGeneralReportDetail_PrintPDF(Department,ItemType,startdate,enddate):
    if not Department:
        Dept=" "
    elif Department:
        Dept = " AND Plant.CODE in (" + str(Department)[1:-1]+")"

    if not ItemType:
        Item=" "
    elif ItemType:
        Item = " AND Product.ITEMTYPECODE in (" + str(ItemType)[1:-1]+")"



    print(Department,ItemType)
    sql = " Select  Product.Longdescription as ProductName" \
          " ,Plant.Longdescription as Divcode" \
          " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
          " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TRANSACTIONNUMBER End as TxnNo" \
          " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
          " , '' As PartyDept" \
          " ,cast(sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End)as decimal(18,3)) as OpBal" \
          " ,cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,3)) as RecQty" \
          " ,cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,3)) as IssQty" \
          " ,cast(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,3)) as BalQty" \
          " From    StockTransaction ST" \
          " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
          " JOIN FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
          " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
          " where Plant.COMPANYCODE = '100' "+Dept+Item+"" \
          " Group By Product.Longdescription" \
          " ,Plant.Longdescription" \
          " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End" \
          " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TRANSACTIONNUMBER End" \
          " ,Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End" \
          " ,Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End" \
          " ,Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End" \
          " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End" \
          " Order By Plant.Longdescription,Product.Longdescription"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        Detpdfrpt.textsize(Detpdfrpt.c, result, Detpdfrpt.d,datetime.strptime(startdate,'%Y-%m-%d'),datetime.strptime(enddate,'%Y-%m-%d'))
        result = con.db.fetch_both(stmt)
    if result == False:
        Detpdfrpt.d = Detpdfrpt.dvalue(startdate, enddate, Detpdfrpt.divisioncode)
        Detpdfrpt.printstoretotal(startdate, enddate, Detpdfrpt.divisioncode)
        Detpdfrpt.d = Detpdfrpt.dvalue(startdate, enddate, Detpdfrpt.divisioncode)
        Detpdfrpt.printtotal()

    Detpdfrpt.c.showPage()
    Detpdfrpt.c.save()
    Detpdfrpt.newrequest()
    Detpdfrpt.d = Detpdfrpt.newpage()
