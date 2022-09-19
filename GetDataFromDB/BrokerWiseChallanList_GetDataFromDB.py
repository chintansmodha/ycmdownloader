from django.shortcuts import render


from Global_Files import Connection_String as con
import os
from datetime import datetime
from PrintPDF import BrokerWiseChallanList_PrintPDF as pdfrpt
from PrintPDF import PrintYeanChallanBoxNoWisePDF as pdfrptboxnowise
# from PrintPDF import PrintYeanChallanBox_PrintPDF as pdfrptboxnowise
from ProcessSelection import BrokerWiseChallanList_ProcessSelection as BWCL
from FormLoad import BrokerWiseChallanList_FormLoad as views

counter = 0
Exception = ""
def BrokerWiseChallanList_PrintPDF(LSselcompany, LSselparty, LSselstate, LSselBrokergroup, LSselitemtype, LSselshade,
                                   LSallparty, LSallshade, LSallstate, LSallbroker, LSallcompany, LSallitemtype,
                                   LDStartDate, LDEndDate, LSRegistertype, sqlwhere, LSFileName,LSLotno,request):
    sql = ""
    global counter
    # pdfrpt.d = 510
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print(sqlwhere)
    sql = "SELECT plantinvoice.code                       AS InvoiceNo, " \
          "       plantinvoice.invoicedate                AS InvoiceDate, " \
          "       businesspartner.legalname1              AS PartyName, " \
          "       AgGrp.longdescription                   AS BrokerGroupName, " \
          "       agent.longdescription                   AS BrokerName, " \
          "       businesspartner.legalname1              AS party, " \
          "       plantinvoiceline.primaryqty             AS QUANTITY, " \
          "       InvRate.calculatedvaluercc              AS InvRate, " \
          "       Itemamt.calculatedvaluercc              AS ItemAmount, " \
          "       nettvalue                               AS InvoiceAmount, " \
          "       Trim (product.longdescription || ' ' || qualitylevel.shortdescription) AS PRODUCT, " \
          "       UGG.longdescription                     AS ShadeName, " \
          "       Company.longdescription                 AS CompanyName, " \
          "       division.longdescription                AS DivisionName, " \
          "       COALESCE(TD.longdescription, '')        AS TruckDriver, " \
          "       COALESCE(TD.drivinglicence, '')         AS TruckDriverLicenceNo, " \
          "       COALESCE(BP_Trpt1.legalname1, 'Not Found')       AS TransporterName1, " \
          "       salesdocument.numberplate               AS VehicleNo " \
          " FROM   plantinvoice " \
          "       JOIN salesdocument " \
          "         ON salesdocument.provisionalcode 					 =            plantinvoice.salesinvoiceprovisionalcode " \
          "          AND salesdocument.DOCUMENTTYPETYPE=06 " \
          "       JOIN orderpartner " \
          "         ON plantinvoice.buyerifotccustomersuppliercode 	 =            orderpartner.customersuppliercode " \
          "            AND plantinvoice.buyerifotccustomersuppliertype =            orderpartner.customersuppliertype " \
          "            AND orderpartner.customersuppliertype = 1 " \
          "            AND salesdocument.ordprncustomersuppliercode =               orderpartner.customersuppliercode " \
          "       JOIN businesspartner " \
          "         ON orderpartner.orderbusinesspartnernumberid = businesspartner.numberid " \
          "       LEFT JOIN truckdriver TD " \
          "              ON salesdocument.truckdrivercode = TD.code " \
          "       JOIN businesspartner AS BP " \
          "         ON orderpartner.orderbusinesspartnernumberid = BP.numberid " \
          "       LEFT JOIN orderpartner AS OP_Trpt1 " \
          "              ON salesdocument.firstcarriercode = OP_Trpt1.customersuppliercode " \
          "                 AND salesdocument.firstcarriertype =                     OP_Trpt1.customersuppliertype " \
          "       LEFT JOIN businesspartner AS BP_Trpt1 " \
          "              ON OP_Trpt1.orderbusinesspartnernumberid = BP_Trpt1.numberid " \
          "       JOIN division " \
          "         ON division.code = plantinvoice.divisioncode " \
          "       JOIN agent " \
          "         ON plantinvoice.agent1code = agent.code " \
          "       JOIN agentsgroupdetail AGD " \
          "         ON plantinvoice.agent1code = AGD.agentcode " \
          "       JOIN agentsgroup AgGrp " \
          "         ON AGD.agentsgroupcode = AgGrp.code " \
          "       JOIN businessunitvscompany BUC " \
          "         ON plantinvoice.divisioncode = BUC.divisioncode " \
          "            AND plantinvoice.factorycode = BUC.factorycode " \
          "       JOIN finbusinessunit BUnit " \
          "         ON BUC.businessunitcode = BUnit.code " \
          "            AND BUnit.groupflag = 0 " \
          "       JOIN finbusinessunit AS Company " \
          "         ON Bunit.groupbucode = Company.code " \
          "            AND Company.groupflag = 1 " \
          "       JOIN plantinvoiceline " \
          "         ON plantinvoice.code = plantinvoiceline.plantinvoicecode " \
          "            AND plantinvoice.divisioncode =                 plantinvoiceline.plantinvoicedivisioncode " \
          "            AND plantinvoice.invoicedate = plantinvoiceline.invoicedate " \
          "       JOIN qualitylevel " \
          "         ON plantinvoiceline.qualitylevelcode = qualitylevel.code " \
          "            AND plantinvoiceline.itemtypecode = qualitylevel.itemtypecode " \
          "       JOIN fullitemkeydecoder FIKD " \
          "         ON plantinvoiceline.itemtypecode = FIKD.itemtypecode " \
          "            AND COALESCE(plantinvoiceline.subcode01, '') =                COALESCE(FIKD.subcode01, '') " \
          "            AND COALESCE(plantinvoiceline.subcode02, '') =                COALESCE(FIKD.subcode02, '') " \
          "            AND COALESCE(plantinvoiceline.subcode03, '') =                COALESCE(FIKD.subcode03, '') " \
          "            AND COALESCE(plantinvoiceline.subcode04, '') =                COALESCE(FIKD.subcode04, '') " \
          "            AND COALESCE(plantinvoiceline.subcode05, '') =                COALESCE(FIKD.subcode05, '') " \
          "            AND COALESCE(plantinvoiceline.subcode06, '') =                COALESCE(FIKD.subcode06, '') " \
          "            AND COALESCE(plantinvoiceline.subcode07, '') =                COALESCE(FIKD.subcode07, '') " \
          "            AND COALESCE(plantinvoiceline.subcode08, '') =                COALESCE(FIKD.subcode08, '') " \
          "            AND COALESCE(plantinvoiceline.subcode09, '') =                COALESCE(FIKD.subcode09, '') " \
          "            AND COALESCE(plantinvoiceline.subcode10, '') =                COALESCE(FIKD.subcode10, '') " \
          "       JOIN product " \
          "         ON plantinvoiceline.itemtypecode = product.itemtypecode " \
          "            AND FIKD.itemuniqueid = product.absuniqueid " \
          "       JOIN itemsubcodetemplate IST " \
          "         ON plantinvoiceline.itemtypecode = IST.itemtypecode " \
          "            AND IST.grouptypecode IN ( 'MB4', 'P09', 'B07' ) " \
          "       JOIN usergenericgroup UGG " \
          "         ON IST.grouptypecode = UGG.usergenericgrouptypecode " \
          "            AND CASE IST.position " \
          "                  WHEN 1 THEN plantinvoiceline.subcode01 " \
          "                  WHEN 2 THEN plantinvoiceline.subcode02 " \
          "                  WHEN 3 THEN plantinvoiceline.subcode03 " \
          "                  WHEN 4 THEN plantinvoiceline.subcode04 " \
          "                  WHEN 5 THEN plantinvoiceline.subcode05 " \
          "                  WHEN 6 THEN plantinvoiceline.subcode06 " \
          "                  WHEN 7 THEN plantinvoiceline.subcode07 " \
          "                  WHEN 8 THEN plantinvoiceline.subcode08 " \
          "                  WHEN 9 THEN plantinvoiceline.subcode09 " \
          "                  WHEN 10 THEN plantinvoiceline.subcode10 " \
          "                END = UGG.code " \
          "       JOIN indtaxdetail ItemAmt " \
          "         ON plantinvoiceline.absuniqueid = ItemAmt.absuniqueid " \
          "           AND ItemAmt.itaxcode = '998' " \
          "            AND ItemAmt.taxcategorycode = 'OTH' " \
          "       JOIN indtaxdetail InvRate " \
          "         ON plantinvoiceline.absuniqueid = InvRate.absuniqueid " \
          "            AND InvRate.itaxcode = 'INR' " \
          "            AND InvRate.taxcategorycode = 'OTH' " \
          " WHERE plantinvoice.INVOICEDATE between '" + str(stdt) + "' and '" + str(etdt) + "' " + sqlwhere + "  " \
          " ORDER  BY Company.longdescription, " \
          "          AgGrp.longdescription, " \
          "          plantinvoice.code, " \
          "          plantinvoice.invoicedate  "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # # print("result is : "+str(result))
    # LSLotno=LSLotno
    # global counter

    if result == False:
        print("false")
        BWCL.Exception = "Note: Please Select Vali"
        return render(request, 'BrokerwiseChallanList.html',
                      {'company': views.company, 'party': views.party, 'state': views.state, 'itemtype': views.itemtype,
                       'shade': views.shade,
                       'broker': views.broker, 'Exception': BWCL.Exception})

    pdfrpt.newrequest()
    while result != False:

        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt,LSLotno,LSRegistertype)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)


        if pdfrpt.d < 40:
            # pdfrpt.d = 730
            pdfrpt.d = 510
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.divisioncode,LSLotno,LSRegistertype)
            pdfrpt.d = pdfrpt.d - 20
    print('after  while')

    print(result)
    if result == False:
        if counter > 0:
            pdfrpt.printitemtotal(pdfrpt.d)
            if LSRegistertype == '0':
                pdfrpt.printbrokertotal(pdfrpt.d)
                pdfrpt.printbrokergrouptotal(pdfrpt.d)
            elif LSRegistertype == '1':
                pdfrpt.printpartytotal(pdfrpt.d)
            pdfrpt.printcompanytotal(pdfrpt.d)
            # pdfrpt.printdepartmenttotal(pdfrpt.d)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            Exceptions = ""
            # pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria"
            return
    print('after result')

    if counter == 0:

        Exception = "Note: No Result found according to your selected criteria "
        print("counter = 0")
    else:
        pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        # url = "file:///D:/New format Report/Generated Reports/Broker Wise Challan List/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
        # print("from  else befoer over")

    print('end of the report')

    return

    # if LSRegistertype=='2':
    #     print("before calling register")
    #     result=""
    #     sql="SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
    #         "        , COMPANY.LONGDESCRIPTION AS  companyname   " \
    #         "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
    #         "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
    #         "        , SALESDOCUMENT.SALESORDERCODE AS REFERANCECODE " \
    #         "        , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT " \
    #         "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
    #         "        , TRIM (UGG.Code)  ||'/'||UGG.LONGDESCRIPTION As ShadeCode  " \
    #         "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
    #         "        , BusinessPartner.ADDRESSLINE1 ||','||" \
    #         "           BusinessPartner.ADDRESSLINE2 ||','||" \
    #         "           BusinessPartner.ADDRESSLINE3 ||','||" \
    #         "           BusinessPartner.ADDRESSLINE4 ||','||" \
    #         "           BusinessPartner.ADDRESSLINE5 as Address " \
    #         "        ,SAlESDOCUMENTLINE.EXTERNALREFERENCEDATE AS LRDATE " \
    #         "        ,SAlESDOCUMENTLINE.EXTERNALREFERENCE AS LRNO " \
    #         "        , BKLELEMENTS.ACTUALGROSSWT AS GROSSWT " \
    #         "        , BKLELEMENTS.ACTUALTAREWT AS TAREWT " \
    #         "        , BKLELEMENTS.ACTUALNETWT AS NETWT " \
    #         "        , BKLELEMENTS.LOTCODE AS LOTCODE " \
    #         "FROM SALESDOCUMENT " \
    #         "join OrderPartner               On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
    #         "                                And     OrderPartner.CustomerSupplierType = 1 " \
    #         "join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
    #         "JOIN BKLELEMENTS                on BKLELEMENTS.BUYERCUSTOMERSUPPLIERTYPE                 = OrderPartner.CUSTOMERSUPPLIERTYPE " \
    #         "                                AND BKLELEMENTS.BUYERCUSTOMERSUPPLIERCODE                = OrderPartner.CUSTOMERSUPPLIERCODE " \
    #         "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                              = Agent.Code    " \
    #         "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
    #         "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
    #         "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
    #         "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
    #         "                                AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
    #         "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
    #         "                                AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
    #         "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
    #         "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
    #         "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
    #         "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
    #         "LEFT JOIN INDTAXDETAIL          ON salesdocumentline.absuniqueid = INDTAXDETAIL.absuniqueid " \
    #         "                                AND INDTAXDETAIL.ITaxCOde = 'INR' " \
    #         "                                And INDTAXDETAIL.TaxCategoryCode = 'OTH' " \
    #         "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
    #         "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
    #         "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
    #         "                                        AND     Case IST.Position  " \
    #         "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
    #         "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06 " \
    #         "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09 " \
    #         "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code  " \
    #         "JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
    #         "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
    #         "Join Product                    On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
    #         "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId          " \
    #         "ORDER BY  COSTCENTER.LONGDESCRIPTION,SALESDOCUMENT.PROVISIONALCODE,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "
    #
    #     # # if pdfrpt.d < 40:
    #     #     # pdfrpt.d = 730
    #     stmt = con.db.prepare(con.conn, sql)
    #     con.db.execute(stmt)
    #     result = con.db.fetch_both(stmt)
    #
    #     # stmt1 = con.db.prepare(con.conn, sql)
    #     # con.db.execute(stmt1)
    #     # result1 = con.db.fetch_both(stmt1)
    #
    #     # # print("result is : "+str(result))
    #     # LSLotno=LSLotno
    #     #
    #     # if result1 != False:
    #     #     pdfrptboxnowise.border(pdfrpt.c, result1)
    #     #
    #     # print (result)
    #     # p=335
    #     # pdfrptboxnowise.data(result,p,pdfrptboxnowise.c)
    #
    #     # pdfrptboxnowise.border(pdfrptboxnowise.c,result)
    #     print(result)
    #     # pdfrptboxnowise.printdetail(result,pdfrptboxnowise.d)
    #
    #     while result != False:
    #         print("while in /*/*/*/*/*/*/*/*")
    #         # global counter
    #         counter = counter + 1
    #         # pdfrptboxnowise.testprint(result)
    #         pdfrptboxnowise.textsize(pdfrptboxnowise.c, result, pdfrptboxnowise.d,pdfrptboxnowise.x)
    #         # pdfrptpyboxwise.textsize(pdfrptpyboxwise.c, result, pdfrptpyboxwise.d)
    #
    #         pdfrptboxnowise.d = pdfrptboxnowise.dvalue()
    #         result = con.db.fetch_both(stmt)
    #         print("while out  *- *- *- *- *")
    #
    #     pdfrptboxnowise.d = 530
    #     pdfrptboxnowise.c.setPageSize(pdfrptboxnowise.landscape(pdfrpt.A4))
    #     # pdfrpt.c.showPage()
    #
    #     # if result != False:
    #     #     pdfrptboxnowise.border(result)
    #     # else:
    #     #     pdfrptboxnowise.border( result)
    #     # pdfrpt.header(stdt, etdt, pdfrpt.divisioncode,LSLotno,LSRegistertype)
    #
    #     pdfrptboxnowise.d = pdfrptboxnowise.d - 20
    #     pdfrptboxnowise.c.showPage()
    #     # pdfrptpyboxwise.print("after calling register")
    #
    #     if counter == 0:
    #         Exceptions = "Note: No Result found according to your selected criteria "
    #         print("counter = 0")
    #     else:
    #         pdfrptboxnowise.c.showPage()
    #         pdfrptboxnowise.c.save()
    #         # url = "file:///D:/New format Report/Generated Reports/Print yan challan/" + LSFileName + ".pdf"
    #         # os.startfile(url)
    #         pdfrptboxnowise.newrequest()
    #         pdfrptboxnowise.d = pdfrpt.newpage()
    #         # print("from  else befoer over")
    #
    #
