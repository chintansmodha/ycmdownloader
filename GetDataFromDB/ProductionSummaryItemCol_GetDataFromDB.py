import os
from datetime import datetime
# from PrintPDF import ProductionSummaryItemCol_PrintPDF as pdfPSIC
from PrintPDF import ProductionSummaryItmColWise_PrintPDF as pdfPSICW
from Global_Files import Connection_String as con
from ProcessSelection import ProductionSummary_ProcessSelection as PRSPS

counter = 0

Quality = []
TOTALS = []
quality_total = []
def ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LDStartDate,LDEndDate):

    global Quality,TOTALS,quality_total
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



    sql = "Select          COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'')  As Product " \
          ", COALESCE(QualityLevel.ShortDescription, '') As Qualty " \
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
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07')" \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
          "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Where   ELEMENTS.ENTRYDATE              Between "+startdate+"      And     "+enddate+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') " \
          ", COALESCE(QualityLevel.ShortDescription, '') " \
          "Order By Department, Product, Qualty "


    sql2 = "Select          COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
           ", COALESCE(QualityLevel.ShortDescription, '') As Quality " \
           ", CAST(Sum(Case When ELEMENTS.ENTRYDATE  Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALNETWT) ELSE 0 END) As DECIMAL(10,3)) As NetWt " \
           "From BKLELEMENTS " \
           "Join    PLANT                           ON      BKLELEMENTS.PLANTCODE = PLANT.CODE " \
           "Join    BUSINESSUNITVSCOMPANY           On      PLANT.CODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
           "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
           "Left Join      QualityLevel             On      BKLELEMENTS.QUALITYCODE = QUALITYLEVEL.CODE " \
           "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
           "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
           "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
           "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
           "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
           "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
           "Where   ELEMENTS.ENTRYDATE              Between "+startdate+"      And     "+enddate+" "+Departmentcodes+" " \
           "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
           "Group By COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
           ", COALESCE(QualityLevel.ShortDescription, '') " \
           "Order By Department, Quality "


    stmt3 = con.db.prepare(con.conn, sql2)
    con.db.execute(stmt3)
    resultss = con.db.fetch_both(stmt3)
    TOTALS = []
    quality_total = []
    while resultss != False:
        if resultss not in TOTALS:
            TOTALS.append(resultss['NETWT'])
            quality_total.append(resultss['QUALITY'])
        resultss = con.db.fetch_both(stmt3)

    stmt2 = con.db.prepare(con.conn, sql)
    con.db.execute(stmt2)
    results = con.db.fetch_both(stmt2)
    Quality = []
    while results != False:
        if results not in Quality:
            Quality.append(results['QUALTY'])
        results = con.db.fetch_both(stmt2)
    Quality = sorted(list(set(Quality)))
    # print(Quality)
    # print(list(set(Quality)))



    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        # pdfPSIC.textsize(pdfPSIC.c, result, pdfPSIC.d,stdt,etdt, Quality)
        # pdfPSIC.d=pdfPSIC.dvalue()
        pdfPSICW.textsize(pdfPSICW.c, result, pdfPSICW.d, stdt, etdt, TOTALS, quality_total)
        pdfPSICW.d = pdfPSICW.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfPSICW.d<80 :
            pdfPSICW.d = 745

            pdfPSICW.c.setPageSize(pdfPSICW.landscape(pdfPSICW.A3))
            pdfPSICW.c.showPage()
            pdfPSICW.header(stdt, etdt)
            # pdfPSICW.header_h(pdfPSICW.d)
            pdfPSICW.fonts(7)


    if result == False:
        if counter > 0:

            # pdfPSIC.d = pdfPSIC.dvalue()
            # pdfPSIC.d = pdfPSIC.dvalueincrease()
            # pdfPSIC.c.drawAlignedString(pdfPSIC.q , pdfPSIC.d, str('{0:1.3f}'.format(pdfPSIC.Netwt)))
            # pdfPSIC.TotalClean()
            # ******************* Wrap End *********************************
            pdfPSICW.d = pdfPSICW.dvalueincrease()
            pdfPSICW.d = pdfPSICW.dvalue()
            pdfPSICW.d_total.append(pdfPSICW.d)
            pdfPSICW.total.append(pdfPSICW.Netwt)
            g = 0
            while g < len(pdfPSICW.wrap_text):
                pdfPSICW.d = pdfPSICW.dvalue()
                pdfPSICW.d = pdfPSICW.dvalue()
                g = g + 1
            # #***************************************************************
            # pdfPSICW.d = pdfPSICW.dvalueincrease()
            # pdfPSICW.d = pdfPSICW.dvalue()
            # pdfPSICW.d_total.append(pdfPSICW.d)
            # pdfPSICW.total.append(pdfPSICW.Netwt)
            # pdfPSICW.d = pdfPSICW.dvalue()
            # pdfPSICW.d = pdfPSICW.dvalue()
            pdfPSICW.fonts(9)
            pdfPSICW.b = pdfPSICW.b + 100
            pdfPSICW.c.drawString(pdfPSICW.b, pdfPSICW.t, "Total")
            e = 0
            while e < len(pdfPSICW.d_total):
                pdfPSICW.fonts(7)
                pdfPSICW.c.drawAlignedString(pdfPSICW.b + 20, int(pdfPSICW.d_total[e]), str('{0:1.3f}'.format(pdfPSICW.total[e])))
                e = e + 1
            n = 215
            pdfPSICW.boldfonts(8)
            pdfPSICW.c.drawString(20, pdfPSICW.d, "Dept Total: ")
            p1 = p = pdfPSICW.r
            r1 = 0
            while pdfPSICW.l < pdfPSICW.j:
                if "'" + quality_total[p] + "'" == "'" + pdfPSICW.Quaty[r1] + "'":
                    pdfPSICW.c.drawAlignedString(n, pdfPSICW.d, str(TOTALS[p]))
                    pdfPSICW.l = pdfPSICW.l + 1
                    r1 = r1 + 1
                    p = p1
                    pdfPSICW.r = pdfPSICW.r + 1
                    n = n + 100
                else:
                    p = p + 1
            # while pdfPSICW.l < pdfPSICW.j:
            #     pdfPSICW.c.drawAlignedString(n, pdfPSICW.d, str(TOTALS[pdfPSICW.l]))
            #     pdfPSICW.l = pdfPSICW.l + 1
            #     n = n + 100
            pdfPSICW.c.drawAlignedString(n+3, pdfPSICW.d, str('{0:1.3f}'.format(pdfPSICW.CompTotal)))
            pdfPSICW.CompClean()
            pdfPSICW.d = pdfPSICW.dvalueincrease()

            pdfPSICW.fonts(9)
            pdfPSICW.d = pdfPSICW.dvalue()
            pdfPSICW.d = pdfPSICW.dvalue()
            pdfPSICW.Quaty = []
            pdfPSICW.TotalClean()
            pdfPSICW.total = []
            pdfPSICW.d_total = []

            PRSPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRSPS.Exceptions="Note: No Report Form For Given Criteria"
            return

    # pdfPSIC.c.setPageSize(pdfPSIC.landscape(pdfPSIC.A3))
    # pdfPSIC.c.showPage()
    # pdfPSIC.c.save()
    #
    # pdfPSIC.newrequest()
    # pdfPSIC.d = pdfPSIC.newpage()
    # Quality = []
    pdfPSICW.c.setPageSize(pdfPSICW.landscape(pdfPSICW.A3))
    pdfPSICW.c.showPage()
    pdfPSICW.c.save()

    pdfPSICW.newrequest()
    pdfPSICW.d = pdfPSICW.newpage()
    Quality = []
    pdfPSICW.TotalClean()
