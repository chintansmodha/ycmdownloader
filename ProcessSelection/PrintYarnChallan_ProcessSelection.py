import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve

from Global_Files import Connection_String as con
from PrintPDF import PrintYarnChallan_PrintPDF as pdfrpt
from PrintPDF import PrintYeanChallanBoxNoWisePDF as pdfrptboxnowise
from PrintPDF import PrintYeanChallanBoxNoWisePDF as printchallanrpt
from reportlab.lib.pagesizes import landscape, A5
from GetDataFromDB import PrintYarnChallan_GetDataFromDB as PYC
GDataChallan=[]
GDataPrintChallan = []
GGSTInvoice = []
Company=[]
GDataTotal = []
Party=[]
Exceptions=""
save_name=""
LSFileName=""
GLotNo=[]
GTotalBoxes=[]
counter=0

def PrintChallan_PrintPDF(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType,request):
    global LSFileName
    global save_name
    global GDataPrintChallan
    global GDataChallan
    global GDataTotal
    global Company
    global Party
    global challanno
    global GTotalBoxes
    global counter
    challanno = []
    GDataChallan=[]
    GDataTotal=[]
    if LSReportType==1:
        PrintChallan(LSCompany, LSParty, LSDespatch, LDStartDate, LDEndDate, LSReportType,request)
        return render(request, 'PrintChallanTable.html',
                      {'GDataPrintChallan': GDataPrintChallan, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal})
    elif LSReportType==2:
        PrintChallanRule55(LSCompany, LSParty, LSDespatch, LDStartDate, LDEndDate, LSReportType,request)
        return render(request, 'PrintChallanTable_Rule55.html',
                      {'GDataPrintChallan': GDataPrintChallan, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal})
    elif LSReportType==3:
        # PrintChallan_Boxes_No_Wise_Table.html
        PrintChallanBoxNoWise(LSCompany,LSDespatch, LSParty, LDStartDate, LDEndDate, LSReportType,request)
        return render(request, 'PrintChallan_Boxes_No_Wise_Table.html',
                      {'GDataPrintChallan': GDataPrintChallan, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal,'LSCompany':LSCompany,'LSParty':LSParty,'Exceptions':Exceptions})
        # save_name=''
        # LSName = datetime.now()
        # LSstring = str(LSName)
        # LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
        #                                                                                                   17:19] + LSstring[
        #                                                                                                            20:]
        # LSFileName = "PrintYeanChallan_BoxNo_Wise" + LSFileName
        # save_name = os.path.join(os.path.expanduser("~"),
        #                          "D:/Report Development/Generated Reports/Print Yarn Challan Box No Wise/",
        #                          LSFileName)
        # # print("file path : " + save_name)
        #
        # printchallanrpt.c = printchallanrpt.canvas.Canvas(save_name + ".pdf")
        # PrintChallanBoxNoWise(LSCompany, LSParty, LDStartDate, LDEndDate, LSReportType,request)
        # filepath =save_name + ".pdf"
        # if not os.path.isfile(filepath):
        #     return render(request, 'PrintChallan.html',
        #               {'GDataPrintChallan': GDataPrintChallan, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal,'Exception': Exceptions})
        #
        # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    elif LSReportType==4:
        DespatchReport(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType, request)
        return render(request, 'DespatchReportTable.html',
                      {'GDataPrintChallan': GDataPrintChallan, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal})
    elif LSReportType=='5':
        PrintChallanBoxNoWiseInternal(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType, request)
        return render(request, 'PrintChallan_Boxes_No_Wise_Table.html',
                      {'GDataPrintChallan': GDataPrintChallan, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal,
                       'LSCompany': LSCompany, 'LSParty': LSParty, 'Exceptions': Exceptions})
    elif LSReportType==6:
        Print_GST_Invoice(LSCompany, LSParty, LSDespatch,LDStartDate, LDEndDate, LSReportType, request)
        return render(request, 'PrintChallan_GST_Invoice_Table.html',
                      {'GGSTInvoice': GGSTInvoice, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal,
                       'LSCompany': LSCompany, 'LSParty': LSParty, 'Exceptions': Exceptions,'counter':counter})
    elif LSReportType==7:
        Print_GST_Export_Invoice(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType, request)
        return render(request, 'PrintChallan_Export_GST_Invoice_Table.html',
                      {'GGSTInvoice': GGSTInvoice, 'GDataChallan': GDataChallan, 'GDataTotal': GDataTotal,
                       'LSCompany': LSCompany, 'LSParty': LSParty, 'Exceptions': Exceptions})

