import os
from datetime import datetime
from PrintPDF import FinishedStockInHandAgeing_PrintPDF as pdf
from Global_Files import Connection_String as con
from ProcessSelection import FinishedStockInHand_ProcessSelection as PRPS

counter = 0

def FinishedStockInHandAgeing_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSWinding, LCWinding, LSLotNo, LCLotNo,
                                       LSItem,LCItem, LSItmtype, LCItmtype, LDBoxondate, LDAsondate, LSDay):


    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    Winding = str(LSWinding)
    LSWindings = '(' + Winding[1:-1] + ')'

    LotNo = str(LSLotNo)
    LSLotNos = '(' + LotNo[1:-1] + ')'

    Item = str(LSItem)
    Items = '(' + Item[1:-1] + ')'

    Itmtype = str(LSItmtype)
    Itmtypes = '(' + Itmtype[1:-1] + ')'

    stdt = datetime.strptime(LDBoxondate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDAsondate, '%Y-%m-%d').date()
    boxondate = "'" + str(stdt) + "'"
    asondate = "'" + str(datetime.strptime(LDAsondate, '%Y-%m-%d').date()) + "'"
    # enddate = "'" + str(etdt) + "'"
    #
    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "And COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)

    if not LSWinding and not LCWinding:
        Windings = " "
    elif LCWinding:
        Windings = " "
    elif LSWinding:
        Windings = "AND BKL.WINDINGTYPECODE in " + str(LSWindings)

    if not LSLotNo and not LCLotNo:
        LotNos = " "
    elif LCLotNo:
        LotNos = " "
    elif LSLotNo:
        LotNos = "AND BKL.LOTCODE in " + str(LSLotNos)

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
        LSItmtypes = "AND BKL.LOTITEMTYPECODE in " + str(Itmtypes)

    string = ''
    i = 0
    while i <= len(LSDay):
        if i == 0:
            string += (
                f"CAST(Sum(Case When DAYS({boxondate}) - DAYS((ELEMENTS.ENTRYDATE)) <= {LSDay[i]}  Then (BKL.ACTUALNETWT) Else 0 End) As Decimal(30,3)) As Less{LSDay[i]}")
        elif i != 0 and i != len(LSDay):
            string += (
                f",CAST(Sum(Case When DAYS({boxondate}) - DAYS((ELEMENTS.ENTRYDATE)) > {LSDay[i - 1]} And DAYS({boxondate}) - DAYS((ELEMENTS.ENTRYDATE)) <= {LSDay[i]} Then (BKL.ACTUALNETWT) Else 0 End) As Decimal(30,3)) As Less{LSDay[i]}")
        elif i == len(LSDay):
            string += (
                f",CAST(Sum(Case When DAYS({boxondate}) - DAYS((ELEMENTS.ENTRYDATE)) > {LSDay[i - 1]} Then (BKL.ACTUALNETWT) Else 0 End) As Decimal(30,3)) As Above{LSDay[i - 1]} ")
        # print(i)
        i += 1
    # print(LSDay)

    sql = "Select          COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department" \
          ", PRODUCT.LONGDESCRIPTION As Item" \
          ", UGG.Code As ShadeCode " \
          ", BKL.LOTCODE As LotNo " \
          ", COALESCE(AVLQlty.AVQUALITYGROUPCODE, '') As QualityGroup  " \
          ", " + string + " " \
          ", CAST(Sum(BKL.ACTUALNETWT) As Decimal(30,3)) As Total " \
          "From    BKLELEMENTS BKL " \
          "JOIN    FULLITEMKEYDECODER FIKD         ON      BKL.LOTITEMTYPECODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(BKL.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         On      BKL.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Left Join AVQUALITYGROUPDETAIL AVLQlty  On      BKL.QUALITYLEVELCODE = AVLQlty.QUALITYCODE " \
          "And     BKL.LOTITEMTYPECODE = AVLQlty.QUALITYITEMTYPECODE " \
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKL.LOTITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then BKL.LOTDECOSUBCODE01 When 2 Then BKL.LOTDECOSUBCODE02 When 3 Then BKL.LOTDECOSUBCODE03 When 4 Then BKL.LOTDECOSUBCODE04 When 5 Then BKL.LOTDECOSUBCODE05 " \
          "When 6 Then BKL.LOTDECOSUBCODE06 When 7 Then BKL.LOTDECOSUBCODE07 When 8 Then BKL.LOTDECOSUBCODE08 When 9 Then BKL.LOTDECOSUBCODE09 When 10 Then BKL.LOTDECOSUBCODE10 End = UGG.Code " \
          "Left Join    StockTransaction Desp      On      BKL.CODE = Desp.CONTAINERELEMENTCODE " \
          "AND     Desp.TEMPLATECODE in ('S04','I04') " \
          "Join    ELEMENTS                        On      BKL.CODE = ELEMENTS.CODE " \
          "And     BKL.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "And     BKL.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
          "Join    LOGICALWAREHOUSE                On      BKL.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Where   ELEMENTS.ENTRYDATE       <=     "+boxondate+" "+Departmentcodes+" "+Windings+" "+LotNos+" "+LSItems+" "+LSItmtypes+" " \
          "AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > "+asondate+") " \
          "Group By        COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
          ", PRODUCT.LONGDESCRIPTION " \
          ", UGG.Code " \
          ", BKL.LOTCODE " \
          ", COALESCE(AVLQlty.AVQUALITYGROUPCODE, '') " \
          "Order By        Department, Item, ShadeCode, LotNo, QualityGroup "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdf.textsize(pdf.c, result, pdf.d, etdt, LSDay)
        pdf.d = pdf.dvalue(etdt,result, pdf.divisioncode,LSDay)
        result = con.db.fetch_both(stmt)


    if result == False:
        if counter > 0:

            pdf.d = pdf.dvalue(etdt, result, pdf.divisioncode, LSDay)
            pdf.ItemTotal(etdt, result, pdf.d, pdf.divisioncode, LSDay)
            pdf.d = pdf.dvalue(etdt, result, pdf.divisioncode, LSDay)
            pdf.d = pdf.dvalue(etdt, result, pdf.divisioncode, LSDay)
            pdf.DepartmentTotal(etdt, result, pdf.d, pdf.divisioncode, LSDay)

            PRPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRPS.Exceptions="Note: No Report Form For Given Criteria"
            return



    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    # print(pdf.pageSize)
    # if pdf.pageSize == 3:
    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    pdf.c.showPage()
    pdf.c.save()

    pdf.newrequest()
    pdf.d = pdf.newpage()
    pdf.departmentTotal = []
    pdf.itemTotal = []
    pdf.itemTotal2 = []