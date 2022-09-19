import os
from datetime import datetime
from PrintPDF import PackingReportBoxNtAlwd_PrintPDF as pdfPRB
from Global_Files import Connection_String as con
from ProcessSelection import PackingReport_ProcessSelection as PRPS

counter = 0


def PackingReport_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo,
                                               LCLotNo, LSMachine, LCMachine, LSWinding,
                                               LCWinding, LSQuality, LCQuality, LSPallet, LCPallet, LDStartDate, LDEndDate):


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


    sql = "Select          Comp.LONGDESCRIPTION As Company " \
          ", COSTCENTER.LONGDESCRIPTION As Department " \
          ", Product.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Item " \
          ", BKLELEMENTS.LOTCODE As LotNo " \
          ", BKLELEMENTS.CODE As BoxNo " \
          ", BKLELEMENTS.WINDINGTYPECODE As WType " \
          ", Cast((BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + " \
          "BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 + " \
          "BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + " \
          "BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) As Int) as Cops " \
          ", CAST(BKLELEMENTS.ACTUALGROSSWT As Decimal(30,3)) As GrossWt " \
          ", Cast(BKLELEMENTS.ACTUALTAREWT As Decimal(30,3)) As TareWt " \
          ", Cast(BKLELEMENTS.ACTUALNETWT As Decimal(30,3)) As NetWt " \
          ", ELEMENTS.ENTRYDATE As BoxDt " \
          "From            BKLELEMENTS " \
          "Join LOGICALWAREHOUSE WHouse    On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = WHouse.CODE " \
          "Join BUSINESSUNITVSCOMPANY BUC  On      WHouse.PLANTCODE = BUC.FACTORYCODE " \
          "Join FINBUSINESSUNIT Comp       On      BUC.BUSINESSUNITCODE = Comp.CODE " \
          "Join COSTCENTER                 On      WHouse.COSTCENTERCODE = COSTCENTER.CODE " \
          "JOIN FULLITEMKEYDECODER FIKD    ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                    On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Left Join QualityLevel          On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05 " \
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code " \
          "Join STOCKTRANSACTION ST        On      BKLELEMENTS.CODE = ST.CONTAINERELEMENTCODE " \
          "AND     BKLELEMENTS.SUBCODEKEY = ST.CONTAINERSUBCODE01 " \
          "AND     ST.TEMPLATECODE = 'PS5' " \
          "Join ELEMENTS                   On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "AND     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where   ELEMENTS.ENTRYDATE      Between "+startdate+"      AND     "+enddate+" " \
          " "+Departmentcodes+" "+LotNos+" "+Machines+" "+Windings+" "+Qualitys+" "+Pallets+"  " \
          "And BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Order By Company, Department, Item, LotNo, BoxNo   "



    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfPRB.textsize(pdfPRB.c, result, pdfPRB.d,stdt,etdt)
        # percentage = (float(result['NETWT']) / pdfPRB.itemtotal) * 100
        pdfPRB.d=pdfPRB.dvalue(pdfPRB.c, result, stdt, etdt)
        result = con.db.fetch_both(stmt)

        # if pdfPRB.d<20 :
        #     pdfPRB.d=735
        #     pdfPRB.c.setPageSize(pdfPRB.portrait(pdfPRB.A4))
        #     pdfPRB.c.showPage()
        #     pdfPRB.header(stdt,etdt,pdfPRB.divisioncode)


    if result == False:
        if counter > 0:

            pdfPRB.boldfonts(7)
            pdfPRB.d = pdfPRB.dvalue(pdfPRB.c, result, stdt, etdt)
            pdfPRB.printLotTotal(pdfPRB.c, result, stdt, etdt)
            pdfPRB.printItmTotal(pdfPRB.c, result, stdt, etdt)
            pdfPRB.printDeptTotal(pdfPRB.c, result, stdt, etdt)
            pdfPRB.printCompTotal(pdfPRB.c, result, stdt, etdt)
            pdfPRB.fonts(7)

            counter = 0
        elif counter==0:
            PRPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfPRB.c.setPageSize(pdfPRB.portrait(pdfPRB.A4))
    pdfPRB.c.showPage()
    pdfPRB.c.save()

    pdfPRB.newrequest()
    pdfPRB.d = pdfPRB.newpage()
