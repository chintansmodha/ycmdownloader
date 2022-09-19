import os
from datetime import datetime

from babel.numbers import format_currency
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from Global_Files import Connection_String as con
from FormLoad import StoreRegister_FormLoad as views

Exceptions = ""

counter = 0
GBasecode = ""  # This code is use to save the uniqueid value from the maintable of the first page
GList = []
GSecondList = []
GLine = []

GChallanno = []
GChallanDate = []
GQuantity = []
save_name = ''
Greportname=""
Gheader=""
startdate = ""
enddate = ""
reporttype = ""


def DispatchDetails(request):
    global save_name

    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSRegisterType = str(request.GET['CboRegisterType'])
    LSReportType = ''
    global GChallanno
    global GChallanDate
    global GQuantity
    global startdate
    global enddate
    global reporttype
    global Greportname
    global Gheader

    startdate = LDStartDate
    enddate = LDEndDate
    reporttype = LSRegisterType
    sqlwhere = ""
    sqlwhere = " AND SD.PROVISIONALDOCUMENTDATE between '" + LDStartDate + "' and '" + LDEndDate + "'"
    print(LSRegisterType)
    if LSRegisterType == '0':
        sql = " SELECT  Product.ABSUNIQUEID as uniqueid, " \
              "        trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS LONGDESCRIPTION " \
              "         , SDL.USERPRIMARYUOMCODE " \
              "        , sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY    " \
              "FROM SALESDOCUMENT SD " \
              "JOIN SALESDOCUMENTLINE SDL      ON SD.PROVISIONALCODE   = SDL.SALESDOCUMENTPROVISIONALCODE " \
              "JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
              "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
              "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
              "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
              "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
              "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
              "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
              "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
              "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
              "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
              "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
              " Join Product                On      SDL.ITEMTYPEAFICODE           	 = Product.ITEMTYPECODE    " \
              "                            And     FIKD.ItemUniqueId                   = Product.AbsUniqueId " \
              " JOIN QUALITYLEVEL               ON      SDL.QUALITYCODE                = QUALITYLEVEL.CODE " \
              "                                AND     SDL.ITEMTYPEAFICODE             = QUALITYLEVEL.ITEMTYPECODE " \
              " WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
                                                                " group by         Product.LONGDESCRIPTION         , QualityLevel.ShortDescription        , SDL.USERPRIMARYUOMCODE         , Product.ABSUNIQUEID "

        Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, Greportname, Gheader)
        Greportname = "Item Wise"
        Gheader = "Item"
        # return itemlist1
        # return  render(request,'DispatchDetailRegister.html',{'GList':GList,"LSRegisterType":LSRegisterType})
    elif LSRegisterType == '1':
        sql = "SELECT agent.code as uniqueid, " \
              "        Agent.LongDescription As LONGDESCRIPTION " \
              "        ,  sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
              "FROM SALESDOCUMENT SD " \
              "        JOIN Agent                      ON      SD.Agent1Code                                     = Agent.Code   " \
              "        JOIN SALESDOCUMENTLINE SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE          = SD.PROVISIONALCODE " \
              "                                        AND     SDL.SALDOCPROVISIONALCOUNTERCODE          = SD.PROVISIONALCOUNTERCODE " \
              "        JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE  " \
              "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
              "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')  " \
              "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')  " \
              "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')  " \
              "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
              "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
              "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')  " \
              "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')  " \
              "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')  " \
              "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')  " \
              "        Join Product                On      SDL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE  " \
              "                                    And     FIKD.ItemUniqueId                           = Product.AbsUniqueId  " \
              "WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
                                                               "GROUP BY " \
                                                               "        Agent.LongDescription,agent.code"
        Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, Greportname, Gheader)
        Greportname = "Agent Wise"
        Gheader = "Agent"
        # return itemlist2
        # return  render(request,'DispatchDetailRegister.html',{'GList':GList,"LSRegisterType":LSRegisterType})
    elif LSRegisterType == '2':
        sql = "SELECT " \
              "		 UGG.ABSUNIQUEID as UNIQUEID , " \
              "        TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As LONGDESCRIPTION , " \
              "         sum(COALESCE(CAST(SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
              "FROM SALESDOCUMENT SD " \
              "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SD.PROVISIONALCODE " \
              "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode " \
              "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
              "JOIN UserGenericGroup UGG      ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode   " \
              "                                AND     Case IST.Position    " \
              "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03    " \
              "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06    " \
              "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09    " \
              "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
              "JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
              "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
              "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
              "WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
                                                               "GROUP BY UGG.LONGDESCRIPTION ,UGG.ABSUNIQUEID , UGG.CODE  "
        Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, Greportname, Gheader)
        Greportname = "Shade Wise"
        Gheader = "Shade"
        # return itemlist3
        # return  render(request,'DispatchDetailRegister.html',{'GList':GList,"LSRegisterType":LSRegisterType})

    return render(request, 'DispatchDetailRegister.html',
                  {'GList': GList, "LSRegisterType": LSRegisterType, "reportname": Greportname, "header": Gheader,
                   "LDStartDate": LDStartDate, "LDEndDate": LDEndDate})


def Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, reportname, header):
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"
    counter = 0
    result = ""
    global Greportname
    global Gheader
    global Exceptions
    GList.clear()
    GLine.clear()
    GSecondList.clear()
    print("sql for item list")
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    if result != False:
        while result != False:
            GList.append(result)
            # print(result['CHALLANNUMBER'])
            result = con.db.fetch_both(stmt)
    else:
        print("from else" )
        # return render(request, 'StoreRegister.html',
        #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
        #                'ccode': ccode})
        Exceptions = "No data found according to entered date"
        print(Exceptions)
        return render(request, 'DispatchDetailRegister.html',
                      {'GList': GList, "LSRegisterType": LSRegisterType, "reportname": Greportname, "header": Gheader,
                       "LDStartDate": LDStartDate, "LDEndDate": LDEndDate, "Exceptions": Exceptions})


def DespatchDetailItemList(request):
    LSItemcode = str(request.GET['uniqueid'])
    LSRegisterType = str(request.GET['regeistertype'])
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    result = ""

    header = ""
    GSecondList.clear()
    GLine.clear()
    global startdate
    global enddate
    global reporttype
    global GBasecode
    global Greportname
    global Gheader
    startdate = LDStartDate
    enddate = LDEndDate
    reporttype = LSRegisterType
    GBasecode = LSItemcode
    print("*--*-*-*-*-*-*-*-*-**-*  from list " + LSItemcode)
    print("register type from list : " + str(LSRegisterType))
    sqlwhere = " AND SD.PROVISIONALDOCUMENTDATE between '" + LDStartDate + "' and '" + LDEndDate + "'"
    print(sqlwhere)
    # sqlorderby = " ORDER BY SALESDOCUMENT.PROVISIONALDOCUMENTDATE,SALESDOCUMENT.PROVISIONALCODE"
    sql = ""
    sqlorderby = ""
    if LSRegisterType == '0':
        header = "Agent"
        sql = " SELECT agent.code as uniqueid," \
              "        Agent.LongDescription As LONGDESCRIPTION " \
              "        ,  sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
              " FROM SALESDOCUMENT SD " \
              "        JOIN Agent                      ON      SD.Agent1Code                                     = Agent.Code   " \
              "        JOIN SALESDOCUMENTLINE SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE          = SD.PROVISIONALCODE " \
              "                                        AND     SDL.SALDOCPROVISIONALCOUNTERCODE          = SD.PROVISIONALCOUNTERCODE " \
              "        JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
              "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
              "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
              "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
              "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
              "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
              "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
              "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
              "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
              "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
              "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
              "        Join Product                On      SDL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE " \
              "                                    And     FIKD.ItemUniqueId             = Product.AbsUniqueId  " \
              " WHERE SD.DocumentTypeType = '06'  " + sqlwhere + " " \
                                                                 "     AND   PRODUCT.ABSUNIQUEID = '" + LSItemcode + "'" \
                                                                                                                     " GROUP BY " \
                                                                                                                     "        Agent.LongDescription ,agent.code "
    elif LSRegisterType == '1':
        header = "Item"
        sql = " SELECT " \
              "        Product.ABSUNIQUEID as uniqueid " \
              "		   , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS LONGDESCRIPTION " \
              "        , SDL.USERPRIMARYUOMCODE  " \
              "        , sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
              " FROM SALESDOCUMENT SD " \
              " JOIN SALESDOCUMENTLINE SDL      ON SD.PROVISIONALCODE   = SDL.SALESDOCUMENTPROVISIONALCODE " \
              " JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
              "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
              "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
              "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
              "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
              "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
              "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
              "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
              "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
              "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
              "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
              " Join Product                		On      SDL.ITEMTYPEAFICODE          = Product.ITEMTYPECODE    " \
              "                            		    And     FIKD.ItemUniqueId            = Product.AbsUniqueId  " \
              " JOIN QUALITYLEVEL               	ON      SDL.QUALITYCODE              = QUALITYLEVEL.CODE " \
              "                                	    AND     SDL.ITEMTYPEAFICODE          = QUALITYLEVEL.ITEMTYPECODE  " \
              " JOIN Agent                      	ON      SD.Agent1Code                = Agent.Code " \
              " WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
            " AND Agent.code='" + LSItemcode + "' " \
                                               " group by  " \
                                               "        Product.LONGDESCRIPTION  " \
                                               "        , QualityLevel.ShortDescription " \
                                               "        , SDL.USERPRIMARYUOMCODE  " \
                                               "        , Product.ABSUNIQUEID "
    elif LSRegisterType == '2':
        header = "Item"
        sql = "select " \
              "		Product.ABSUNIQUEID as uniqueid " \
              "        , Product.LONGDESCRIPTION " \
              "        , SALESDOCUMENTLINE.USERPRIMARYUOMCODE  " \
              "        , sum(COALESCE(CAST(SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY    " \
              "FROM SALESDOCUMENT  SD " \
              "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SD.PROVISIONALCODE " \
              "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode " \
              "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
              "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode   " \
              "                                AND     Case IST.Position    " \
              "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03    " \
              "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06    " \
              "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09    " \
              "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
              "JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
              "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
              "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
              "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
              " JOIN QUALITYLEVEL               	ON      SALESDOCUMENTLINE.QUALITYCODE              = QUALITYLEVEL.CODE " \
              "                                	    AND     SALESDOCUMENTLINE.ITEMTYPEAFICODE          = QUALITYLEVEL.ITEMTYPECODE  " \
              "WHERE SD.DocumentTypeType = '06' " + sqlwhere + "  " \
               "AND UGG.CODE='" + LSItemcode + "' " \
               "GROUP BY Product.LONGDESCRIPTION  " \
               "        , QualityLevel.ShortDescription " \
               "        , SALESDOCUMENTLINE.USERPRIMARYUOMCODE  " \
               "        , Product.ABSUNIQUEID "

    sql += sqlorderby
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result != False:
        while result != False:
            GSecondList.append(result)
            print(result)
            # print(result['CHALLANNUMBER'])
            result = con.db.fetch_both(stmt)
        return render(request, 'DispatchDetailRegisterList.html',
                      {'GSecondList': GSecondList, 'startdate': startdate, 'enddate': enddate, 'reporttype': reporttype,
                       'header': header})
    else:
        # return render(request, 'StoreRegister.html',
        #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
        #                'ccode': ccode})
        Exceptions = "Note: Please Select Valid Credentials"
        return render(request, 'DispatchDetailRegister.html',
                      {'GList': GList, "LSRegisterType": LSRegisterType, "reportname": Greportname, "header": Gheader,
                       "LDStartDate": LDStartDate, "LDEndDate": LDEndDate, "Exceptions": Exceptions})

        # return
    return render(request, 'DispatchDetailRegisterList.html',
                  {'GList': GSecondList, 'startdate': startdate, 'enddate': enddate, 'reporttype': reporttype})


