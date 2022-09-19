import os
from datetime import datetime
from PrintPDF import ProductionSummaryWindng_PrintPDF as pdfPSW
from Global_Files import Connection_String as con
from ProcessSelection import ProductionSummary_ProcessSelection as PRSPS

counter = 0
Box = []
Cop = []
Grosswt = []
Tarewt = []
NETwt = []

def ProductionSummary_PrintPDF(LSDepartmentCode, LCDepartmentCode, LSProduction, LCProduction, LSLotNo, LCLotNo,LSItm, LCItm,
                                          LDStartDate, LDEndDate):

    global Box, Cop, Grosswt, Tarewt
    global NETwt
    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    Production = str(LSProduction)
    LSProductions = '(' + Production[1:-1] + ')'

    LotNo = str(LSLotNo)
    LSLotNos = '(' + LotNo[1:-1] + ')'

    Itm = str(LSItm)
    Itms = '(' + Itm[1:-1] + ')'

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

    if not LSLotNo and not LCLotNo:
        LotNos = " "
    elif LCLotNo:
        LotNos = " "
    elif LSLotNo:
        LotNos = "AND BKLELEMENTS.LOTCODE in " + str(LSLotNos)

    if not LSItm and not LCItm:
        LSItms = " "
    elif LCItm:
        LSItms = " "
    elif LSItm:
        LSItms = "AND Product.AbsUniqueId in " + str(Itms)



    sql = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", LOT.CODE As LotNo " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product " \
          ", RTRIM(NVL(LOT.CODE, '')) ||'   - '|| COALESCE(BKLELEMENTS.WINDINGTYPECODE,'') As LotWT " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 " \
          "+ BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 " \
          "+ BKLELEMENTS.COPSQUANTITY8 + BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 " \
          "+ BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15 ) ELSE 0 END) AS INT) As Cops " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALGROSSWT) ELSE 0 END) As DECIMAL(10,3)) As GrossWt " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALTAREWT) ELSE 0 END) As DECIMAL(10,3)) As TareWt " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALNETWT) ELSE 0 END) As DECIMAL(10,3)) As NetWt " \
          ", CAST(SUM(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then BKLELEMENTS.TOTALBOXES Else 0 End) AS INT) As Boxes " \
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
          "Where   ELEMENTS.ENTRYDATE              Between "+startdate+"      And     "+enddate+" "+LotNos+" "+LSItms+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
          ", LOT.CODE " \
          ", RTRIM(NVL(LOT.CODE, '')) ||'   - '|| COALESCE(BKLELEMENTS.WINDINGTYPECODE,'') " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') " \
          "Order By CompName, Department, Product, LotNo "


    sql2 = "Select          FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", LOT.CODE As LotNo " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 " \
          "+ BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 " \
          "+ BKLELEMENTS.COPSQUANTITY8 + BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 " \
          "+ BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15 ) ELSE 0 END) AS INT) As Cop " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALGROSSWT) ELSE 0 END) As DECIMAL(10,3)) As Gross " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALTAREWT) ELSE 0 END) As DECIMAL(10,3)) As Tare " \
          ", CAST(Sum(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then (BKLELEMENTS.ACTUALNETWT) ELSE 0 END) As DECIMAL(10,3)) As Net " \
          ", CAST(SUM(Case When ELEMENTS.ENTRYDATE Between "+startdate+"      And     "+enddate+" Then BKLELEMENTS.TOTALBOXES Else 0 End) AS INT) As Box " \
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
          "Where   ELEMENTS.ENTRYDATE              Between "+startdate+"      And     "+enddate+" "+LotNos+" "+LSItms+" "+Departmentcodes+" " \
          "And     BKLELEMENTS.ITEMTYPECODE = 'CNT' " \
          "Group By FINBUSINESSUNIT.LONGDESCRIPTION, COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
          ", LOT.CODE " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| COALESCE(QualityLevel.ShortDescription, '') " \
          "Order By CompName, Department, Product, LotNo "

    stmt2 = con.db.prepare(con.conn, sql2)
    con.db.execute(stmt2)
    results = con.db.fetch_both(stmt2)
    Box = []
    Cop = []
    Grosswt = []
    Tarewt = []
    NETwt = []
    while results != False:
        if results not in NETwt:
            Box.append(results['BOX'])
            Cop.append((results['COP']))
            Grosswt.append(float(results['GROSS']))
            Tarewt.append(float(results['TARE']))
            NETwt.append(float(results['NET']))
        results = con.db.fetch_both(stmt2)


    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfPSW.textsize(pdfPSW.c, result, pdfPSW.d,stdt,etdt,Box,Cop,Grosswt,Tarewt,NETwt)
        pdfPSW.d=pdfPSW.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfPSW.d<40 :
            pdfPSW.d = 745
            pdfPSW.c.showPage()
            pdfPSW.header(stdt,etdt, pdfPSW.divisioncode)
            pdfPSW.fonts(7)


    if result == False:
        pdfPSW.i = 0
        if counter > 0:

            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.boldfonts(7)
            pdfPSW.c.drawString(30, pdfPSW.d, "Lot-wise Total :")
            pdfPSW.c.drawAlignedString(140, pdfPSW.d, str(Box[-1]))
            pdfPSW.c.drawAlignedString(210, pdfPSW.d, str(Cop[-1]))
            pdfPSW.c.drawAlignedString(315, pdfPSW.d, str('{0:1.3f}'.format(Grosswt[-1])))
            pdfPSW.c.drawAlignedString(410, pdfPSW.d, str('{0:1.3f}'.format(Tarewt[-1])))
            pdfPSW.c.drawAlignedString(510, pdfPSW.d, str('{0:1.3f}'.format(NETwt[-1])))
            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.c.drawString(30, pdfPSW.d, "Item-wise Total :")
            pdfPSW.c.drawAlignedString(140, pdfPSW.d, str(pdfPSW.ItmBoxes))
            pdfPSW.c.drawAlignedString(210, pdfPSW.d, str(pdfPSW.ItmCops))
            pdfPSW.c.drawAlignedString(315, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.ItmGross)))
            pdfPSW.c.drawAlignedString(410, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.ItmTare)))
            pdfPSW.c.drawAlignedString(510, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.ItmNetwt)))
            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.c.drawString(30, pdfPSW.d, "Dept-wise Total :")
            pdfPSW.c.drawAlignedString(140, pdfPSW.d, str(pdfPSW.DeptBoxes))
            pdfPSW.c.drawAlignedString(210, pdfPSW.d, str(pdfPSW.DeptCops))
            pdfPSW.c.drawAlignedString(315, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.DeptGross)))
            pdfPSW.c.drawAlignedString(410, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.DeptTare)))
            pdfPSW.c.drawAlignedString(510, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.DeptNetwt)))
            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.d = pdfPSW.dvalue()
            pdfPSW.c.drawString(30, pdfPSW.d, "Company Total :")
            pdfPSW.c.drawAlignedString(140, pdfPSW.d, str(pdfPSW.CompBoxes))
            pdfPSW.c.drawAlignedString(210, pdfPSW.d, str(pdfPSW.CompCops))
            pdfPSW.c.drawAlignedString(315, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.CompGross)))
            pdfPSW.c.drawAlignedString(410, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.CompTare)))
            pdfPSW.c.drawAlignedString(510, pdfPSW.d, str('{0:1.3f}'.format(pdfPSW.CompNetwt)))
            pdfPSW.ItemClean()
            pdfPSW.DepartmentClean()
            pdfPSW.CompanyClean()
            pdfPSW.fonts(7)

            PRSPS.Exceptions = ""
            counter = 0
        elif counter==0:
            PRSPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfPSW.c.showPage()
    pdfPSW.c.save()

    pdfPSW.newrequest()
    pdfPSW.d = pdfPSW.newpage()
    pdfPSW.ItemClean()
    pdfPSW.DepartmentClean()
    pdfPSW.CompanyClean()
    pdfPSW.i = 0