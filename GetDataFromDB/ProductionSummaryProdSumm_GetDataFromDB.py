import os
from datetime import datetime
from PrintPDF import ProductionSummaryProdSumm_PrintPDF as pdfPSPS
from Global_Files import Connection_String as con
from ProcessSelection import ProductionSummary_ProcessSelection as PRSPS

counter = 0


def ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate,LDEndDate):


    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    Production = str(LSProduction)
    LSProductions = '(' + Production[1:-1] + ')'

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    #
    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "AND COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)

    # if not LSProduction and not LCProduction:
    #     Productions = " "
    # elif LCProduction:
    #     Productions = " "
    # elif LSProduction:
    #     Productions = "AND INTERNALDOCUMENT.WAREHOUSECODE in " + str(LSProductions)



    sql = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", (Cast( LOT.Code AS VARCHAR(4))) As MachineCode " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product " \
          ", LOT.CODE As LotNo " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALNETWT) ELSE 0 END) As DECIMAL(10,3)) As NetWt " \
          "From BKLELEMENTS " \
          "Join    PLANT                           ON      BKLELEMENTS.PLANTCODE = PLANT.CODE " \
          "Join    BUSINESSUNITVSCOMPANY           On      PLANT.CODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE " \
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
          "Left Join      QualityLevel             On      BKLELEMENTS.QUALITYCODE = QUALITYLEVEL.CODE " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code " \
          "Join    Lot                             On      BKLELEMENTS.LOTITEMTYPECODE = LOT.ITEMTYPECODE " \
          "And     BKLELEMENTS.LOTCODE = LOT.CODE " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
          "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE  " \
          "Where   ELEMENTS.ENTRYDATE              Between "+startdate+"      And     "+enddate+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By FINBUSINESSUNIT.LONGDESCRIPTION " \
          ", (Cast( LOT.Code AS VARCHAR(4))) " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') " \
          ", LOT.CODE " \
          "Order By CompName, MachineCode, Product, LotNo "





    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfPSPS.textsize(pdfPSPS.c, result, pdfPSPS.d,stdt,etdt)
        pdfPSPS.d=pdfPSPS.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfPSPS.d<40 :
            pdfPSPS.d = 745
            pdfPSPS.c.showPage()
            pdfPSPS.header(stdt,etdt, pdfPSPS.divisioncode)
            pdfPSPS.fonts(7)


    if result == False:
        if counter > 0:

            pdfPSPS.boldfonts(7)
            pdfPSPS.d = pdfPSPS.dvalue()
            pdfPSPS.c.drawString(350, pdfPSPS.d, "Company Total: ")
            pdfPSPS.c.drawAlignedString(570, pdfPSPS.d, str('{0:1.3f}'.format(pdfPSPS.Netwt)))
            pdfPSPS.CompanyClean()
            pdfPSPS.fonts(7)

            PRSPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRSPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfPSPS.c.showPage()
    pdfPSPS.c.save()

    pdfPSPS.newrequest()
    pdfPSPS.d = pdfPSPS.newpage()