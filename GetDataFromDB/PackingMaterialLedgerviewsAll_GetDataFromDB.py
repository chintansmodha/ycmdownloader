from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import PackingMaterialLedger_FormLoad as views
from PrintPDF import PackingMaterialLedgerAll_PrintPDF as pdfrpt
from ProcessSelection import PackingMaterialLedger_ProcessSelection as PMLV
counter=0
new=0
def PackingMaterialLedgerAll_PrintPDF(LSCompany, LSParty, LSItem,LSPalleteType, LSReportType, LCCompany,LCParty, LCItem,LCPalleteType,LDStartDate, LDEndDate,request):
    global new
    new = 0
    company = str(LSCompany)
    party = str(LSParty)
    item = str(LSItem)
    palletetype = str(LSPalleteType)
    reporttype = str(LSReportType)
    stdate = str(LDStartDate)
    etdate = str(LDEndDate)
    startdate = "'" + LDStartDate + "'"
    enddate = "'" + LDEndDate + "'"
    LSCompanys = '(' + company[1:-1] + ')'
    LSPartys = '(' + party[1:-1] + ')'
    LSItems = '(' + item[1:-1] + ')'
    LSPalleteTypes = '(' + palletetype[1:-1] + ')'
    # print("Sanika")

    if not LCCompany and not LSCompany:
        Company = ""
    elif LCCompany:
        Company = " "
    elif LSCompany:
        Company = " AND PLANT.CODE in " + str(LSCompanys)

    if not LCParty and not LSParty:
        Party = ""
    elif LCParty:
        Party = " "
    elif LSParty:
        Party = " And BP.NumberId in " + str(LSPartys)

    if not LCItem and not LSItem:
        Item = ""
    elif LCItem:
        Item = " "
    elif LSItem:
        Item = " AND IDL.ITEMTYPEAFICODE IN " + str(LSItems)

    if not LCPalleteType and not LSPalleteType:
        PalleteType = ""
    elif LCPalleteType:
        PalleteType = " "
    elif LSPalleteType:
        PalleteType = "  " + str(LSPalleteTypes)

    sql="SELECT PLANT.LONGDESCRIPTION AS PLANTNAME" \
        " ,plant.companycode as companycode" \
        " ,ID.TEMPLATECODE AS TYPEOF" \
        " ,'' AS ECXNO" \
        " ,'' AS EXCDATE" \
        " ,BP.LEGALNAME1 AS CUSTOMER" \
        " ,ID.PROVISIONALCODE AS InvNo" \
        " ,ID.PROVISIONALDOCUMENTDATE AS InvDate" \
        " ,PRODUCT.SUBCODE01 AS PALLETETYPECODE" \
        " ,PRODUCT.LONGDESCRIPTION AS PALLETNAME" \
        " ,Case When  ID.TEMPLATECODE In ('PMC') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End as ReceivedQuantity" \
        " ,Case When  ID.TEMPLATECODE In ('PMS') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End as IssuedQuantity" \
        " ,-ABS(Case When  ID.TEMPLATECODE In ('PMS') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End) AS BALANCE" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN INTERNALORDERTEMPLATE AS IOT       ON      ID.TemplateCode = IOT.Code" \
        " JOIN LOGICALWAREHOUSE                   ON      IDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN ORDERPARTNER AS OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     IOT.DESTINATIONTYPE     = OP.CustomerSupplierType" \
        " AND     OP.CustomerSupplierType = 2" \
        " JOIN BUSINESSPARTNER AS BP              ON      OP.OrderBusinessPartnerNumberId = BP.NumberId" \
        " JOIN FullItemKeyDecoder FIKD            ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
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
        " JOIN PRODUCT                            ON      IDL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = PRODUCT.AbsUniqueId" \
        " JOIN QUALITYLEVEL                       ON      IDL.QUALITYCODE = QUALITYLEVEL.CODE" \
        " AND     IDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.TEMPLATECODE = 'PMS'  " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
        " And ID.PROVISIONALDOCUMENTDATE Between "+startdate+" And "+enddate+" " \
        " Union " \
        " Select  PLANT.LONGDESCRIPTION AS PLANTNAME" \
        " ,plant.companycode as companycode" \
        " ,ID.TEMPLATECODE AS TYPEOF" \
        " ,'' AS ECXNO" \
        " ,'' AS EXCDATE" \
        " ,BP.LEGALNAME1 AS CUSTOMER" \
        " ,ID.PROVISIONALCODE AS InvNo" \
        " ,ID.PROVISIONALDOCUMENTDATE AS InvDate" \
        " ,PRODUCT.SUBCODE01 AS PalletTypeCode" \
        " ,Product.LONGDESCRIPTION AS PalletName" \
        " ,Case When  ID.TEMPLATECODE In ('PMC') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End as ReceivedQuantity" \
        " ,0 As IssuedQuantity" \
        " ,ABS(Case When  ID.TEMPLATECODE In ('PMC') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End) AS BALANCE" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN INTERNALORDERTEMPLATE AS IOT       ON      ID.TemplateCode = IOT.Code" \
        " JOIN LOGICALWAREHOUSE                   ON      IDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN ORDERPARTNER AS OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     IOT.DESTINATIONTYPE     = OP.CustomerSupplierType" \
        " AND     OP.CustomerSupplierType = 1" \
        " JOIN BUSINESSPARTNER AS BP              ON      OP.OrderBusinessPartnerNumberId = BP.NumberId" \
        " JOIN FullItemKeyDecoder AS FIKD         ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
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
        " Join Product                            ON      IDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = Product.AbsUniqueId" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.TEMPLATECODE = 'PMC' " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
        " And ID.PROVISIONALDOCUMENTDATE Between "+startdate+" And "+enddate+" " \
        " Union " \
        " Select  PKG.PLANTNAME,PKG.COMPANYCODE,PKG.TYPEOF,PKG.ECXNO,PKG.EXCDATE,PKG.CUSTOMER" \
        " ,PKG.InvNo,PKG.InvDate, PKG.PalletTypeCode, PKG.PalletName, 0 As ReceivedQuantity, Sum(PKG.PalletQuantity) As IssuedQuantity,-ABS(PKG.PalletQuantity) AS BALANCE" \
        " From" \
        " (Select PLANT.LONGDESCRIPTION AS PLANTNAME," \
        " plant.companycode as companycode," \
        " SD.TEMPLATECODE AS TYPEOF," \
        " '' AS ECXNO," \
        " '' AS EXCDATE," \
        " BP.LEGALNAME1 AS CUSTOMER," \
        " PlantInvoice.CODE As InvNo," \
        " PlantInvoice.INVOICEDATE As InvDate," \
        " BKLE.PalletType1Code As PalletTypeCode," \
        " UGG.LongDescription As PalletName," \
        " BKLE.PalletQuantity1 As PalletQuantity" \
        " From    PlantInvoice" \
        " JOIN SalesDocument SD           ON      PlantInvoice.CODE                     = SD.PROVISIONALCODE" \
        " and     SD.DocumentTypeType = '06'" \
        " JOIN SalesDocumentLine SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE      = SD.PROVISIONALCODE" \
        " AND     SDL.SALDOCPROVISIONALCOUNTERCODE      = SD.PROVISIONALCOUNTERCODE" \
        " And     SDL.DocumentTypeType  = '06'" \
        " JOIN LOGICALWAREHOUSE           ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                      ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN OrderPartner AS OP         ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 1" \
        " JOIN BusinessPartner AS BP      ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
        " JOIN StockTransaction ST        ON      SDL.PreviousCode      = ST.OrderCode" \
        " AND     ST.TemplateCode         = 'S04'" \
        " And ST.TransactionDetailNumber = (Select Min(ST1.TransactionDetailNumber) From StockTransaction ST1 Where ST1.ContainerElementCode = ST.ContainerElementCode)" \
        " JOIN BKLElements BKLE           ON      ST.CONTAINERELEMENTCODE                 = BKLE.Code" \
        " AND     ST.CONTAINERSUBCODE01                   = BKLE.SubCodeKey" \
        " AND     BKLE.ItemTypeCode                       = 'CNT'" \
        " JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode            = 'PKG'" \
        " AND     BKLE.PalletType1Code                    = UGG.Code" \
        " Where   BKLE.PalletType1Code is Not Null" +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
        " Union" \
        " Select  PLANT.LONGDESCRIPTION AS PLANTNAME," \
        " plant.companycode as companycode," \
        " SD.TEMPLATECODE AS TYPEOF," \
        " '' AS ECXNO," \
        " '' AS EXCDATE," \
        " BP.LEGALNAME1 AS CUSTOMER," \
        " PlantInvoice.CODE As InvNo," \
        " PlantInvoice.INVOICEDATE As InvDate," \
        " BKLE.PalletType2Code As PalletTypeCode," \
        " UGG.LongDescription As PalletName," \
        " BKLE.PalletQuantity2 As PalletQuantity" \
        " From    PlantInvoice" \
        " JOIN SalesDocument SD           ON      PlantInvoice.CODE                     = SD.PROVISIONALCODE" \
        " and     SD.DocumentTypeType = '06'" \
        " JOIN SalesDocumentLine SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE      = SD.PROVISIONALCODE" \
        " AND     SDL.SALDOCPROVISIONALCOUNTERCODE      = SD.PROVISIONALCOUNTERCODE" \
        " And     SDL.DocumentTypeType  = '06'" \
        " JOIN LOGICALWAREHOUSE           ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                      ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN OrderPartner AS OP         ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 1" \
        " JOIN BusinessPartner AS BP      ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
        " JOIN StockTransaction ST        ON      SDL.PreviousCode      = ST.OrderCode" \
        " AND     ST.TemplateCode         = 'S04'" \
        " And ST.TransactionDetailNumber = (Select Min(ST1.TransactionDetailNumber) From StockTransaction ST1 Where ST1.ContainerElementCode = ST.ContainerElementCode)" \
        " JOIN BKLElements BKLE           ON      ST.CONTAINERELEMENTCODE                 = BKLE.Code" \
        " AND     ST.CONTAINERSUBCODE01                   = BKLE.SubCodeKey" \
        " AND     BKLE.ItemTypeCode                       = 'CNT'" \
        " JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode            = 'PKG'" \
        " AND     BKLE.PalletType2Code                    = UGG.Code" \
        " Where   BKLE.PalletType2Code is Not Null" +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
        " Union" \
        " Select  PLANT.LONGDESCRIPTION AS PLANTNAME," \
        " plant.companycode as companycode," \
        " SD.TEMPLATECODE AS TYPEOF," \
        " '' AS ECXNO," \
        " '' AS EXCDATE," \
        " BP.LEGALNAME1 AS CUSTOMER," \
        " PlantInvoice.CODE As InvNo," \
        " PlantInvoice.INVOICEDATE As InvDate," \
        " BKLE.PalletType3Code As PalletTypeCode," \
        " UGG.LongDescription As PalletName," \
        " BKLE.PalletQuantity3 As PalletQuantity" \
        " From    PlantInvoice" \
        " JOIN SalesDocument SD           ON      PlantInvoice.CODE                     = SD.PROVISIONALCODE" \
        " and     SD.DocumentTypeType = '06'" \
        " JOIN SalesDocumentLine SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE      = SD.PROVISIONALCODE" \
        " AND     SDL.SALDOCPROVISIONALCOUNTERCODE      = SD.PROVISIONALCOUNTERCODE" \
        " And     SDL.DocumentTypeType  = '06'" \
        " JOIN LOGICALWAREHOUSE           ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                      ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN OrderPartner AS OP         ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 1" \
        " JOIN BusinessPartner AS BP      ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
        " JOIN StockTransaction ST        ON      SDL.PreviousCode      = ST.OrderCode" \
        " AND     ST.TemplateCode         = 'S04'" \
        " And ST.TransactionDetailNumber = (Select Min(ST1.TransactionDetailNumber) From StockTransaction ST1 Where ST1.ContainerElementCode = ST.ContainerElementCode)" \
        " JOIN BKLElements BKLE           ON      ST.CONTAINERELEMENTCODE                 = BKLE.Code" \
        " AND     ST.CONTAINERSUBCODE01                   = BKLE.SubCodeKey" \
        " AND     BKLE.ItemTypeCode                       = 'CNT'" \
        " JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode            = 'PKG'" \
        " AND     BKLE.PalletType3Code                    = UGG.Code" \
        " Where   BKLE.PalletType3Code is Not Null" +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
        " Union" \
        " Select  PLANT.LONGDESCRIPTION AS PLANTNAME," \
        " plant.companycode as companycode," \
        " SD.TEMPLATECODE AS TYPEOF," \
        " '' AS ECXNO," \
        " '' AS EXCDATE," \
        " BP.LEGALNAME1 AS CUSTOMER," \
        " PlantInvoice.CODE As InvNo," \
        " PlantInvoice.INVOICEDATE As InvDate," \
        " BKLE.PalletType4Code As PalletTypeCode," \
        " UGG.LongDescription As PalletName," \
        " BKLE.PalletQuantity4 As PalletQuantity" \
        " From    PlantInvoice" \
        " JOIN SalesDocument SD           ON      PlantInvoice.CODE                     = SD.PROVISIONALCODE" \
        " and     SD.DocumentTypeType = '06'" \
        " JOIN SalesDocumentLine SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE      = SD.PROVISIONALCODE" \
        " AND     SDL.SALDOCPROVISIONALCOUNTERCODE      = SD.PROVISIONALCOUNTERCODE" \
        " And     SDL.DocumentTypeType  = '06'" \
        " JOIN LOGICALWAREHOUSE           ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                      ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN OrderPartner AS OP         ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 1" \
        " JOIN BusinessPartner AS BP      ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
        " JOIN StockTransaction ST        ON      SDL.PreviousCode      = ST.OrderCode" \
        " AND     ST.TemplateCode         = 'S04'" \
        " And ST.TransactionDetailNumber = (Select Min(ST1.TransactionDetailNumber) From StockTransaction ST1 Where ST1.ContainerElementCode = ST.ContainerElementCode)" \
        " JOIN BKLElements BKLE           ON      ST.CONTAINERELEMENTCODE                 = BKLE.Code" \
        " AND     ST.CONTAINERSUBCODE01                   = BKLE.SubCodeKey" \
        " AND     BKLE.ItemTypeCode                       = 'CNT'" \
        " JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode            = 'PKG'" \
        " AND     BKLE.PalletType4Code                    = UGG.Code" \
        " Where   BKLE.PalletType4Code is Not Null" +Company+" " +Party+" " +Item+" " +PalleteType+ " "  \
        " Union" \
        " Select  PLANT.LONGDESCRIPTION AS PLANTNAME," \
        " plant.companycode as companycode," \
        " SD.TEMPLATECODE AS TYPEOF," \
        " '' AS ECXNO," \
        " '' AS EXCDATE," \
        " BP.LEGALNAME1 AS CUSTOMER," \
        " PlantInvoice.CODE As InvNo," \
        " PlantInvoice.INVOICEDATE As InvDate," \
        " BKLE.PalletType5Code As PalletTypeCode," \
        " UGG.LongDescription As PalletName," \
        " BKLE.PalletQuantity5 As PalletQuantity" \
        " From    PlantInvoice" \
        " JOIN SalesDocument SD           ON      PlantInvoice.CODE                     = SD.PROVISIONALCODE" \
        " and     SD.DocumentTypeType = '06'" \
        " JOIN SalesDocumentLine SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE      = SD.PROVISIONALCODE" \
        " AND     SDL.SALDOCPROVISIONALCOUNTERCODE      = SD.PROVISIONALCOUNTERCODE" \
        " And     SDL.DocumentTypeType  = '06'" \
        " JOIN LOGICALWAREHOUSE           ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                      ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN OrderPartner AS OP         ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 1" \
        " JOIN BusinessPartner AS BP      ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
        " JOIN StockTransaction ST        ON      SDL.PreviousCode      = ST.OrderCode" \
        " AND     ST.TemplateCode         = 'S05'" \
        " And ST.TransactionDetailNumber = (Select Min(ST1.TransactionDetailNumber) From StockTransaction ST1 Where ST1.ContainerElementCode = ST.ContainerElementCode)" \
        " JOIN BKLElements BKLE           ON      ST.CONTAINERELEMENTCODE                 = BKLE.Code" \
        " AND     ST.CONTAINERSUBCODE01                   = BKLE.SubCodeKey" \
        " AND     BKLE.ItemTypeCode                       = 'CNT'" \
        " JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode            = 'PKG'" \
        " AND     BKLE.PalletType5Code                    = UGG.Code" \
        " Where   BKLE.PalletType5Code is Not Null "+Company+" " +Party+" " +Item+" " +PalleteType+ "  ) As PKG " \
        " WHERE PKG.COMPANYCODE='100' And PKG.InvDate Between "+startdate+" And  "+enddate+" " \
        " Group By PKG.PLANTNAME,PKG.COMPANYCODE,PKG.TYPEOF,PKG.ECXNO,PKG.EXCDATE,PKG.CUSTOMER,PKG.InvNo,InvDate, PKG.PalletTypeCode, PKG.PalletName,-ABS(PKG.PalletQuantity) " \
        "union " \
        "Select  Plant.LongDescription As PLANTNAME " \
        ", plant.companycode as companycode  " \
        ", 'MRN' As TypeOf " \
        ", '' AS ECXNO " \
        ", '' AS EXCDATE " \
        ", BP.LEGALNAME1 AS CUSTOMER " \
        ", Varchar(MRNHeader.Code)  AS InvNO " \
        ", MRNHeader.MRNDate AS InvDAte " \
        ", UGG.Code AS PALLETETYPECODE " \
        ", UGG.LongDescription AS PALLETENAME " \
        ", PMD.PrimaryQuantity As ReceivedQuantity " \
        ", 0 As IssuedQuantity " \
        ", PMD.PrimaryQuantity AS BALANCE " \
        "From    BKLPACKINGMRNDETAIL PMD " \
        "JOIN LogicalWarehouse           ON      PMD.WarehouseCode               = LogicalWarehouse.Code " \
        "JOIN Plant                      ON      LogicalWarehouse.PlantCode      = Plant.Code " \
        "JOIN MRNHeader                  ON      PMD.MRNHEADERCODE        =  MRNHEADER.CODE " \
        "JOIN ORDERPARTNER AS OP         ON      MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode " \
        "AND     MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE     = OP.CustomerSupplierType " \
        "JOIN BUSINESSPARTNER AS BP              ON      OP.OrderBusinessPartnerNumberId = BP.NumberId " \
        "JOIN AdStorage COPPKGSubcode01  ON      COPPKGSubcode01.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode01.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode01.FieldName       = 'COPPKGSubcode01' " \
        "AND     COPPKGSubcode01.ValueString     = PMD.Subcode01 " \
        "JOIN AdStorage COPPKGSubcode02  ON      COPPKGSubcode02.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode02.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode02.FieldName       = 'COPPKGSubcode02' " \
        "AND     COPPKGSubcode02.ValueString     = PMD.Subcode02 " \
        "JOIN AdStorage COPPKGSubcode03  ON      COPPKGSubcode03.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode03.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode03.FieldName       = 'COPPKGSubcode03' " \
        "AND     COPPKGSubcode03.ValueString     = PMD.Subcode03 " \
        "JOIN AdStorage COPPKGSubcode04  ON      COPPKGSubcode04.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode04.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode04.FieldName       = 'COPPKGSubcode04' " \
        "AND     COPPKGSubcode04.ValueString     = PMD.Subcode04 " \
        "JOIN AdStorage COPPKGSubcode05  ON      COPPKGSubcode05.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode05.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode05.FieldName       = 'COPPKGSubcode05' " \
        "AND     COPPKGSubcode05.ValueString     = PMD.Subcode05 " \
        "JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode    = 'PKG' " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode01.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode02.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode03.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode04.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode05.UniqueId " \
        "Where   PMD.ItemTypeCode = 'PKG' "+Company+" "+Party+" "+PalleteType+" " \
        " And MRNHeader.MRNDate Between "+startdate+" And "+enddate+" " \
        " Order By PLANTNAME,CUSTOMER,InvDate,InvNo"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    # print("Sanika")

    # if result == False:
    #     PMLV.Exceptions = "Note: No Result found according to your selected criteria "
    #     return render(request, "PackingMaterialLedger.html",
    #                   {'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty, 'GDataItem': views.GDataItem,
    #                    'Exception': PMLV.Exceptions})

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.plantcode)
        result = con.db.fetch_both(stmt)
        if pdfrpt.d < 20:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.d, result, pdfrpt.plantcode)

    if result == False:
        if counter > 0:
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.plantcode)
            pdfrpt.printtotal(pdfrpt.d)
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.plantcode)
            pdfrpt.grandtotal()
            pdfrpt.companyclean()
            PMLV.Exceptions = ""
        elif counter == 0:
            PMLV.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.companyclean()
