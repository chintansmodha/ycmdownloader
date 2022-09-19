from django.http import HttpResponse
from PrintPDF import PackingRegister_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
import os
from  datetime import datetime
from ProcessSelection import PackingRegister_ProcessSelection as PRV
counter=0
def PackingPalletRegister(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                             LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                             LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                             LDStartDate,LDEndDate,LSFileName,sqlwhere):

    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"
    where = " AND ELEMENTS.ENTRYDATE BETWEEN " +StartDate +" AND "+EndDate
    # where=""
    sql=""
    sqlpalletlist = "Select  Distinct PltName as PALLETNAME from " \
                "( " \
            "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        From BKLELEMENTS " \
            "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE1CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
            "        Where BKLELEMENTS.PALLETTYPE1CODE Is Not Null "+where +" "\
            " Union All " \
            "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        From BKLELEMENTS " \
            "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE2CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
            "        Where BKLELEMENTS.PALLETTYPE2CODE Is Not Null "+where+" " \
            " Union All " \
            "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        From BKLELEMENTS " \
            "               Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE3CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
            "        Where BKLELEMENTS.PALLETTYPE3CODE Is Not Null "+where+" " \
            " Union All " \
            "       Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        From BKLELEMENTS " \
            "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE4CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
            "        Where BKLELEMENTS.PALLETTYPE4CODE Is Not Null "+where+" " \
            " Union All " \
            "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        From BKLELEMENTS " \
            "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE5CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
            "        Where BKLELEMENTS.PALLETTYPE5CODE Is Not Null "+where+" " \
            ") As PltName " \
            "Order By PltName "
    # print(sqlpalletlist)
    resultpallet=""
    stmt = con.db.prepare(con.conn, sqlpalletlist)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    resultpallet = con.db.fetch_both(stmt)
    # except:
    #     PRV.Exceptions = "Database Connection Lost"
    #     return
    if resultpallet != False:
        while resultpallet != False:
            global counter
            counter = counter + 1
            print(resultpallet)
            pdfrpt.palletlist(resultpallet)
            # pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            pdfrpt.d = pdfrpt.dvalue()
            resultpallet = con.db.fetch_both(stmt)

    result=""
    sql="Select     BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName  " \
            "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
            "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product  " \
            "          , LOT.CODE As LotNo  " \
            "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'') " \
            "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName " \
            "          , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "          , Cast(BKLELEMENTS.PALLETQUANTITY1 AS DEcimal(20,0)) As PltQty          " \
            ", BKLELEMENTS.NoOfSpools As COPS          " \
            ", BKLELEMENTS.ACTUALGROSSWT AS GROSSWT          " \
            ", BKLELEMENTS.ACTUALTAREWT AS TAREWT          " \
            ", BKLELEMENTS.ACTUALNETWT AS NETWT " \
        ",ELEMENTS.ENTRYDATE as ENTRYDATE " \
            "From BKLELEMENTS " \
            "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE " \
            "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
            "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
            "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
            "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE  " \
            "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId " \
            "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
            "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE  " \
            "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
            "                                          AND     IST.GroupTypeCode  In ('P09','B07')  " \
            "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode  " \
            "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
            "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
            "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
            "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
            "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05   " \
            "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
            "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
            "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08     " \
            "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
            "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code    " \
            "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE   " \
            "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
            "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE  " \
            "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
            "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE  " \
            "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
            "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
            "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE1CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "  Where BKLELEMENTS.PALLETTYPE1CODE Is Not Null  "+where +" "\
            "Union All " \
            "Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
            "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
            "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product   " \
            "          , LOT.CODE As LotNo   " \
            "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'') " \
            "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName  " \
            "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        , Cast(BKLELEMENTS.PALLETQUANTITY1 AS DEcimal(20,0)) As PltQty          " \
            ", BKLELEMENTS.NoOfSpools As COPS          " \
            ", BKLELEMENTS.ACTUALGROSSWT AS GROSSWT          " \
            ", BKLELEMENTS.ACTUALTAREWT AS TAREWT          " \
            ", BKLELEMENTS.ACTUALNETWT AS  NETWT " \
                                                                       ",ELEMENTS.ENTRYDATE as ENTRYDATE " \
            "From BKLELEMENTS   " \
            "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
            "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE  " \
            "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
            "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
            "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE   " \
            "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
            "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
            "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE " \
            "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
            "                                          AND     IST.GroupTypeCode  In ('P09','B07')  " \
            "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode   " \
            "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
            "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
            "                                         When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
            "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
            "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05  " \
            "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
            "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
            "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08   " \
            "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
            "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code   " \
            "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE  " \
            "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
            "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE  " \
            "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY   " \
            "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE  " \
            "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
            "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
            "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE2CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "  Where BKLELEMENTS.PALLETTYPE2CODE Is Not Null  "+where +" "\
            "Union All " \
            "Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName   " \
            "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
            "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product   " \
            "          , LOT.CODE As LotNo   " \
            "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'')  " \
            "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName    " \
            "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        , Cast(BKLELEMENTS.PALLETQUANTITY1 AS DEcimal(20,0)) As PltQty          " \
            ", BKLELEMENTS.NoOfSpools As COPS          " \
            ", BKLELEMENTS.ACTUALGROSSWT AS GROSSWT          " \
            ", BKLELEMENTS.ACTUALTAREWT AS TAREWT          " \
            ", BKLELEMENTS.ACTUALNETWT AS  NETWT " \
                                                                       ",ELEMENTS.ENTRYDATE as ENTRYDATE " \
            "From BKLELEMENTS   " \
            "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
            "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
            "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
            "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '') " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
            "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE   " \
            "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
            "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
            "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE   " \
            "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
            "                                          AND     IST.GroupTypeCode  In ('P09','B07')   " \
            "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode " \
            "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
            "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
            "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
            "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
            "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05  " \
            "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
            "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
            "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08    " \
            "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
            "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code  " \
            "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE   " \
            "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
            "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE   " \
            "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
            "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE  " \
            "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
            "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
            "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE3CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "  Where BKLELEMENTS.PALLETTYPE3CODE Is Not Null   "+where +" "\
            "  Union All " \
            " Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName   " \
            "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
            "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product  " \
            "          , LOT.CODE As LotNo   " \
            "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'')   " \
            "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName   " \
            "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        , Cast(BKLELEMENTS.PALLETQUANTITY1 AS DEcimal(20,0)) As PltQty          " \
            ", BKLELEMENTS.NoOfSpools As COPS          " \
            ", BKLELEMENTS.ACTUALGROSSWT AS GROSSWT          " \
            ", BKLELEMENTS.ACTUALTAREWT AS TAREWT          " \
            ", BKLELEMENTS.ACTUALNETWT AS  NETWT " \
                                                                        ",ELEMENTS.ENTRYDATE as ENTRYDATE " \
            "From BKLELEMENTS   " \
            "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
            "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
            "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
            "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
            "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE   " \
            "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
            "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
            "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE   " \
            "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
            "                                          AND     IST.GroupTypeCode  In ('P09','B07')   " \
            "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode   " \
            "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
            "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
            "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
            "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
            "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05   " \
            "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
            "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
            "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08     " \
            "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
            "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code   " \
            "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE " \
            "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
            "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE   " \
            "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
            "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE " \
            "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
            "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
            "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE4CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "  Where BKLELEMENTS.PALLETTYPE4CODE Is Not Null  "+where +" "\
            "  Union All " \
            " Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName   " \
            "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
            "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product " \
            "          , LOT.CODE As LotNo   " \
            "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'')  " \
            "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName   " \
            "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
            "        , Cast(BKLELEMENTS.PALLETQUANTITY1 AS DEcimal(20,0)) As PltQty          " \
            ", BKLELEMENTS.NoOfSpools As COPS          " \
            ", BKLELEMENTS.ACTUALGROSSWT AS GROSSWT          " \
            ", BKLELEMENTS.ACTUALTAREWT AS TAREWT          " \
            ", BKLELEMENTS.ACTUALNETWT AS  NETWT " \
            ",ELEMENTS.ENTRYDATE as ENTRYDATE " \
            " From BKLELEMENTS   " \
            "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
            "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
            "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
            "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
            "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
            "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE  " \
            "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
            "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
            "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE  " \
            "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
            "                                          AND     IST.GroupTypeCode  In ('P09','B07')   " \
            "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode   " \
            "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
            "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
            "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
            "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
            "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05   " \
            "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
            "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
            "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08      " \
            "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
            "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code   " \
            "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE  " \
            "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
            "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE   " \
            "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
            "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE " \
            "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
            "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE " \
            "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE5CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
            "  Where BKLELEMENTS.PALLETTYPE5CODE Is Not Null   "+where +" "\
            " Order By BoxNo, PltName "

    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # except:
    #     PRV.Exceptions = "Database Connection Lost"
    #     return
    pdfrpt.newrequest()
    if result!=False:
        while result != False:
    #         global counter
    #         counter=counter+1
            pdfrpt.textsize(pdfrpt.c, result,stdt,etdt)
            # pdfrpt.d=pdfrpt.dvalue()
            # print(result)
            result = con.db.fetch_both(stmt)


            if pdfrpt.d<20:
                # pdfrpt.d=690
                # pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
                pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A2))
                pdfrpt.c.showPage()
                pdfrpt.header(stdt,etdt,pdfrpt.divisioncode)

        pdfrpt.printasttotal()
        pdfrpt.dvalue()
        pdfrpt.printpallettotal()
        pdfrpt.printdepertmenttotal()
        if result == False:
            if counter>0:
                pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
                pdfrpt.fonts(7)
                # pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
                # pdfrpt.c.drawString(490, pdfrpt.d, "Basic Value Total : " + str("%.2f" % float(pdfrpt.ItemAmountTotal)))
                # pdfrpt.c.drawAlignedString(690, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))
                # pdfrpt.d = pdfrpt.dvalue()
                # pdfrpt.c.drawString(490, pdfrpt.d, "Charges Total : " + str("%.2f" % float(pdfrpt.ChargesTotal)))
                # pdfrpt.companyclean()
                PRV.Exceptions=""
            elif counter==0:
                PRV.Exceptions="Note: Please Select Valid Credentials"
                return

        # pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        # pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d=pdfrpt.newpage()
    else:
        PRV.Exceptions = "Note: Please Select Valid Credentials"
        return

    result=""