from django.shortcuts import render
from datetime import datetime, date
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
from babel.numbers import format_currency
from django.shortcuts import render
from Global_Files import Connection_String as con
GDataBrokerWiseOS=[]
GDataCompany=[]
GDataTotal=[]
GDataTotalCompany=[]
total=0
upto15=0
range16=0
over30=0
dnamt=0
advance=0
unbilled=0
unadj=0
olddays=0
GNetTotal=0
GCollection=0
GReturn=0

TOTAL=0

# Create your views here.
def AgentWiseCollectionMIS(request):
    print("from process selection")
    b=0
    t=0
    u=0
    r=0
    o=0
    d=0
    un=0
    od=0

    global total
    global upto15
    global range16
    global over30
    global dnamt
    global advance
    global unbilled
    global unadj
    global olddays
    global TOTAL
    global i

    total = 0
    upto15 = 0
    range16 = 0
    over30 = 0
    dnamt = 0
    advance = 0
    unbilled = 0
    unadj = 0
    olddays = 0
    TOTAL=0

    global GDataBrokerWiseOS
    global GDataCompany
    global GDataTotal
    global GNetTotal
    global GCollection
    global GReturn

    GDataBrokerWiseOS=[]
    GDataCompany=[]
    GDataTotal=[]
    sqlwhere=""
    try:
        if request.GET['startdate']:
            LDStartDate = str(request.GET['startdate'])
            LDEndDate = str(request.GET['enddate'])
            # sqlwhere = " AND SD.PROVISIONALDOCUMENTDATE = '" + LDStartDate + "' "
            sqlwhere = "   AND ADS_Cheque_Date.ValueDate between '"+LDStartDate+"' and '"+LDEndDate+"' "
            print(sqlwhere)
        else:
            sqlwhere=""
        print("from try")
    except:
        print("from exception problem in getting the date")
        today = date.today()
        LDStartDate=today.strftime("%Y-%m-%d")
        LDEndDate=today.strftime("%Y-%m-%d")
        sqlwhere = "   AND ADS_Cheque_Date.ValueDate between '" + LDStartDate + "' and '" + LDEndDate + "' "


    sql = " SELECT  Company.LONGDESCRIPTION                                 AS COMPANYNAME " \
          "		, agent.Longdescription                                         AS BROKERGRP  " \
          "     , Sum(CAST(FINDOC.DOCUMENTAMOUNT AS DECIMAL(20,2)))             AS AMOUNT  " \
          " FROM FINDOCUMENT FINDOC  " \
          "           LEFT JOIN AGENT                 ON      FINDOC.AGENT1CODE               = AGENT.CODE  " \
          "           Join AgentsGroupDetail AGD      On      FINDOC.Agent1Code               = AGD.AgentCode  " \
          "           Join AgentsGroup AgGrp          On      AGD.AgentsGroupCode             = AgGrp.Code  " \
          "           JOIN FinBusinessUnit BUnit      ON      FINDOC.BusinessUnitCODE         = Bunit.CODE And BUnit.GroupFlag = 0  " \
          "           JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode               = Company.Code And Company.GroupFlag = 1 " \
          "           JoiN GLMaster As BankMaster     On      FINDOC.GLCODE                   = BankMaster.Code   " \
          "           JOIN AdStorage ADS_SlipNo       ON      FINDOC.AbsUniqueId              = ADS_SlipNo.UniqueId  " \
          "                                           AND     ADS_SlipNo.NameEntityNAme       ='FINDocument' And ADS_SlipNo.FieldName = 'IssuesSlipNO'  " \
          "           JOIN AdStorage ADS_IssSlipStatus    ON  FINDOC.AbsUniqueId              = ADS_IssSlipStatus.UniqueId  " \
          "                                           AND     ADS_IssSlipStatus.NameEntityNAme  ='FINDocument'  " \
          "                                           And     ADS_IssSlipStatus.FieldName     = 'IssueSlipStatus'  " \
          "                                           AND     ADS_IssSlipStatus.ValueString   = '2'  " \
          "           JOIN ADStorage ADS_Cheque_Date  ON      ADS_Cheque_Date.UniqueID        = FINDOC.AbsUniqueId  " \
          "                                           AND     ADS_Cheque_Date.NameEntityNAme  = 'FINDocument'   " \
          "                                           And     ADS_Cheque_Date.FieldName       = 'ChequeDate'   " \
          "           JOIN ADStorage ADS_Cheque_No    ON      ADS_Cheque_No.UniqueID          = FinDoc.AbsUniqueId " \
          "                                           AND     ADS_Cheque_No.NameEntityNAme    = 'FINDocument'   " \
          "                                           And     ADS_Cheque_No.FieldName         = 'CustomerCheque'  " \
          " WHERE FINDOC.DOCUMENTTYPECODE IN('BR','CR')  " \
          "   AND FINDOC.CURRENTSTATUS = 1  " \
          "   AND FINDOC.DOCUMENTTEMPLATECODE In ('B12','B18') "
    sql+=sqlwhere+  " Group By Company.LONGDESCRIPTION  " \
          "     , AGENT.Longdescription   " \
          " Order by agent.Longdescription "

    print(sql)
    total=0
    t=0
    resultset=[]
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        total=float("%.2f" % float(result['AMOUNT']))
        GCollection = GCollection + float(result['AMOUNT'])
        GDataBrokerWiseOS.append(result)
        result = con.db.fetch_both(stmt)

        # GDataCompany.append(i['BROKERGRP'])
    for i in GDataBrokerWiseOS:
        if i['BROKERGRP'] not in GDataCompany:
            GDataCompany.append(i['BROKERGRP'])
    # GDataCompany.append(i['BROKERGRP'])

    for j in GDataCompany:
        for k in GDataBrokerWiseOS:
            if j == k['BROKERGRP']:
                b=k['BROKERGRP']
                t = t+float(k['AMOUNT'])
                # u = u+float(k['UPTO15'])
                # r = r+float(k['RANGE16'])
                # o = o+float(k['OVER30'])
                # d = d+float(k['DNAMT'])
                # un = un+float(k['UNBILLEDAMT'])
                # od = od + float(k['ABOVEODDAYS'])
            else:
                if b!=0:
                    resultset = {
                        'BROKER':b,
                        'TOTAL':  str('₹ '+format_currency("%.2f" % float(t), '', locale='en_IN')),
                    }
                    print(GDataBrokerWiseOS)
                    GDataTotal.append(resultset)
                    b = 0
                    t = 0
                    u = 0
                    r = 0
                    o = 0
                    d = 0
                    un = 0
                    od = 0
    # i=i+1
    # GDataCompany.append(i['BROKERGRP'])
    # GDataTotal.append(resultset)

    # print(GDataBrokerWiseOS)
    # print(GDataTotal)
    # print(GDataCompany)

    print(GCollection)


    return render(request, 'AgentWiseCollection_MIS.html', {'GDataBrokerWiseOS': GDataBrokerWiseOS,'GDataCompany':GDataCompany,'GDataTotal':GDataTotal,'s':0,
                                                       'total': str(
                                                           format_currency((float("%.2f" % float(total))),
                                                                           'INR', locale='en_IN')).replace('₹', ''),
                                                 'TOTAL': str(
                                                     format_currency((float("%.2f" % float(TOTAL))),
                                                                     'INR', locale='en_IN')).replace('₹', '')
                                                       # 'startdate': stdt.strftime("%d %B %Y"),
                                                       # 'enddate': etdt.strftime("%d %B %Y")}
                                                            ,'GCollection':str('₹ '+format_currency("%.2f" % float(GCollection), '', locale='en_IN'))
                                                 })




