import os
from datetime import datetime
from PrintPDF import ProductionAnalysisMach_PrintPDF as pdfPR
from Global_Files import Connection_String as con
from ProcessSelection import ProductionAnalysis_ProcessSelection as PRAPS

counter = 0

def ProductionAnalysis_PrintPDF( LSDepartmentCode, LCDepartmentCode, LSItemCode, LCItemCode, LSItmtype, LCItmtype,
                                                     LSProduction, LCProduction, LSQuality, LCQuality, LSShadeCode, LCShadeCode,
                                                     LSMachine, LCMachine, LSLotNo, LCLotNo, LDStartDate, LDEndDate):


    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    Itemcode = str(LSItemCode)
    LSItemCodes = '(' + Itemcode[1:-1] + ')'

    Itemtypecode = str(LSItmtype)
    LSItmtypes = '(' + Itemtypecode[1:-1] + ')'

    Production = str(LSProduction)
    LSProductions = '(' + Production[1:-1] + ')'

    Quality = str(LSQuality)
    LSQualitys = '(' + Quality[1:-1] + ')'

    Shadecode = str(LSShadeCode)
    LSShadeCodes = '(' + Shadecode[1:-1] + ')'

    Machine = str(LSMachine)
    LSMachines = '(' + Machine[1:-1] + ')'

    LotNo = str(LSLotNo)
    LSLotNos = '(' + LotNo[1:-1] + ')'

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

    if not LCItemCode and not LSItemCode:
        Itemcodes = " "
    elif LCItemCode:
        Itemcodes = " "
    elif LSItemCode:
        Itemcodes = " And Product.AbsUniqueId in " + str(LSItemCodes)

    if not LCItmtype and not LSItmtype:
        Itemtypecodes = " "
    elif LCItmtype:
        Itemtypecodes = " "
    elif LSItmtype:
        Itemtypecodes = " And BKLELEMENTS.LOTITEMTYPECODE in " + str(LSItmtypes)

    if not LSProduction and not LCProduction:
        Productions = " "
    elif LCProduction:
        Productions = " "
    elif LSProduction:
        Productions = "AND  in " + str(LSProductions)

    if not LSQuality and not LCQuality:
        Qualitys = " "
    elif LCQuality:
        Qualitys = " "
    elif LSQuality:
        Qualitys = "AND QUALITYLEVEL.LONGDESCRIPTION ||'-'|| QUALITYLEVEL.ITEMTYPECODE in " + str(LSQualitys)

    if not LSShadeCode and not LCShadeCode:
        Shadecodes = " "
    elif LCShadeCode:
        Shadecodes = " "
    elif LSShadeCode:
        Shadecodes = " And COALESCE(UGG.CODE,BKLELEMENTS.SHADECODE,'') in " + str(LSShadeCodes)

    if not LSMachine and not LCMachine:
        Machines = " "
    elif LCMachine:
        Machines = " "
    elif LSMachine:
        Machines = "AND Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) in " + str(LSMachines)

    if not LSLotNo and not LCLotNo:
        LotNos = " "
    elif LCLotNo:
        LotNos = " "
    elif LSLotNo:
        LotNos = " And BKLELEMENTS.LOTCODE in " + str(LSLotNos)

    # Department wise Shade in header
    sql1 = "Select          COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
           ", COALESCE(QualityLevel.ShortDescription, '') As Quality " \
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
           "Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE  " \
           "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
           "Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
           "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
           "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.ITEMTYPECODE = IST.ItemTypeCode " \
           "AND     IST.GroupTypeCode  In ('P09','B07') " \
           "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
           "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
           "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code " \
           "Join LOGICALWAREHOUSE              On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
           "Left Join COSTCENTER                    On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
           "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
           "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
           "Where   ELEMENTS.ENTRYDATE Between " + startdate + "  And  " + enddate + " " \
           " " + Departmentcodes + " " + Itemcodes + " " + Itemtypecodes + " " + Qualitys + " " + Shadecodes + " " + Machines + " " + LotNos + " " \
           "And     BKLELEMENTS.ACTUALNETWT  > 0 " \
           "Group By COSTCENTER.LONGDESCRIPTION " \
           ", COALESCE(QualityLevel.ShortDescription, '') " \
           "Order By Department, Quality "

    stmt1 = con.db.prepare(con.conn, sql1)
    con.db.execute(stmt1)
    result = con.db.fetch_both(stmt1)

    department = []
    Qualities = []

    while result != False:
        department.append(result['DEPARTMENT'])
        Qualities.append(str(result['QUALITY']))
        result = con.db.fetch_both(stmt1)

    # main sql
    sql = "Select          COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) As machine " \
          ", COALESCE(QualityLevel.ShortDescription, '') As Quality " \
          ", CAST(SUM(Case When ELEMENTS.ENTRYDATE Between " + startdate + "  And  " + enddate + " Then BKLELEMENTS.ACTUALNETWT Else 0 End) As DECIMAL(10,3)) As NetWt " \
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
          "Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE  " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.ITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code  " \
          "Join LOGICALWAREHOUSE              On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join COSTCENTER                    On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where   ELEMENTS.ENTRYDATE              Between " + startdate + "  And  " + enddate + " " \
          "And     BKLELEMENTS.ACTUALNETWT  > 0 " \
          " " + Departmentcodes + " " + Itemcodes + " " + Itemtypecodes + " " + Qualitys + " " + Shadecodes + " " + Machines + " " + LotNos + " " \
          "Group By  COSTCENTER.LONGDESCRIPTION " \
          ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) " \
          ", COALESCE(QualityLevel.ShortDescription, '') " \
          "Order By Department, machine, Quality "


    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfPR.textsize(pdfPR.c, result, pdfPR.d,stdt,etdt, department, Qualities)
        pdfPR.d=pdfPR.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfPR.d<60 :
            pdfPR.d=735
            pdfPR.c.showPage()
            pdfPR.p = pdfPR.header(stdt,etdt,pdfPR.divisioncode, department, Qualities)
            pdfPR.fonts(7)


    if result == False:
        if counter > 0:
            pdfPR.d = pdfPR.dvalue()
            pdfPR.fonts(7)
            pdfPR.d = pdfPR.dvalueincrese()
            pdfPR.PrintClmTotal()
            l = 0
            totalSumPer = 0
            while l < len(pdfPR.PercentageQ):
                percentage = round(((float(pdfPR.PercentageQ[l]) / float(pdfPR.clmtotal)) * 100), 2)
                pdfPR.c.drawAlignedString(pdfPR.PercentageQX[l], pdfPR.d - 10, str(percentage) + ' %')
                totalSumPer = totalSumPer + percentage
                l = l + 1
            pdfPR.c.drawAlignedString(pdfPR.p + 22, pdfPR.d - 10, str(totalSumPer) + ' %')
            pdfPR.d = pdfPR.dvalue()
            pdfPR.d = pdfPR.dvalue()
            pdfPR.d = pdfPR.dvalue()
            pdfPR.d = pdfPR.dvalue()
            pdfPR.boldfonts(7)
            pdfPR.c.drawString(10, pdfPR.d, 'Department Total: ')
            l = 0
            X = 90
            totalSumPer = 0
            while l < len(pdfPR.QultyCheck):
                j = 0
                sum = 0
                while j < len(pdfPR.DeptTotalQuality):
                    if pdfPR.QultyCheck[l] == pdfPR.DeptTotalQuality[j]:
                        sum = sum + pdfPR.DeptTotal[j]
                    j = j + 1
                if int(sum) != 0:
                    pdfPR.c.drawAlignedString(X + 15, pdfPR.d, str('{0:1.3f}'.format(sum)))
                    percentage = round(((float(sum) / float(pdfPR.departmentTotal)) * 100), 2)
                    pdfPR.c.drawAlignedString(X + 22, pdfPR.d - 10, str(percentage) + ' %')
                    totalSumPer = totalSumPer + percentage
                l = l + 1
                X = X + 70
            pdfPR.c.drawAlignedString(pdfPR.p + 15, pdfPR.d, str('{0:1.3f}'.format(pdfPR.departmentTotal)))
            pdfPR.c.drawAlignedString(pdfPR.p + 22, pdfPR.d - 10, str(totalSumPer) + ' %')
            pdfPR.DepartmentClean()
            pdfPR.fonts(7)

            PRAPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRAPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfPR.c.showPage()
    pdfPR.c.save()
    pdfPR.d = pdfPR.newpage()
    pdfPR.newrequest()
    pdfPR.i = 0
