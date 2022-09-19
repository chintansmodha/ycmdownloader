# function to generate report
import os
from datetime import datetime
from babel.numbers import format_currency
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from PrintPDF import PackingRegister_PrintPDF as pdfrpt
from FormLoad import PackingRegister_FormLoad as views
from GetDataFromDB import PackingRegister_GetDataFromDB as PR
from Global_Files import Connection_String as con
# from . import views
Exceptions= ""
counter = 0

def PackingRegister(request):
    LSName =datetime.now()
    LSstring =str(LSName)
    sqlwhere=''
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Packing Register/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    # pdfrpt.c = pdfrpt.canvas.Canvas(LSFileName + ".pdf")
    LSselcompany = request.GET.getlist('selcompany')
    LSselparty = request.GET.getlist('selparty')
    LSsellotno = request.GET.getlist('sellotno')
    LSselquality = request.GET.getlist('selquality')
    LSselfromdepartment = request.GET.getlist('selfromdepartment')
    LSseltodepartment = request.GET.getlist('seltodepartment')
    LSselwindingtype = request.GET.getlist('selwindingtype')
    LSselagent = request.GET.getlist('selagent')
    LSselshade = request.GET.getlist('selshade')

    try:
        LSallcompany = str(request.GET['allcompany'])
    except:
        LSallcompany=False
    try:
        LSallparty = str(request.GET['allparty'])
    except:
        LSallparty=False
    try:
        LSalllotno = str(request.GET['alllotno'])
    except:
        LSalllotno=False
    try:
        LSallquality = str(request.GET['allquality'])
    except:
        LSallquality=False
    try:
        LSallfromdepartment = str(request.GET['allfromdepartment'])
    except:
        LSallfromdepartment=False
    try:
        LSalltodepartment = str(request.GET['alltodepartment'])
    except:
        LSalltodepartment=False
    try:
        LSallwindingtype = str(request.GET['allwindingtype'])
    except:
        LSallwindingtype=False
    try:
        LSallagent = str(request.GET['allagent'])
    except:
        LSallagent=False
    try:
        LSallshade = str(request.GET['allshade'])
    except:
        LSallshade=False
    try:
        if LSallcompany == 'None' and len(LSselcompany) != 0 or str(LSallcompany) == 'False':
            company = str(LSselcompany)
            LSCompanycode = '(' + company[1:-1] + ')'
            sqlwhere += ' AND  BUnit.CODE IN ' + LSCompanycode

        if LSallparty == 'None' and len(LSselparty) != 0 or str(LSallparty) == 'False':
            party = str(LSselparty)
            LSPartycode = '(' + party[1:-1] + ')'
            sqlwhere += ' AND BusinessPartner.NumberID IN ' + LSPartycode

        if LSallquality == 'None' and len(LSselquality) != 0 or str(LSallquality) == 'False':
            quanlity = str(LSselquality)
            LSqualitycode = '(' + quanlity[1:-1] + ')'
            sqlwhere += ' AND QUALITYLEVEL.CODE IN ' + LSqualitycode

        if LSallfromdepartment == 'None' and len(LSselfromdepartment) != 0 or str(LSallfromdepartment) == 'False':
            fromdepartment = str(LSselfromdepartment)
            LSfromdepartmentcode = '(' + fromdepartment[1:-1] + ')'
            sqlwhere += ' AND COSTCENTER.CODE IN ' + LSfromdepartmentcode

        if LSalltodepartment == 'None' and len(LSseltodepartment) != 0 or str(LSalltodepartment) == 'False':
            todepartment = str(LSseltodepartment)
            LStodepartmentcode = '(' + todepartment[1:-1] + ')'
            sqlwhere += ' AND COSTCENTER.CODE IN ' + LStodepartmentcode
        #
        # if LSallwindingtype == 'None' and len(LSselwindingtype) != 0 or str(LSallwindingtype) == 'False':
        #     windingcode = str(LSselwindingtype)
        #     LSwinding = '(' + windingcode[1:-1] + ')'
        #     sqlwhere += ' AND ORDERPARTNER.CUSTOMERSUPPLIERCODE IN ' + LSwinding

        # if LSalllotno == 'None' and len(LSsellotno) != 0 or str(LSalllotno) == 'False':
        #     lotno = str(LSsellotno)
        #     LSlotnocode = '(' + lotno[1:-1] + ')'
        #     sqlwhere += ' AND  ' + LSlotnocode
        #

        if LSallagent == 'None' and len(LSselagent) != 0 or str(LSallagent) == 'False':
            agent = str(LSselagent)
            LSagentcode = '(' + agent[1:-1] + ')'
            sqlwhere += ' AND AGENT.CODE IN ' + LSagentcode

        if LSallshade == 'None' and len(LSselshade) != 0 or str(LSallshade) == 'False':
            shade = str(LSselshade)
            LSshadecode = '(' + shade[1:-1] + ')'
            sqlwhere += ' AND UGG.CODE IN ' + LSshadecode

    except:
        print("from Process selectiuon exception ")
        pass

    LSRegistertype=str(request.GET['CboRegisterType'])
    LDStartDate=str(request.GET['startdate'])
    LDEndDate=str(request.GET['enddate'])

    if LSRegistertype == '0':
        # LSFileName="Challan Reg. Details & Summary "+LSFileName
        PR.PackingPalletRegister(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                             LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                             LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                             LDStartDate,LDEndDate,LSFileName,sqlwhere)

    filepath = save_name + ".pdf"
    print(filepath)
    if not os.path.isfile(filepath):
        return render(request, 'PackingRegister.html',
                      {'company': views.company, 'party': views.party, 'lot': views.lot, 'quality': views.quality,
                       'department': views.department,'agent': views.agent, 'winding': views.winding, 'shade': views.shade})

    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

