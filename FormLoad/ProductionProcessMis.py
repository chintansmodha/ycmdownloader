import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
import os.path
from Global_Files import Connection_String as con

GDataItemSummary = []


def Production(request):
    return render(request, 'productionProcessmis.html')


# ******************** Process Wise **************************************************
def ProccessWisefunctions(request):
    GDataProcessSummary = []
    PoyFamily = "( 'POY', 'FDY', 'MOY', 'MON' )"
    BcfFamily = "( 'BCF', 'CAB', 'HST' )"
    DtyFamily = "( 'DTY', 'ATY', 'TWD', 'PLY' )"
    startdate = "'" + str(request.GET['startdate']) + "'"
    Date = (datetime.strptime(str(request.GET['startdate']), '%Y-%m-%d').date()).strftime('%d-%m-%Y')
    product = str(request.GET.getlist('Product'))[2:-27]
    print(product)
    if product != '':
        if int(product) == 1:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + PoyFamily

        elif int(product) == 2:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + BcfFamily

        elif int(product) == 3:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + DtyFamily
    else:
        Itemtype = " "
    day = Date[0:2]
    month = Date[3:5]
    year = Date[6:]
    month1stdate = startdate[:-3] + '01' + "'"
    fromdate = (datetime.strptime(str(startdate[1:-3] + '01'), '%Y-%m-%d').date()).strftime('%d-%m-%Y')
    lastday = int(Date[:2])

    # ******************* Process Wise Query ********************************************************
    sql = "Select          UGG_Process.LongDescription As ProcessName " \
          ", Int(Round(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty " \
          ", Int(Round(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
          ", Int(Round(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
          ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
          ", int(Round(SUM(BKLELEMENTS.ACTUALNETWT))) As UpToDate_Qty " \
          ", Int(Round(SUM(Case When QG.Code = 'A'  Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
          ", Int(Round(SUM(Case When QG.Code <> 'A' Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
          ", CAST((SUM(Case When QG.Code <> 'A' Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(BKLELEMENTS.ACTUALNETWT),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
          "From            BKLELEMENTS " \
          "Join            ELEMENTS                                On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Join            QualityLevel                            On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE  " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Join            Resources R                             On      (Left(BKLELEMENTS.LOTCODE,3) = R.CODE Or Left(BKLELEMENTS.LOTCODE,4) = R.CODE) " \
          "Join            AdStorage ADS_Process                   On      R.AbsUniqueId = ADS_Process.UniqueId " \
          "And     ADS_Process.NameEntityName = 'Resources' " \
          "And     ADS_Process.NameName = 'Process' " \
          "And     ADS_Process.FieldName = 'ProcessCode' " \
          "Join            UserGenericGroup As UGG_Process         On      UGG_Process.UserGenericGroupTypeCode = 'PRO' " \
          "And     UGG_Process.Code = ADS_Process.ValueString " \
          "And     UGG_Process.Code = BKLELEMENTS.LOTITEMTYPECODE " \
          "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
          "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
          "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code " \
          "Where           ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" " \
          "And     BKLELEMENTS.ACTUALNETWT  > 0   "+Itemtype+" " \
          "Group by        UGG_Process.LongDescription " \
          "Order By        ProcessName"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    #*******************total****************************************
    todaytotal = 0
    uptodatetotal = 0
    today1st = 0
    today2nd = 0
    upto1st = 0
    upto2nd = 0
    while result != False:
        result['average']= int(round(float(result['UPTODATE_QTY']/lastday)))
        GDataProcessSummary.append(result)
        todaytotal += float(result['TODAY_QTY'])
        uptodatetotal += float(result['UPTODATE_QTY'])
        today1st += float(result['TODAY_1STQTY'])
        today2nd += float(result['TODAY_PQQTY'])
        upto1st += float(result['UPTODATE_1STQTY'])
        upto2nd += float(result['UPTODATE_PQQTY'])
        result = con.db.fetch_both(stmt)

    if todaytotal != 0:
        today11per = float(today2nd * 100/todaytotal)
    else:
        today11per = float(todaytotal)

    if uptodatetotal != 0:
        upto11per = float(upto2nd * 100/uptodatetotal)
    else:
        upto11per = float(uptodatetotal)

    #     2nd Query For sites ********************************************
    GDataSites = []
    sql = "Select    UGG_Process.LongDescription As ProcessName " \
          ", PLANT.SHORTDESCRIPTION As Sites " \
          ", Int(Round(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty " \
          ", Int(Round(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
          ", Int(Round(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
          ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
          ", int(Round(SUM(BKLELEMENTS.ACTUALNETWT))) As UpToDate_Qty " \
          ", Int(Round(SUM(Case When QG.Code = 'A'  Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
          ", Int(Round(SUM(Case When QG.Code <> 'A' Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
          ", CAST((SUM(Case When QG.Code <> 'A' Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(BKLELEMENTS.ACTUALNETWT),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
          "From            BKLELEMENTS " \
          "Join            ELEMENTS                                On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Join            QualityLevel                            On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE  " \
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Join            PLANT                                   On      BKLELEMENTS.PLANTCODE = PLANT.CODE " \
          "Join            Resources R                             On      (Left(BKLELEMENTS.LOTCODE,3) = R.CODE Or Left(BKLELEMENTS.LOTCODE,4) = R.CODE) " \
          "Join            AdStorage ADS_Process                   On      R.AbsUniqueId = ADS_Process.UniqueId " \
          "And     ADS_Process.NameEntityName = 'Resources' " \
          "And     ADS_Process.NameName = 'Process' " \
          "And     ADS_Process.FieldName = 'ProcessCode' " \
          "Join            UserGenericGroup As UGG_Process         On      UGG_Process.UserGenericGroupTypeCode = 'PRO' " \
          "And     UGG_Process.Code = ADS_Process.ValueString " \
          "And     UGG_Process.Code = BKLELEMENTS.LOTITEMTYPECODE " \
          "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
          "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
          "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code " \
          "Where           ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" " \
          "And     BKLELEMENTS.ACTUALNETWT  > 0   "+Itemtype+" " \
          "Group by          UGG_Process.LongDescription " \
          ", PLANT.SHORTDESCRIPTION " \
          "Order By        ProcessName, Sites"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # total sites
    todaytotalsites = 0
    uptoTotalsite = 0
    todaysite1st = 0
    todaytotal2nd = 0
    uptosite1st = 0
    uptosite2nd = 0

    while result != False:
        result['average'] = int(round(float(result['UPTODATE_QTY']/lastday)))
        GDataSites.append(result)
        todaytotalsites += float(result['TODAY_QTY'])
        uptoTotalsite += float(result['UPTODATE_QTY'])
        todaysite1st += float(result['TODAY_1STQTY'])
        todaytotal2nd += float(result['TODAY_PQQTY'])
        uptosite1st += float(result['UPTODATE_1STQTY'])
        uptosite2nd += float(result['UPTODATE_PQQTY'])
        result = con.db.fetch_both(stmt)

    if todaytotalsites != 0:
        todaysite11per = float(today2nd * 100 / todaytotalsites)
    else:
        todaysite11per = float(todaytotalsites)

    if uptoTotalsite != 0:
        uptosite11per = float(upto2nd * 100 / uptoTotalsite)
    else:
        uptosite11per = float(uptoTotalsite)

    #*************** Query Print Machine Data ****************************************
    GDataMachine = []
    sql= "Select          UGG_Process.LongDescription As ProcessName " \
         ", PLANT.SHORTDESCRIPTION As Sites " \
         ", R.Code As Machine" \
         ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
         ", Int(Round(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty " \
         ", Int(Round(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
         ", Int(Round(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
         ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
         "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
         ", int(Round(SUM(BKLELEMENTS.ACTUALNETWT))) As UpToDate_Qty " \
         ", Int(Round(SUM(Case When QG.Code = 'A'  Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
         ", Int(Round(SUM(Case When QG.Code <> 'A' Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
         ", CAST((SUM(Case When QG.Code <> 'A' Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
         "NULLIF(SUM(BKLELEMENTS.ACTUALNETWT),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
         "From            BKLELEMENTS " \
         "Join            ELEMENTS                                On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
         "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
         "Join            QualityLevel                            On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE  " \
         "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
         "Join            PLANT                                   On      BKLELEMENTS.PLANTCODE = PLANT.CODE " \
         "left Join LOGICALWAREHOUSE              On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
         "Left Join COSTCENTER                    On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
         "Join            Resources R                             On      (Left(BKLELEMENTS.LOTCODE,3) = R.CODE Or Left(BKLELEMENTS.LOTCODE,4) = R.CODE) " \
         "Join            AdStorage ADS_Process                   On      R.AbsUniqueId = ADS_Process.UniqueId " \
         "And     ADS_Process.NameEntityName = 'Resources' " \
         "And     ADS_Process.NameName = 'Process' " \
         "And     ADS_Process.FieldName = 'ProcessCode' " \
         "Join            UserGenericGroup As UGG_Process         On      UGG_Process.UserGenericGroupTypeCode = 'PRO' " \
         "And     UGG_Process.Code = ADS_Process.ValueString " \
         "And     UGG_Process.Code = BKLELEMENTS.LOTITEMTYPECODE " \
         "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
         "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
         "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code " \
         "Where           ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" " \
         "And     BKLELEMENTS.ACTUALNETWT  > 0   "+Itemtype+" " \
         "Group by        UGG_Process.LongDescription " \
         ", PLANT.SHORTDESCRIPTION " \
         ", R.Code " \
         ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
         "Order By        ProcessName, Sites, Machine"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # total machine
    todaytotalmachine = 0
    uptoTotalmachine = 0
    todaymachine1st = 0
    todaytotalmach2nd = 0
    uptomachine1st = 0
    uptomachine2nd = 0

    while result != False:
        result['average'] = int(round(float(result['UPTODATE_QTY'] / lastday)))
        GDataMachine.append(result)
        todaytotalmachine += float(result['TODAY_QTY'])
        uptoTotalmachine += float(result['UPTODATE_QTY'])
        todaymachine1st += float(result['TODAY_1STQTY'])
        todaytotalmach2nd += float(result['TODAY_PQQTY'])
        uptomachine1st += float(result['UPTODATE_1STQTY'])
        uptomachine2nd += float(result['UPTODATE_PQQTY'])
        result = con.db.fetch_both(stmt)

    if todaytotalmachine != 0:
        todaymachine11per = float(todaytotalmach2nd * 100 / todaytotalmachine)
    else:
        todaymachine11per = float(todaytotalmachine)

    if uptoTotalmachine != 0:
        uptomachine11per = float(uptomachine2nd * 100 / uptoTotalmachine)
    else:
        uptomachine11per = float(uptoTotalmachine)


    return render(request, 'ProductionProccesswise.html',{'Date': Date, 'day': day, 'month': month, 'year': year, 'fromdate': fromdate,
                                                          'product': product, 'GDataProcessSummary': GDataProcessSummary,
                                                          'todaytotal': int(todaytotal),
                                                          'today11per': str('{0:1.2f}'.format(today11per)),
                                                          'uptodatetotal': int(uptodatetotal),
                                                          'upto11per': str('{0:1.2f}'.format(upto11per)),
                                                          'totalAvg': int(round(float(uptodatetotal/lastday))),
                                                          'today1st': int(today1st),
                                                          'today2nd': int(today2nd),
                                                          'upto1st': int(upto1st),
                                                          'upto2nd': int(upto2nd),

                                                          'GDataSites': GDataSites,
                                                          'todaytotalsites': int(todaytotalsites),
                                                          'todaysite11per': str('{0:1.2f}'.format(todaysite11per)),
                                                          'uptoTotalsite': int(uptoTotalsite),
                                                          'uptosite11per': str('{0:1.2f}'.format(uptosite11per)),
                                                          'totalsiteAvg': int(round(float(uptoTotalsite / lastday))),
                                                          'todaysite1st': int(todaysite1st),
                                                          'todaytotal2nd': int(todaytotal2nd),
                                                          'uptosite1st': int(uptosite1st),
                                                          'uptosite2nd': int(uptosite2nd),

                                                          'GDataMachine': GDataMachine,
                                                          'todaytotalmachine': int(todaytotalmachine),
                                                          'todaymachine11per': str('{0:1.2f}'.format(todaymachine11per)),
                                                          'uptoTotalmachine': int(uptoTotalmachine),
                                                          'uptomachine11per': str('{0:1.2f}'.format(uptomachine11per)),
                                                          'totalmachineAvg': int(round(float(uptoTotalmachine / lastday))),
                                                          'todaymachine1st': int(todaymachine1st),
                                                          'todaytotalmach2nd': int(todaytotalmach2nd),
                                                          'uptomachine1st': int(uptomachine1st),
                                                          'uptomachine2nd': int(uptomachine2nd)
                                                          })