# import os
# from datetime import datetime
#
# from babel.numbers import format_currency
# from django.shortcuts import render
# from django.utils.datastructures import MultiValueDictKeyError
# from django.views.static import serve
#
# from Global_Files import Connection_String as con
# from FormLoad import StoreRegister_FormLoad as views
# from CreateXLS import Dispatch_Detail_Export_To_XLS as xlsrpt
#
# Exceptions = ""
#
# counter = 0
# GBasecode = ""  # This code is use to save the uniqueid value from the maintable of the first page
# GList = []
# GSecondList = []
# GLine = []
#
# GChallanno = []
# GChallanDate = []
# GQuantity = []
# save_name = ''
# Greportname=""
# Gheader=""
# startdate = ""
# enddate = ""
# reporttype = ""
#
#
# def DispatchDetails(request):
#     global save_name
#
#     LDStartDate = str(request.GET['startdate'])
#     LDEndDate = str(request.GET['enddate'])
#     LSRegisterType = str(request.GET['CboRegisterType'])
#     LSReportType = ''
#     global GChallanno
#     global GChallanDate
#     global GQuantity
#     global startdate
#     global enddate
#     global reporttype
#     global Greportname
#     global Gheader
#
#     startdate = LDStartDate
#     enddate = LDEndDate
#     reporttype = LSRegisterType
#     sqlwhere = ""
#     sqlwhere = " AND SD.PROVISIONALDOCUMENTDATE between '" + LDStartDate + "' and '" + LDEndDate + "'"
#     print(LSRegisterType)
#     if LSRegisterType == '0':
#         sql = " SELECT  Product.ABSUNIQUEID as uniqueid, " \
#               "        trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS LONGDESCRIPTION " \
#               "        , SDL.USERPRIMARYUOMCODE " \
#               "        , sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY    " \
#               "FROM SALESDOCUMENT SD " \
#               "JOIN SALESDOCUMENTLINE SDL      ON SD.PROVISIONALCODE   = SDL.SALESDOCUMENTPROVISIONALCODE " \
#               "JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
#               "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
#               " Join Product                On      SDL.ITEMTYPEAFICODE           	 = Product.ITEMTYPECODE    " \
#               "                            And     FIKD.ItemUniqueId                   = Product.AbsUniqueId " \
#               " JOIN QUALITYLEVEL               ON      SDL.QUALITYCODE                = QUALITYLEVEL.CODE " \
#               "                                AND     SDL.ITEMTYPEAFICODE             = QUALITYLEVEL.ITEMTYPECODE " \
#               " WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
#              " group by         Product.LONGDESCRIPTION         , QualityLevel.ShortDescription        , SDL.USERPRIMARYUOMCODE         , Product.ABSUNIQUEID "
#
#         Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, Greportname, Gheader)
#         Greportname = "Item Wise"
#         Gheader = "Item"
#         # return itemlist1
#         # return  render(request,'DispatchDetailRegister.html',{'GList':GList,"LSRegisterType":LSRegisterType})
#     elif LSRegisterType == '1':
#         sql = "SELECT agent.code as uniqueid, " \
#               "        Agent.LongDescription As LONGDESCRIPTION " \
#               "        ,  sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
#               "FROM SALESDOCUMENT SD " \
#               "        JOIN Agent                      ON      SD.Agent1Code                                     = Agent.Code   " \
#               "        JOIN SALESDOCUMENTLINE SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE          = SD.PROVISIONALCODE " \
#               "                                        AND     SDL.SALDOCPROVISIONALCOUNTERCODE          = SD.PROVISIONALCOUNTERCODE " \
#               "        JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE  " \
#               "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')  " \
#               "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')  " \
#               "        Join Product                On      SDL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE  " \
#               "                                    And     FIKD.ItemUniqueId                           = Product.AbsUniqueId  " \
#               "WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
#                                                                "GROUP BY " \
#                                                                "        Agent.LongDescription,agent.code"
#         Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, Greportname, Gheader)
#         Greportname = "Agent Wise"
#         Gheader = "Agent"
#         # return itemlist2
#         # return  render(request,'DispatchDetailRegister.html',{'GList':GList,"LSRegisterType":LSRegisterType})
#     elif LSRegisterType == '2':
#         sql = "SELECT " \
#               "		 UGG.ABSUNIQUEID as UNIQUEID , " \
#               "      TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As LONGDESCRIPTION , " \
#               "      sum(COALESCE(CAST(SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
#               "FROM SALESDOCUMENT SD " \
#               "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SD.PROVISIONALCODE " \
#               "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode " \
#               "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
#               "JOIN UserGenericGroup UGG      ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode   " \
#               "                                AND     Case IST.Position    " \
#               "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03    " \
#               "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06    " \
#               "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09    " \
#               "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
#               "JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
#               "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
#               "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
#               "WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
#                                                                "GROUP BY UGG.LONGDESCRIPTION ,UGG.ABSUNIQUEID , UGG.CODE  "
#         Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, Greportname, Gheader)
#         Greportname = "Shade Wise"
#         Gheader = "Shade"
#         # return itemlist3
#         # return  render(request,'DispatchDetailRegister.html',{'GList':GList,"LSRegisterType":LSRegisterType})
#
#     return render(request, 'DispatchDetailRegister.html',
#                   {'GList': GList, "LSRegisterType": LSRegisterType, "reportname": Greportname, "header": Gheader,
#                    "LDStartDate": LDStartDate, "LDEndDate": LDEndDate})
#
#
# def Itemlist(LDStartDate, LDEndDate, request, sql, LSRegisterType, reportname, header):
#     StartDate = "'" + LDStartDate + "'"
#     EndDate = "'" + LDEndDate + "'"
#     counter = 0
#     result = ""
#     global Greportname
#     global Gheader
#     global Exceptions
#     GList.clear()
#     GLine.clear()
#     GSecondList.clear()
#     print("sql for item list")
#     print(sql)
#     stmt = con.db.prepare(con.conn, sql)
#     con.db.execute(stmt)
#     result = con.db.fetch_both(stmt)
#     # print(result)
#     if result != False:
#         while result != False:
#             GList.append(result)
#             # print(result['CHALLANNUMBER'])
#             result = con.db.fetch_both(stmt)
#     else:
#         print("from else" )
#         # return render(request, 'StoreRegister.html',
#         #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
#         #                'ccode': ccode})
#         Exceptions = "No data found according to entered date"
#         print(Exceptions)
#         return render(request, 'DispatchDetailRegister.html',
#                       {'GList': GList, "LSRegisterType": LSRegisterType, "reportname": Greportname, "header": Gheader,
#                        "LDStartDate": LDStartDate, "LDEndDate": LDEndDate, "Exceptions": Exceptions})
#
#
# def DespatchDetailItemList(request):
#
#     LSItemcode = str(request.GET['uniqueid'])
#     LSRegisterType = str(request.GET['regeistertype'])
#     LDStartDate = str(request.GET['startdate'])
#     LDEndDate = str(request.GET['enddate'])
#     LSItemname =str(request.GET['itemname'])
#     print("itemname : "+LSItemname)
#     result = ""
#
#     header = ""
#     GSecondList.clear()
#     GLine.clear()
#     global startdate
#     global enddate
#     global reporttype
#     global GBasecode
#     global Greportname
#     global Gheader
#     startdate = LDStartDate
#     enddate = LDEndDate
#     reporttype = LSRegisterType
#     GBasecode = LSItemcode
#     print("*--*-*-*-*-*-*-*-*-**-*  from list " + LSItemcode)
#     print("register type from list : " + str(LSRegisterType))
#     sqlwhere = " AND SD.PROVISIONALDOCUMENTDATE between '" + LDStartDate + "' and '" + LDEndDate + "'"
#     print(sqlwhere)
#     # sqlorderby = " ORDER BY SALESDOCUMENT.PROVISIONALDOCUMENTDATE,SALESDOCUMENT.PROVISIONALCODE"
#     sql = ""
#     sqlorderby = ""
#     if LSRegisterType == '0':
#         header = "Agent"
#         sql = " SELECT agent.code as uniqueid," \
#               "        Agent.LongDescription As LONGDESCRIPTION " \
#               " , SD.PROVISIONALDOCUMENTDATE as sdate" \
#               "        ,  sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
#               " FROM SALESDOCUMENT SD " \
#               "        JOIN Agent                      ON      SD.Agent1Code                                     = Agent.Code   " \
#               "        JOIN SALESDOCUMENTLINE SDL      ON      SDL.SALESDOCUMENTPROVISIONALCODE          = SD.PROVISIONALCODE " \
#               "                                        AND     SDL.SALDOCPROVISIONALCOUNTERCODE          = SD.PROVISIONALCOUNTERCODE " \
#               "        JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
#               "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
#               "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
#               "        Join Product                On      SDL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE " \
#               "                                    And     FIKD.ItemUniqueId             = Product.AbsUniqueId  " \
#               " WHERE SD.DocumentTypeType = '06'  " + sqlwhere + " " \
#               "     AND   PRODUCT.ABSUNIQUEID = '" + LSItemcode + "'" \
#               " GROUP BY " \
#               "        Agent.LongDescription ,agent.code,SD.PROVISIONALDOCUMENTDATE "
#     elif LSRegisterType == '1':
#         header = "Item"
#         sql = " SELECT " \
#               "        Product.ABSUNIQUEID as uniqueid " \
#               "		   , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS LONGDESCRIPTION " \
#               "        , SDL.USERPRIMARYUOMCODE  " \
#               "        , sum(COALESCE(CAST(SDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY " \
#               " FROM SALESDOCUMENT SD " \
#               " JOIN SALESDOCUMENTLINE SDL      ON SD.PROVISIONALCODE   = SDL.SALESDOCUMENTPROVISIONALCODE " \
#               " JOIN FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
#               "                                    AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
#               "                                    AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
#               " Join Product                		On      SDL.ITEMTYPEAFICODE          = Product.ITEMTYPECODE    " \
#               "                            		    And     FIKD.ItemUniqueId            = Product.AbsUniqueId  " \
#               " JOIN QUALITYLEVEL               	ON      SDL.QUALITYCODE              = QUALITYLEVEL.CODE " \
#               "                                	    AND     SDL.ITEMTYPEAFICODE          = QUALITYLEVEL.ITEMTYPECODE  " \
#               " JOIN Agent                      	ON      SD.Agent1Code                = Agent.Code " \
#               " WHERE SD.DocumentTypeType = '06' " + sqlwhere + " " \
#               " AND Agent.code='" + LSItemcode + "' " \
#               " group by  " \
#               "        Product.LONGDESCRIPTION  " \
#               "        , QualityLevel.ShortDescription " \
#               "        , SDL.USERPRIMARYUOMCODE  " \
#               "        , Product.ABSUNIQUEID "
#     elif LSRegisterType == '2':
#         header = "Item"
#         sql = "select " \
#               "		Product.ABSUNIQUEID as uniqueid " \
#               "        , Product.LONGDESCRIPTION " \
#               "        , SALESDOCUMENTLINE.USERPRIMARYUOMCODE  " \
#               "        , sum(COALESCE(CAST(SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ,'')) AS QUANTITY    " \
#               "FROM SALESDOCUMENT  SD " \
#               "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SD.PROVISIONALCODE " \
#               "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode " \
#               "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
#               "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode   " \
#               "                                AND     Case IST.Position    " \
#               "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03    " \
#               "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06    " \
#               "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09    " \
#               "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
#               "JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
#               "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
#               "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
#               "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
#               " JOIN QUALITYLEVEL               	ON      SALESDOCUMENTLINE.QUALITYCODE              = QUALITYLEVEL.CODE " \
#               "                                	    AND     SALESDOCUMENTLINE.ITEMTYPEAFICODE          = QUALITYLEVEL.ITEMTYPECODE  " \
#               "WHERE SD.DocumentTypeType = '06' " + sqlwhere + "  " \
#                "AND UGG.ABSUNIQUEID='" + LSItemcode + "' " \
#                "GROUP BY Product.LONGDESCRIPTION  " \
#                "        , QualityLevel.ShortDescription " \
#                "        , SALESDOCUMENTLINE.USERPRIMARYUOMCODE  " \
#                "        , Product.ABSUNIQUEID "
#
#     sql += sqlorderby
#
#     print(sql)
#     stmt = con.db.prepare(con.conn, sql)
#     con.db.execute(stmt)
#     result = con.db.fetch_both(stmt)
#     print(result)
#     if result != False:
#         while result != False:
#             GSecondList.append(result)
#             print(result)
#             # print(result['CHALLANNUMBER'])
#             result = con.db.fetch_both(stmt)
#         return render(request, 'DispatchDetailRegisterList.html',
#                       {'GSecondList': GSecondList, 'startdate': startdate, 'enddate': enddate, 'reporttype': reporttype,
#                        'header': header,'itemname':LSItemname})
#     else:
#         # return render(request, 'StoreRegister.html',
#         #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
#         #                'ccode': ccode})
#         Exceptions = "Note: Please Select Valid Credentials"
#         return render(request, 'DispatchDetailRegister.html',
#                       {'GList': GList, "LSRegisterType": LSRegisterType, "reportname": Greportname, "header": Gheader,
#                        "LDStartDate": LDStartDate, "LDEndDate": LDEndDate, "Exceptions": Exceptions,'itemname':LSItemname})
#
#         # return
#     # return render(request, 'DispatchDetailRegisterList.html',
#     #               {'GList': GSecondList, 'startdate': startdate, 'enddate': enddate, 'reporttype': reporttype})
#
#
# def DespatchDetailLine(request):
#     global GSecondList
#     global reporttype
#     global startdate
#     global enddate
#     global GBasecode
#     result = ""
#     GLine.clear()
#     LSItemcode = str(request.GET['uniqueid'])
#     # LDStartDate = str(request.GET['startdate'])
#     # LDEndDate = str(request.GET['enddate'])
#     print("*--*-*-*-*-*-*-*-*-**-* from line  " + LSItemcode)
#     print("*--*-*-*-*-*-*-*-*-**-*  start date  fromm line" + startdate)
#     print("*--*-*-*-*-*-*-*-*-**-*  end date fron line " + enddate)
#     print("*--*-*-*-*-*-*-*-*-**-*  report type  from line " + reporttype)
#     print("*--*-*-*-*-*-*-*-*-**-*  Base code  from line " + GBasecode)
#     sql = ""
#     sqlwhere = " AND SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + startdate + "' and '" + enddate + "' "
#     if reporttype == '0':
#         # sqlwhere += " AND AGENT.CODE = '" + LSItemcode + "' AND PRODUCT.ABSUNIQUEID = '" + GBasecode + "' "
#         sqlwhere += " AND SALESDOCUMENT.Agent1CODE = '" + LSItemcode + "'  "
#     elif reporttype == '1':
#         sqlwhere += " AND PRODUCT.ABSUNIQUEID = " + LSItemcode + " AND AGENT.CODE = '" + GBasecode + "' "
#     elif reporttype == '2':
#         sqlwhere += " AND UGG.ABSUNIQUEID = '" + LSItemcode + "' AND PRODUCT.ABSUNIQUEID = '" + GBasecode + "' "
#
#     print("from Despatch Detail Line")
#     print(sqlwhere)
#     sqlwhere += " ORDER BY SALESDOCUMENT.PROVISIONALDOCUMENTDATE,SALESDOCUMENT.PROVISIONALCODE"
#
#     sql = " SELECT SALESDOCUMENT.PROVISIONALCODE                   AS INVOICENUMBER " \
#           "        , VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE,'DD/MM/YYYY')         AS INVOICEDATE " \
#           "        , Coalesce(Doc05.ExternalReference,'')          as LRNO " \
#           "        , Coalesce(TZ_DespTo.LONGDESCRIPTION,'')        as DespTO " \
#           "        , PLANTINVOICE.TRUCKNO                          AS LORRYNO " \
#           "        , BP_Consignee.LEGALNAME1                       AS CUSTOMER " \
#           "        , COALESCE(SaleLot.ValueString,ST.LOTCODE)      AS LOTNUMBER " \
#           "        , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As ShadeCode " \
#           "        , CAST(SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS DECIMAL(20,3)) AS QUANTITY " \
#           "        , COALESCE(CAST(InvRate.calculatedvalueRCC  AS DECIMAL(20,2)), PlantInvoiceLine.OrderPrice) AS RATE  " \
#           "        , PLANTINVOICELINE.NUMBEROFBALES                as Boxes  " \
#           "        , CAST(PLANTINVOICE.NETTVALUE AS DECIMAL(20,2)) As INVOICEAMOUNT  " \
#           "        , Agent.LongDescription                         AS BROKERNAME " \
#           "        , SALESDOCUMENT.SALESORDERCODE                  AS ORDERNO " \
#           "        , SALESDOCUMENTline.PreviousCode                AS CHALLANNO " \
#           "        , Agent.Longdescription                         AS CONSIGNERNAME " \
#           "        , COMPANY.LONGDESCRIPTION                       AS companyname  " \
#           "        , trim (Product.LONGDESCRIPTION )               AS PRODUCT " \
#           "        , trim ( QualityLevel.ShortDescription)         AS QUALITY " \
#           "FROM SALESDOCUMENT " \
#           "join OrderPartner               On      SALESDOCUMENT.OrdPrnCustomerSupplierCode 			  = OrderPartner.CustomerSupplierCode " \
#           "                                And     OrderPartner.CustomerSupplierType 					  = 1 " \
#           "join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId            = BusinessPartner.NumberID " \
#           "JOIN Agent                      ON      SALESDOCUMENT.Agent1Code                             = Agent.Code   " \
#           "JOIN SALESDOCUMENTLINE          ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
#           "                                AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE       = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
#           "                                AND     SALESDOCUMENTLINE.DOCUMENTTYPETYPE                   ='06' " \
#           "JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
#           "JOIN BusinessUnitVsCompany BUC  ON      SalesDocument.DivisionCode                           = BUC.DivisionCode " \
#           "                                AND     LOGICALWAREHOUSE.plantcode                           = BUC.factorycode " \
#           "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode                                 = BUnit.Code And BUnit.GroupFlag = 0 " \
#           "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode                                    = Company.Code And Company.GroupFlag = 1 " \
#           "JOIN ITEMTYPE                   ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
#           "JOIN QUALITYLEVEL               ON      SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
#           "                                AND     SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = QUALITYLEVEL.ITEMTYPECODE " \
#           "JOIN FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
#           "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
#           "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
#           "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
#           "JOIN PlantInvoice           ON      SALESDOCUMENT.PROVISIONALCODE               = PLANTINVOICE.CODE " \
#           "                            and     SALESDOCUMENT.DocumentTypeType              = '06' " \
#           "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = IST.ItemTypeCode " \
#           "                                AND     IST.GroupTypeCode In ('P09','B07') " \
#           "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode                                  = UGG.UserGenericGroupTypeCode   " \
#           "                                AND     Case IST.Position    " \
#           "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03    " \
#           "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06    " \
#           "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09    " \
#           "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
#           "LEFT Join StockTransaction St   On      SALESDOCUMENTline.PreviousCode          =  ST.OrderCode " \
#           "                            And     ST.TemplateCode                             = 'S04' " \
#           "                            and     St.transactiondetailnumber                  = 1 " \
#           "Left Join SalesDocument Doc05      On      Doc05.ProvisionalCode     			 = SALESDOCUMENTline.PreviousCode " \
#           "                                	And     Doc05.DocumentTypeType         		 = '05' " \
#           "LEFT JOIN OrderPartner OP_Consignee     On      PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERCODE 	 = OP_Consignee.CustomerSupplierCode " \
#           "                                        And     OP_Consignee.CustomerSupplierType 				 = 1 " \
#           "join BusinessPartner   BP_Consignee     On      OP_Consignee.OrderbusinessPartnerNumberId       = BP_Consignee.NumberID " \
#           "LEFT JOIN Address ADDRESS_Consignee     ON      BP_Consignee.ABSUNIQUEID         				 = ADDRESS_Consignee.UNIQUEID " \
#           "                                        AND     PlantInvoice.DELIVERYPOINTCODE             	 = ADDRESS_Consignee.CODE   " \
#           "left JOIN Transportzone TZ_DespTo   on          ADDRESS_Consignee.TRANSPORTZONECODE             = TZ_DespTo.code  " \
#           "JOIN PLANTINVOICELINE               ON          PLANTINVOICELINE.PLANTINVOICECODE               = PLANTINVOICE.CODE " \
#           "                                    AND         PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE       = PLANTINVOICE.DIVISIONCODE " \
#           "JOIN INDTAXDETAIL InvRate           ON          PlantInvoiceLine.ABSUNIQUEID                    = InvRate.ABSUNIQUEID " \
#           "                                    AND         InvRate.itaxcode                                = 'INR'  " \
#           "                                    AND         InvRate.TAXCATEGORYCODE                         = 'OTH' " \
#           "LEFT Join LOT                       On          St.LotCode                                      = Lot.Code " \
#           "LEFT JOIN ADSTORAGE SaleLot         ON          Lot.ABSUNIQUEID                                 = SaleLot.ABSUNIQUEID " \
#           "                                    And         SaleLot.NameEntityName                          = 'Lot'  " \
#           "                                    And         SaleLot.NameName                                = 'SaleLot'  " \
#           "                                    And         SaleLot.FieldName                               = 'SaleLot'  " \
#           "WHERE     SALESDOCUMENT.DocumentTypeType = '06'   "  + sqlwhere
#
#     print(sql)
#     stmt = con.db.prepare(con.conn, sql)
#     con.db.execute(stmt)
#     result = con.db.fetch_both(stmt)
#     # print(result)
#     if result != False:
#         while result != False:
#             GLine.append(result)
#             # print(result)
#             # print(result['CHALLANNUMBER'])
#             result = con.db.fetch_both(stmt)
#         return render(request, 'DispatchDetailRegisterList.html',
#                       {'GSecondList': GSecondList, 'GLine': GLine})
#     else:
#         # return render(request, 'StoreRegister.html',
#         #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
#         #                'ccode': ccode})
#         Exceptions = "Note: Please Select Valid Credentials"
#         # return
#         return render(request, 'DispatchDetailRegisterList.html', {'GSecondList': GSecondList, 'GLine': GLine,'Exceptions':Exceptions})
#
#
# def genratexls():
#     LSName = datetime.now()
#     LSstring = str(LSName)
#     LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
#                                                                                                       17:19] + LSstring[
#                                                                                                                20:]
#     LSFileName = " Invoice Without Shipping Bill No Register " + LSFileName + ".xlsx"
#     save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Export Invoice/",
#                                  LSFileName)
#     print(save_name)
#     #     xlsrpt.ExportInvoiceXLS(LSallParty, LSallcompany, LSParty, LSCompany,
#     #                                                             LDStartDate, LDEndDate, LSReportType)
#     #     save_name = os.path.join(os.path.expanduser("~"),
#     #                              "D:/Report Development/ReportDevelopment/" + xlsrpt.LSFileName)
#     #     filepath = xlsrpt.LSFileName
#     # if not os.path.isfile(filepath):
#     #     return render(request, 'Export_Invoice.html',
#     #               {'company': views.company, 'party': views.party, 'Exception': Exceptions})
