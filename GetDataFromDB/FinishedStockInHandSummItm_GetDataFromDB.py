import os
from datetime import datetime
from PrintPDF import FinishedStockInHandSummItm_PrintPDF as pdfFSIHSI
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
    startdate = "'" + str(stdt) + "'"
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


    sql = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < "+startdate+" AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= "+startdate+") Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As OpNetWt " \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE = "+startdate+" Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As RNetWt " \
          ", CAST(SUM (Case When Desp.TRANSACTIONDATE = "+startdate+" Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As IssueNetWt " \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= "+startdate+" AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > "+startdate+") Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3)) As ClNetWt " \
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
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code  " \
          "Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE " \
          "And     ELEMENTS.ENTRYDATE       <=     "+startdate+" " \
          "Left Join    StockTransaction Desp             On      BKLELEMENTS.CODE = Desp.CONTAINERELEMENTCODE " \
          "AND     Desp.TEMPLATECODE in ('S04','I04') " \
          "Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join    COSTCENTER                 On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE  " \
          "Join    BUSINESSUNITVSCOMPANY           On      LOGICALWAREHOUSE.PLANTCODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "Where   BKLELEMENTS.ITEMTYPECODE = 'CNT' "+Qualitys+" "+Windings+" "+LotNos+" "+LSItems+" "+LSItmtypes+" "+Departmentcodes+" " \
          "Group BY FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,'')   " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') " \
          "Having CAST(SUM (Case When ELEMENTS.ENTRYDATE < "+startdate+" AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= "+startdate+") Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000 " \
          "Or CAST(SUM (Case When ELEMENTS.ENTRYDATE = "+startdate+" Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  " \
          "Or CAST(SUM (Case When Desp.TRANSACTIONDATE = "+startdate+" Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  " \
          "Or CAST((SUM (Case When ELEMENTS.ENTRYDATE <= "+startdate+" AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > "+startdate+") Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3)) <> 0.000 " \
          "Order By CompName, Department, Product, shade "





    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfFSIHSI.textsize(pdfFSIHSI.c, result, pdfFSIHSI.d,stdt)
        pdfFSIHSI.d=pdfFSIHSI.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfFSIHSI.d<30 :
            pdfFSIHSI.d=745
            pdfFSIHSI.c.showPage()
            pdfFSIHSI.header(stdt,pdfFSIHSI.divisioncode)
            pdfFSIHSI.fonts(7)


    if result == False:
        if counter > 0:

            pdfFSIHSI.boldfonts(7)
            pdfFSIHSI.d = pdfFSIHSI.dvalue()
            pdfFSIHSI.c.drawString(150, pdfFSIHSI.d, "Department Total: ")
            pdfFSIHSI.c.drawAlignedString(355, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.DepOpBal)))
            pdfFSIHSI.c.drawAlignedString(430, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.DepReceipt)))
            pdfFSIHSI.c.drawAlignedString(490, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.DepIssue)))
            pdfFSIHSI.c.drawAlignedString(574, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.DepClBal)))
            pdfFSIHSI.d = pdfFSIHSI.dvalue()
            pdfFSIHSI.d = pdfFSIHSI.dvalue()
            pdfFSIHSI.c.drawString(150, pdfFSIHSI.d, "Company Total: ")
            pdfFSIHSI.c.drawAlignedString(355, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.OpBal)))
            pdfFSIHSI.c.drawAlignedString(430, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.Receipt)))
            pdfFSIHSI.c.drawAlignedString(490, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.Issue)))
            pdfFSIHSI.c.drawAlignedString(574, pdfFSIHSI.d, str('{0:1.3f}'.format(pdfFSIHSI.ClBal)))
            pdfFSIHSI.DepartmentClean()
            pdfFSIHSI.CompanyClean()
            pdfFSIHSI.fonts(7)

            PRPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfFSIHSI.c.showPage()
    pdfFSIHSI.c.save()

    pdfFSIHSI.newrequest()
    pdfFSIHSI.d = pdfFSIHSI.newpage()
    pdfFSIHSI.DepartmentClean()
    pdfFSIHSI.CompanyClean()
