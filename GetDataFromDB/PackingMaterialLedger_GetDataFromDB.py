from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import PackingMaterialLedger_FormLoad as views
from PrintPDF import PackingMaterialLedgerSupplier_PrintPDF as pdfrpt
from ProcessSelection import PackingMaterialLedger_ProcessSelection as PMLV
counter=0

def PackingMaterialLedgerSupplier_PrintPDF(LSCompany, LSParty, LSItem, LSPalleteType,LSReportType, LCCompany,LCParty, LCItem,LCPalleteType,LDStartDate, LDEndDate,request):
    global new
    company = str(LSCompany)
    party = str(LSParty)
    item = str(LSItem)
    palletetype=str(LSPalleteType)
    reporttype = str(LSReportType)
    startdate = "'" + LDStartDate + "'"
    enddate = "'" + LDEndDate + "'"
    # stdate = str(LDStartDate)
    # etdate = str(LDEndDate)
    LSCompanys = '(' + company[1:-1] + ')'
    LSPartys = '(' + party[1:-1] + ')'
    LSItems = '(' + item[1:-1] + ')'
    LSPalleteTypes = '(' + palletetype[1:-1] + ')'

    if not LCCompany and not LSCompany:
        Company = ""
    elif LCCompany:
        Company = " "
    elif LSCompany:
        Company = "AND PLANT.CODE in " + str(LSCompanys)

    if not LCParty and not LSParty:
        Party = ""
    elif LCParty:
        Party = " "
    elif LSParty:
        Party = " And BP.NumberId in " + str(LSPartys)

    # if not LCItem and not LSItem:
    #     Item = ""
    # elif LCItem:
    #     Item = " "
    # elif LSItem:
    #     Item = " AND IDL.ITEMTYPEAFICODE IN " + str(LSItems)

    if not LCPalleteType and not LSPalleteType:
        PalleteType = ""
    elif LCPalleteType:
        PalleteType = " "
    elif LSPalleteType:
        PalleteType = " And UGG.CODE IN " + str(LSPalleteTypes)

    sql="SELECT PLANT.LONGDESCRIPTION AS PLANTNAME " \
        ",ID.PROVISIONALCODE AS GATEPASSNO " \
        ",ID.PROVISIONALDOCUMENTDATE AS GATEPASSDATE " \
        ", 'IND' AS TYPEOF " \
        ",'' AS ECXNO " \
        ",'' AS EXCDATE " \
        ",Case When  ID.TEMPLATECODE In ('PMC') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End as RECDQTY " \
        ",Case When  ID.TEMPLATECODE In ('PMS') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End as ISSQTY " \
        ",-ABS(Case When  ID.TEMPLATECODE In ('PMS') And ID.PROVISIONALDOCUMENTDATE>='01-01-1900' Then IDL.USERPRIMARYQUANTITY Else 0 End) AS BALANCE " \
        ",BP.LEGALNAME1 AS SUPPLIER " \
        ", UGG.Code AS PALLETETYPECODE " \
        ", UGG.LONGDESCRIPTION AS PALLETENAME " \
        "FROM INTERNALDOCUMENT AS ID " \
        "JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE  " \
        "AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE " \
        "JOIN INTERNALORDERTEMPLATE AS IOT       ON      ID.TemplateCode = IOT.Code " \
        "JOIN LOGICALWAREHOUSE                   ON      IDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
        "JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE " \
        "JOIN ORDERPARTNER AS OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode " \
        "AND     IOT.DESTINATIONTYPE     = OP.CustomerSupplierType " \
        "AND     OP.CustomerSupplierType = 2 " \
        "JOIN BUSINESSPARTNER AS BP              ON      OP.OrderBusinessPartnerNumberId = BP.NumberId " \
        "JOIN AdStorage COPPKGSubcode01  ON      COPPKGSubcode01.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode01.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode01.FieldName       = 'COPPKGSubcode01' " \
        "AND     COPPKGSubcode01.ValueString     = IDL.Subcode01 " \
        "JOIN AdStorage COPPKGSubcode02  ON      COPPKGSubcode02.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode02.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode02.FieldName       = 'COPPKGSubcode02' " \
        "AND     COPPKGSubcode02.ValueString     = IDL.Subcode02 " \
        "JOIN AdStorage COPPKGSubcode03  ON      COPPKGSubcode03.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode03.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode03.FieldName       = 'COPPKGSubcode03' " \
        "AND     COPPKGSubcode03.ValueString     = IDL.Subcode03 " \
        "JOIN AdStorage COPPKGSubcode04  ON      COPPKGSubcode04.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode04.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode04.FieldName       = 'COPPKGSubcode04' " \
        "AND     COPPKGSubcode04.ValueString     = IDL.Subcode04 " \
        "JOIN AdStorage COPPKGSubcode05  ON      COPPKGSubcode05.NameEntityName  = 'UserGenericGroup' " \
        "AND     COPPKGSubcode05.NameName        = 'COPPKG' " \
        "AND     COPPKGSubcode05.FieldName       = 'COPPKGSubcode05' " \
        "AND     COPPKGSubcode05.ValueString     = IDL.Subcode05 " \
        "JOIN UserGenericGroup UGG       ON      UGG.UserGenericGroupTypeCode    = 'PKG' " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode01.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode02.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode03.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode04.UniqueId " \
        "AND     UGG.AbsUniqueId                 = COPPKGSubcode05.UniqueId " \
        "JOIN QUALITYLEVEL                       ON      IDL.QUALITYCODE = QUALITYLEVEL.CODE " \
        "AND     IDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
        "WHERE ID.DocumentTypeType = '05'  AND ID.TEMPLATECODE = 'PMS' "+Company+" "+Party+" "+PalleteType+" " \
        "And ID.PROVISIONALDOCUMENTDATE Between "+startdate+" And "+enddate+" " \
        "union " \
        "Select  Plant.LongDescription As PLANTNAME " \
        ", Varchar(MRNHeader.Code)  AS GATEPASSNO " \
        ", MRNHeader.MRNDate AS GATEPASSDATE " \
        ", 'MRN' As TypeOf " \
        ", '' AS ECXNO " \
        ", '' AS EXCDATE " \
        ", PMD.PrimaryQuantity As RECDQTY " \
        ", 0 As IssQty " \
        ", PMD.PrimaryQuantity AS BALANCE " \
        ", BP.LEGALNAME1 AS SUPPLIER " \
        ", UGG.Code AS PALLETETYPECODE " \
        ", UGG.LongDescription AS PALLETENAME " \
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
        "And MRNHeader.MRNDate Between "+startdate+" And "+enddate+" " \
        "ORDER BY PLANTNAME,SUPPLIER,PALLETENAME,GATEPASSDATE "

    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)

    # if result==False:
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