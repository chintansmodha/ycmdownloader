import os
from datetime import datetime
from PrintPDF import PackingReportSumm_PrintPDF as pdfPR
from Global_Files import Connection_String as con
from ProcessSelection import PackingReport_ProcessSelection as PRPS

counter = 0

Summary = " "
IssueStatus = " "
Total =[]
todateTotalNetwt = []
TotalCops = []
def PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                               LCLotNo, LSMachine, LCMachine, LSWinding,
                                               LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LDStartDate, LDEndDate):
    global Total
    global todateTotalNetwt
    global TotalCops
    Total = []
    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    Production = str(LSProduction)
    LSProductions = '(' + Production[1:-1] + ')'

    LotNo = str(LSLotNo)
    LSLotNos = '(' + LotNo[1:-1] + ')'

    Machine = str(LSMachine)
    LSMachines = '(' + Machine[1:-1] + ')'

    Winding = str(LSWinding)
    LSWindings = '(' + Winding[1:-1] + ')'

    Quality = str(LSQuality)
    LSQualitys = '(' + Quality[1:-1] + ')'

    Pallet = str(LSPallet)
    LSPallets = '(' + Pallet[1:-1] + ')'

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    sdate = str(stdt)[:-2] + '01'
    SDate = datetime.strptime(sdate, '%Y-%m-%d').date()
    StartDate = "'" + str(SDate) + "'"

    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "AND COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)

    if not LSProduction and not LCProduction:
        Productions = " "
    elif LCProduction:
        Productions = " "
    elif LSProduction:
        Productions = "AND INTERNALDOCUMENT.WAREHOUSECODE in " + str(LSProductions)

    if not LSLotNo and not LCLotNo:
        LotNos = " "
    elif LCLotNo:
        LotNos = " "
    elif LSLotNo:
        LotNos = "AND BKLELEMENTS.LOTCODE in " + str(LSLotNos)

    if not LSMachine and not LCMachine:
        Machines = " "
    elif LCMachine:
        Machines = " "
    elif LSMachine:
        Machines = "AND Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) in " + str(LSMachines)

    if not LSWinding and not LCWinding:
        Windings = " "
    elif LCWinding:
        Windings = " "
    elif LSWinding:
        Windings = "AND BKLELEMENTS.WINDINGTYPECODE in " + str(LSWindings)

    if not LSQuality and not LCQuality:
        Qualitys = " "
    elif LCQuality:
        Qualitys = " "
    elif LSQuality:
        Qualitys = "AND QUALITYLEVEL.LONGDESCRIPTION ||'-'|| QUALITYLEVEL.ITEMTYPECODE in " + str(LSQualitys)

    if not LSPallet and not LCPallet:
        Pallets = " "
    elif LCPallet:
        Pallets = " "
    elif LSPallet:
        Pallets = "AND UGG.CODE in " + str(LSPallets)


    sql = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", PRODUCT.LONGDESCRIPTION As Product " \
          ", LOT.CODE As LotNo " \
          ", COALESCE(UGG.CODE,'') As ShadeCode " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName " \
          ", COALESCE(QualityLevel.ShortDescription, '') As Quality " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+startdate+" AND    "+enddate+" THEN (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 " \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 " \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13 " \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15 ) ELSE 0 END)) AS INT) As Cops " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+startdate+" AND    "+enddate+" THEN BKLELEMENTS.ACTUALTAREWT ELSE 0 END)) As DECIMAL(10,3)) As TareWt " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+startdate+" AND    "+enddate+" THEN BKLELEMENTS.ACTUALNETWT ELSE 0 END)) As DECIMAL(10,3)) As NetWt " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+startdate+" AND    "+enddate+" THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As Boxes " \
          ", '' As Perc " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+StartDate+" AND     "+enddate+"  THEN BKLELEMENTS.ACTUALNETWT ELSE 0 END)) As DECIMAL(10,3)) As ToNetWt " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+StartDate+" AND     "+enddate+"  THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As ToBoxes " \
          "From BKLELEMENTS " \
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
          "Join    BUSINESSUNITVSCOMPANY           On      LOGICALWAREHOUSE.PLANTCODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Where   ELEMENTS.ENTRYDATE             between "+StartDate+" AND     "+enddate+" "+LotNos+" "+Machines+" "+Windings+" "+Qualitys+" "+Pallets+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By  FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,''), PRODUCT.LONGDESCRIPTION, LOT.CODE, COALESCE(UGG.CODE,''), COALESCE(UGG.LONGDESCRIPTION,''), '' " \
          ", COALESCE(QualityLevel.ShortDescription, '') " \
          "Order By CompName, Department, PRODUCT    "