def PrintChallan(LSCompany, LSParty, LSDespatch,LDStartDate, LDEndDate, LSReportType,request):
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    Despatch = str(LSDespatch)
    Despatch = '(' + Despatch[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"

    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And BUnit.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BP.NumberId in " + Party
    if not LSDespatch:
        Despatch = " "
    elif LSDespatch:
        Despatch = " And TZ_DespFrom.CODE in " + Despatch

    sql = "Select Company.LongDescription As Company,SD.PROVISIONALCODE As ChallanNo," \
          " VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ChallanDate," \
          " '' As LotNo, Sum(Cast(SDL.USERPRIMARYQUANTITY as Decimal(18,3))) As Quantity, SD.EXTERNALREFERENCE As LRNO,0 As Boxes" \
          " from SalesDocument As SD" \
          " join SalesDocumentLine  AS SDL  on SD.PROVISIONALCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE" \
          " AND SD.PROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE" \
          " JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode" \
          " JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1" \
          " JOIN LOGICALWAREHOUSE           ON SDL.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE" \
          " AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode" \
          " join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " And OP.CustomerSupplierType = 1" \
          " join BusinessPartner As BP  On OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID" \
          " where SD.DOCUMENTTYPETYPE='05'" \
          " And SD.PROVISIONALDOCUMENTDATE between" + StartDate + " and " + EndDate +""+ Company + Party+Despatch+"" \
                                                                                                         " Group By Company.LongDescription, SD.PROVISIONALCODE, VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY'),SD.EXTERNALREFERENCE" \
                                                                                                         " order by ChallanNo"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters


    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataPrintChallan.append(result)
        result = con.db.fetch_both(stmt)

def PrintChallanRule55(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType,request):
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    Despatch = str(LSDespatch)
    Despatch = '(' + Despatch[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"

    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And BUnit.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BP.NumberId in " + Party
    if not LSDespatch:
        Despatch = " "
    elif LSDespatch:
        Despatch = " And TZ_DespFrom.CODE in " + Despatch

    sql = "Select Company.LongDescription As Company,SD.PROVISIONALCODE As ChallanNo," \
          " VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ChallanDate," \
          " '' As LotNo, Sum(Cast(SDL.USERPRIMARYQUANTITY as Decimal(18,3))) As Quantity, SD.EXTERNALREFERENCE As LRNO,0 As Boxes" \
          " from SalesDocument As SD" \
          " join SalesDocumentLine  AS SDL  on SD.PROVISIONALCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE" \
          " AND SD.PROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE" \
          " JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode" \
          " JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1" \
          " JOIN LOGICALWAREHOUSE           ON SDL.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE" \
          " AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode" \
          " join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " And OP.CustomerSupplierType = 1" \
          " join BusinessPartner As BP  On OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID" \
          " where SD.DOCUMENTTYPETYPE='05'" \
          " And SD.PROVISIONALDOCUMENTDATE between" + StartDate + " and " + EndDate +""+ Company + Party+Despatch+"" \
          " Group By Company.LongDescription, SD.PROVISIONALCODE, VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY'),SD.EXTERNALREFERENCE" \
          " order by ChallanNo"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters


    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataPrintChallan.append(result)
        result = con.db.fetch_both(stmt)

def DespatchReport(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType, request):

    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"

    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And BUnit.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BP.NumberId in " + Party

    sql = "SELECT  SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER" \
          " , VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY') AS CHALLANDATE" \
          " , ADDRESS.TOWN As Despatch" \
          " , ST.LOTCODE As LotNo" \
          " , SAlESDOCUMENTLINE.EXTERNALREFERENCE AS LRNO" \
          " , Sum(Boxes.ACTUALNETWT) AS QUANTITY" \
          " , count(*) BOXESCOUNT" \
          " FROM SALESDOCUMENT" \
          " join OrderPartner               On      SALESDOCUMENT.OrdPrnCustomerSupplierCode        = OrderPartner.CustomerSupplierCode" \
          " And     OrderPartner.CustomerSupplierType = 1" \
          " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID" \
          " JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE" \
          " AND SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE      = SALESDOCUMENT.PROVISIONALCOUNTERCODE" \
          " JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE" \
          " JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode                           = BUC.DivisionCode" \
          " AND LOGICALWAREHOUSE.plantcode                            = BUC.factorycode" \
          " JOIN FinBusinessUnit BUnit      ON BUC.BusinessUnitcode                                 = BUnit.Code And BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit As Company ON Bunit.GroupBUCode                                    = Company.Code And Company.GroupFlag = 1" \
          " JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE" \
          " JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE" \
          " AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE" \
          " JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
          " JOIN UserGenericGroup UGG      ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.Position" \
          " When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03" \
          " When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06" \
          " When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09" \
          " When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code" \
          " JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " LEFT JOIN ADDRESS               ON      BusinessPartner.ABSUNIQUEID = ADDRESS.UNIQUEID" \
          " AND     SALESDOCUMENT.DELIVERYPOINTCODE = ADDRESS.CODE" \
          " Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId                           = Product.AbsUniqueId" \
          " Join StockTransaction St     On      SALESDOCUMENT.ProvisionalCode              = ST.OrderCode" \
          " And      ST.TemplateCode                            = 'S04'" \
          " Join    BKLElements Boxes    On      ST.ContainerElementCode                    = Boxes.Code" \
          " Left Join SalesDocumentLine PILine      On      PILine.DocumentTypeType         = '06'" \
          " And     PILine.PreviousCode                     = SALESDOCUMENT.ProvisionalCode" \
          " And     PILine.PreviousDocumentTypeType         = '05'" \
          " Left Join SalesDocument PI      On      PILine.SalesDocumentProvisionalCode     = PI.ProvisionalCode" \
          " And     PILine.DocumentTypeType                 = PI.DocumentTypeType" \
          " And     PILine.SaldocPROVISIONALCOUNTERCODE     = PI.PROVISIONALCOUNTERCODE" \
          " And     PI.PreviousCode                         = SALESDOCUMENT.ProvisionalCode" \
          " WHERE SALESDOCUMENT.DocumentTypeType = '05'" \
          " And SALESDOCUMENT.PROVISIONALDOCUMENTDATE between" + StartDate + " and " + EndDate + "" + Company + Party + "" \
          " Group By Company.LongDescription, SALESDOCUMENT.PROVISIONALCODE, " \
          " VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY'),SALESDOCUMENT.EXTERNALREFERENCE,ST.LOTCODE,SALESDOCUMENTLINE.EXTERNALREFERENCE,ADDRESS.TOWN" \
          " order by CHALLANNUMBER"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)

    while result != False:
        GDataPrintChallan.append(result)
        result = con.db.fetch_both(stmt)

def PrintChallanBoxNoWise(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType,request):
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    Despatch = str(LSDespatch)
    Despatch = '(' + Despatch[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"
    counter=0
    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And Company.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BusinessPartner.NumberId in " + Party
    if not LSDespatch:
        Despatch = " "
    elif LSDespatch:
        Despatch = " And TZ_DespFrom.CODE in " + Despatch

    sql = "SELECT  SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
          "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
          "        , '' As LotNo " \
          "        , sum(cast(BOXES.ACTUALNETWT as decimal(18,3))) AS QUANTITY " \
          "        ,count(*) BOXESCOUNT " \
          "FROM SALESDOCUMENT " \
          "join OrderPartner               On      SALESDOCUMENT.OrdPrnCustomerSupplierCode        = OrderPartner.CustomerSupplierCode " \
          "                                And     OrderPartner.CustomerSupplierType = 1 " \
          " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
          "                                AND SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE      = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
          "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
          "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode                           = BUC.DivisionCode " \
          "                                AND LOGICALWAREHOUSE.plantcode                            = BUC.factorycode " \
          "JOIN FinBusinessUnit BUnit      ON BUC.BusinessUnitcode                                 = BUnit.Code And BUnit.GroupFlag = 0 " \
          "JOIN FinBusinessUnit As Company ON Bunit.GroupBUCode                                    = Company.Code And Company.GroupFlag = 1 " \
          "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
          "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
          "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
          "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode " \
          "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
          " JOIN UserGenericGroup UGG      ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode   " \
          "                                AND     Case IST.Position  " \
          "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03 " \
          "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
          "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
          "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code  " \
          "JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')  " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
          "                            AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
          "Join Product                On      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = Product.ITEMTYPECODE    " \
          "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId    " \
          "Join StockTransaction St     On      SALESDOCUMENT.ProvisionalCode              = ST.OrderCode   " \
          "                            And      ST.TemplateCode                            = 'S04'   " \
          "Join    BKLElements Boxes    On      ST.ContainerElementCode                    = Boxes.Code  " \
          "Left Join SalesDocumentLine PILine      On      PILine.DocumentTypeType         = '06' " \
          "                                And     PILine.PreviousCode                     = SALESDOCUMENT.ProvisionalCode " \
          "                                And     PILine.PreviousDocumentTypeType         = '05' " \
          "Left Join SalesDocument PI      On      PILine.SalesDocumentProvisionalCode     = PI.ProvisionalCode " \
          "                                And     PILine.DocumentTypeType                 = PI.DocumentTypeType " \
          "                                And     PILine.SaldocPROVISIONALCOUNTERCODE     = PI.PROVISIONALCOUNTERCODE   " \
          "                                And     PI.PreviousCode                         = SALESDOCUMENT.ProvisionalCode " \
          " WHERE SALESDOCUMENT.DocumentTypeType = '05'  and SALESDOCUMENT.PROVISIONALDOCUMENTDATE between " + str(
        StartDate) + " and " + str(EndDate) +" "+ Company + Party+Despatch+" " \
          "GROUP BY " \
          "        SALESDOCUMENT.PROVISIONALCODE " \
          "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE " \
          " ORDER  BY  " \
          "          SALESDOCUMENT.PROVISIONALCODE, " \
          "          SALESDOCUMENT.PROVISIONALDOCUMENTDATE  " \

    print(sql)
    GDataPrintChallan.clear()
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result != False:
        while result != False:
            GDataPrintChallan.append(result)
            result = con.db.fetch_both(stmt)

    # if result != False:
    #     pdfrptboxnowise.newrequest()

    #     while result != False:
    #         # global counter
    #         counter = counter + 1
    #         # pdfrptboxnowise.textsize(pdfrptboxnowise.c, result, pdfrptboxnowise.d,pdfrptboxnowise.x)
    #         pdfrptboxnowise.textsize(pdfrptboxnowise.c, result)
    #
    #         pdfrptboxnowise.d = pdfrptboxnowise.dvalue()
    #         result = con.db.fetch_both(stmt)
    #
    #     pdfrptboxnowise.printlasttotal(pdfrptboxnowise.d)
    #     pdfrptboxnowise.printtotalmain()
    #     pdfrptboxnowise.d = 530
    #
    #     pdfrptboxnowise.d = pdfrptboxnowise.d - 20
    #     pdfrptboxnowise.c.showPage()
    #     # pdfrptpyboxwise.print("after calling register")
    #
    #     if counter == 0:
    #         Exceptions = "Note: No Result found according to your selected criteria "
    #         print("counter = 0")
    #     else:
    #         # pdfrptboxnowise.c.showPage()
    #         # pdfrptboxnowise.c.setPageSize(landscape(A5))
    #         # pdfrptboxnowise.c.save()
    #         # pdfrptboxnowise.newrequest()
    #         # pdfrptboxnowise.d = pdfrpt.newpage()
    #         # print("from  else befoer over")
    #         pdfrptboxnowise.c.showPage()
    #         pdfrptboxnowise.c.save()
    #         # url = "file:///D:/New format Report/Generated Reports/Print yan challan/" + LSFileName + ".pdf"
    #         # os.startfile(url)
    #         pdfrptboxnowise.newrequest()
    #         pdfrptboxnowise.d = pdfrpt.newpage()
    else:
        Exceptions = "Note: Please Select Valid Credentials"
        return

def Print_GST_Invoice(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType,request):
    global counter
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    Despatch = str(LSDespatch)
    Despatch = '(' + Despatch[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"
    counter=0
    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And Company.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BusinessPartner.NumberId in " + Party
    if not LSDespatch:
        Despatch = " "
    elif LSDespatch:
        Despatch = " And TZ_DespFrom.CODE in " + Despatch

    SQLWHERE = str(StartDate) + " and " + str(EndDate) + " " + Company + Party+Despatch
    print(SQLWHERE)
    sql=""
    # sql = " SELECT  plantinvoice.code as INVOICENO " \
    #       "        ,SALESDOCUMENTLINE.PreviousCode AS CHALLANNUMBER  " \
    #       "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
    #       "        , BusinessPartner.LEGALNAME1  AS CUSTOMER  " \
    #       "        , '' As LotNo  " \
    #       "        , cast(Sum(SALESDOCUMENTLINE.USERPRIMARYQUANTITY) as decimal(18,2)) AS QUANTITY  " \
    #       "        ,count(*) BOXESCOUNT  " \
    #       " From PlantInvoice  " \
    #       "        JOIN SALESDOCUMENT      ON       PLANTINVOICE.CODE                                      = SALESDOCUMENT.PROVISIONALCODE  " \
    #       "        JOIN OrderPartner       ON      SALESDOCUMENT.OrdPrnCustomerSupplierCode                = OrderPartner.CustomerSupplierCode " \
    #       "                                And     OrderPartner.CustomerSupplierType                       = 1  " \
    #       "        JOIN BusinessPartner    ON      OrderPartner.OrderbusinessPartnerNumberId               = BusinessPartner.NumberID  " \
    #       "        JOIN SALESDOCUMENTLINE  ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE          = SALESDOCUMENT.PROVISIONALCODE " \
    #       "                                AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE          = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
    #       "    JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
    #       " WHERE SALESDOCUMENT.DocumentTypeType = '06'  and SALESDOCUMENT.PROVISIONALDOCUMENTDATE between "
    # sql += SQLWHERE + "GROUP BY " \
    #                   "        PLANTINVOICE.CODE " \
    #                   "        , SALESDOCUMENT.PROVISIONALCODE " \
    #                   "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE" \
    #                   "        ,BusinessPartner.LEGALNAME1 " \
    #                   "        ,SALESDOCUMENTLINE.PreviousCode " \
    #                   " ORDER  BY  " \
    #                   "          plantinvoice.code "
    sql = " SELECT  plantinvoice.code as INVOICENO  " \
          "	  , SALESDOCUMENTLINE.PreviousCode AS CHALLANNUMBER " \
          "	  , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE  " \
          "	  , BP_Customer.LEGALNAME1  AS CUSTOMER " \
          " From PlantInvoice   " \
          "	JOIN SALESDOCUMENT      ON PLANTINVOICE.CODE                   = SALESDOCUMENT.PROVISIONALCODE  " \
          "						  and SALESDOCUMENT.DocumentTypeType = '06'   " \
          "	JOIN DIVISION                             ON PLANTINVOICE.DIVISIONCODE    = DIVISION.CODE  " \
          "	JOIN OrderPartner OP_Customername 	on PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP_Customername. CustomerSupplierCode   " \
          "											AND  PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_Customername.CustomerSupplierType   " \
          "	join BusinessPartner BP_Customer 		On      OP_Customername.OrderbusinessPartnerNumberId = BP_Customer.NumberID   " \
          "	JOIN AddressGst   CUSTOMERGSTIN  		ON      CUSTOMERGSTIN.UniqueID = BP_Customer.AbsUniqueId           " \
          "	JOIN SALESDOCUMENTLINE          ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE  " \
          "								  AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE      = SALESDOCUMENT.PROVISIONALCOUNTERCODE    " \
          "								  and     SALESDOCUMENTline.DocumentTypeType = '06'    " \
          "	join salesdocumentline sdline05 on      sdline05.salesdocumentprovisionalcode = SALESDOCUMENTLINE.PreviousCode  " \
          "								  and     sdline05.documenttypetype='05'  " \
          "	JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE   " \
          "	JOIN BusinessUnitVsCompany BUC  ON      SalesDocument.DivisionCode                       = BUC.DivisionCode  " \
          "								  AND     LOGICALWAREHOUSE.plantcode                       = BUC.factorycode " \
          " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between   "
    sql += SQLWHERE + " GROUP BY           PLANTINVOICE.CODE  " \
                              "		, SALESDOCUMENT.PROVISIONALCODE  " \
                              "       , SALESDOCUMENT.PROVISIONALDOCUMENTDATE " \
                              "       , BP_Customer.LEGALNAME1   " \
                              "       , SALESDOCUMENTLINE.PreviousCode " \
                              "       ORDER  BY   plantinvoice.code "

    print("query for the gst invoice table")
    print(sql)

    GGSTInvoice.clear()
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result != False:
        while result != False:
            GGSTInvoice.append(result)
            print(result['CHALLANNUMBER'])
            result = con.db.fetch_both(stmt)
            counter=counter+1
    else:
        Exceptions = "Note: Please Select Valid Credentials"
        return

def Print_GST_Export_Invoice(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType,request):
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    Despatch = str(LSDespatch)
    Despatch = '(' + Despatch[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"
    counter=0
    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And Company.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BusinessPartner.NumberId in " + Party
    if not LSDespatch:
        Despatch = " "
    elif LSDespatch:
        Despatch = " And TZ_DespFrom.CODE in " + Despatch

    SQLWHERE = str(StartDate) + " and " + str(EndDate) + " " + Company + Party+Despatch

    sql=""
    sql = " SELECT  plantinvoice.code as INVOICENO " \
          "	  ,SALESDOCUMENTLINE.PreviousCode AS CHALLANNUMBER  " \
          "	  , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE  " \
          "	  , BusinessPartner.LEGALNAME1  AS CUSTOMER   " \
          " From PlantInvoice  " \
          "	  JOIN SALESDOCUMENT      ON       PLANTINVOICE.CODE                                      = SALESDOCUMENT.PROVISIONALCODE   " \
          "							  AND   SALESDOCUMENT.DocumentTypeType 							  = '06'     " \
          "	  JOIN OrderPartner       ON      SALESDOCUMENT.OrdPrnCustomerSupplierCode                = OrderPartner.CustomerSupplierCode  " \
          "							  And     OrderPartner.CustomerSupplierType                       = 1   " \
          "	  JOIN BusinessPartner    ON      OrderPartner.OrderbusinessPartnerNumberId               = BusinessPartner.NumberID   " \
          "	  JOIN SALESDOCUMENTLINE  ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE          = SALESDOCUMENT.PROVISIONALCODE  " \
          "							  AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE          = SALESDOCUMENT.PROVISIONALCOUNTERCODE  " \
          "	  JOIN    SALESORDER      ON SALESORDER.CODE      										  = SALESDOCUMENT.SALESORDERCODE " \
          "	  JOIN    SALESORDERIE    ON SALESORDERIE.CODE    										  = SALESORDER.CODE " \
          "	  JOIN LOGICALWAREHOUSE   ON      SALESDOCUMENTLINE.WAREHOUSECODE                         = LOGICALWAREHOUSE.CODE  " \
          "	  JOIN PLANT              ON     LOGICALWAREHOUSE.plantcode                			      = PLANT.CODE  " \
          "	 left JOIN Transportzone TZ_DespFrom     on      Plant.TRANSPORTZONECODE     			  = TZ_DespFrom.code   " \
          " WHERE SALESORDERIE.TYPEOFINVOICE ='2'      and SALESDOCUMENT.PROVISIONALDOCUMENTDATE between  "
    sql+=SQLWHERE +  "GROUP BY " \
          "        PLANTINVOICE.CODE " \
          "        , SALESDOCUMENT.PROVISIONALCODE " \
          "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE" \
          "        ,BusinessPartner.LEGALNAME1 " \
          "        ,SALESDOCUMENTLINE.PreviousCode " \
          " ORDER  BY  " \
          "          plantinvoice.code "

    print("query for the gst invoice table")
    print(sql)
    GGSTInvoice.clear()
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result != False:
        while result != False:
            GGSTInvoice.append(result)
            print(result['CHALLANNUMBER'])
            result = con.db.fetch_both(stmt)
    else:
        Exceptions = "Note: Please Select Valid Credentials"
        return

def PrintChallanBoxNoWiseInternal(LSCompany, LSParty,LSDespatch, LDStartDate, LDEndDate, LSReportType,request):
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"

    if not LSCompany:
        Company = " "
    elif LSCompany:
        Company = " And BUnit.Code in " + Company
    if not LSParty:
        Party = " "
    elif LSParty:
        Party = " And BP.NumberId in " + Party

    sql="Select  ID.PROVISIONALCODE As CHALLANNUMBER" \
        " ,ID.PROVISIONALDOCUMENTDATE As CHALLANDATE" \
        " ,ST.LOTCODE As LotNo" \
        " ,ID.EXTERNALREFERENCE As LRNO" \
        " ,count(*) BOXESCOUNT" \
        " FROM InternalDocument As ID" \
        " JOIN OrderPartner As OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 3" \
        " JOIN LOGICALWAREHOUSE ToDept            ON      OP.ORDERLOGICALWAREHOUSECODE = ToDept.CODE" \
        " JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN LOGICALWAREHOUSE                   ON      IDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
        " JOIN FullItemKeyDecoder FIKD            ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
        " AND     COALESCE(IDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
        " AND     COALESCE(IDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
        " AND     COALESCE(IDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
        " AND     COALESCE(IDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
        " AND     COALESCE(IDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
        " AND     COALESCE(IDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
        " AND     COALESCE(IDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
        " AND     COALESCE(IDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
        " AND     COALESCE(IDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
        " AND     COALESCE(IDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
        " JOIN Product                            ON      IDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = Product.AbsUniqueId" \
        " JOIN QUALITYLEVEL                       ON      IDL.QUALITYCODE = QUALITYLEVEL.CODE" \
        " AND     IDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
        " JOIN ItemSubcodeTemplate As IST         ON      IDL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
        " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
        " JOIN UserGenericGroup As UGG            ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
        " AND     Case IST.Position" \
        " When 1 Then IDL.SubCode01 When 2 Then IDL.SubCode02 When 3 Then IDL.SubCode03" \
        " When 4 Then IDL.SubCode04 When 5 Then IDL.SubCode05 When 6 Then IDL.SubCode06" \
        " When 7 Then IDL.SubCode07 When 8 Then IDL.SubCode08 When 9 Then IDL.SubCode09" \
        " When 10 Then IDL.SubCode10 End = UGG.Code" \
        " JOIN StockTransaction ST                ON      IDL.IntDocProvisionalCounterCode = ST.OrderCounterCode" \
        " AND     IDL.IntDocumentProvisionalCode = ST.OrderCode" \
        " AND     IDL.OrderLine = ST.OrderLine" \
        " AND     IDL.OrderSubLine = ST.OrderSubLine" \
        " AND     ST.ContainerElementCode IS NOT NULL" \
        " JOIN BKLELEMENTS BE                     ON      ST.ContainerItemTypeCode = BE.ItemTypeCode" \
        " AND     ST.ContainerSubCode01 = BE.SubCodeKey" \
        " AND     ST.ContainerElementCode = BE.Code" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.PROVISIONALCOUNTERCODE='I04' AND ID.TEMPLATECODE='I04'" \
        " And ID.PROVISIONALDOCUMENTDATE between" + StartDate + " and " + EndDate + "" + Company + Party + "" \
        " GROUP BY ID.PROVISIONALDOCUMENTDATE, ST.LOTCODE,ID.PROVISIONALCODE,ID.EXTERNALREFERENCE"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)

    while result != False:
        GDataPrintChallan.append(result)
        result = con.db.fetch_both(stmt)