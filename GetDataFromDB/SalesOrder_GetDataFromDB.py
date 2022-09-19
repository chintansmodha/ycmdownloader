from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import SalesOrder_PrintPDF as pdfrpt


def SalesOrder_GetData(LSDivision,LSAgent,LSParty,LSDocumentType,LSTemplate,LCDivision,LCAgent,LCParty,LCDocumentType,LCTemplate,LDStartDate,LDEndDate):
    if not LCDivision and not LSDivision or LCDivision:
        LSDivision = " "
    elif LSDivision:
        LSDivision = " AND FINBUSINESSUNIT.CODE in (" + str(LSDivision)[1:-1] + ")"

    if not LCAgent and not LSAgent or LCAgent:
        LSAgent = " "
    elif LSAgent:
        LSAgent = " AND FINBUSINESSUNIT.CODE in (" + str(LSAgent)[1:-1] + ")"

    if not LCParty and not LSParty or LCParty:
        LSParty = " "
    elif LSParty:
        LSParty = " AND FINBUSINESSUNIT.CODE in (" + str(LSParty)[1:-1] + ")"
    
    if not LCDocumentType and not LSDocumentType or LCDocumentType:
        LSDocumentType = " "
    elif LSDocumentType:
        LSDocumentType = " AND FINBUSINESSUNIT.CODE in (" + str(LSDocumentType)[1:-1] + ")"
    
    if not LCTemplate and not LSTemplate or LCTemplate:
        LSTemplate = " "
    elif LSTemplate:
        LSTemplate = " AND FINBUSINESSUNIT.CODE in (" + str(LSTemplate)[1:-1] + ")"


    stdt = datetime.strptime(LDStartDate, "%Y-%m-%d").date()
    etdt = datetime.strptime(LDEndDate, "%Y-%m-%d").date()

    sql=("Select  Division.Longdescription as Divcode "
        ",Plant.Longdescription as Company "
        ",SO.TEMPLATECODE as Temp "
        ",SO.DOCUMENTTYPETYPE as DocType "
        ",SO.CODE As OrdNo   "
        ",SO.ORDERDATE As OrdDt "
        ",SO.ORDERDATE as reqduedate "
        ",BP.legalname1||' '||BP.Addressline1||'-'||BP.numberid as customer "
        ",BP.legalname1||' '||BP.Addressline1||'-'||BP.numberid as consignee "
        ",AGENT.LONGDESCRIPTION||'-'||AGENT.CODE as broker "
        ", SO.CODE As ContNo   "
          ", PRODUCT.LONGDESCRIPTION||'-'||COALESCE(QUALITYLEVEL.LONGDESCRIPTION,'') As Item   "
          ", COALESCE(UGG.CODE,'') As Shade   "
          ", SOL.ITEMTYPEAFICODE As ItemTyp   "
          ", COALESCE(Cast(ContRate.BASEVALUE AS DEcimal(20,2)),0) As ContractRate   "
          ", COALESCE(Cast(BillRate.BASEVALUE AS DEcimal(20,2)),0) As BillRat   "
          ", COALESCE(Cast(GST.CALCULATEDVALUE AS DEcimal(20,2)),0) As GST "
          ", COALESCE(Cast(IC.CALCULATEDVALUE AS DEcimal(20,2)),0) As INITIALCOMM "
          ", COALESCE(Cast(BC.CALCULATEDVALUE AS DEcimal(20,2)),0) As BALCOMM "
          ", COALESCE(Cast(DR.BASEVALUE AS DEcimal(20,2)),0) As DHARARATE          "
          ", COALESCE(Cast(NR.BASEVALUE AS DEcimal(20,2)),0) As NETRATE          "
          ", Cast(SOL.USERPRIMARYQUANTITY-SOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As OrdQty   "
          ", COALESCE(ADSTORAGE.ValueString,ASB_LOTNO.Code,'') AS LOTNUMBER "
          ",TZ.Longdescription as despatchto "
          ",NT.NOTE as remark "
        ",SOI.TypeOfInvoice as invtype "
"from  "
"SalesOrder SO "
"JOIN DIVISION                                   ON SO.DIVISIONCODE=DIVISION.CODE "
"JOIN SalesOrderIE SOI                           ON So.Code = SOI.CODE "
"join ORDERPARTNER  OP                           On      SO.ORDPRNCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE   "
                                                "And     OP.CUSTOMERSUPPLIERTYPE = 1   "
"Join BUSINESSPARTNER  BP                        On      OP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID  "
"Left Join  TransportZone        TZ              ON      BP.TRANSPORTZONECODE = TZ.Code "
"Left Join AGENT                                 On      SO.AGENT1CODE = AGENT.CODE "
"Join SALESORDERLINE SOL                         On      SO.CODE = SOL.SALESORDERCODE   "
                                                "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE    "
                                                "And     SO.DOCUMENTTYPETYPE = SOL.DOCUMENTTYPETYPE  "
"Join LOGICALWAREHOUSE                           On      SOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE   "
"Join PLANT                                      On      LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE   "
"Left Join SALESORDERDELIVERY ContSOD    On      SOL.SALESORDERCODE= ContSOD.SALESORDERLINESALESORDERCODE "
           "And     SOL.SALESORDERCOUNTERCODE = ContSOD.SALORDLINESALORDERCOUNTERCODE   "
           "And     SOL.OrderLine = ContSOD.SalesOrderLineOrderLine   "
           "join FULLITEMKEYDECODER FIKD            ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   "
           "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   "
           "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   "
           "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   "
           "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   "
           "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   "
           "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   "
           "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   "
           "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   "
           "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   "
           "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   "
           "Join PRODUCT                            On      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE   "
           "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID   "
           "Left JOIN IndTaxDETAIL ContRate              ON      SOL.AbsUniqueId = ContRate.ABSUNIQUEID   "
           "AND     ContRate.ITaxCode = 'CNR' "
           "Left JOIN IndTaxDETAIL BillRate              ON      SOL.AbsUniqueId = BillRate.ABSUNIQUEID   "
           "AND     ContRate.ITaxCode = 'INR'   "
           "Left Join IndTaxDETAIL    GST                   ON      SOL.AbsUniqueId = GST.ABSUNIQUEID   "
           "AND     GST.TAXCATEGORYCODE = 'GST'   "
           "Left Join IndTaxDETAIL       IC                ON      SOL.AbsUniqueId = IC.ABSUNIQUEID   "
           "AND     IC.ITaxCode = 'AG1'   "
           "Left Join IndTaxDETAIL    BC                   ON      SOL.AbsUniqueId = BC.ABSUNIQUEID   "
           "AND     BC.ITaxCode = 'BS1'   "
            "Left Join IndTaxDETAIL    DR                   ON      SOL.AbsUniqueId = DR.ABSUNIQUEID   "
           "AND     DR.ITaxCode = 'DRD'  "
           "Left Join IndTaxDETAIL    NR                   ON      SOL.AbsUniqueId = NR.ABSUNIQUEID   "
           "AND     DR.ITaxCode = 'BSR'  "
          "LEFT JOIN ADSTORAGE                     ON      SOL.ABSUNIQUEID = ADSTORAGE.ABSUNIQUEID   "
           "LEFT Join LOT ASB_LOTNO                 On      SOL.ABSUNIQUEID = ASB_LOTNO.ABSUNIQUEID "
                                      "AND     ADSTORAGE.NameEntityName = 'Lot'  "
                                      "And ADSTORAGE.NameName = 'SaleLot'  "
                                      "And ADSTORAGE.FieldName = 'SaleLot' "
           "LEFT JOIN    NOTE   NT                            ON   SOL.AbsUniqueId = NT.FATHERID "
            "Left JOIN ItemSubcodeTemplate IST    ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode   "
           "AND     IST.GroupTypeCode  In ('MB4','P09','B07')   "
           "LEFT JOIN USERGENERICGROUP UGG       On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode   "
           "AND     Case IST.Position When 1 Then SOL.SUBCODE01 When 2 Then SOL.SUBCODE02 When 3 Then SOL.SUBCODE03 When 4 Then SOL.SUBCODE04 When 5 Then SOL.SUBCODE05   "
           "When 6 Then SOL.SUBCODE06 When 7 Then SOL.SUBCODE07 When 8 Then SOL.SUBCODE08 When 9 Then SOL.SUBCODE09 When 10 Then SOL.SUBCODE10 End = UGG.Code   "
"JOIN QUALITYLEVEL                       ON      SOL.QUALITYCODE = QUALITYLEVEL.CODE   "
           "AND     SOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE   "
"WHERE      SO.ORDERDATE     Between '"+str(stdt)+"' AND '"+str(etdt)+"'"
"           Order BY Divcode,Company, Broker, ItemTyp, Item, ContNo, Shade, OrdNo, OrdQty    "
    )
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result == False:
        return
    while result != False:
       pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
       pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode,result)
       result = con.db.fetch_both(stmt)
       
    
    pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
   
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()