# Total Calculated Query
    sql2 = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
           ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", PRODUCT.LONGDESCRIPTION As Product " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+startdate+" AND    "+enddate+" THEN BKLELEMENTS.ACTUALNETWT ELSE 0 END)) As DECIMAL(10,3)) As totalNetWt " \
          "From BKLELEMENTS " \
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
          "Left Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          " Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode " \
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
          "Join    BUSINESSUNITVSCOMPANY           On      LOGICALWAREHOUSE.PLANTCODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Where   ELEMENTS.ENTRYDATE              between "+StartDate+" AND    "+enddate+" "+LotNos+" "+Machines+" "+Windings+" "+Qualitys+" "+Pallets+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By  FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,''), PRODUCT.LONGDESCRIPTION " \
          "Order By CompName, Department, PRODUCT "

    stmt2 = con.db.prepare(con.conn, sql2)
    con.db.execute(stmt2)
    results = con.db.fetch_both(stmt2)
    Total = []
    while results != False:
        if results not in Total:
            Total.append(float(results['TOTALNETWT']))
        results = con.db.fetch_both(stmt2)




    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)


    while result != False:
        global counter
        counter = counter + 1

        pdfPR.textsize(pdfPR.c, result, pdfPR.d,stdt,etdt,Total)
        pdfPR.d=pdfPR.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfPR.d<60 :
            pdfPR.d=735
            pdfPR.c.showPage()
            pdfPR.header(stdt,etdt,pdfPR.divisioncode)
            pdfPR.fonts(7)


    if result == False:
        if counter > 0:
            pdfPR.boldfonts(7)
            pdfPR.d = pdfPR.dvalue()
            # pdfPR.d = pdfPR.dvalue()
            pdfPR.c.drawString(120, pdfPR.d, "Item Total: ")
            pdfPR.c.drawAlignedString(270, pdfPR.d, str(pdfPR.Box))
            pdfPR.c.drawAlignedString(320, pdfPR.d, str(pdfPR.cops))
            pdfPR.c.drawAlignedString(395, pdfPR.d, str('{0:1.3f}'.format(pdfPR.netwt)))
            pdfPR.c.drawAlignedString(505, pdfPR.d, str('{0:1.3f}'.format(pdfPR.netwtS)))
            pdfPR.c.drawAlignedString(575, pdfPR.d, str(pdfPR.Boxes))
            # print(todateTotalNetwt)
            pdfPR.d = pdfPR.dvalue()
            pdfPR.d = pdfPR.dvalue()
            pdfPR.c.drawString(120, pdfPR.d, "Dept Total: ")
            pdfPR.c.drawAlignedString(270, pdfPR.d, str(pdfPR.DeptBox))
            pdfPR.c.drawAlignedString(320, pdfPR.d, str(pdfPR.Deptcops))
            pdfPR.c.drawAlignedString(395, pdfPR.d, str('{0:1.3f}'.format(pdfPR.Deptnetwt)))
            pdfPR.c.drawAlignedString(505, pdfPR.d, str('{0:1.3f}'.format(pdfPR.DeptnetwtS)))
            pdfPR.c.drawAlignedString(575, pdfPR.d, str(pdfPR.DeptBoxes))
            pdfPR.d = pdfPR.dvalue()
            pdfPR.d = pdfPR.dvalue()
            pdfPR.c.drawString(120, pdfPR.d, "Company Total: ")
            pdfPR.c.drawAlignedString(270, pdfPR.d, str(pdfPR.CompBox))
            pdfPR.c.drawAlignedString(320, pdfPR.d, str(pdfPR.Compcops))
            pdfPR.c.drawAlignedString(395, pdfPR.d, str('{0:1.3f}'.format(pdfPR.Compnetwt)))
            pdfPR.c.drawAlignedString(505, pdfPR.d, str('{0:1.3f}'.format(pdfPR.CompnetwtS)))
            pdfPR.c.drawAlignedString(575, pdfPR.d, str(pdfPR.CompBoxes))
            pdfPR.CleanWt()
            pdfPR.DepartmentClean()
            pdfPR.CompanyClean()
            pdfPR.i = 0
            pdfPR.fonts(7)

            PRPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfPR.c.showPage()
    pdfPR.c.save()

    pdfPR.newrequest()
    pdfPR.d = pdfPR.newpage()
    pdfPR.CleanWt()
    pdfPR.DepartmentClean()
    pdfPR.CompanyClean()
    pdfPR.i = 0
    pdfPR.total = 0
    # Total = []