# def PackingPalletRegister(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
#                              LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
#                              LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
#                              LDStartDate,LDEndDate,LSFileName,sqlwhere):
#     sqlpalletlist="Select  Distinct PltName as PALLETNAME from " \
#         "( " \
#         "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        From BKLELEMENTS " \
#         "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE1CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "        Where BKLELEMENTS.PALLETTYPE1CODE Is Not Null " \
#         "Union All " \
#         "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        From BKLELEMENTS " \
#         "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE2CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "        Where BKLELEMENTS.PALLETTYPE2CODE Is Not Null " \
#         "Union All " \
#         "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        From BKLELEMENTS " \
#         "               Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE3CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "        Where BKLELEMENTS.PALLETTYPE3CODE Is Not Null " \
#         "Union All " \
#         "       Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        From BKLELEMENTS " \
#         "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE4CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "        Where BKLELEMENTS.PALLETTYPE4CODE Is Not Null " \
#         "Union All " \
#         "        Select    COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        From BKLELEMENTS " \
#         "                Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE5CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "        Where BKLELEMENTS.PALLETTYPE5CODE Is Not Null " \
#         ") As PltName " \
#         "Order By PltName "
#     stmtpalletlist = con.db.prepare(con.conn, sqlpalletlist)
#     stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
#     etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
#
#     # Explicitly bind parameters
#     # con.db.bind_param(stmtpalletlist, 1, stdt)
#     # con.db.bind_param(stmtpalletlist, 2, etdt)
#
#     con.db.execute(stmtpalletlist)
#     resultpalletlist = con.db.fetch_both(stmtpalletlist)
#
#     while resultpalletlist != False:
#         global counter
#         counter = counter + 1
#         pdfrpt.palletlist(resultpalletlist)
#         pdfrpt.d = pdfrpt.dvalue()
#         resultpalletlist = con.db.fetch_both(stmtpalletlist)
#         # print("after pallet append")
#
#
#
#     sql="Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName  " \
#         "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
#         "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product  " \
#         "          , LOT.CODE As LotNo  " \
#         "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'') " \
#         "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName " \
#         "          , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "          , COALESCE (BKLELEMENTS.PALLETQUANTITY1,'') As PltQty " \
#         "From BKLELEMENTS " \
#         "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE " \
#         "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
#         "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
#         "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
#         "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE  " \
#         "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId " \
#         "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
#         "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE  " \
#         "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
#         "                                          AND     IST.GroupTypeCode  In ('P09','B07')  " \
#         "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode  " \
#         "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
#         "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
#         "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
#         "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
#         "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05   " \
#         "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
#         "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
#         "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08     " \
#         "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
#         "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code    " \
#         "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE   " \
#         "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
#         "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE  " \
#         "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
#         "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE  " \
#         "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
#         "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
#         "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE1CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "  Where BKLELEMENTS.PALLETTYPE1CODE Is Not Null " \
#         "Union All " \
#         "Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
#         "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
#         "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product   " \
#         "          , LOT.CODE As LotNo   " \
#         "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'') " \
#         "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName  " \
#         "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        , COALESCE (BKLELEMENTS.PALLETQUANTITY2,'') As PltQty " \
#         "From BKLELEMENTS   " \
#         "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
#         "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE  " \
#         "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
#         "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
#         "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE   " \
#         "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
#         "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
#         "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE " \
#         "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
#         "                                          AND     IST.GroupTypeCode  In ('P09','B07')  " \
#         "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode   " \
#         "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
#         "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
#         "                                         When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
#         "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
#         "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05  " \
#         "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
#         "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
#         "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08   " \
#         "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
#         "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code   " \
#         "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE  " \
#         "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
#         "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE  " \
#         "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY   " \
#         "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE  " \
#         "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
#         "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
#         "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE2CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "  Where BKLELEMENTS.PALLETTYPE2CODE Is Not Null " \
#         "Union All " \
#         "Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName   " \
#         "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
#         "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product   " \
#         "          , LOT.CODE As LotNo   " \
#         "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'')  " \
#         "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName    " \
#         "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        , COALESCE (BKLELEMENTS.PALLETQUANTITY3,'') As PltQty " \
#         "From BKLELEMENTS   " \
#         "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
#         "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
#         "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
#         "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '') " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
#         "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE   " \
#         "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
#         "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
#         "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE   " \
#         "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
#         "                                          AND     IST.GroupTypeCode  In ('P09','B07')   " \
#         "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode " \
#         "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
#         "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
#         "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
#         "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
#         "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05  " \
#         "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
#         "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
#         "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08    " \
#         "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
#         "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code  " \
#         "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE   " \
#         "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
#         "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE   " \
#         "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
#         "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE  " \
#         "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
#         "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
#         "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE3CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "  Where BKLELEMENTS.PALLETTYPE3CODE Is Not Null " \
#         "  Union All " \
#         "Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName   " \
#         "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
#         "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product  " \
#         "          , LOT.CODE As LotNo   " \
#         "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'')   " \
#         "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName   " \
#         "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        , COALESCE (BKLELEMENTS.PALLETQUANTITY4,'') As PltQty " \
#         "From BKLELEMENTS   " \
#         "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
#         "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
#         "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
#         "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
#         "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE   " \
#         "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
#         "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
#         "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE   " \
#         "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
#         "                                          AND     IST.GroupTypeCode  In ('P09','B07')   " \
#         "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode   " \
#         "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
#         "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
#         "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
#         "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
#         "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05   " \
#         "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
#         "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
#         "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08     " \
#         "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
#         "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code   " \
#         "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE " \
#         "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
#         "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE   " \
#         "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
#         "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE " \
#         "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
#         "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE  " \
#         "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE4CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "  Where BKLELEMENTS.PALLETTYPE4CODE Is Not Null " \
#         "  Union All " \
#         " Select    BKLELEMENTS.CODE As BoxNo , FINBUSINESSUNIT.LONGDESCRIPTION As CompName   " \
#         "          , COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department   " \
#         "          , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')  As Product " \
#         "          , LOT.CODE As LotNo   " \
#         "          , (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN '(' END) ||''|| COALESCE(UGG.CODE,'')  " \
#         "          ||''|| (Case COALESCE(UGG.CODE,'') When UGG.CODE THEN ')' END) ||'   '|| COALESCE(UGG.LONGDESCRIPTION,'') As ShadeName   " \
#         "        , COALESCE (UGG_PLT.LONGDESCRIPTION,'') As PltName " \
#         "        , COALESCE (BKLELEMENTS.PALLETQUANTITY5,'') As PltQty " \
#         "From BKLELEMENTS   " \
#         "  Join    PLANT                           ON      BKLELEMENTS.PLANTCODE                 = PLANT.CODE   " \
#         "  Join    BUSINESSUNITVSCOMPANY           ON      PLANT.CODE                            = BUSINESSUNITVSCOMPANY.FACTORYCODE   " \
#         "  Join    FINBUSINESSUNIT                 ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   " \
#         "  JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE           = FIKD.ITEMTYPECODE   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')   " \
#         "                                          AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')   " \
#         "  Join PRODUCT                            ON      BKLELEMENTS.LOTITEMTYPECODE             = PRODUCT.ITEMTYPECODE  " \
#         "                                          And     FIKD.ItemUniqueId                       = Product.AbsUniqueId   " \
#         "  Left Join QualityLevel                  ON      BKLELEMENTS.QUALITYLEVELCODE            = QUALITYLEVEL.CODE   " \
#         "                                          And     BKLELEMENTS.LOTITEMTYPECODE             = QUALITYLEVEL.ITEMTYPECODE  " \
#         "  Left JOIN ItemSubcodeTemplate IST       ON      BKLELEMENTS.LOTITEMTYPECODE             = IST.ItemTypeCode   " \
#         "                                          AND     IST.GroupTypeCode  In ('P09','B07')   " \
#         "  LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode                       = UGG.UserGenericGroupTypeCode   " \
#         "                                          AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01  " \
#         "                                          When 2 Then BKLELEMENTS.LOTDECOSUBCODE02  " \
#         "                                          When 3 Then BKLELEMENTS.LOTDECOSUBCODE03  " \
#         "                                          When 4 Then BKLELEMENTS.LOTDECOSUBCODE04  " \
#         "                                          When 5 Then BKLELEMENTS.LOTDECOSUBCODE05   " \
#         "                                          When 6 Then BKLELEMENTS.LOTDECOSUBCODE06  " \
#         "                                          When 7 Then BKLELEMENTS.LOTDECOSUBCODE07  " \
#         "                                          When 8 Then BKLELEMENTS.LOTDECOSUBCODE08      " \
#         "                                          When 9 Then BKLELEMENTS.LOTDECOSUBCODE09  " \
#         "                                          When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End    = UGG.Code   " \
#         "  Join    Lot                             ON      BKLELEMENTS.LOTITEMTYPECODE              = LOT.ITEMTYPECODE  " \
#         "                                          And     BKLELEMENTS.LOTCODE                      = LOT.CODE   " \
#         "  Join    ELEMENTS                        ON      BKLELEMENTS.CODE                         = ELEMENTS.CODE   " \
#         "                                          And     BKLELEMENTS.SUBCODEKEY                   = ELEMENTS.SUBCODEKEY  " \
#         "                                          And     BKLELEMENTS.ITEMTYPECODE                 = ELEMENTS.ITEMTYPECODE " \
#         "  Join    LOGICALWAREHOUSE                ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
#         "  Left Join    COSTCENTER                 ON      LOGICALWAREHOUSE.COSTCENTERCODE           = COSTCENTER.CODE " \
#         "  Join UserGenericGroup UGG_PLT     ON      BKLELEMENTS.PALLETTYPE5CODE        = UGG_PLT.Code AND     UGG_PLT.USERGENERICGROUPTYPECODE = 'PKG' " \
#         "  Where BKLELEMENTS.PALLETTYPE5CODE Is Not Null " \
#         "Order By BoxNo "
#     # print("after sql query")
#     stmt = con.db.prepare(con.conn, sql)
#     stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
#     etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
#
#     ## Explicitly bind parameters
#     # con.db.bind_param(stmt, 1, stdt)
#     # con.db.bind_param(stmt, 2, etdt)
#
#     con.db.execute(stmt)
#     result = con.db.fetch_both(stmt)
#     print("before while result")
#     # print(result)
#     tempcounter=0
#     # pdfrpt.printpalletlist()
#
#     while result != False:
#         pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
#         pdfrpt.d = pdfrpt.dvalue()
#         result = con.db.fetch_both(stmt)
#
#         if pdfrpt.d < 20:
#             pdfrpt.d = 730
#             pdfrpt.c.showPage()
#             pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
#
#     print("after while")
#     if result == False:
#         if counter > 0:
#             pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
#             pdfrpt.fonts(7)
#
#         #     Exceptions = ""
#         # elif counter == 0:
#         #     Exceptions = "Note: Please Select Valid Credentials"
#         #     return
#
#
#         pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
#         pdfrpt.c.showPage()
#         pdfrpt.c.save()
#         # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
#         # os.startfile(url)
#         pdfrpt.newrequest()
#         pdfrpt.d=pdfrpt.newpage()
#     # else:
#     #     PRV.Exceptions = "Note: Please Select Valid Credentials"
#     #     return
#
# #
# # def printpalletlist ():
# #     counter=0
# #     printing=100
# #     while counter!= len(palletnamelist):
# #         c.drawString(60+printing, 758, palletnamelist[counter])
# #         printing=printing+100