# *****************************************         ************************************************************************
# ************************************* ITEM WISE *************************************************************************

def ItemWisefunction(request):
    global GDataItemSummary
    GDataItemSummary = []
    PoyFamily = "( 'POY', 'FDY', 'MOY', 'MON' )"
    BcfFamily = "( 'BCF', 'CAB', 'HST' )"
    DtyFamily = "( 'DTY', 'ATY', 'TWD', 'PLY' )"
    startdate = "'" + str(request.GET['startdate']) + "'"
    Date = (datetime.strptime(str(request.GET['startdate']), '%Y-%m-%d').date()).strftime('%d-%m-%Y')
    product = str(request.GET.getlist('Product'))[2:-27]
    print(product)
    if product != '':
        if int(product) == 1:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + PoyFamily

        elif int(product) == 2:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + BcfFamily

        elif int(product) == 3:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + DtyFamily
    else:
        Itemtype = " "
    day = Date[0:2]
    month = Date[3:5]
    year = Date[6:]
    # print(Date, day, month, year)
    # print(Date[:1])
    month1stdate = startdate[:-3] + '01' + "'"
    # print(month1stdate)
    fromdate = (datetime.strptime(str(startdate[1:-3] + '01'), '%Y-%m-%d').date()).strftime('%d-%m-%Y')
    lastday = int(Date[:2])
    # print(lastday)
    # print(fromdate)
    # print(startdate)

    sql = "Select          PRODUCT.LONGDESCRIPTION As Item " \
          ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty " \
          ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
          ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
          ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
          ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_Qty " \
          ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
          ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
          ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
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
          "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
          "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
          "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where   ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+"  And     BKLELEMENTS.ACTUALNETWT  > 0  "+Itemtype+" " \
          "Group by PRODUCT.LONGDESCRIPTION " \
          "Order By Item"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    # Total
    toalTodayPro = 0
    totalUpToDtPro = 0
    totaTodayQuality1 = 0
    totaTodayQuality2 = 0
    totaUptoQuality1 = 0
    totaUptoQuality2 = 0
    # ******

    cur_item = ''
    pre_item = ''
    Quality1 = 0
    Quality2 = 0
    upToQuality1 = 0
    upToQuality2 = 0
    toProduction = 0
    UptoPro = 0
    # totalUpToDtPro = 0
    dict = {}
    # print('rohit')
    while result != False:
        result['average'] = round((float(result['UPTODATE_QTY'])/lastday))
        # print(result)
        GDataItemSummary.append(result)
        toalTodayPro = toalTodayPro + float(result['TODAY_QTY'])
        totalUpToDtPro = totalUpToDtPro + float(result['UPTODATE_QTY'])
        totaTodayQuality1 = totaTodayQuality1 + float(result['TODAY_1STQTY'])
        totaTodayQuality2 = totaTodayQuality2 + float(result['TODAY_PQQTY'])
        totaUptoQuality1 = totaUptoQuality1 + float(result['UPTODATE_1STQTY'])
        totaUptoQuality2 = totaUptoQuality2 + float(result['UPTODATE_PQQTY'])

        result = con.db.fetch_both(stmt)
    if toalTodayPro != 0:
        totaltoday_11per = (totaTodayQuality2 * 100)/toalTodayPro
    else:
        totaltoday_11per = toalTodayPro

    if totalUpToDtPro != 0:
        totalUpToDtPro_11per = (totaUptoQuality2 * 100)/totalUpToDtPro
    else:
        totalUpToDtPro_11per = totalUpToDtPro


    #  ************************************   Second Query For Machine Show **************************************************
    GDataMachine = []
    sql ="Select          PRODUCT.LONGDESCRIPTION As Item " \
         ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) As Machine " \
         ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
         ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty         " \
         ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
         ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
         ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
         "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
         ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_Qty " \
         ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
         ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
         ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
         "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
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
         "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
         "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
         "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code " \
         "left Join LOGICALWAREHOUSE              On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
         "Left Join COSTCENTER                    On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
         "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
         "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
         "Where   ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+"  And     BKLELEMENTS.ACTUALNETWT  > 0 "+Itemtype+" " \
         "Group by  PRODUCT.LONGDESCRIPTION ,Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) " \
         ", COSTCENTER.LONGDESCRIPTION " \
         "Order By Item, Machine"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    toalTodayPromach = 0
    totalUpToDtPromach = 0
    totaTodayQualitymach1 = 0
    totaTodayQualitymach2 = 0
    totaUptoQualitymach1 = 0
    totaUptoQualitymach2 = 0

    while result != False:
        result['mashaverage'] = round((float(result['UPTODATE_QTY'])/lastday))
        GDataMachine.append(result)
        toalTodayPromach = toalTodayPromach + float(result['TODAY_QTY'])
        totalUpToDtPromach = totalUpToDtPromach + float(result['UPTODATE_QTY'])
        totaTodayQualitymach1 = totaTodayQualitymach1 + float(result['TODAY_1STQTY'])
        totaTodayQualitymach2 = totaTodayQualitymach2 + float(result['TODAY_PQQTY'])
        totaUptoQualitymach1 = totaUptoQualitymach1 + float(result['UPTODATE_1STQTY'])
        totaUptoQualitymach2 = totaUptoQualitymach2 + float(result['UPTODATE_PQQTY'])

        result = con.db.fetch_both(stmt)

    if toalTodayPromach != 0:
        totaltoday_11per_mach = (totaTodayQualitymach2 * 100)/toalTodayPromach
    else:
        totaltoday_11per_mach = toalTodayPromach

    if totalUpToDtPromach != 0:
        totalUpToDtPro_11per_mach = (totaUptoQualitymach2 * 100)/totalUpToDtPro
    else:
        totalUpToDtPro_11per_mach = totalUpToDtPromach


    return render(request, 'productionProcessItemMis.html', { 'GDataItemSummary': GDataItemSummary, 'Date': Date,
                                                        'day': day, 'month': month, 'year': year, 'product': product,
                                                        'fromdate': fromdate,'toalTodayPro': round(float(toalTodayPro))  ,
                                                        'totaltoday_11per': str('{0:1.2f}'.format(float(totaltoday_11per))),
                                                        'totalUpToDtPro': round(float(totalUpToDtPro)) ,
                                                        'totalUpToDtPro_11per': str('{0:1.2f}'.format(float(totalUpToDtPro_11per))),
                                                        'totalAverage': round((totalUpToDtPro/lastday)),
                                                        'totaTodayQuality1': round(float(totaTodayQuality1)) ,
                                                        'totaTodayQuality2': round(float(totaTodayQuality2)) ,
                                                        'totaUptoQuality1': round(float(totaUptoQuality1)) ,
                                                        'totaUptoQuality2': round(float(totaUptoQuality2)),

                                                        'GDataMachine':GDataMachine,'toalTodayPromach': round(float(toalTodayPromach))  ,
                                                        'totaltoday_11per_mach': str('{0:1.2f}'.format(float(totaltoday_11per_mach))),
                                                        'totalUpToDtPromach': round(float(totalUpToDtPromach)) ,
                                                        'totalUpToDtPro_11per_mach': str('{0:1.2f}'.format(float(totalUpToDtPro_11per_mach))),
                                                        'totalAverage_mach': round((totalUpToDtPro_11per_mach/lastday)),
                                                        'totaTodayQualitymach1': round(float(totaTodayQualitymach1)) ,
                                                        'totaTodayQualitymach2': round(float(totaTodayQualitymach2)) ,
                                                        'totaUptoQualitymach1': round(float(totaUptoQualitymach1)) ,
                                                        'totaUptoQualitymach2': round(float(totaUptoQualitymach2))})

