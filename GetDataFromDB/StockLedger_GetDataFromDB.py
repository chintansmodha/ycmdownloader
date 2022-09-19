from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import  StockLedger_PrintPDF as pdfrpt
def StockLedger_GetData(LSCompany, LSItem, LSItemGroup,LCCompany,LCItem,LCItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType):

    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = "AND plant.CODE in (" + str(LSCompany)[1:-1] + ")"

    if not LCItem and not LSItem or LCItem:
        LSItem = " "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1] + ")"

    if not LCItemGroup and not LSItemGroup or LCItemGroup:
        LSItemGroup = " "
    elif LSItemGroup:
        LSItemGroup = "AND Product.ITEMTYPECODE in (" + str(LSItemGroup)[1:-1] + ")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = LDStartDate
    enddate = LDEndDate
    sql =   " Select Production.Company,Production.Item,Production.ServiceType " \
            "   ,Production.StType" \
            " ,Production.Dept" \
            " ,Production.TxnDate" \
            " ,Production.TxnNo" \
            " ,Production.TxnType" \
            " ,(Production.OpBal) as Opbal" \
            " ,(Production.RecQty) as RecQty" \
            " ,(Production.IssQty) as IssQty" \
            " ,(Production.BalQty) as BalQty" \
            " from" \
            " (" \
            " Select  Plant.Longdescription as Company,Product.LongDescription as Item,Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType" \
            ", Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End as StType" \
            ",Costcenter.SHORTDESCRIPTION as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2))) as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as IssQty" \
            " ,SUM(cast(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2))) as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
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
            " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE " \
            " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') " \
            " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') " \
            " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') " \
            " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') " \
            " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') " \
            " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') " \
            " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') " \
            " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') " \
            " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') " \
            " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '')" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join MRNHEADER             ON      St.ORDERCODE = MRNHEADER.PURCHASEORDERCODE " \
            " And St.ORDERCOUNTERCODE = MRNHEADER.PURCHASEORDERCOUNTERCODE " \
            " Left Join Costcenter            On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.CODE " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and ST.TemplateCode in ('098','099','CGI','G02','GES','P01','PKC','PKE','PKG'" \
            ",'PS1','PS2','PS3','PS4','PS5','QC2', 'QCT' " \
            ",'REJ','REN','SC2','SCP','T01','T02','T03','T04','T05'" \
            ",'T06','T07','W01') "+LSCompany+LSItemGroup+LSItem+"" \
            " Group By Plant.Longdescription ,ProductIE.SERVICEBILLFLAG,Product.LongDescription" \
            ", Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE End " \
            ",Costcenter.SHORTDESCRIPTION " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union ALl" \
            " Select  Plant.Longdescription as Company,Product.LongDescription as Item,Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType" \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,Costcenter.SHORTDESCRIPTION as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.ProductionOrderCode) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))   as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
             " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
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
            " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE " \
            " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') " \
            " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') " \
            " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') " \
            " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') " \
            " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') " \
            " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') " \
            " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') " \
            " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') " \
            " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') " \
            " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '')" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Join PRODUCTIONORDER PO    On      ST.ProductionOrderCode = PO.CODE " \
            " Left Join BKLELEMENTS      On      ST.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
            " Left Join LOGICALWAREHOUSE bklLogic ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = bklLogic.CODE  " \
            " Left Join Costcenter                 On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.CODE" \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and ST.TemplateCode in ('M01','M02','M03','M04','M05') "+LSCompany+LSItemGroup+LSItem+"" \
            " Group By Plant.Longdescription,ProductIE.SERVICEBILLFLAG,Product.Longdescription " \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,Costcenter.SHORTDESCRIPTION " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.ProductionOrderCode) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company,Product.LongDescription as Item,Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType " \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,PoBp.LEGALNAME1 as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(MD.MRNHEADERCODE) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
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
            " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE " \
            " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') " \
            " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') " \
            " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') " \
            " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') " \
            " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') " \
            " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') " \
            " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') " \
            " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') " \
            " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') " \
            " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '')" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join PurchaseOrder PO      On      ST.OrderCode = PO.Code" \
            " Left Join MrnDetail MD On PO.Code = MD.PURCHASEORDERCODE" \
            " AND PO.CounterCode = MD.PURCHASEORDERCOUNTERCODE " \
            " AND ST.TRANSACTIONNUMBER  = MD.TRANSACTIONNUMBER " \
            " Left Join ORDERPARTNER PoOrpn    ON     PO.ORDPRNCUSTOMERSUPPLIERCODE = PoOrpn.CUSTOMERSUPPLIERCODE " \
            " And PoOrpn.CUSTOMERSUPPLIERTYPE = 1 " \
            " Left Join BUSINESSPARTNER PoBp    On      PoOrpn.ORDERBUSINESSPARTNERNUMBERID = PoBp.NUMBERID " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and ST.TemplateCode in ('101','110','G01') "+LSCompany+LSItemGroup+LSItem+"" \
            " Group By Plant.Longdescription,ProductIE.SERVICEBILLFLAG,Product.LongDescription " \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,PoBp.LEGALNAME1 " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(MD.MRNHEADERCODE) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company,Product.LongDescription as Item,Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,SDBp.LEGALNAME1 as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.OrderCode) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
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
            " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE " \
            " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') " \
            " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') " \
            " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') " \
            " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') " \
            " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') " \
            " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') " \
            " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') " \
            " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') " \
            " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') " \
            " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '')" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join SalesDocument SD           On      ST.OrderCode = SD.ProvisionalCode" \
            " And SD.DocumentTypeType = '05'" \
            " Left Join ORDERPARTNER SDOrpn    ON     SD.ORDPRNCUSTOMERSUPPLIERCODE = SDOrpn.CUSTOMERSUPPLIERCODE " \
            " And SDOrpn.CUSTOMERSUPPLIERTYPE = 1 " \
            " Left Join BUSINESSPARTNER SDBp    On      SDOrpn.ORDERBUSINESSPARTNERNUMBERID = SDBp.NUMBERID " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and ST.TemplateCode in ('S04') "+LSCompany+LSItemGroup+LSItem+"" \
            " Group By Plant.Longdescription,ProductIE.SERVICEBILLFLAG,Product.LongDescription " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,SDBp.LEGALNAME1 " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.OrderCode) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company,Product.LongDescription as Item,Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,SOBp.LEGALNAME1 as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
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
            " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE " \
            " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') " \
            " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') " \
            " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') " \
            " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') " \
            " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') " \
            " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') " \
            " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') " \
            " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') " \
            " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') " \
            " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '')" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join SalesOrder SO              On      ST.Projectcode = SO.Code" \
            " Left Join ORDERPARTNER SOOrpn    ON     SO.ORDPRNCUSTOMERSUPPLIERCODE = SOOrpn.CUSTOMERSUPPLIERCODE " \
            " And SOOrpn.CUSTOMERSUPPLIERTYPE = 1 " \
            " Left Join BUSINESSPARTNER SOBp    On      SOOrpn.ORDERBUSINESSPARTNERNUMBERID = SOBp.NUMBERID " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and ST.TemplateCode in ('S05') " +LSCompany+LSItemGroup+LSItem+""\
            " Group By Plant.Longdescription,ProductIE.SERVICEBILLFLAG,Product.LongDescription " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,SOBp.LEGALNAME1 " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company,Product.LongDescription as Item,Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,Costcenter.SHORTDESCRIPTION as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ID.PROVISIONALCOUNTERCODE ||' '|| VARCHAR(ID.PROVISIONALCODE) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            "  ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
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
            " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE " \
            " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') " \
            " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') " \
            " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') " \
            " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') " \
            " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') " \
            " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') " \
            " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') " \
            " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') " \
            " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') " \
            " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '')" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join InternalDocument ID        ON      ST.OrderCode = ID.PROVISIONALCODE" \
            " Join LOGICALWAREHOUSE IdLogical On      ID.DESTINATIONWAREHOUSECODE = IdLogical.CODE " \
            " Left Join Costcenter                 On      IdLogical.COSTCENTERCODE = Costcenter.CODE" \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and ST.TemplateCode in ('201','209','210','215','310','311','FFO','I03','I04') "+LSCompany+LSItemGroup+LSItem+"" \
            " Group By Plant.Longdescription,ProductIE.SERVICEBILLFLAG,Product.LongDescription " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,Costcenter.SHORTDESCRIPTION " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ID.PROVISIONALCOUNTERCODE ||' '|| Varchar(ID.PROVISIONALCODE) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " ) as Production" \
            " order by Production.Company,Production.ServiceType,Production.Item,Production.TxnDate,Production.TxnNo "
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result==False:
        return
    while result != False:
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        result = con.db.fetch_both(stmt)
    pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
    pdfrpt.boldfonts(9)
    pdfrpt.c.drawString(200, pdfrpt.d, "Item Total : ")
    pdfrpt.c.drawAlignedString(530, pdfrpt.d, str("%.2f" % float(pdfrpt.ItemQuantityTotal)))
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.ItemAmountTotal)))
    pdfrpt.ItemAmountTotal = 0
    pdfrpt.ItemQuantityTotal = 0
    pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
    pdfrpt.c.drawString(200, pdfrpt.d, "Grand Total : ")
    pdfrpt.c.drawAlignedString(530, pdfrpt.d, str("%.2f" % float(pdfrpt.GrandQuantityTotal)))
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.GrandAmountTotal)))
    pdfrpt.GrandQuantityTotal = 0
    pdfrpt.GrandAmountTotal = 0
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()


