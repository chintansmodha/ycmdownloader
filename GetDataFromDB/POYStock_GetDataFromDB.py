from datetime import datetime
from re import L
from Global_Files import Connection_String as con
from PrintPDF import POYStock_PrintPDF as Sumpdfrpt
from PrintPDF import POYStockDetail_PrintPDF as Detpdfrpt
Logicalwarehouse=[]
def POYStock_PrintPDF(Department,ItemType,startdate,enddate,year):
    global Logicalwarehouse
    Logicalwarehouse=[]
    sql = "select FROMDATE from finfinancialyear where code='"+year+"'"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    YEAR = con.db.fetch_both(stmt)
    print(YEAR)
    if not Department:
        Dept=" "
        sql= "select CODE from Logicalwarehouse order by Longdescription"
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            Logicalwarehouse.append(result)
            result = con.db.fetch_both(stmt)
    elif Department:
        print(Department)
        sql= "select CODE from Logicalwarehouse where Logicalwarehouse.Code in( "+str(Department)[1:-1]+") order by Longdescription"
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            Logicalwarehouse.append(result)
            result = con.db.fetch_both(stmt)

    # if not ItemType:
    #     Item=" "
    # elif ItemType:
    #     Item = " AND Product.ITEMTYPECODE in (" + str(ItemType)[1:-1]+")"

    for i in Logicalwarehouse:
        sql="Select  Logicalwarehouse.Longdescription as Divcode,MrnHeader.CODE as MrnNo" \
            ",COALESCE(BUSINESSPARTNER.Legalname1,'') as Supplier" \
            ",Product.Longdescription as ItemName" \
            ",MRNHEADER.CHALLANDATE AS CHALLANDATE" \
            ",MRNHEADER.CHALLANNO AS CHALLANNO" \
            ",MRNDETAIL.LRDATE AS LRDATE" \
            ",MRNDETAIL.LRNO AS LRNO" \
            ",COALESCE(StkTxn.Lotcode,'') as Lotcode" \
            ",cast(MRNDETAIL.BASEPRIMARYQTY as decimal(18,2)) as RecdWt" \
            ",MRNHEADER.DISPATCHSTATION as place" \
            ",cast(MRNDETAIL.NOOFPACKAGES as decimal(18,2)) as Boxes" \
            " From MrnHeader" \
            " JOIN ORDERPARTNER             ON      MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE" \
            " AND     MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE" \
            " JOIN BUSINESSPARTNER          ON      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID" \
            " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE" \
            " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE" \
            " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE" \
            " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE" \
            " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " JOIN    PRODUCT                         ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE" \
            " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID" \
            " Join     StockTransaction StkTxn On      MRNDetail.TransactionNumber = StkTxn.TransactionNumber" \
            " Join LOGICALWAREHOUSE           On      StkTxn.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Costcenter                 On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.code" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " where MRNHEADER.MRNDATE Between '"+startdate+"' And '"+enddate+"' AND Logicalwarehouse.CODE = '"+str(i['CODE'])+"'"\
                " order by Divcode"
        
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        if result != False:
            Sumpdfrpt.mrnheader(datetime.strptime(startdate,'%Y-%m-%d')
                ,datetime.strptime(enddate,'%Y-%m-%d'), str(result['DIVCODE']))
            while result != False:
                Sumpdfrpt.mrntextsize(Sumpdfrpt.c, result
                                    , Sumpdfrpt.d, datetime.strptime(startdate, '%Y-%m-%d')
                                    , datetime.strptime(enddate, '%Y-%m-%d'))
                result = con.db.fetch_both(stmt)

            if result == False:
                Sumpdfrpt.d = Sumpdfrpt.dvalue(startdate, enddate, Sumpdfrpt.divisioncode)
                
            Sumpdfrpt.printmrntotallast()
            Sumpdfrpt.c.showPage()
            Sumpdfrpt.mrnnewrequest()
            Sumpdfrpt.d = Sumpdfrpt.newpage()

        sql = "Select (Select cast(Sum(ST.USERPRIMARYQUANTITY)as decimal(18,3)) As Quantity"\
                " From StockTransaction as ST"\
                " JOIN FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
             " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '') "\
             " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '') "\
             " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '') "\
             " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '') "\
             " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '') "\
             " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '') "\
             " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '') "\
             " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '') "\
             " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '') "\
             " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '') "\
             " Join Product     as Item               On      ST.ITEMTYPECODE           = Item.ITEMTYPECODE "\
             " And     FIKD.ItemUniqueId             = Item.AbsUniqueId"\
             " Where ST.TRANSACTIONDATE Between FIRST_DAY('"+startdate+"') and '"+startdate+"'"\
             " and Item.AbsUniqueId = Product.AbsUniqueId) as MTDPUR           "\
            ",Product.Longdescription as ProductName" \
            ",Costcenter.SHORTDESCRIPTION as Base" \
            ",Product.ABSUNIQUEID as ABSUNIQUEID" \
            ",Logicalwarehouse.Longdescription as Divcode" \
            ",COALESCE(St.Lotcode,'') as Lotcode" \
            ",COALESCE(QualityLevel.ShortDescription, '') As Quality" \
            ",cast(sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End)as decimal(18,3)) as OpBal" \
            ",cast(sum(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,3)) as RecQty" \
            ",cast(sum(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,3)) as IssQty" \
            ",cast(sum(Case When ST.TransactionDate <= '"+enddate+"' Then ST.UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End)as decimal(18,3)) as BalQty" \
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
                                                                " Join    QualityLevel                    On      ST.QUALITYLEVELCODE = QualityLevel.Code" \
                " where ST.TRANSACTIONDATE Between '"+str(YEAR["FROMDATE"])+"' And '"+enddate+"' AND Logicalwarehouse.CODE ='"+str(i['CODE'])+"'"\
            " Group By Logicalwarehouse.Longdescription,Product.Longdescription,Product.ABSUNIQUEID,Costcenter.SHORTDESCRIPTION,QualityLevel.ShortDescription,St.Lotcode" \
            " Order By Logicalwarehouse.Longdescription,Product.Longdescription,QualityLevel.ShortDescription"

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        if result != False:
            Sumpdfrpt.header(datetime.strptime(startdate,'%Y-%m-%d')
                ,datetime.strptime(enddate,'%Y-%m-%d'), str(result['DIVCODE']))
            while result != False:
                Sumpdfrpt.textsize(Sumpdfrpt.c, result
                ,Sumpdfrpt.d,datetime.strptime(startdate,'%Y-%m-%d')
                ,datetime.strptime(enddate,'%Y-%m-%d'))
                result = con.db.fetch_both(stmt)

            if result == False:
                Sumpdfrpt.d = Sumpdfrpt.dvalue(startdate, enddate, Sumpdfrpt.divisioncode)
            Sumpdfrpt.printtotallast()
            Sumpdfrpt.c.showPage()
            Sumpdfrpt.mrnnewrequest()
            Sumpdfrpt.d = Sumpdfrpt.newpage()

        sql="Select  Logicalwarehouse.Longdescription as Divcode, LOGICALWAREHOUSE.LONGDESCRIPTION  As Department" \
            ", Stxn.DERIVATIONCODE As IssueNo" \
            ", VARCHAR_FORMAT(Stxn.TRANSACTIONDATE, 'DD-MM-YYYY') As IssueDt" \
            ", INTERNALDOCUMENT.PROVISIONALCODE As ReqNumber" \
            ", VARCHAR_FORMAT(INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ReqDate" \
            ", COALESCE(IsuDept.LONGDESCRIPTION,' ') As   toDepartment" \
            ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LongDescription,'') As ItemName" \
            ", COALESCE(QualityLevel.ShortDescription, '') As Quality" \
            ", Cast(Sum(Stxn.USERPRIMARYQUANTITY) As Decimal(20,3)) As Quantity" \
            ", Cast(Coalesce(Sum(BKLELEMENTS.TOTALBOXES),0) As INT) As Boxes" \
            ", Cast(Coalesce(Sum(BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 +" \
            " BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 +" \
            "BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 +" \
            "BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15),0) As Int) As Cops" \
            ", COALESCE(Stxn.LotCode,'')  As LotNo" \
            ", '' As BaseName" \
            " From    INTERNALDOCUMENT" \
            " join    LOGICALWAREHOUSE                On      INTERNALDOCUMENT.WAREHOUSECODE            =      LOGICALWAREHOUSE.Code" \
            " left join    LOGICALWAREHOUSE As IsuDept    On       INTERNALDOCUMENT.DESTINATIONWAREHOUSECODE  =      IsuDept.CODE" \
            " Join Costcenter                 On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.code" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Join    INTERNALDOCUMENTLINE IDL       On       INTERNALDOCUMENT.PROVISIONALCOUNTERCODE   =  IDL.INTDOCPROVISIONALCOUNTERCODE" \
            " And      INTERNALDOCUMENT.PROVISIONALCODE          =  IDL.INTDOCUMENTPROVISIONALCODE" \
            " Join    StockTransaction  Stxn          On      INTERNALDOCUMENT.PROVISIONALCODE  =  Stxn.OrderCode" \
            " AND     INTERNALDOCUMENT.PROVISIONALCOUNTERCODE   =  Stxn.ORDERCOUNTERCODE" \
            " And     IDL.ORDERLINE = Stxn.ORDERLINE" \
            " AND     Stxn.DERIVATIONCODE is Not Null" \
            " Left Join    BKLELEMENTS                On      Stxn.CONTAINERELEMENTCODE =  BKLELEMENTS.Code" \
            " And     Stxn.CONTAINERSUBCODE01 =  BKLELEMENTS.SUBCODEKEY" \
            " join         FULLITEMKEYDECODER FIKD    ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(IDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(IDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(IDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(IDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(IDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(IDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(IDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(IDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(IDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(IDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join         PRODUCT                    On      IDL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId = Product.AbsUniqueId" \
            " Join    QualityLevel                    On      IDL.QualityCode = QualityLevel.Code" \
            " And     IDL.ItemTypeAfiCode = QualityLevel.ItemTypeCode" \
            " Left JOIN    ItemSubcodeTemplate IST         ON      IDL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
            " AND     IST.GroupTypeCode  In ('MB4','P09','B07')" \
            " LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
            " AND     Case IST.Position When 1 Then IDL.SubCode01 When 2 Then IDL.SubCode02 When 3 Then IDL.SubCode03 When 4 Then IDL.SubCode04 When 5 Then IDL.SubCode05" \
            " When 6 Then IDL.SubCode06 When 7 Then IDL.SubCode07 When 8 Then IDL.SubCode08 When 9 Then IDL.SubCode09 When 10 Then IDL.SubCode10 End = UGG.Code" \
            " Where INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE between '"+startdate+"' And '"+enddate+"' AND Logicalwarehouse.CODE ='"+str(i['CODE'])+"'"\
            " Group By Logicalwarehouse.Longdescription , LOGICALWAREHOUSE.LONGDESCRIPTION" \
            ", Stxn.DERIVATIONCODE" \
            ", VARCHAR_FORMAT(Stxn.TRANSACTIONDATE, 'DD-MM-YYYY'), INTERNALDOCUMENT.PROVISIONALCODE , VARCHAR_FORMAT(INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY')" \
            ", COALESCE(IsuDept.LONGDESCRIPTION,' ')" \
            ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LongDescription,'')" \
            ", COALESCE(QualityLevel.ShortDescription, '')" \
            ", COALESCE(Stxn.LotCode,'')" \
            " order  by Divcode,IssueNo, IssueDt Desc, ReqNumber,  ReqDate,  Department, toDepartment " \

        
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        if result != False:
            Sumpdfrpt.YarnIssueHeader(datetime.strptime(startdate,'%Y-%m-%d')
                ,datetime.strptime(enddate,'%Y-%m-%d'), str(result['DIVCODE']))
            while result != False:
                Sumpdfrpt.YarnIssuetextsize(Sumpdfrpt.c, result
                ,Sumpdfrpt.d,datetime.strptime(startdate,'%Y-%m-%d')
                ,datetime.strptime(enddate,'%Y-%m-%d'))
                result = con.db.fetch_both(stmt)

            if result == False:
                Sumpdfrpt.d = Sumpdfrpt.dvalue(startdate, enddate, Sumpdfrpt.divisioncode)

            Sumpdfrpt.printissuetotallast()
            Sumpdfrpt.c.showPage()
            Sumpdfrpt.newrequest()
            Sumpdfrpt.d = Sumpdfrpt.newpage()

    Sumpdfrpt.c.save()
    Sumpdfrpt.newrequest()
    Sumpdfrpt.d = Sumpdfrpt.newpage()

def POYStockDetail_PrintPDF(Department,ItemType,startdate,enddate):
    if not Department:
        Dept=" "
    elif Department:
        Dept = " AND Plant.CODE in (" + str(Department)[1:-1]+")"

    if not ItemType:
        Item=" "
    elif ItemType:
        Item = " AND Product.ITEMTYPECODE in (" + str(ItemType)[1:-1]+")"


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