# ***********************************************       *************************************************


# *************************************** MACHINE WISE *****************************************************************

def MachineWisefunction(request):
    GDataItemSummary = []
    GDatamachinwise = []
    PoyFamily = "( 'POY', 'FDY', 'MOY', 'MON' )"
    BcfFamily = "( 'BCF', 'CAB', 'HST' )"
    DtyFamily = "( 'DTY', 'ATY', 'TWD', 'PLY' )"
    product = str(request.GET.getlist('Product'))[2:-27]
    if product != '':
        if int(product) == 1:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + PoyFamily

        elif int(product) == 2:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + BcfFamily

        elif int(product) == 3:
            Itemtype = " And BKLELEMENTS.LOTITEMTYPECODE In " + DtyFamily
    else:
        Itemtype = " "
    startdate = "'" + str(request.GET['startdate']) + "'"
    Date = (datetime.strptime(str(request.GET['startdate']), '%Y-%m-%d').date()).strftime('%d-%m-%Y')
    day = Date[:2]
    month = Date[3:5]
    year = Date[6:]
    # print(Date, day, month, year)
    month1stdate = startdate[:-3] + '01' + "'"
    fromdate = (datetime.strptime(str(startdate[1:-3] + '01'), '%Y-%m-%d').date()).strftime('%d-%m-%Y')
    lastday = int(Date[:2])

    sql ="Select          Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) As Machine " \
         ", COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
         ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty         " \
         ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
         ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
         ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
         "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
         ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_Qty " \
         ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
         ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
         ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
         "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
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
         "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
         "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
         "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code " \
         "left Join LOGICALWAREHOUSE              On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
         "Left Join COSTCENTER                    On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
         "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
         "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
         "Where   ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+"  And     BKLELEMENTS.ACTUALNETWT  > 0 "+Itemtype+" " \
         "Group by  Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) " \
         ", COSTCENTER.LONGDESCRIPTION " \
         "Order By  Machine"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    # total machine
    toalTodaymach = 0
    totalUpToDtmach = 0
    totaltodaymachQ1 = 0
    totaltodaymachQ2 = 0
    totalupdtmachQ1 = 0
    totalupdtmachQ2 = 0
    toalTodaymach11 = 0
    # ************

    cur_mach = ''
    pre_mach = ''
    today = 0
    uptoday = 0
    todayQ1 = 0
    todayQ2 = 0
    uptodayQ1 = 0
    uptodayQ2 = 0
    totalUpToDtmach11 = 0
    dept = ''
    dicts = {}
    while result != False:
        result['average'] = round((float(result['UPTODATE_QTY'])/lastday))
        GDatamachinwise.append(result)
        toalTodaymach = toalTodaymach + float(result['TODAY_QTY'])
        totalUpToDtmach = totalUpToDtmach + float(result['UPTODATE_QTY'])
        totaltodaymachQ1 = totaltodaymachQ1 + float(result['TODAY_1STQTY'])
        totaltodaymachQ2 = totaltodaymachQ2 + float(result['TODAY_PQQTY'])
        totalupdtmachQ1 = totalupdtmachQ1 + float(result['UPTODATE_1STQTY'])
        totalupdtmachQ2 = totalupdtmachQ2 + float(result['UPTODATE_PQQTY'])
        result = con.db.fetch_both(stmt)
    if toalTodaymach != 0:
        totalToday11per = round(float(totaltodaymachQ2 * 100/toalTodaymach),2)
    else:
        totalToday11per = toalTodaymach
    if totalUpToDtmach != 0:
        totalUpto11per = round(float(totalupdtmachQ2 * 100/totalUpToDtmach),2)
    else:
        totalUpto11per = totalUpToDtmach

    #     ****************************   Second Query  ***********************************
    sql = "Select          PRODUCT.LONGDESCRIPTION As Item " \
          ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) As Machine " \
          ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_Qty " \
          ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_1stQty " \
          ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As ToDay_PQQty " \
          ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
          ", INT(ROUND(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_Qty " \
          ", INT(ROUND(SUM(Case When QG.Code = 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_1stQty " \
          ", INT(ROUND(SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End))) As UpToDate_PQQty " \
          ", CAST(COALESCE(((SUM(Case When QG.Code <> 'A' And ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As upToDate_IIndPerc " \
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
          "Join    AvQualityGroupdetail As QGD                     On      QGD.QualityITEMTYPECODE = BKLELEMENTS.LOTITEMTYPECODE " \
          "And     QGD.QUALITYCODE = BKLELEMENTS.QUALITYLEVELCODE " \
          "Join    AvQualityGroup  As QG                           On      QGD.AVQUALITYGROUPCODE = QG.Code  " \
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where   ELEMENTS.ENTRYDATE Between "+month1stdate+" and "+startdate+"  And     BKLELEMENTS.ACTUALNETWT  > 0  "+Itemtype+" " \
          "Group by PRODUCT.LONGDESCRIPTION " \
          ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) " \
          "Order By  Machine, Item"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    # Total
    toalTodayPro = 0
    totalUpToDtPro = 0
    totaTodayQuality1 = 0
    totaTodayQuality2 = 0
    totaUptoQuality1 = 0
    totaUptoQuality2 = 0
    # ******

    cur_item = ''
    pre_item = ''
    Quality1 = 0
    Quality2 = 0
    upToQuality1 = 0
    upToQuality2 = 0
    toProduction = 0
    UptoPro = 0
    # totalUpToDtPro = 0
    dict = {}
    # print('rohit')
    while result != False:
        result['average'] = round((float(result['UPTODATE_QTY'])/lastday))
        # print(result)
        GDataItemSummary.append(result)
        toalTodayPro = toalTodayPro + float(result['TODAY_QTY'])
        totalUpToDtPro = totalUpToDtPro + float(result['UPTODATE_QTY'])
        totaTodayQuality1 = totaTodayQuality1 + float(result['TODAY_1STQTY'])
        totaTodayQuality2 = totaTodayQuality2 + float(result['TODAY_PQQTY'])
        totaUptoQuality1 = totaUptoQuality1 + float(result['UPTODATE_1STQTY'])
        totaUptoQuality2 = totaUptoQuality2 + float(result['UPTODATE_PQQTY'])

        result = con.db.fetch_both(stmt)
    if toalTodayPro != 0:
        totaltoday_11per = (totaTodayQuality2 * 100)/toalTodayPro
    else:
        totaltoday_11per = toalTodayPro

    if totalUpToDtPro != 0:
        totalUpToDtPro_11per = (totaUptoQuality2 * 100)/totalUpToDtPro
    else:
        totalUpToDtPro_11per = totalUpToDtPro



    return render(request, 'productionProcess_machineMis.html',
                  {'Date': Date, 'day': day, 'month': month, 'year': year, 'fromdate': fromdate,
                   'GDatamachinwise': GDatamachinwise, 'product': product,
                   'toalTodaymach': round(float(toalTodaymach)),
                   'totalToday11per': str('{0:1.2f}'.format(float(totalToday11per))),
                   'totalUpToDtmach': round(float(totalUpToDtmach)),
                   'totalUpto11per': str('{0:1.2f}'.format(float(totalUpto11per))),
                   'totalAveragemach': round((totalUpToDtmach/lastday)),
                   'totaltodaymachQ1': round(float(totaltodaymachQ1)),
                   'totaltodaymachQ2': round(float(totaltodaymachQ2)),
                   'totalupdtmachQ1': round(float(totalupdtmachQ1)),
                   'totalupdtmachQ2': round(float(totalupdtmachQ2)),

                   'GDataItemSummary': GDataItemSummary,
                   'toalTodayPro': str('{0:1.2f}'.format(float(toalTodayPro))),
                   'totaltoday_11per': str('{0:1.2f}'.format(float(totaltoday_11per))),
                   'totalUpToDtPro': str('{0:1.2f}'.format(float(totalUpToDtPro))),
                   'totalUpToDtPro_11per': str('{0:1.2f}'.format(float(totalUpToDtPro_11per))),
                   'totalAverage': str('{0:1.2f}'.format(round((totalUpToDtPro / lastday), 2))),
                   'totaTodayQuality1': str('{0:1.2f}'.format(float(totaTodayQuality1))),
                   'totaTodayQuality2': str('{0:1.2f}'.format(float(totaTodayQuality2))),
                   'totaUptoQuality1': str('{0:1.2f}'.format(float(totaUptoQuality1))),
                   'totaUptoQuality2': str('{0:1.2f}'.format(float(totaUptoQuality2)))

                   })

# ******************************        ********************************************************************************