def StockLedgerSummary_GetData(LSCompany, LSItem, LSItemGroup,LCCompany,LCItem,LCItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType):
    pass
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = "AND plant.CODE in (" + str(LSCompany)[1:-1] + ")"
    
    if not LCItem and not LSItem or LCItem:
        LSItem = " "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1] + ")"
        
    if not LCItemGroup and not LSItemGroup or LCItemGroup:
        LSItemGroup = " "
    elif LSItemGroup:
        LSItemGroup = "AND Product.ITEMTYPECODE in (" + str(LSItemGroup)[1:-1] + ")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = LDStartDate
    enddate = LDEndDate
    sql = "Select Product.Longdescription  as Item  "\
           ",Product.ItemTypeCode  as ItemGroup  "\
          ", Case when ProductIE.SERVICEBILLFLAG = 1 Then 'SERVICE' Else 'GOODS' End as ServiceType"\
          ",cast(Sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0  "\
          "End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End)as decimal(18,2)) as OpBal "\
          ",cast(Sum(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' "\
          "And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,2)) as RecQty "\
          ",cast(Sum(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"'  "\
          "And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,2)) as IssQty "\
          ",cast(Sum(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case  "\
          "When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End)as decimal(18,2)) as BalQty "\
          ",Plant.Longdescription as DIVCODE "\
          ",0 as chalanret"\
          " From StockTransaction ST "\
          " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code "\
          " JOIN FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE "\
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
           " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE "\
           " And     FIKD.ItemUniqueId             = Product.AbsUniqueId "\
           " Join ProductIE               ON           Product.ITEMTYPECODE    = ProductIE.ITEMTYPECODE "\
           " AND     COALESCE(Product.SubCode01, '') = COALESCE(ProductIE.SubCode01, '') "\
           " AND     COALESCE(Product.SubCode02, '') = COALESCE(ProductIE.SubCode02, '') "\
           " AND     COALESCE(Product.SubCode03, '') = COALESCE(ProductIE.SubCode03, '') "\
           " AND     COALESCE(Product.SubCode04, '') = COALESCE(ProductIE.SubCode04, '') "\
           " AND     COALESCE(Product.SubCode05, '') = COALESCE(ProductIE.SubCode05, '') "\
           " AND     COALESCE(Product.SubCode06, '') = COALESCE(ProductIE.SubCode06, '') "\
           " AND     COALESCE(Product.SubCode07, '') = COALESCE(ProductIE.SubCode07, '') "\
           " AND     COALESCE(Product.SubCode08, '') = COALESCE(ProductIE.SubCode08, '') "\
           " AND     COALESCE(Product.SubCode09, '') = COALESCE(ProductIE.SubCode09, '') "\
           " AND     COALESCE(Product.SubCode10, '') = COALESCE(ProductIE.SubCode10, '') "\
           " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE "\
           " Join Costcenter                 On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.CODE "\
           " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code  "\
           " Where ST.TRANSACTIONDATE <=   '"+enddate+"'  "\
           " And ST.TemplateCode not in('QC1','QCR')  "+LSCompany+LSItemGroup+LSItem+""\
           " Group by Plant.Longdescription,ProductIE.SERVICEBILLFLAG,Product.ItemTypeCode,Product.Longdescription "\
           " Having Sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0  "\
          " End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End) != 0 Or Sum(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"'  "\
          " And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End) != 0 Or Sum(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"'  "\
          " And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End) != 0 Or Sum(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case  "\
          " When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End) != 0  "\
          " Order By DIVCODE,ITEMGROUP,ServiceType,ITEM"
    
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result==False:
        return
    while result != False:
        pdfrpt.sumtextsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.sumdvalue(stdt,etdt,pdfrpt.sumdivisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt.boldfonts(8)
    pdfrpt.c.drawString(200, pdfrpt.d, "Group Total : ")
    pdfrpt.c.drawAlignedString(430, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrpOpnTotal)))
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrpRecTotal)))
    pdfrpt.c.drawAlignedString(530, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrpIssTotal)))
    # c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssRetTotal)))
    pdfrpt.c.drawAlignedString(580, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrpChlRetTotal)))
    pdfrpt.SumGrpOpnTotal = 0
    pdfrpt.SumGrpRecTotal = 0
    pdfrpt.SumGrpIssTotal = 0
    pdfrpt.SumGrpChlRetTotal = 0

    pdfrpt.d=pdfrpt.sumdvalue(stdt,etdt,pdfrpt.sumdivisioncode)
    pdfrpt.c.drawString(200, pdfrpt.d, "Grand Total : ")
    pdfrpt.c.drawAlignedString(430, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrandOpnTotal)))
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrandRecTotal)))
    pdfrpt.c.drawAlignedString(530, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrandIssTotal)))
    # c.drawAlignedString(530, d, str("%.2f" % float(SumGrpIssRetTotal)))
    pdfrpt.c.drawAlignedString(580, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrandChlRetTotal)))
    pdfrpt.SumGrandOpnTotal=0
    pdfrpt.SumGrandRecTotal=0
    pdfrpt.SumGrandIssTotal=0
    pdfrpt.SumGrandChlRetTotal=0
    
    
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt.sumnewrequest()
    pdfrpt.d=pdfrpt.newpage()
