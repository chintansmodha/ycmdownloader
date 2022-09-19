import os
from datetime import datetime
from PrintPDF import PackingReportItmTyp_PrintPDF as pdfPRI
from Global_Files import Connection_String as con
from ProcessSelection import PackingReport_ProcessSelection as PRPS

counter = 0

CopsTotal = []
netwt = []
Tonewt = []
def PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                               LCLotNo, LSMachine, LCMachine, LSWinding,
                                               LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LSItmtype, LCItmtype, LDStartDate, LDEndDate):

    global CopsTotal
    global netwt
    global Tonewt
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

    Itmtype = str(LSItmtype)
    LSItmtypes = '(' + Itmtype[1:-1] + ')'

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

    if not LSItmtype and not LCItmtype:
        Itmtypes = " "
    elif LCItmtype:
        Itmtypes = " "
    elif LSItmtype:
        Itmtypes = "AND BKLELEMENTS.LOTITEMTYPECODE in " + str(LSItmtypes)


    sql = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", ITEMTYPE.LONGDESCRIPTION ||' - '|| ITEMTYPE.CODE As ItmType " \
          ", PRODUCT.LONGDESCRIPTION ||' '||COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product " \
          ", '' AS Boxes " \
          ", CAST(SUM(Case When ELEMENTS.ENTRYDATE between"+startdate+" AND    "+enddate+"   Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 " \
          "+ BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 + BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 " \
          "+ BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15 ) Else 0 End) AS INT) As Cops " \
          ", CAST(SUM(Case When ELEMENTS.ENTRYDATE between"+startdate+" AND    "+enddate+"   Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(10,3)) As NetWt " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between"+startdate+" AND    "+enddate+" THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As Boxes " \
          ", CAST(SUM(Case When ELEMENTS.ENTRYDATE between "+StartDate+" AND    "+enddate+"   Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(10,3)) As TONetwt " \
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE between "+StartDate+" AND    "+enddate+" THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As Box " \
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
          "Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
          "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join    BUSINESSUNITVSCOMPANY           On      LOGICALWAREHOUSE.PLANTCODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Where   ELEMENTS.ENTRYDATE             between "+StartDate+" AND    "+enddate+" "+LotNos+" "+Machines+" "+Windings+" "+Qualitys+" "+Pallets+" "+Itmtypes+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
          ", ITEMTYPE.LONGDESCRIPTION ||' - '|| ITEMTYPE.CODE " \
          ", PRODUCT.LONGDESCRIPTION ||' '||COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') " \
          "Order By CompName, Department, ItmType, Product  "


    sql2 = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
           ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
           ", ITEMTYPE.LONGDESCRIPTION ||' - '|| ITEMTYPE.CODE As ItmType " \
           ", CAST(SUM(Case When ELEMENTS.ENTRYDATE between "+startdate+" AND    "+enddate+"   Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(10,3)) As TOTALNETWT " \
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
           "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode " \
           "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
           "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
           "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
           "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code " \
           "Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE " \
           "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
           "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
           "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
           "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
           "Join    BUSINESSUNITVSCOMPANY           On      LOGICALWAREHOUSE.PLANTCODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
           "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
           "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
           "Where   ELEMENTS.ENTRYDATE             between "+startdate+" AND    "+enddate+" "+LotNos+" "+Machines+" "+Windings+" "+Qualitys+" "+Pallets+" "+Itmtypes+" "+Departmentcodes+" " \
           "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
           "Group By FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
           ", ITEMTYPE.LONGDESCRIPTION ||' - '|| ITEMTYPE.CODE " \
           "Order By CompName, Department, ItmType "

    stmt2 = con.db.prepare(con.conn, sql2)
    con.db.execute(stmt2)
    results = con.db.fetch_both(stmt2)
    netwt = []
    while results != False:
        if results not in netwt:
            netwt.append(float(results['TOTALNETWT']))
        results = con.db.fetch_both(stmt2)


    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfPRI.textsize(pdfPRI.c, result, pdfPRI.d,stdt,etdt,netwt)
        # percentage = (float(result['NETWT']) / pdfPRI.itemtotal) * 100
        pdfPRI.d=pdfPRI.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfPRI.d<20 :
            pdfPRI.d=735
            pdfPRI.c.showPage()
            pdfPRI.header(stdt,etdt,pdfPRI.divisioncode)


    if result == False:
        pdfPRI.i = 0
        if counter > 0:

            pdfPRI.boldfonts(7)
            pdfPRI.d = pdfPRI.dvalue()
            pdfPRI.c.drawString(100, pdfPRI.d, "Item Type Total: ")
            pdfPRI.c.drawAlignedString(275, pdfPRI.d, str(pdfPRI.Boxes))
            pdfPRI.c.drawAlignedString(320, pdfPRI.d, str(pdfPRI.cops))
            pdfPRI.c.drawAlignedString(400, pdfPRI.d, str('{0:1.3f}'.format(pdfPRI.itemtotal)))
            pdfPRI.c.drawAlignedString(510, pdfPRI.d, str('{0:1.3f}'.format(pdfPRI.itemtotals)))
            pdfPRI.c.drawAlignedString(585, pdfPRI.d, str(pdfPRI.Box))
            pdfPRI.d = pdfPRI.dvalue()
            pdfPRI.d = pdfPRI.dvalue()
            pdfPRI.c.drawString(100, pdfPRI.d, "Dept Total: ")
            pdfPRI.c.drawAlignedString(275, pdfPRI.d, str(pdfPRI.DeptBoxes))
            pdfPRI.c.drawAlignedString(320, pdfPRI.d, str(pdfPRI.Deptcops))
            pdfPRI.c.drawAlignedString(400, pdfPRI.d, str('{0:1.3f}'.format(pdfPRI.Deptitemtotal)))
            pdfPRI.c.drawAlignedString(510, pdfPRI.d, str('{0:1.3f}'.format(pdfPRI.Deptitemtotals)))
            pdfPRI.c.drawAlignedString(585, pdfPRI.d, str(pdfPRI.DeptBox))
            pdfPRI.d = pdfPRI.dvalue()
            pdfPRI.d = pdfPRI.dvalue()
            pdfPRI.c.drawString(100, pdfPRI.d, "Company Total: ")
            pdfPRI.c.drawAlignedString(275, pdfPRI.d, str(pdfPRI.CompBoxes))
            pdfPRI.c.drawAlignedString(320, pdfPRI.d, str(pdfPRI.Compcops))
            pdfPRI.c.drawAlignedString(400, pdfPRI.d, str('{0:1.3f}'.format(pdfPRI.Compitemtotal)))
            pdfPRI.c.drawAlignedString(510, pdfPRI.d, str('{0:1.3f}'.format(pdfPRI.Compitemtotals)))
            pdfPRI.c.drawAlignedString(585, pdfPRI.d, str(pdfPRI.CompBox))
            pdfPRI.ItemTotalClean()
            pdfPRI.DepartmentClean()
            pdfPRI.CompanyClean()
            pdfPRI.fonts(7)
            PRPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfPRI.c.showPage()
    pdfPRI.c.save()

    pdfPRI.i = 0
    pdfPRI.newrequest()
    pdfPRI.ItemTotalClean()
    pdfPRI.DepartmentClean()
    pdfPRI.CompanyClean()
    pdfPRI.d = pdfPRI.newpage()
