from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import LotNoListing_PrintPDF as pdfrpt
from ProcessSelection import LotNoListing_ProcessSelection as LLV
counter=0
def LotNoListing_PrintPDF(LSResource,LSLotNo,LCResource,LCLotNo,LDStartDate,LDEndDate,LSFileName,LDProductFamily):
    resource=str(LSResource)
    lotno=str(LSLotNo)
    stdate=str(LDStartDate)
    etdate=str(LDEndDate)
    LSResources = '(' + resource[1:-1] + ')'
    LSLotNos = '(' + lotno[1:-1] + ')'

    BomItemType = ""
    PoyFamily = "( 'POY', 'FDY', 'MOY', 'MON' )"
    BcfFamily = "( 'BCF', 'CAB', 'HST' )"
    DtyFamily = "( 'DTY', 'ATY', 'TWD', 'PLY' )"

    if LDProductFamily == 1:
        Itemtype = " And LT.ITEMTYPECODE In " + PoyFamily
        BomItemType = "(" + "'MBP','CHP'" +")"
    elif LDProductFamily == 2:
        Itemtype = " And LT.ITEMTYPECODE In " + BcfFamily
        BomItemType = "(" + "'MBB','CHP'" + ")"
    elif LDProductFamily == 3:
        Itemtype = " And LT.ITEMTYPECODE In " + DtyFamily
        BomItemType = "(" + "'POY','FDY','DTY','TWD'" + ")"

    # print(BomItemType)

    if not LCResource and not LSResource:
        Resource=""
    elif LCResource:
        Resource=" "
    elif LSResource:
        Resource = "AND RESOURCES.CODE in " + str(LSResources)
        # print(Resource)

    if not LCLotNo and not LSLotNo:
        LotNo=""
    elif LCLotNo:
        LotNo=" "
    elif LSLotNo:
        LotNo="AND LT.CODE in "+str(LSLotNos)

    sql="select  COALESCE(PLANT.LONGDESCRIPTION,' Plant Name Not Updated In Lot') AS PLANTNAME" \
        " , LT.CODE AS LOTNO" \
        " , TRIM(RESOURCES.CODE) || ' - ' ||RESOURCES.LONGDESCRIPTION AS RESOURCENO" \
        " , Product.LONGDESCRIPTION AS ITEM" \
        " , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As SHADECODE" \
        " , LT.LOTCREATIONDATE AS LOTDATE" \
        " , COALESCE(LOT_ActualDenier.VALUEINT,0) AS DENIER" \
        " , COALESCE(LOT_LDR.VALUEDECIMAL,0) AS LDR" \
        " , COALESCE(LOT_Remarks.VALUESTRING,'') AS LDRREMARKS" \
        " , PD.PROJECTCODE As SALESORDERNO " \
        ", Cast(BoMComponent.QUANTITYPER As Decimal(10,2)) As BOM_InputPerc " \
        ", Allocation.LotCode As BOM_PrevLotNo " \
        ", Allocation.DecoSubcode02 As BOM_PrevLotBase " \
        ", Case When ProdRsv.ItemTypeAFICode In "+BomItemType+" Then Product_MB.LONGDESCRIPTION Else '' End As BOM_PrevLotItem " \
        ", Case When ProdRsv.ItemTypeAFICode In "+BomItemType+" Then TRIM (UGG_MB.Code)  ||' / '||UGG_MB.LONGDESCRIPTION Else '' End As BOM_PrevLotShade " \
        ", Case When ProdRsv.ItemTypeAFICode In "+BomItemType+" Then Quality_MB.ShortDescription Else '' End As BOM_PrevLotQuality " \
        "FROM LOT AS LT" \
        " Left JOIN PLANT                 ON      LT.PLANTCODE = PLANT.CODE" \
        " JOIN FullItemKeyDecoder FIKD    ON      LT.ITEMTYPECODE = FIKD.ITEMTYPECODE" \
        " AND     COALESCE(LT.DECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')" \
        " AND     COALESCE(LT.DECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')" \
        " AND     COALESCE(LT.DECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')" \
        " AND     COALESCE(LT.DECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')" \
        " AND     COALESCE(LT.DECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')" \
        " AND     COALESCE(LT.DECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')" \
        " AND     COALESCE(LT.DECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')" \
        " AND     COALESCE(LT.DECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')" \
        " AND     COALESCE(LT.DECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')" \
        " AND     COALESCE(LT.DECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')" \
        " JOIN PRODUCT                    ON      LT.ITEMTYPECODE = PRODUCT.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = Product.AbsUniqueId" \
        " Left JOIN ItemSubcodeTemplate AS IST ON       LT.ITEMTYPECODE = IST.ItemTypeCode" \
        " AND      IST.GroupTypeCode In ('MB4','P09','B07')" \
        " Left JOIN UserGenericGroup AS UGG    ON       IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
        " AND      Case IST.Position" \
        " When 1 Then LT.DECOSUBCODE01 When 2 Then LT.DECOSUBCODE02" \
        " When 3 Then LT.DECOSUBCODE03 When 4 Then LT.DECOSUBCODE04" \
        " When 5 Then LT.DECOSUBCODE05 When 6 Then LT.DECOSUBCODE06" \
        " When 7 Then LT.DECOSUBCODE07 When 8 Then LT.DECOSUBCODE08" \
        " When 9 Then LT.DECOSUBCODE09 When 10 Then LT.DECOSUBCODE10" \
        " End = UGG.Code" \
        " Left JOIN ProductionDemand As PD                     ON      LT.LOTCREATIONORDERNUMBER = PD.CODE" \
        " LEFT Join AdStorage  As LOT_ActualDenier        ON      LT.ABSUNIQUEID = LOT_ActualDenier.UNIQUEID" \
        " AND     LOT_ActualDenier.NameEntityName = 'Lot' And LOT_ActualDenier.NameName = 'ActualDenier' And LOT_ActualDenier.FieldName = 'ActualDenier'" \
        " LEFT Join AdStorage  As LOT_LDR                 ON      LT.ABSUNIQUEID = LOT_LDR.UNIQUEID" \
        " AND     LOT_LDR.NameEntityName = 'Lot' And LOT_LDR.NameName = 'ActualLDR' And LOT_LDR.FieldName = 'ActualLDR'" \
        " LEFT Join AdStorage  As LOT_Remarks             ON      LT.ABSUNIQUEID = LOT_Remarks.UNIQUEID" \
        " AND     LOT_Remarks.NameEntityName = 'Lot' And LOT_Remarks.NameName = 'Remarks' And LOT_Remarks.FieldName = 'Remarks'" \
        " JOIN RESOURCES                                  ON      (Left(LT.CODE,3) = RESOURCES.CODE Or Left(LT.CODE,4) = RESOURCES.CODE) " \
        "Left JOIN ProductionReservation ProdRsv              ON      LT.LOTCREATIONORDERNUMBER = ProdRsv.OrderCode " \
        "AND     ProdRsv.ItemTypeAFICode In "+BomItemType+" " \
        "Left JOIN QualityLevel Quality_MB                    ON      ProdRsv.QualityCode = Quality_MB.Code " \
        "AND     ProdRsv.ItemTypeAFICode = Quality_MB.ItemTypeCode " \
        "Left JOIN FullItemKeyDecoder As FIKD_MB              ON      ProdRsv.ItemTypeAFICode = FIKD_MB.ITEMTYPECODE " \
        "AND     COALESCE(ProdRsv.SUBCODE01, '') = COALESCE(FIKD_MB.SubCode01, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE02, '') = COALESCE(FIKD_MB.SubCode02, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE03, '') = COALESCE(FIKD_MB.SubCode03, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE04, '') = COALESCE(FIKD_MB.SubCode04, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE05, '') = COALESCE(FIKD_MB.SubCode05, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE06, '') = COALESCE(FIKD_MB.SubCode06, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE07, '') = COALESCE(FIKD_MB.SubCode07, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE08, '') = COALESCE(FIKD_MB.SubCode08, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE09, '') = COALESCE(FIKD_MB.SubCode09, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE10, '') = COALESCE(FIKD_MB.SubCode10, '') " \
        "Left JOIN PRODUCT As Product_MB                      ON      ProdRsv.ItemTypeAFICode  = Product_MB.ITEMTYPECODE " \
        "AND     FIKD_MB.ItemUniqueId = Product_MB.AbsUniqueId " \
        "Left JOIN UserGenericGroup AS UGG_MB            ON      ProdRsv.SUBCODE04 = UGG_MB.Code " \
        "And    UGG_MB.UserGenericGroupTypeCode = 'MB4'  " \
        "Left JOIN BoMComponent                               ON      PD.BomNumberId       = BoMComponent.BillOfMaterialNumberId " \
        "AND     BoMComponent.ItemTypeAFICode In "+BomItemType+" " \
        "AND     ProdRsv.ItemTypeAFICode = BomComponent.ItemTypeAFICode " \
        "AND     COALESCE(ProdRsv.SUBCODE01, '') = COALESCE(BomComponent.SubCode01, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE02, '') = COALESCE(BomComponent.SubCode02, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE03, '') = COALESCE(BomComponent.SubCode03, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE04, '') = COALESCE(BomComponent.SubCode04, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE05, '') = COALESCE(BomComponent.SubCode05, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE06, '') = COALESCE(BomComponent.SubCode06, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE07, '') = COALESCE(BomComponent.SubCode07, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE08, '') = COALESCE(BomComponent.SubCode08, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE09, '') = COALESCE(BomComponent.SubCode09, '') " \
        "AND     COALESCE(ProdRsv.SUBCODE10, '') = COALESCE(BomComponent.SubCode10, '') " \
        "Left Join Allocation                            ON      Lt.LOTCREATIONORDERNUMBER = Allocation.OrderCode " \
        "AND     Allocation.TemplateCode         = 'WTR' " \
        "WHERE  LT.LOTCREATIONDATE between ? and ? " + Resource + " " + LotNo + " " + Itemtype + " " \
        " ORDER BY PLANTNAME,RESOURCENO,LOTNO"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    con.db.bind_param(stmt, 1, stdt)
    con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)

    if result==False:
        LLV.Exceptions = "Note: No Result found according to your selected criteria "
        return

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        result = con.db.fetch_both(stmt)

        if pdfrpt.d<80:
            pdfrpt.d=730
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
            pdfrpt.c.showPage()
            pdfrpt.header(stdt,etdt,result,pdfrpt.plantcode)

    if result == False:
        if counter > 0:
            pdfrpt.d = pdfrpt.dvalue(stdt,etdt,result,pdfrpt.plantcode)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dvalue(stdt,etdt,result,pdfrpt.plantcode)
            LLV.Exceptions = ""
        elif counter==0:
            LLV.Exceptions="Note: No Result found according to your selected criteria "

    pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
