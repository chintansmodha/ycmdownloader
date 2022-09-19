from django.http import HttpResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import Challan_Register_Customer_FormLoad as views
from PrintPDF import Challan_Register_Customer_Purchase_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
import os
from datetime import datetime
from ProcessSelection import Challan_Register_Customer_ProcessSelection as PRV


def Challan_Register_Customer_Purchase(LSparty, LScompany, LStransporter,LSselparty, LSselcompany,LSseltransporter, LDStartDate, LDEndDate, request, sqlwhere):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                            20:]
    sql=""
    result=""
    # sqlwhere =""?
    # print("Report type : "+LSReporttype)
    # print(LSselcompany)
    # print(LSselparty)
    print(sqlwhere)
    # if LSstring == '0':
    #     sql = " SELECT  Company.LONGDESCRIPTION                                     AS COMPANYNAME " \
    #       "         , COALESCE(AGENT.Longdescription,'')                            AS AGENTNAME " \
    #       "         , BankMaster.LongDescription                                    As BankName " \
    #       "         , ADS_SLipNo.ValueString                                        AS VOUCHERNUMBER " \
    #       "         , VARCHAR_FORMAT(FINDOC.FinanceDocumentDate,'DD/MM/YYYY')       AS VOUCHERDATE  " \
    #       "         , AgGrp.Longdescription                                         AS BrokerGroupName " \
    #       "         , agent.Longdescription                                         AS BrokerName " \
    #       "         , VARCHAR_FORMAT(ADS_Cheque_Date.ValueDate,'DD/MM/YYYY')        AS CHEQUEDATE " \
    #       "         , ADS_Cheque_No.ValueString                                     AS CHEQUENO " \
    #       "         , Sum(CAST(FINDOC.DOCUMENTAMOUNT AS DECIMAL(20,2)))             AS AMOUNT " \
    #       " FROM FINDOCUMENT FINDOC " \
    #       " LEFT JOIN AGENT                 ON      FINDOC.AGENT1CODE               = AGENT.CODE " \
    #       " Join AgentsGroupDetail AGD      On      FINDOC.Agent1Code               = AGD.AgentCode " \
    #       " Join AgentsGroup AgGrp          On      AGD.AgentsGroupCode             = AgGrp.Code " \
    #       " JOIN FinBusinessUnit BUnit      ON      FINDOC.BusinessUnitCODE         = Bunit.CODE And BUnit.GroupFlag = 0 " \
    #       " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode               = Company.Code And Company.GroupFlag = 1 " \
    #       " JoiN GLMaster As BankMaster  On      FINDOC.GLCODE                      = BankMaster.Code  " \
    #       " JOIN AdStorage ADS_SlipNo    ON      FINDOC.AbsUniqueId                 = ADS_SlipNo.UniqueId " \
    #       "                                 AND     ADS_SlipNo.NameEntityNAme       ='FINDocument' And ADS_SlipNo.FieldName = 'IssuesSlipNO' " \
    #       " JOIN AdStorage ADS_IssSlipStatus    ON  FINDOC.AbsUniqueId              = ADS_IssSlipStatus.UniqueId " \
    #       "                                 AND     ADS_IssSlipStatus.NameEntityNAme  ='FINDocument' " \
    #       "                                 And     ADS_IssSlipStatus.FieldName     = 'IssueSlipStatus' " \
    #       "                                 AND     ADS_IssSlipStatus.ValueString   = '2' " \
    #       " JOIN ADStorage ADS_Cheque_Date  ON      ADS_Cheque_Date.UniqueID        = FINDOC.AbsUniqueId " \
    #       "                                 AND     ADS_Cheque_Date.NameEntityNAme  = 'FINDocument'  " \
    #       "                                 And     ADS_Cheque_Date.FieldName       = 'ChequeDate'  " \
    #       " JOIN ADStorage ADS_Cheque_No    ON      ADS_Cheque_No.UniqueID          = FinDoc.AbsUniqueId " \
    #       "                                 AND     ADS_Cheque_No.NameEntityNAme    = 'FINDocument'  " \
    #       "                                 And     ADS_Cheque_No.FieldName         = 'CustomerCheque' " \
    #       " WHERE FINDOC.DOCUMENTTYPECODE IN('BR','CR') " \
    #       "         AND FINDOC.CURRENTSTATUS = 1 " \
    #       "         AND FINDOC.FINANCEDOCUMENTDATE BETWEEN '"+LDStartDate+"' AND '"+LDEndDate+"' " \
    #       "         AND FINDOC.DOCUMENTTEMPLATECODE In ('B12','B18') "+ sqlwhere+" " \
    #       " Group By Company.LONGDESCRIPTION " \
    #       "         , AGENT.Longdescription " \
    #       "         , AgGrp.Longdescription " \
    #       "         , AGENT.Longdescription " \
    #       "         , BankMaster.LongDescription " \
    #       "         , ADS_SLipNo.ValueString   " \
    #       "         , FINDOC.FinanceDocumentDate " \
    #       "         , ADS_Cheque_Date.ValueDate   " \
    #       "         , ADS_Cheque_No.ValueString   " \
    #       " Order by CompanyName " \
    #       "         , AgentName " \
    #       "         , FINDOC.FinanceDocumentDate,Company.LONGDESCRIPTION "
    #     stmt = con.db.prepare(con.conn, sql)
    #     stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    #     etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    #     con.db.execute(stmt)
    #     result = con.db.fetch_both(stmt)
    # elif LSReporttype == '2':
    #     sql = " SELECT  Company.LONGDESCRIPTION                                   AS COMPANYNAME " \
    #           "        , COALESCE(AGENT.Longdescription,'')                            AS AGENTNAME " \
    #           "        , BankMaster.LongDescription                                    As BankName " \
    #           "        , ADS_SLipNo.ValueString                                        AS VOUCHERNUMBER " \
    #           "        , VARCHAR_FORMAT(FINDOC.FinanceDocumentDate,'DD/MM/YYYY')       AS VOUCHERDATE " \
    #           "        , AgGrp.Longdescription                                         AS BrokerGroupName " \
    #           "        , agent.Longdescription                                         AS BrokerName " \
    #           "        , VARCHAR_FORMAT(ADS_Cheque_Date.ValueDate,'DD/MM/YYYY')        AS CHEQUEDATE " \
    #           "        , ADS_Cheque_No.ValueString                                     AS CHEQUENO " \
    #           "        , cast(FOD.AMOUNTINCC - FOD.ClearedAmount as decimal(18,2))     As UnAdjusted " \
    #           "        , Sum(CAST(FINDOC.DOCUMENTAMOUNT AS DECIMAL(20,2)))             AS AMOUNT " \
    #           " FROM FINDOCUMENT FINDOC " \
    #           " LEFT JOIN AGENT                 ON      FINDOC.AGENT1CODE               = AGENT.CODE " \
    #           " Join AgentsGroupDetail AGD      On      FINDOC.Agent1Code               = AGD.AgentCode " \
    #           " Join AgentsGroup AgGrp          On      AGD.AgentsGroupCode             = AgGrp.Code " \
    #           " JOIN FinBusinessUnit BUnit      ON      FINDOC.BusinessUnitCODE         = Bunit.CODE And BUnit.GroupFlag = 0 " \
    #           " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode               = Company.Code And Company.GroupFlag = 1 " \
    #           " JoiN GLMaster As BankMaster  On      FINDOC.GLCODE                      = BankMaster.Code  " \
    #           " JOIN AdStorage ADS_SlipNo    ON      FINDOC.AbsUniqueId                 = ADS_SlipNo.UniqueId " \
    #           "                                AND     ADS_SlipNo.NameEntityNAme       ='FINDocument' And ADS_SlipNo.FieldName = 'IssuesSlipNO' " \
    #           " JOIN AdStorage ADS_IssSlipStatus    ON  FINDOC.AbsUniqueId              = ADS_IssSlipStatus.UniqueId " \
    #           "                                AND     ADS_IssSlipStatus.NameEntityNAme  ='FINDocument' " \
    #           "                                And     ADS_IssSlipStatus.FieldName     = 'IssueSlipStatus' " \
    #           "                                AND     ADS_IssSlipStatus.ValueString   = '2' " \
    #           " JOIN ADStorage ADS_Cheque_Date  ON      ADS_Cheque_Date.UniqueID        = FINDOC.AbsUniqueId  " \
    #           "                                AND     ADS_Cheque_Date.NameEntityNAme  = 'FINDocument'  " \
    #           "                                And     ADS_Cheque_Date.FieldName       = 'ChequeDate'  " \
    #           " JOIN ADStorage ADS_Cheque_No    ON      ADS_Cheque_No.UniqueID          = FinDoc.AbsUniqueId " \
    #           "                                AND     ADS_Cheque_No.NameEntityNAme    = 'FINDocument'  " \
    #           "                                And     ADS_Cheque_No.FieldName         = 'CustomerCheque' " \
    #           " Join FINOpenDocuments FOD       On      FOD.CODE                        = FINDOC.Code  " \
    #           "                                AND     FOD.BusinessUnitCode            = FINDOC.BusinessUnitCode  " \
    #           "                                AND     FOD.FinancialYearCode           = FINDOC.FinancialYearCode  " \
    #           "                                AND     FOD.DocumentTemplateCode        = FINDOC.DocumentTemplateCode  " \
    #           "                                AND     FOD.DocumentTypeCode = 'BR' " \
    #           " WHERE FINDOC.DOCUMENTTYPECODE IN('BR','CR') " \
    #           "        AND FINDOC.CURRENTSTATUS = 1 " \
    #           "        AND FINDOC.FINANCEDOCUMENTDATE BETWEEN '"+LDStartDate+"' AND '"+LDEndDate+"' " \
    #           "        AND FINDOC.DOCUMENTTEMPLATECODE In ('B12','B18') " \
    #           "        AND FOD.AMOUNTINCC > 0  " \
    #           "        AND FOD.AMOUNTINCC - FOD.ClearedAmount <> 0  "+sqlwhere+" " \
    #           " Group By Company.LONGDESCRIPTION  " \
    #           ", AGENT.Longdescription  " \
    #           ", AgGrp.Longdescription    " \
    #           ", AGENT.Longdescription " \
    #           ", BankMaster.LongDescription " \
    #           ", ADS_SLipNo.ValueString     " \
    #           ", FINDOC.FinanceDocumentDate " \
    #           ", ADS_Cheque_Date.ValueDate  " \
    #           ", ADS_Cheque_No.ValueString   " \
    #           ", FOD.AMOUNTINCC   " \
    #           ", FOD.ClearedAmount " \
    #           " Order by CompanyName " \
    #           "        , AgentName " \
    #           "        , FINDOC.FinanceDocumentDate "
    #     stmt = con.db.prepare(con.conn, sql)
    #     stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    #     etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    #     con.db.execute(stmt)
    #     result = con.db.fetch_both(stmt)
    #
    # if LSReporttype == '0':
    sql = " SELECT  BUnit.LONGDESCRIPTION AS DIVISIONCODE   " \
          "          , COALESCE (BP_Trpt.Legalname1,'Transporter Not Entered') AS TRANSPORTERNAME    " \
          "          , sum(PLANTINVOICELINE.PRIMARYQTY)  AS QUANTITY " \
          "          , Sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE " \
          "          , Sum(INDTAXDETAILGST.CALCULATEDVALUER) as GSTChargeVALUE " \
          " From PlantInvoice   " \
          "        JOIN SALESDOCUMENT      ON PLANTINVOICE.CODE                            = SALESDOCUMENT.PROVISIONALCODE   " \
          "                              and SALESDOCUMENT.DocumentTypeType = '06'   " \
          "        JOIN DIVISION                           ON PLANTINVOICE.DIVISIONCODE    = DIVISION.CODE   " \
          "        left JOIN AGENT         	ON      PLANTINVOICE.AGENT1CODE = AGENT.CODE     " \
          "        Left join OrderPartner OP_Trpt    On      PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE  " \
          "                                        And     PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE    " \
          "        Left join BusinessPartner BP_Trpt  On     OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID  " \
          "        JOIN SALESDOCUMENTLINE          ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE    " \
          "                                      AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE      = SALESDOCUMENT.PROVISIONALCOUNTERCODE  " \
          "                                      and     SALESDOCUMENTline.DocumentTypeType = '06'   " \
          "        join salesdocumentline sdline05 on      sdline05.salesdocumentprovisionalcode = SALESDOCUMENTLINE.PreviousCode   " \
          "                                      and     sdline05.documenttypetype='05'   " \
          "        JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                  = LOGICALWAREHOUSE.CODE   " \
          "        JOIN BusinessUnitVsCompany BUC  ON      SalesDocument.DivisionCode                       = BUC.DivisionCode  " \
          "                                      AND     LOGICALWAREHOUSE.plantcode                       = BUC.factorycode   " \
          "        JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode                             = BUnit.Code And BUnit.GroupFlag = 0 " \
          "        JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode                                = Company.Code And Company.GroupFlag = 1  " \
          "        JOIN PLANTINVOICELINE           ON PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE    " \
          "                                        AND PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE  " \
          "                                        AND PLANTINVOICELINE.ITEMTYPECODE = SALESDOCUMENTLINE.ITEMTYPEAFICODE  " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode01, '') = COALESCE(SALESDOCUMENTLINE.SubCode01, '')  " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode02, '') = COALESCE(SALESDOCUMENTLINE.SubCode02, '')  " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode03, '') = COALESCE(SALESDOCUMENTLINE.SubCode03, '')   " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode04, '') = COALESCE(SALESDOCUMENTLINE.SubCode04, '')   " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode05, '') = COALESCE(SALESDOCUMENTLINE.SubCode05, '')   " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode06, '') = COALESCE(SALESDOCUMENTLINE.SubCode06, '')   " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode07, '') = COALESCE(SALESDOCUMENTLINE.SubCode07, '')   " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode08, '') = COALESCE(SALESDOCUMENTLINE.SubCode08, '')   " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode09, '') = COALESCE(SALESDOCUMENTLINE.SubCode09, '')  " \
          "                                        AND     COALESCE(PLANTINVOICELINE.SubCode10, '') = COALESCE(SALESDOCUMENTLINE.SubCode10, '')  " \
          "         JOIN FullItemKeyDecoder FIKD   ON      PLANTINVOICELINE.ITEMTYPECODE = FIKD.ITEMTYPECODE    " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')  " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')  " \
          "                                  AND     COALESCE(PLANTINVOICELINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')  " \
          "        Join Product                On      PLANTINVOICELINE.ITEMTYPECODE           = Product.ITEMTYPECODE   " \
          "                                  And     FIKD.ItemUniqueId                          = Product.AbsUniqueId   " \
          "         JOIN INDTAXDETAIL   ON     PLANTINVOICELINE.AbsUniqueID       =       INDTAXDETAIL.AbsUniqueID   " \
          "         JOIN ITax           ON     IndTaxDetail.ITaxCode    	= Itax.Code    " \
          "         JOIN INDTAXDETAIL    as INDTAXDETAILGST   ON     PLANTINVOICELINE.AbsUniqueID       =       INDTAXDETAILGST.AbsUniqueID    " \
          "         JOIN ITax as  ITaxGST               ON IndTaxDetailGST.ITaxCode        = ItaxGST.Code    " \
          " WHERE     plantinvoice.invoicedate   BETWEEN '" + LDStartDate + "' AND '" + LDEndDate + "'" \
          "  And IndTaxDetail.CALCULATEDVALUER <> 0   " \
          "  AND (ITax.TaxCategoryCode IN('FRT'))   " \
          " AND ITaxGST.TaxCategoryCode IN ('IGS','CGS','SGS') "+sqlwhere+" " \
          " GROUP BY  BUnit.LONGDESCRIPTION, BP_Trpt.Legalname1 " \
          " ORDER BY BUnit.LONGDESCRIPTION"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    pdfrpt.newrequest()
    print(sql)
    # print(result)

    global counter
    counter = 0
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    if result != False:
        while result != False:
            # print(result)
            pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)

            # pdfrpt.d=pdfrpt.dvalue()
            # print(result)
            result = con.db.fetch_both(stmt)
            counter = counter + 1
            if pdfrpt.d < 20:
                pdfrpt.d = 765
                pdfrpt.c.showPage()
                pdfrpt.header(stdt, etdt, pdfrpt.CompanyName)
        pdfrpt.d=pdfrpt.dvalue()
        pdfrpt.printotal(pdfrpt.d)
        pdfrpt.printGrandtotal()

        if result == False:
            if counter > 0:
                # pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
                pdfrpt.fonts(7)
                PRV.Exception = ""
            elif counter == 0:
                PRV.Exception = "Note: Please Select Valid Credentials"
                return

        pdfrpt.c.showPage()
        pdfrpt.c.save()
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
    else:
        PRV.Exception = "Note: Please Select Valid Credentials"
        return
    print("*-*-*-*-*-*-*-* end *-*-*-*-*-*---*")

    # result=""
