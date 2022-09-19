import os
from datetime import datetime
from PrintPDF import FinishedStockInHandLtBox_PrintPDF as pdf
from Global_Files import Connection_String as con
from ProcessSelection import FinishedStockInHand_ProcessSelection as PRPS

counter = 0

def FinishedStockInHand_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSQuality, LCQuality, LSWinding,
                                               LCWinding, LSLotNo, LCLotNo, LSItem,LCItem, LSItmtype, LCItmtype, LDAsondate):


    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    Quality = str(LSQuality)
    LSQualitys = '(' + Quality[1:-1] + ')'

    Winding = str(LSWinding)
    LSWindings = '(' + Winding[1:-1] + ')'

    LotNo = str(LSLotNo)
    LSLotNos = '(' + LotNo[1:-1] + ')'

    Item = str(LSItem)
    Items = '(' + Item[1:-1] + ')'

    Itmtype = str(LSItmtype)
    Itmtypes = '(' + Itmtype[1:-1] + ')'

    stdt = datetime.strptime(LDAsondate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    Asondate = "'" + str(stdt) + "'"
    # enddate = "'" + str(etdt) + "'"
    #
    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "AND COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)

    if not LSQuality and not LCQuality:
        Qualitys = " "
    elif LCQuality:
        Qualitys = " "
    elif LSQuality:
        Qualitys = "AND QUALITYLEVEL.LONGDESCRIPTION ||'-'|| QUALITYLEVEL.ITEMTYPECODE in " + str(LSQualitys)

    if not LSWinding and not LCWinding:
        Windings = " "
    elif LCWinding:
        Windings = " "
    elif LSWinding:
        Windings = "AND BKLELEMENTS.WINDINGTYPECODE in " + str(LSWindings)

    if not LSLotNo and not LCLotNo:
        LotNos = " "
    elif LCLotNo:
        LotNos = " "
    elif LSLotNo:
        LotNos = "AND BKLELEMENTS.LOTCODE in " + str(LSLotNos)

    if not LSItem and not LCItem:
        LSItems = " "
    elif LCItem:
        LSItems = " "
    elif LSItem:
        LSItems = "AND Product.AbsUniqueId in " + str(Items)

    if not LSItmtype and not LCItmtype:
        LSItmtypes = " "
    elif LCItmtype:
        LSItmtypes = " "
    elif LSItmtype:
        LSItmtypes = "AND BKLELEMENTS.LOTITEMTYPECODE in " + str(Itmtypes)


    sql = "Select          Comp.LONGDESCRIPTION as Plant " \
          ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product " \
          ", BKLELEMENTS.LOTCODE As LotNo " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName " \
          ", BKLELEMENTS.Code As BoxNo " \
          ", ELEMENTS.ENTRYDATE As BoxDt " \
          ", Cast((BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + " \
          "BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 + " \
          "BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + " \
          "BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) As Int) as Cops " \
          ", CAST(BKLELEMENTS.ACTUALGROSSWT As Decimal(30,3)) As GrossWt " \
          ", Cast(BKLELEMENTS.ACTUALTAREWT As Decimal(30,3)) As TareWt " \
          ", Cast(BKLELEMENTS.ACTUALNETWT As Decimal(30,3)) As NetWt " \
          ", BKLELEMENTS.PACKSIZECODE As PSz " \
          ", BKLELEMENTS.WINDINGTYPECODE As WType " \
          "From    BKLELEMENTS " \
          "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join    BUSINESSUNITVSCOMPANY BUC       On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
          "Join    FINBUSINESSUNIT Comp            On      BUC.BUSINESSUNITCODE = Comp.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
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
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code  " \
          "Left Join    StockTransaction Desp      On      BKLELEMENTS.CODE = Desp.CONTAINERELEMENTCODE " \
          "AND     Desp.TEMPLATECODE in ('S04','I04') " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
          "And     ELEMENTS.ENTRYDATE       <=       "+Asondate+" " \
          "Where   BKLELEMENTS.ITEMTYPECODE = 'CNT' "+Qualitys+" "+Windings+" "+LotNos+" "+LSItems+" "+LSItmtypes+" "+Departmentcodes+" " \
          "AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > "+Asondate+") " \
          "Order By Plant, Department, Product, LotNo, BoxDt Desc, BoxNo  "

    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdf.textsize(pdf.c, result, pdf.d,stdt)
        pdf.d=pdf.dvalue(pdf.c, result, stdt)
        result = con.db.fetch_both(stmt)


    if result == False:
        if counter > 0:

            pdf.d = pdf.dvalue(pdf.c, result, stdt)
            if pdf.lotboxcount > 1:
                pdf.PrintLotTotal()
                pdf.d = pdf.dvalue(pdf.c, result, stdt)
                pdf.d = pdf.dvalue(pdf.c, result, stdt)
            pdf.lotboxcount = 0
            if pdf.itemlotcount > 1:
                pdf.PrintItemTotal()
                pdf.d = pdf.dvalue(pdf.c, result, stdt)
                pdf.d = pdf.dvalue(pdf.c, result, stdt)
            pdf.itemlotcount = 0
            pdf.PrintDeptTotal()

            PRPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdf.c.showPage()
    pdf.c.save()

    pdf.newrequest()
    pdf.d = pdf.newpage()
    pdf.LotTotalClean()
    pdf.ItemTotalClean()
    pdf.lotboxcount = 0
    pdf.itemlotcount = 0
    pdf.itemboxcount = 0
    pdf.deptboxcount = 0