def DespatchDetailLine(request):
    global GSecondList
    global reporttype
    global startdate
    global enddate
    global GBasecode
    result = ""
    GLine.clear()
    LSItemcode = str(request.GET['uniqueid'])
    # LDStartDate = str(request.GET['startdate'])
    # LDEndDate = str(request.GET['enddate'])
    print("*--*-*-*-*-*-*-*-*-**-* from line  " + LSItemcode)
    print("*--*-*-*-*-*-*-*-*-**-*  start date  fromm line" + startdate)
    print("*--*-*-*-*-*-*-*-*-**-*  end date fron line " + enddate)
    print("*--*-*-*-*-*-*-*-*-**-*  report type  from line " + reporttype)
    print("*--*-*-*-*-*-*-*-*-**-*  Base code  from line " + GBasecode)
    sql = ""
    sqlwhere = " AND SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + startdate + "' and '" + enddate + "' "
    if reporttype == '0':
        sqlwhere += " AND AGENT.CODE = '" + LSItemcode + "' AND PRODUCT.ABSUNIQUEID = '" + GBasecode + "' "
    elif reporttype == '1':
        sqlwhere += " AND PRODUCT.ABSUNIQUEID = " + LSItemcode + " AND AGENT.CODE = '" + GBasecode + "' "
    elif reporttype == '2':
        sqlwhere += " AND UGG.CODE = '" + LSItemcode + "' AND PRODUCT.ABSUNIQUEID = " + GBasecode + " "

    sqlwhere += " ORDER BY SALESDOCUMENT.PROVISIONALDOCUMENTDATE,SALESDOCUMENT.PROVISIONALCODE"

    sql = " SELECT SALESDOCUMENT.PROVISIONALCODE                   AS INVOICENUMBER " \
          "        , VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE,'DD/MM/YYYY')         AS INVOICEDATE " \
          "        , Coalesce(Doc05.ExternalReference,'')          as LRNO " \
          "        , Coalesce(TZ_DespTo.LONGDESCRIPTION,'')        as DespTO " \
          "        , ''                                            AS LIFTDATE " \
          "        , PLANTINVOICE.TRUCKNO                          AS LORRYNO " \
          "        , BP_Consignee.LEGALNAME1                       AS CUSTOMER " \
          "        , COALESCE(SaleLot.ValueString,ST.LOTCODE)      AS LOTNUMBER " \
          "        , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As ShadeCode " \
          "        , CAST(SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS DECIMAL(20,3)) AS QUANTITY " \
          "        , CAST(InvRate.calculatedvalueRCC  AS DECIMAL(20,2))         AS RATE " \
          "        , PLANTINVOICELINE.NUMBEROFBALES                as Boxes  " \
          "        , CAST(PLANTINVOICE.NETTVALUE AS DECIMAL(20,2)) As INVOICEAMOUNT  " \
          "        , Agent.LongDescription                         AS BROKERNAME " \
          "        , SALESDOCUMENT.SALESORDERCODE                  AS ORDERNO " \
          "        , SALESDOCUMENTline.PreviousCode                AS CHALLANNO " \
          "        , Agent.Longdescription                         AS CONSIGNERNAME " \
          "        , COMPANY.LONGDESCRIPTION                       AS companyname  " \
          "        , trim (Product.LONGDESCRIPTION )               AS PRODUCT " \
          "        , trim ( QualityLevel.ShortDescription)         AS QUALITY " \
          "FROM SALESDOCUMENT " \
          "join OrderPartner               On      SALESDOCUMENT.OrdPrnCustomerSupplierCode 			  = OrderPartner.CustomerSupplierCode " \
          "                                And     OrderPartner.CustomerSupplierType 					  = 1 " \
          "join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId            = BusinessPartner.NumberID " \
          "JOIN Agent                      ON      SALESDOCUMENT.Agent1Code                             = Agent.Code   " \
          "JOIN SALESDOCUMENTLINE          ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
          "                                AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE       = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
          "                                AND     SALESDOCUMENTLINE.DOCUMENTTYPETYPE                   ='06' " \
          "JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
          "JOIN BusinessUnitVsCompany BUC  ON      SalesDocument.DivisionCode                           = BUC.DivisionCode " \
          "                                AND     LOGICALWAREHOUSE.plantcode                           = BUC.factorycode " \
          "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode                                 = BUnit.Code And BUnit.GroupFlag = 0 " \
          "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode                                    = Company.Code And Company.GroupFlag = 1 " \
          "JOIN ITEMTYPE                   ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
          "JOIN QUALITYLEVEL               ON      SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
          "                                AND     SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = QUALITYLEVEL.ITEMTYPECODE " \
          "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = IST.ItemTypeCode " \
          "                                AND     IST.GroupTypeCode In ('P09','B07') " \
          "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode                                  = UGG.UserGenericGroupTypeCode   " \
          "                                AND     Case IST.Position    " \
          "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03    " \
          "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06    " \
          "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09    " \
          "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
          "JOIN FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
          "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
          "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
          "JOIN PlantInvoice           ON      SALESDOCUMENT.PROVISIONALCODE               = PLANTINVOICE.CODE " \
          "                            and     SALESDOCUMENT.DocumentTypeType              = '06' " \
          "LEFT Join StockTransaction St   On      SALESDOCUMENTline.PreviousCode          =  ST.OrderCode " \
          "                            And     ST.TemplateCode                             = 'S04' " \
          "                            and     St.transactiondetailnumber                  = 1 " \
          "Left Join SalesDocument Doc05      On      Doc05.ProvisionalCode     			 = SALESDOCUMENTline.PreviousCode " \
          "                                	And     Doc05.DocumentTypeType         		 = '05' " \
          "LEFT JOIN OrderPartner OP_Consignee     On      PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERCODE 	 = OP_Consignee.CustomerSupplierCode " \
          "                                        And     OP_Consignee.CustomerSupplierType 				 = 1 " \
          "join BusinessPartner   BP_Consignee     On      OP_Consignee.OrderbusinessPartnerNumberId       = BP_Consignee.NumberID " \
          "LEFT JOIN Address ADDRESS_Consignee     ON      BP_Consignee.ABSUNIQUEID         				 = ADDRESS_Consignee.UNIQUEID " \
          "                                        AND     PlantInvoice.DELIVERYPOINTCODE             	 = ADDRESS_Consignee.CODE   " \
          "left JOIN Transportzone TZ_DespTo   on          ADDRESS_Consignee.TRANSPORTZONECODE             = TZ_DespTo.code  " \
          "JOIN PLANTINVOICELINE               ON          PLANTINVOICELINE.PLANTINVOICECODE               = PLANTINVOICE.CODE " \
          "                                    AND         PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE       = PLANTINVOICE.DIVISIONCODE " \
          "JOIN INDTAXDETAIL InvRate           ON          PlantInvoiceLine.ABSUNIQUEID                    = InvRate.ABSUNIQUEID " \
          "                                    AND         InvRate.itaxcode                                = 'INR'  " \
          "                                    AND         InvRate.TAXCATEGORYCODE                         = 'OTH' " \
          "LEFT Join LOT                       On          St.LotCode                                      = Lot.Code " \
          "LEFT JOIN ADSTORAGE SaleLot         ON          Lot.ABSUNIQUEID                                 = SaleLot.ABSUNIQUEID " \
          "                                    And         SaleLot.NameEntityName                          = 'Lot'  " \
          "                                    And         SaleLot.NameName                                = 'SaleLot'  " \
          "                                    And         SaleLot.FieldName                               = 'SaleLot'  " \
          "WHERE     SALESDOCUMENT.DocumentTypeType = '06'   "  + sqlwhere

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    if result != False:
        while result != False:
            GLine.append(result)
            # print(result)
            # print(result['CHALLANNUMBER'])
            result = con.db.fetch_both(stmt)
        return render(request, 'DispatchDetailRegisterList.html',
                      {'GSecondList': GSecondList, 'GLine': GLine})
    else:
        # return render(request, 'StoreRegister.html',
        #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
        #                'ccode': ccode})
        Exceptions = "Note: Please Select Valid Credentials"
        # return
        return render(request, 'DispatchDetailRegisterList.html', {'GSecondList': GSecondList, 'GLine': GLine,'Exceptions':Exceptions})
