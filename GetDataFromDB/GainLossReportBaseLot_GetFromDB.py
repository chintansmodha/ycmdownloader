import os
from datetime import datetime
from PrintPDF import GainLossReportBaseLot_PrintPDF as pdf
from Global_Files import Connection_String as con
from ProcessSelection import GainLossReport_ProcessSelection as Gain

counter = 0


def GainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate):
    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    stdt = datetime.strptime(LDStartdate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    #
    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "And COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)
    # print(LSDay)

    sql = "Select                  COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", Coalesce(Trim(ALLOCATION.LOTCODE),'BaseLotNotEntered') As BaseLot " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product" \
          ", Trim(LOT.Code) As LotNo " \
          ", Cast(SUM(BKLELEMENTS.ACTUALNETWT) As Decimal(30,3)) As netWt " \
          ", Cast(BoMComponent.QUANTITYPER As Decimal(10,2)) As InputPerc" \
          ", Cast((BoMComponent.QUANTITYPER/100) * SUM(BKLELEMENTS.ACTUALNETWT) As Decimal(30,3)) As ConsumeNetWt " \
          ", Cast((Select Sum(Case When TRANSACTIONDATE <= "+enddate+" Then UserPrimaryQuantity * Case When OnHandUpdate = 1  " \
          "Then 1 Else -1 End Else 0 End) From STOCKTRANSACTION " \
          "Where LotCode = ALLOCATION.LOTCODE And ALLOCATION.LOGICALWAREHOUSECODE = LOGICALWAREHOUSECODE And " \
          "ALLOCATION.QUALITYLEVELCODE = QUALITYLEVELCODE And TemplateCode not in('QC1','QCR')) AS Decimal(30,3) " \
          ") aS StkQty " \
          "From BKLELEMENTS " \
          "Join LOGICALWAREHOUSE                   On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join COSTCENTER                    On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "JOIN FULLITEMKEYDECODER FIKD            ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Left Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code " \
          "Join LOT                                On  BKLELEMENTS.LOTCODE = LOT.CODE " \
          "Join PRODUCTIONRESERVATION Prdsv        ON  LOT.LOTCREATIONORDERNUMBER = Prdsv.ORDERCODE " \
          "And LOT.LOTCREATIONORDERCOUNTER = Prdsv.ORDERCOUNTERCODE " \
          "And LOT.LOTCREATIONORDERTYPE = Prdsv.ORIGINTYPE " \
          "Join ALLOCATION                         On  Prdsv.ORDERCODE = ALLOCATION.ORDERCODE " \
          "And Prdsv.ORDERCOUNTERCODE = ALLOCATION.COUNTERCODE " \
          "And Prdsv.RESERVATIONLINE = ALLOCATION.ORDERLINE " \
          "ANd Allocation.TemplateCode         = 'WTR' " \
          "JOIN BoMComponent                       ON  Prdsv.BOMCOMPBILLOFMATERIALNUMBERID = BoMComponent.BillOfMaterialNumberId " \
          "And Prdsv.BOMCOMPSEQUENCE = BoMComponent.SEQUENCE " \
          "Join ELEMENTS                           ON  BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where Prdsv.ItemTypeAFICode in ( 'POY', 'FDY', 'MOY', 'MON', 'BCF', 'CAB', 'HST', 'DTY', 'ATY', 'TWD', 'PLY' ) " \
          "And ELEMENTS.ENTRYDATE   Between        "+startdate+"    And     "+enddate+" " \
          " "+Departmentcodes+" " \
          "Group By                COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
          ", ALLOCATION.LOTCODE " \
          ", ALLOCATION.LOGICALWAREHOUSECODE " \
          ", ALLOCATION.QUALITYLEVELCODE " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') " \
          ", LOT.Code " \
          ", BoMComponent.QUANTITYPER " \
          "Order By Department, BaseLot, Product, LotNo "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdf.textsize(pdf.c, result, pdf.d, stdt, etdt)
        pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
        result = con.db.fetch_both(stmt)

    if result == False:
        if counter > 0:

            pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
            pdf.PrintBaseTotal()
            pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
            pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
            pdf.PrintTotal()
            pdf.fonts(7)

            Gain.Exceptions = ""
            counter = 0
        elif counter == 0:
            Gain.Exceptions = "Note: No Report Form For Given Criteria"
            return

    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    # print(pdf.pageSize)
    # if pdf.pageSize == 3:
    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    pdf.c.showPage()
    pdf.c.save()

    pdf.newrequest()
    pdf.d = pdf.newpage()