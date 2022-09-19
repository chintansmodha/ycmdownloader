from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import PackingMaterialLedger_FormLoad as views
from PrintPDF import PackingMaterialLedgerCustomer_PrintPDF as pdfrpt
from ProcessSelection import PackingMaterialLedger_ProcessSelection as PMLV
counter=0
new=0
def PackingMaterialLedgerCustomer_PrintPDF(LSCompany, LSParty, LSItem,LSPalleteType, LSReportType, LCCompany, LCParty, LCItem,LCPalleteType,LDStartDate, LDEndDate,request):
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

    # if LSCompany or LSParty or LSItem or LSPalleteType:
    #     where = 'where'
    # else:
    #     where = ''

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
        PalleteType = " AND UGG.Code IN " + str(LSPalleteTypes)

    sql="Select  PLANT.LONGDESCRIPTION AS PLANTNAME" \
        " ,plant.companycode as companycode" \
        " ,ID.TEMPLATECODE AS TYPEOF" \
        " ,'' AS ECXNO" \
        " ,'' AS EXCDATE" \
        " ,BP.LEGALNAME1 AS CUSTOMER" \
        " ,ID.PROVISIONALCODE AS InvNo" \
        " ,ID.PROVISIONALDOCUMENTDATE AS InvDate" \
        " ,PRODUCT.SUBCODE01 AS PalletTypeCode" \
        " ,UGG.LONGDESCRIPTION AS PalletName" \
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
        " Join    UserGenericGroup UGG            On      UGG.UserGenericGroupTypeCode    = 'PKG'" \
        " Join    AdStorage AD_COPPKGItemType     On      AD_COPPKGItemType.NameEntityName = 'UserGenericGroup' And AD_COPPKGItemType.NameName = 'COPPKG'" \
        " And     AD_COPPKGItemType.FieldName = 'COPPKGItemTypeCode'" \
        " And     UGG.AbsUniqueId                 = AD_COPPKGItemType.UniqueId" \
        " Join    AdStorage AD_COPPKGSubCode01    On      AD_COPPKGSubCode01.NameEntityName = 'UserGenericGroup' And AD_COPPKGSubCode01.NameName = 'COPPKG'" \
        " And     AD_COPPKGSubcode01.FieldName = 'COPPKGSubcode01'" \
        " And     UGG.AbsUniqueId                 = AD_COPPKGSubCode01.UniqueId" \
        " Join    AdStorage AD_COPPKGSubcode02    On      AD_COPPKGSubcode02.NameEntityName = 'UserGenericGroup' And AD_COPPKGSubcode02.NameName = 'COPPKG'" \
        " And     AD_COPPKGSubcode02.FieldName = 'COPPKGSubcode02'" \
        " And     UGG.AbsUniqueId                 = AD_COPPKGSubCode02.UniqueId" \
        " Join    AdStorage AD_COPPKGSubcode03    On      AD_COPPKGSubcode03.NameEntityName = 'UserGenericGroup' And AD_COPPKGSubcode03.NameName = 'COPPKG'" \
        " And     AD_COPPKGSubcode03.FieldName = 'COPPKGSubcode03'" \
        " And     UGG.AbsUniqueId                 = AD_COPPKGSubCode03.UniqueId" \
        " Join    AdStorage AD_COPPKGSubcode04    On      AD_COPPKGSubcode04.NameEntityName = 'UserGenericGroup' And AD_COPPKGSubcode04.NameName = 'COPPKG'" \
        " And     AD_COPPKGSubcode04.FieldName = 'COPPKGSubcode04'" \
        " And     UGG.AbsUniqueId                 = AD_COPPKGSubCode04.UniqueId" \
        " Join    AdStorage AD_COPPKGSubcode05    On      AD_COPPKGSubcode05.NameEntityName = 'UserGenericGroup' And AD_COPPKGSubcode05.NameName = 'COPPKG'" \
        " And     AD_COPPKGSubcode05.FieldName = 'COPPKGSubcode05'" \
        " And     UGG.AbsUniqueId                 = AD_COPPKGSubCode05.UniqueId" \
        " AND     IDL.ItemTypeAfiCode     = AD_COPPKGItemType.ValueString" \
        " And     IDL.SubCode01           = AD_COPPKGSubCode01.ValueString" \
        " And     IDL.SubCode02           = AD_COPPKGSubCode02.ValueString" \
        " And     IDL.SubCode03           = AD_COPPKGSubCode03.ValueString" \
        " And     IDL.SubCode04           = AD_COPPKGSubCode04.ValueString" \
        " And     IDL.SubCode05           = AD_COPPKGSubCode05.ValueString" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.TEMPLATECODE = 'PMC'  " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
        "And ID.PROVISIONALDOCUMENTDATE Between "+startdate+" And "+enddate+" " \
        " Union All" \
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
        " Where   BKLE.PalletType1Code is Not Null " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
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
        " Where   BKLE.PalletType2Code is Not Null " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
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
        " Where   BKLE.PalletType3Code is Not Null " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
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
        " Where   BKLE.PalletType4Code is Not Null " +Company+" " +Party+" " +Item+" " +PalleteType+ " " \
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
        " Where   BKLE.PalletType5Code is Not Null " +Company+" " +Party+" " +Item+" " +PalleteType+ " ) As PKG " \
        " WHERE PKG.COMPANYCODE='100' And PKG.InvDate Between "+startdate+" And "+enddate+" " \
        "Group By PKG.PLANTNAME,PKG.COMPANYCODE,PKG.TYPEOF,PKG.ECXNO,PKG.EXCDATE,PKG.CUSTOMER,PKG.InvNo,InvDate, PKG.PalletTypeCode, PKG.PalletName,-ABS(PKG.PalletQuantity)" \
        " Order By PLANTNAME,CUSTOMER,PalletName, InvDate"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # print(sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(PalleteType)
    # print(result)
    # print("Sanika")

    if result == False:
        PMLV.Exceptions = "Note: No Result found according to your selected criteria "
        return render(request, "PackingMaterialLedger.html",
                      {'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty, 'GDataItem': views.GDataItem,
                       'Exception': PMLV.Exceptions})
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.plantcode)
        result = con.db.fetch_both(stmt)
        if pdfrpt.d < 20:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.d,result, pdfrpt.plantcode)

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